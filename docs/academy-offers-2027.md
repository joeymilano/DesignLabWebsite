# 2027 Academy offer library

Added 2026-11-23. User confirmed all supplied cases are Academy students.

- Source: 布大+华威+利兹+格大+谢大2027学年500个录取案例2026.11.10(1).xlsx.
- Five sheets, 100 numbered rows each; ignore trailing formatted empty rows in Glasgow sheet.
- 500 records, not unique applicants; 498 CO and 2 UO. No addition to existing aggregate marketing statistics, since overlap is unknown.
- 97 creative-related records selected by target programme: design/games/immersive arts 9, media 50, fashion/textiles 7, culture/music 26, urban studies 5. Other subjects remain searchable by selecting all subjects.
- Numeric fractional grades/conditions converted to percentages; strings, including GPA and offer conditions, retained. Each record has sheet and Excel row provenance. No invented testimonial, project, student name or offer image.
- Official SVG sources recorded in assets/site/admissions/2027.json. Logos identify institutions; no partnership claims.
- Render module: scripts/admission_library.py. Integrated in build-site.py; running the module alone idempotently updates only the two Academy pages.
- Latest origin/main was used in isolated worktree to preserve seven newer upstream commits. Existing unrelated local build-site.py edits were not included.

Validation: all 500 records compared with source spreadsheet; 97 default/500 all/2 UO; school selection, Chinese programme search, reset, load more; English display; desktop 1440 and mobile 390 with no horizontal overflow; all five local SVGs load; no browser page errors.

## Visual revision — 2026-11-23

User rejected the cream/green palette, serif typography, slogan and explanatory copy. Reworked the section into the existing ink/vermilion/sans system: plain 案例库 title, a continuous university logo strip, border-separated offer rows, compact filters and expandable conditions. Removed public source/readme prose and row identifiers while retaining provenance in the data and this document. Removed Chinese full stops in Academy headings. Mobile university strip scrolls independently; dataset and filtering behaviour unchanged.
