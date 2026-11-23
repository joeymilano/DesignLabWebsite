# QS Art & Design guide

Added 2026-11-23 to Chinese Academy page, anchor `#universities`.

## Scope

- Latest official subject edition is 2026. QS 2027 overall university rankings are not a 2027 Art & Design ranking.
- 2024 and 2025 each have 20 institutions ranked <=20. In 2026, three institutions tie at 19 (CMU, NUS, RMIT), giving 21 institutions. All ties retained; no arbitrary cutoff to 20 rows.
- Union of all three editions: 26 institutions. Exact three-year ranks retained even when outside the selected year's top 20.
- Each school has separate UG and PG application routes. Programme and applicant-route scope is explicit. These are representative arts/design pathways, not every programme at each university.
- Application cycle is 2027 regardless of selected ranking year. Recurring dates have no inferred year. Pending and historical entries are visibly labelled. Dates follow the institution's local time, with precise timezone where supplied.
- Mainland admissions routes are not mixed with international admissions. MIT/Stanford/Yale unified UG admissions are not portrayed as direct art-school admissions. RCA's new jointly awarded Norwich UG route is explicitly distinguished.

## Sources and data

`assets/site/universities/data.json` includes QS page and original ranking data URLs, logo provenance, and degree-specific official admissions links. All school admission records were researched on 2026-11-23. Private research intermediates are not published.

QS data endpoints were discovered from each official Chinese website page's Drupal `qs_rankings_datatables.rank_url`:

- 2024: https://www.qs-topuniversities.cn/sites/default/files/qs-rankings-data/en/2237673.txt
- 2025: https://www.qs-topuniversities.cn/sites/default/files/qs-rankings-data/en/2278552.txt
- 2026: https://www.qs-topuniversities.cn/sites/default/files/qs-rankings-data/en/56b56a082c6486938a0c8bbc459d6a86.txt

25 logos use 200×200 institutional marks from official QS profiles. Pratt's QS image represented its School of Information, so the university's main SVG was obtained from its official homepage instead.

NTU PRC/Gaokao deadline: current General Admission Requirements and the PRC-specific Chinese PDF give 19 March 2027. An English summary PDF still gives 20 January; the discrepancy is recorded in the source data. ADM portfolio deadline remains qualification/portal-specific and is not inferred from the university application deadline.

## Maintenance

Edit the data JSON to update verified source facts. Do not move deadlines into the next year mechanically. Keep the programme, applicant route and cycle attached to every requirement.

`python3 scripts/university_guide.py` idempotently injects only the Chinese Academy section. The module is also integrated with `build-site.py`. Existing 500-case library and English Academy page remain intact.

## Validation

Verified year counts 21/20/20, tie handling, 26 unique institutions/52 degree records, per-degree source links, undergraduate/graduate switching with expanded row preservation, name search and empty state, mobile width, all local logos, no JS page errors, and idempotent generation.
