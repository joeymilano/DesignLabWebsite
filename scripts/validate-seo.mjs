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

if (sitemapSet.size !== sitemapUrls.length) errors.push('sitemap.xml contains duplicate URLs');
if (sitemapUrls.some((url) => url.endsWith('.html'))) errors.push('sitemap.xml contains redirecting .html URLs');

for (const file of await walk(root)) {
  const source = await readFile(file, 'utf8');
  const relative = path.relative(root, file);
  const expectedCanonical = canonicalFor(file);
  const canonical = source.match(/<link rel="canonical" href="([^"]+)"/i)?.[1];
  const description = source.match(/<meta name="description" content="([^"]+)"/i)?.[1];

  if (canonical !== expectedCanonical) errors.push(`${relative}: canonical should be ${expectedCanonical}`);
  if (!sitemapSet.has(expectedCanonical)) errors.push(`${relative}: canonical is missing from sitemap.xml`);
  if (!description || Array.from(description).length < 70) errors.push(`${relative}: meta description is missing or shorter than 70 characters`);
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
    if (!existsSync(localFileFor(resolved))) errors.push(`${relative}: broken internal link ${href} -> ${resolved.pathname}`);
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
