import { readFile } from 'node:fs/promises';

const key = 'a5fee90557ac1ed1bc0b36eca238c386';
const host = '1-design-lab.com';
const sitemap = await readFile(new URL('../sitemap.xml', import.meta.url), 'utf8');
const urlList = [...sitemap.matchAll(/<loc>(https:\/\/1-design-lab\.com\/[^<]*)<\/loc>/g)].map((match) => match[1]);

if (urlList.length === 0) {
  throw new Error('No canonical URLs found in sitemap.xml');
}

const payload = {
  host,
  key,
  keyLocation: `https://${host}/${key}.txt`,
  urlList,
};

if (process.argv.includes('--dry-run')) {
  console.log(JSON.stringify(payload, null, 2));
  process.exit(0);
}

const response = await fetch('https://api.indexnow.org/indexnow', {
  method: 'POST',
  headers: { 'content-type': 'application/json; charset=utf-8' },
  body: JSON.stringify(payload),
});

if (!response.ok) {
  throw new Error(`IndexNow submission failed: ${response.status} ${await response.text()}`);
}

console.log(`IndexNow accepted ${urlList.length} canonical URLs (${response.status}).`);
