"""Maintain SEO metadata without regenerating or changing page bodies.

Run python3 scripts/seo_metadata.py after editing existing static pages.
The brand-page generator uses the same graph enrichment function.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORIGIN = 'https://1-design-lab.com'


def enrich_graph(data, url, title, description, language):
    graph = data.get('@graph')
    if not graph:
        return data
    organization = next((n for n in graph if n.get('@id') == ORIGIN + '/#organization'), None)
    if not organization:
        return data
    # Personal sites and independently built products are not brand aliases.
    organization.pop('sameAs', None)
    website = next((n for n in graph if n.get('@type') == 'WebSite'), None)
    if not website:
        graph.append({'@type': 'WebSite', '@id': ORIGIN + '/#website',
                      'name': '1% Design Lab', 'url': ORIGIN + '/',
                      'inLanguage': ['zh-CN', 'en'],
                      'publisher': {'@id': ORIGIN + '/#organization'}})
    service = next((n for n in graph if n.get('@type') == 'Service'), None)
    breadcrumb = next((n for n in graph if n.get('@type') == 'BreadcrumbList'), None)
    page = {'@type': 'WebPage', '@id': url + '#webpage', 'url': url,
            'name': title, 'description': description, 'inLanguage': language,
            'isPartOf': {'@id': ORIGIN + '/#website'},
            'about': {'@id': service['@id'] if service else ORIGIN + '/#organization'}}
    if service:
        page['mainEntity'] = {'@id': service['@id']}
        service['url'] = url
        service['mainEntityOfPage'] = {'@id': page['@id']}
        for offer in service.get('hasOfferCatalog', {}).get('itemListElement', []):
            if 'price' in offer:
                offer['priceSpecification'] = {
                    '@type': 'PriceSpecification',
                    'minPrice': float(offer.pop('price')),
                    'priceCurrency': offer.pop('priceCurrency', 'CNY')}
    if breadcrumb:
        breadcrumb['@id'] = url + '#breadcrumb'
        page['breadcrumb'] = {'@id': breadcrumb['@id']}
    graph[:] = [n for n in graph if n.get('@id') != page['@id']]
    graph.append(page)
    return data


def update(source):
    def meta(key):
        match = re.search(r'<meta (?:name|property)="' + re.escape(key) + r'" content="([^"]*)"', source)
        return html.unescape(match[1]) if match else ''

    title = html.unescape(re.search(r'<title>(.*?)</title>', source, re.S)[1])
    url = re.search(r'<link rel="canonical" href="([^"]+)"', source)[1]
    language = re.search(r'<html lang="([^"]+)"', source)[1]
    description = meta('description')
    def graph(match):
        data = json.loads(match[1])
        updated = enrich_graph(data, url, title, description, language)
        # Leave unrelated article, FAQ, and service data formatting intact.
        if not any(n.get('@type') == 'WebPage' for n in updated.get('@graph', [])):
            return match[0]
        return '<script type="application/ld+json">\n' + json.dumps(updated, ensure_ascii=False, indent=2) + '\n</script>'
    source = re.sub(r'<script type="application/ld\+json">(.*?)</script>', graph, source, flags=re.S)
    additions = []
    for key, value in [('twitter:card', 'summary_large_image'), ('twitter:title', title),
                       ('twitter:description', description), ('twitter:image', meta('og:image'))]:
        if not meta(key):
            additions.append(f'<meta name="{key}" content="{html.escape(value, quote=True)}">')
    if additions:
        source = source.replace('</head>', '\n'.join(additions) + '\n</head>', 1)
    source = re.sub(r'(<meta name="robots" content=")index, follow("\s*/?>)',
                    r'\1index, follow, max-image-preview:large\2', source)
    return source


if __name__ == '__main__':
    changed = 0
    for file in sorted(ROOT.rglob('*.html')):
        if file == ROOT / '404.html':
            continue
        if any(part.startswith('.') or part == '_archive' for part in file.relative_to(ROOT).parts):
            continue
        source = file.read_text()
        result = update(source)
        if result != source:
            file.write_text(result)
            changed += 1
    print(f'Updated metadata on {changed} pages; page bodies preserved.')
