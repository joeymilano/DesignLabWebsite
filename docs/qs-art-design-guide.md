# QS Art & Design guide

Added 2026-11-23 to Chinese Academy page, anchor `#universities`.

## Scope

- Latest official subject edition is 2026. QS 2027 overall university rankings are not a 2027 Art & Design ranking.
- The 2024, 2025 and 2026 editions each contain 50 institutions ranked <=50. All ties are preserved. Pagination presents 20, 20 and 10 schools, independent of rank ties.
- Union of all three editions: 64 institutions. Exact three-year ranks retained even when outside the selected year's top 50.
- QS ranks institutions within the subject, not separate degree levels. Each school has separate UG and PG application routes, selected inside its expanded detail panel. Programme and applicant-route scope is explicit. These are representative arts/design pathways, not every programme at each university.
- Application cycle is 2027 regardless of selected ranking year. Recurring dates have no inferred year. Pending and historical entries are visibly labelled. Dates follow the institution's local time, with precise timezone where supplied.
- Mainland admissions routes are not mixed with international admissions. MIT/Stanford/Yale unified UG admissions are not portrayed as direct art-school admissions. RCA's new jointly awarded Norwich UG route is explicitly distinguished.

## Sources and data

`assets/site/universities/data.json` includes QS page and original ranking data URLs, logo provenance, and degree-specific official admissions links. All school admission records were researched on 2026-11-23. Private research intermediates are not published.

QS data endpoints were discovered from each official Chinese website page's Drupal `qs_rankings_datatables.rank_url`:

- 2024: https://www.qs-topuniversities.cn/sites/default/files/qs-rankings-data/en/2237673.txt
- 2025: https://www.qs-topuniversities.cn/sites/default/files/qs-rankings-data/en/2278552.txt
- 2026: https://www.qs-topuniversities.cn/sites/default/files/qs-rankings-data/en/56b56a082c6486938a0c8bbc459d6a86.txt

63 logos use 200×200 institutional marks from official QS profiles. Pratt's QS image represented its School of Information, so the university's main SVG was obtained from its official homepage instead.

NTU PRC/Gaokao deadline: current General Admission Requirements and the PRC-specific Chinese PDF give 19 March 2027. An English summary PDF still gives 20 January; the discrepancy is recorded in the source data. ADM portfolio deadline remains qualification/portal-specific and is not inferred from the university application deadline.

## Maintenance

Edit the data JSON to update verified source facts. Do not move deadlines into the next year mechanically. Keep the programme, applicant route and cycle attached to every requirement.

`python3 scripts/university_guide.py` idempotently injects only the Chinese Academy section. The module is also integrated with `build-site.py`. Existing 500-case library and English Academy page remain intact.

## Interface and validation

Title: 全球院校榜单. Hero links use an aligned two-column grid. Degree selection belongs to each school's admissions panel; changing it never reorders the ranking. Year or search changes reset pagination to page 1. School-specific degree and expanded state persist across pages. Official ranking and admissions source links remain available, without the removed footer annotation.

Validation covers three editions, 20/20/10 rows, unique schools and ordered ranks across pages, full logo loading, undergraduate/graduate switching, search and empty state, mobile overflow, and idempotent generation.
