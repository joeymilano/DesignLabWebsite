import { readFile } from 'node:fs/promises';

const site = '1-design-lab.com';
const sitemap = await readFile(new URL('../sitemap.xml', import.meta.url), 'utf8');
const urlList = [...sitemap.matchAll(/<loc>(https:\/\/1-design-lab\.com\/[^<]*)<\/loc>/g)]
  .map((match) => match[1]);

if (urlList.length === 0) {
  throw new Error('No canonical URLs found in sitemap.xml');
}

if (urlList.some((url) => url.endsWith('.html'))) {
  throw new Error('Baidu submission must use final canonical URLs, not redirecting .html URLs');
}

if (process.argv.includes('--dry-run')) {
  console.log(JSON.stringify({
    site,
    endpoint: 'http://data.zz.baidu.com/urls',
    tokenRequired: true,
    urlCount: urlList.length,
    urlList,
  }, null, 2));
  process.exit(0);
}

const token = process.env.BAIDU_PUSH_TOKEN?.trim();
if (!token) {
  throw new Error('BAIDU_PUSH_TOKEN is required. Copy it from Baidu Search Resource Platform without committing it to the repository.');
}

const endpoint = new URL('http://data.zz.baidu.com/urls');
endpoint.searchParams.set('site', site);
endpoint.searchParams.set('token', token);

const response = await fetch(endpoint, {
  method: 'POST',
  headers: { 'content-type': 'text/plain; charset=utf-8' },
  body: urlList.join('\n'),
});

const responseText = await response.text();
let result;
try {
  result = JSON.parse(responseText);
} catch {
  throw new Error(`Baidu submission returned an unreadable response (${response.status}).`);
}

if (!response.ok || result.error || result.not_same_site?.length || result.not_valid?.length) {
  const safeResult = {
    status: response.status,
    error: result.error,
    message: result.message,
    notSameSite: result.not_same_site?.length ?? 0,
    notValid: result.not_valid?.length ?? 0,
  };
  throw new Error(`Baidu submission failed: ${JSON.stringify(safeResult)}`);
}

console.log(JSON.stringify({
  submitted: urlList.length,
  accepted: result.success ?? 0,
  remainingQuota: result.remain ?? null,
}, null, 2));
