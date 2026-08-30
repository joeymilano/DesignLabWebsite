import { existsSync } from 'node:fs';
import { readFile, readdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const origin = 'https://1-design-lab.com';
const errors = [];

async function walk(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    if (entry.name === '.git' || entry.name === '_archive') continue;
    const absolute = path.join(directory, entry.name);
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
const inboundLinks = new Map(sitemapUrls.map((url) => [url, new Set()]));
const titleOwners = new Map();
const descriptionOwners = new Map();

if (sitemapSet.size !== sitemapUrls.length) errors.push('sitemap.xml contains duplicate URLs');
if (sitemapUrls.some((url) => url.endsWith('.html'))) errors.push('sitemap.xml contains redirecting .html URLs');

for (const file of await walk(root)) {
  const source = await readFile(file, 'utf8');
  const relative = path.relative(root, file);
  const expectedCanonical = canonicalFor(file);
  const canonical = source.match(/<link rel="canonical" href="([^"]+)"/i)?.[1];
  const title = source.match(/<title>([^<]+)<\/title>/i)?.[1]?.trim();
  const description = source.match(/<meta name="description" content="([^"]+)"/i)?.[1];
  const lang = source.match(/<html[^>]*\slang="([^"]+)"/i)?.[1];
  const h1Count = [...source.matchAll(/<h1(?:\s[^>]*)?>/gi)].length;
  const ogUrl = source.match(/<meta property="og:url" content="([^"]+)"/i)?.[1];

  if (canonical !== expectedCanonical) errors.push(`${relative}: canonical should be ${expectedCanonical}`);
  if (!sitemapSet.has(expectedCanonical)) errors.push(`${relative}: canonical is missing from sitemap.xml`);
  if (!title) errors.push(`${relative}: title is missing`);
  if (!description || Array.from(description).length < 70) errors.push(`${relative}: meta description is missing or shorter than 70 characters`);
  if (!lang) errors.push(`${relative}: html lang is missing`);
  if (h1Count !== 1) errors.push(`${relative}: expected exactly one h1, found ${h1Count}`);
  if (ogUrl && ogUrl !== expectedCanonical) errors.push(`${relative}: og:url should match canonical ${expectedCanonical}`);
  if (title) {
    if (titleOwners.has(title)) errors.push(`${relative}: duplicate title also used by ${titleOwners.get(title)}`);
    titleOwners.set(title, relative);
  }
  if (description) {
    if (descriptionOwners.has(description)) errors.push(`${relative}: duplicate meta description also used by ${descriptionOwners.get(description)}`);
    descriptionOwners.set(description, relative);
  }

  for (const match of source.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/gi)) {
    try {
      JSON.parse(match[1]);
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
    const targetFile = localFileFor(resolved);
    if (!existsSync(targetFile)) {
      errors.push(`${relative}: broken internal link ${href} -> ${resolved.pathname}`);
    } else if (targetFile.endsWith('.html')) {
      const targetCanonical = canonicalFor(targetFile);
      if (targetCanonical !== expectedCanonical && inboundLinks.has(targetCanonical)) {
        inboundLinks.get(targetCanonical).add(expectedCanonical);
      }
    }
  }

  for (const match of source.matchAll(/<link\s+rel="alternate"\s+hreflang="([^"]+)"\s+href="([^"]+)"/gi)) {
    const [, hreflang, href] = match;
    const resolved = new URL(href, expectedCanonical);
    if (resolved.origin === origin && !existsSync(localFileFor(resolved))) {
      errors.push(`${relative}: broken hreflang ${hreflang} -> ${resolved.pathname}`);
    }
  }
}

for (const sitemapUrl of sitemapUrls) {
  const parsed = new URL(sitemapUrl);
  if (parsed.origin !== origin) errors.push(`sitemap.xml contains a non-canonical origin ${sitemapUrl}`);
  if (!existsSync(localFileFor(parsed))) errors.push(`sitemap.xml URL has no local HTML page ${sitemapUrl}`);
  if (sitemapUrl !== `${origin}/` && inboundLinks.get(sitemapUrl)?.size === 0) {
    errors.push(`${sitemapUrl}: canonical page has no incoming internal HTML link`);
  }
}

const robots = await readFile(path.join(root, 'robots.txt'), 'utf8');
if (!robots.includes('Sitemap: https://1-design-lab.com/sitemap.xml')) errors.push('robots.txt is missing the canonical sitemap URL');
if (!existsSync(path.join(root, 'llms.txt'))) errors.push('llms.txt is missing');

if (errors.length) {
  console.error(errors.join('\n'));
  process.exit(1);
}

console.log(`SEO validation passed: ${sitemapUrls.length} canonical URLs and valid metadata, JSON-LD, and internal links.`);
