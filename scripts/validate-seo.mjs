import { existsSync } from 'node:fs';
import { readFile, readdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const origin = 'https://1-design-lab.com';
const errors = [];
const pages = new Map();
const titles = new Map();
const descriptions = new Map();
const inbound = new Set();

async function walk(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    if (entry.name === '.git' || entry.name === '_archive') continue;
    const absolute = path.join(directory, entry.name);
    if (absolute === path.join(root, '404.html')) continue;
    if (entry.isDirectory()) files.push(...await walk(absolute));
    if (entry.isFile() && entry.name.endsWith('.html')) files.push(absolute);
  }
  return files;
}

function canonicalFor(file) {
  const relative = path.relative(root, file).split(path.sep).join('/');
  if (relative === 'index.html') return `${origin}/`;
  if (relative.endsWith('/index.html')) return `${origin}/${relative.slice(0, -10)}`;
  return `${origin}/${relative.slice(0, -5)}`;
}

function localFileFor(url) {
  const pathname = decodeURIComponent(url.pathname);
  if (pathname === '/') return path.join(root, 'index.html');
  if (path.posix.extname(pathname)) return path.join(root, pathname.slice(1));
  if (pathname.endsWith('/')) return path.join(root, pathname, 'index.html');
  return path.join(root, `${pathname.slice(1)}.html`);
}

const sitemapSource = await readFile(path.join(root, 'sitemap.xml'), 'utf8');
const sitemapUrls = [...sitemapSource.matchAll(/<loc>([^<]+)<\/loc>/g)].map((match) => match[1]);
const sitemapSet = new Set(sitemapUrls);

if (sitemapSet.size !== sitemapUrls.length) errors.push('sitemap.xml contains duplicate URLs');
if (sitemapUrls.some((url) => url.endsWith('.html'))) errors.push('sitemap.xml contains redirecting .html URLs');

for (const file of await walk(root)) {
  const source = await readFile(file, 'utf8');
  const relative = path.relative(root, file);
  const expectedCanonical = canonicalFor(file);
  const canonical = source.match(/<link rel="canonical" href="([^"]+)"/i)?.[1];
  const description = source.match(/<meta name="description" content="([^"]+)"/i)?.[1];
  pages.set(expectedCanonical, { source, relative });
  const title = source.match(/<title>([^<]+)<\/title>/i)?.[1];
  for (const [value, seen, label] of [[title, titles, 'title'], [description, descriptions, 'description']]) {
    if (!value) errors.push(`${relative}: missing ${label}`);
    else if (seen.has(value)) errors.push(`${relative}: duplicate ${label} with ${seen.get(value)}`);
    else seen.set(value, relative);
  }
  if ([...source.matchAll(/<h1\b/gi)].length !== 1) errors.push(`${relative}: expected one H1`);
  if (source.match(/<meta name="robots" content="[^"]*noindex/i)) errors.push(`${relative}: sitemap page is noindex`);
  if (source.match(/<meta property="og:url" content="([^"]+)"/i)?.[1] !== expectedCanonical) errors.push(`${relative}: og:url differs from canonical`);
  for (const key of ['twitter:card', 'twitter:title', 'twitter:description', 'twitter:image', 'og:image']) {
    const value = source.match(new RegExp(`<meta (?:name|property)="${key}" content="([^"]+)"`, 'i'))?.[1];
    if (!value) errors.push(`${relative}: missing ${key}`);
    if (key.endsWith(':image') && value) {
      if (!value.startsWith('https://')) errors.push(`${relative}: ${key} must be absolute HTTPS`);
      else {
        const image = new URL(value);
        if (image.origin === origin && !existsSync(localFileFor(image))) errors.push(`${relative}: missing share image ${value}`);
      }
    }
  }

  if (canonical !== expectedCanonical) errors.push(`${relative}: canonical should be ${expectedCanonical}`);
  if (!sitemapSet.has(expectedCanonical)) errors.push(`${relative}: canonical is missing from sitemap.xml`);
  if (!description || Array.from(description).length < 70) errors.push(`${relative}: meta description is missing or shorter than 70 characters`);
  for (const match of source.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/gi)) {
    try {
      const data = JSON.parse(match[1]);
      const graph = data['@graph'] ?? [];
      const org = graph.find((node) => node['@id'] === `${origin}/#organization`);
      if (org?.legalName) {
        if (org.sameAs?.some((url) => /joeyzhao|finfold|billvampire|joeymilano/.test(url))) errors.push(`${relative}: organization sameAs conflates personal or product identities`);
        const page = graph.find((node) => node['@type'] === 'WebPage');
        if (page?.url !== expectedCanonical || !page?.inLanguage || !page?.isPartOf) errors.push(`${relative}: missing linked WebPage metadata`);
        const service = graph.find((node) => node['@type'] === 'Service');
        for (const offer of service?.hasOfferCatalog?.itemListElement ?? []) {
          if ('price' in offer || !(offer.priceSpecification?.minPrice >= 0)) errors.push(`${relative}: starting price must use minPrice`);
        }
      }
    } catch (error) {
      errors.push(`${relative}: invalid JSON-LD (${error.message})`);
    }
  }

  for (const match of source.matchAll(/href="([^"]+)"/gi)) {
    const href = match[1];
    if (/^(?:#|mailto:|tel:|javascript:)/i.test(href) || href.includes('${')) continue;
    const resolved = new URL(href, expectedCanonical);
    if (resolved.origin !== origin) continue;
    if (/\.html$/i.test(resolved.pathname)) errors.push(`${relative}: contains a redirecting internal .html URL ${href}`);
    resolved.hash = '';
    resolved.search = '';
    if (!existsSync(localFileFor(resolved))) errors.push(`${relative}: broken internal link ${href} -> ${resolved.pathname}`);
  }
}

for (const url of sitemapUrls) {
  if (!pages.has(url)) errors.push(`sitemap.xml: no canonical page for ${url}`);
}
for (const [url, { source, relative }] of pages) {
  const alternates = [...source.matchAll(/<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"/gi)];
  const language = source.match(/<html lang="([^"]+)"/i)?.[1];
  if (alternates.length && !alternates.some(([, lang, href]) => lang === language && href === url)) errors.push(`${relative}: hreflang missing self reference`);
  for (const [, lang, href] of alternates) {
    const target = pages.get(href);
    if (!target) { errors.push(`${relative}: hreflang target is not canonical: ${href}`); continue; }
    if (lang !== 'x-default' && !target.source.includes(`hreflang="${language}" href="${url}"`)) errors.push(`${relative}: non-reciprocal hreflang ${href}`);
    if (lang !== 'x-default' && target.source.match(/<html lang="([^"]+)"/i)?.[1] !== lang) errors.push(`${relative}: hreflang language mismatch ${href}`);
  }
  for (const [, href] of source.matchAll(/<a\b[^>]*href="([^"]+)"/gi)) {
    const target = new URL(href, url);
    if (target.origin !== origin) continue;
    const base = `${target.origin}${target.pathname}`;
    if (base !== url) inbound.add(base);
    if (target.hash && pages.has(base)) {
      const id = decodeURIComponent(target.hash.slice(1));
      if (!pages.get(base).source.includes(`id="${id}"`) && !pages.get(base).source.includes(`id='${id}'`)) errors.push(`${relative}: broken anchor ${href}`);
    }
  }
}
for (const url of sitemapUrls) {
  if (url !== `${origin}/` && !inbound.has(url)) errors.push(`Orphan page: ${url}`);
}

const robots = await readFile(path.join(root, 'robots.txt'), 'utf8');
const notFound = path.join(root, '404.html');
if (!existsSync(notFound)) errors.push('404.html is required to prevent the Pages homepage fallback');
else if (!(await readFile(notFound, 'utf8')).includes('content="noindex, follow"')) errors.push('404.html must be noindex');
if (!robots.includes('Sitemap: https://1-design-lab.com/sitemap.xml')) errors.push('robots.txt is missing the canonical sitemap URL');
if (!existsSync(path.join(root, 'llms.txt'))) errors.push('llms.txt is missing');

if (errors.length) {
  console.error(errors.join('\n'));
  process.exit(1);
}

console.log(`SEO validation passed: ${sitemapUrls.length} canonical URLs and valid metadata, JSON-LD, and internal links.`);
