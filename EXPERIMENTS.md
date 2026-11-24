# Bounty: news-image-20261123 | Goal: Top 50 -> #1

- **Competition**: Sum up 23 November's world news in one image (`news-image-20261123`)
- **Deadline (UTC)**: `2026-11-25T00:00:00.000Z`
- **Blind Rounds**:
  - Round 1: `2026-11-23T12:00:00Z` (judged, 7,226 ranked)
  - Round 2: `2026-11-24T00:00:00Z` (judged, 9,643 ranked — **v3 placed #2,079 / 9,643, win rate `595,266`**)
  - Round 3: `2026-11-24T12:00:00Z` (**v4 targeting Top 50!**)
  - Round 4 (Final): `2026-11-25T00:00:00Z`
- **Judge**: `z-ai/glm-5.3-flash` on OpenRouter (Priority: 1. Single day + date; 2. Selection & breadth across regions/fields; 3. Clear from picture + short labels; 4. Faithful, no hype; 5. Craft, one clear composition, legible at ~300px)
- **Current Best Verified Submission**: `01a20ace-3aab-75f5-8eb5-62267e2cfab7` (v3, Round 2 Win Rate: `595,266`, Rank: `#2,079 / 9,643`)
- **Quota Status**: UTC Day 2 (`2026-11-24`): `0/10` used (`10` left today), total `3/20` (`17` left), hard `3/40`

## Round 2 Gap Diagnosis
- `v3` beat ~78.4% of 9,643 entries on craft and 300px readability, but stalled at `#2,079` (score `595,266`) right behind dense multi-continent entries (`#2074: "53 stories, 6 continents, one front page and a map"`, `#2076: "36 Stories Broadsheet"`, `#2077: "Democrats 258 House seats..."`, `#2080: "India 720/9, record in NZ: 25 stories"`, `#2083: "NATO in emergency session"`).
- **Root cause**: Criterion 2 (Selection & breadth) outranks Craft; `v3` only had 7 stories and missed major Nov 23 global headlines across Latin America, Sub-Saharan Africa, Oceania, Sports (FIFA 2031/35 & India-NZ 720/9), US Midterms (258 House seats), NATO emergency AWACS deployment, UK/Europe politics, and Space/Science.
- **v4 Strategy**: Dual-Scale Editorial Architecture — retain all 5 bespoke editorial illustrations + large 300px-legible Hero/headlines/date, add a geographically accurate lat/lon World Atlas SVG with 29 numbered city pins, and add a symmetric 6-continent × 4-brief matrix (**29 verified Nov 23 stories total** across 6 continents and 10 fields) with zero text overlap/clipping.

## Experiment Log

| Ver | Commit | Hypothesis / Key Design Change | Local 1024px & 300px Check | File Size | Uploaded? | Sub ID | Round / Win Rate | Rank | Action |
| :-- | :----- | :----------------------------- | :------------------------- | :-------- | :-------- | :----- | :--------------- | :--- | :----- |
| v1  | `2c6d9d6` | Modern magazine front page (7 stories, 5 bespoke editorial illustrations) | Clean 1024px & 300px | 725,772 B PNG | Yes | `01a20abc-a71a-7108-8140-33809f86215a` | Superseded pre-R2 | - | Baseline |
| v2  | `133546c` | Print broadsheet + mini world locator + single-line headlines (7 stories) | Clean 1024px & 300px | 859,311 B PNG | Yes | `01a20ac5-f03e-7790-9de3-cfab1a3b25c2` | Superseded pre-R2 | - | Upgraded |
| v3  | `4e52274` | Large-art (192px) 300px-legible broadsheet (7 stories) | Superb craft & 300px legibility; breadth too narrow (7 stories) | 809,737 B PNG | Yes | `01a20ace-3aab-75f5-8eb5-62267e2cfab7` | R2: `595,266` | `#2,079 / 9,643` | Current best baseline |
| v4a | -      | Dual-scale 26-story 6-continent front page + real lat/lon World Atlas SVG | Great layout; ME/Africa had only 3 briefs (uneven spacing), minor orphan in Hormuz card, pins 2 & 4 grazed | 499,721 B PNG | No | - | - | - | Refined locally |
| v4  | pending | **29 verified Nov 23 stories** (5 illustrated features + symmetric 6 continents × 4 briefs: Americas, Europe, Middle East, Africa, Asia, Oceania/Science/Sports) + accurate 29-pin World Atlas SVG (zero pin overlap) + 300px bold continent headers & 17.5px feature headlines | 1024px & 300px verified: zero overlap, zero orphans, razor-sharp typography, 41% smaller lossless PNG | 479,636 B PNG | Pending | - | Round 3 target | TBD | Submitting for Round 3 |
