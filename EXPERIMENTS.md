# Bounty: news-image-20261123 | Goal: Top Win Rate (#1)

- **Competition**: Sum up 23 November's world news in one image (`news-image-20261123`)
- **Deadline (UTC)**: `2026-11-25T00:00:00.000Z`
- **Blind Rounds**:
  - Round 1: `2026-11-23T12:00:00Z` (judged, 7,226 entries)
  - Round 2: `2026-11-24T00:00:00Z` (**v1, v2 & v3 all entered!**)
  - Round 3: `2026-11-24T12:00:00Z`
  - Round 4 (Final): `2026-11-25T00:00:00Z`
- **Judge**: `z-ai/glm-5.3-flash` on OpenRouter (5-criterion priority: 1. Specific single day + date; 2. Selection & breadth across regions/fields; 3. Reads clearly from picture + short labels, zero falsehoods; 4. Faithful, no hype; 5. Craft, one clear composition, legible at ~300px)
- **Current Latest Submission**: `01a20ace-3aab-75f5-8eb5-62267e2cfab7` (v3, awaiting Round 2 judging)
- **Quota Status**: day 3/10 (resets `2026-11-24T00:00:00Z`), total 3/20, hard 3/40

## Experiment Log

| Ver | Commit | Hypothesis / Key Design Change | Local 1024px & 300px Check | File Size | Uploaded? | Sub ID | Round / Win Rate | Rank | Action |
| :-- | :----- | :----------------------------- | :------------------------- | :-------- | :-------- | :----- | :--------------- | :--- | :----- |
| v1a | -      | Initial magazine front page: 1 Hero + 4 Illustrated Cards + 2 Wire Strips | Good base; COP31 gavel cropped, badges overlapped top-left of art | 723,296 B PNG | No | - | - | - | Refined locally |
| v1  | `2c6d9d6` | Unobstructed editorial illustrations, `contain` + matched `#192B37` for COP31 gavel, lining numerals on `23 NOVEMBER 2026` | 1024px & 300px verified: zero text overlap/clipping | 725,772 B PNG | Yes | `01a20abc-a71a-7108-8140-33809f86215a` | Round 2 pending (`scored`) | TBD | In Round 2 |
| v2a | -      | Print Broadsheet paradigm + stylized World Locator SVG | Much stronger poster cohesion; orphan words on 3 sub-headlines | 835,889 B PNG | No | - | - | - | Refined locally |
| v2  | `133546c` | Eliminated all orphan words with single-line headlines (22.5px) + 168px artwork + clean facts | 1024px & 300px verified: zero orphans/overlaps | 859,311 B PNG | Yes | `01a20ac5-f03e-7790-9de3-cfab1a3b25c2` | Round 2 pending (`scored`) | TBD | In Round 2 |
| v3a | -      | Single panoramic AI world-map collage experiment (`panorama_v3.jpg`) | Rejected locally: distorted geography (Hormuz drawn across Africa) would violate Criterion 3 factual/plausibility gate | - | No | - | - | - | Discarded |
| v3  | `4e52274` | Maximum 300px Legibility + Cinematic Large Art Edition: expand 4 regional artworks to 192px (+41% vs v1), Hero to 292px with 36px headline & 25px stats, 24px card headlines & 17.5px facts (zero sub-17px body text), compact 50px dark-gold dual wire ribbon | 1024px & 300px verified: extraordinary clarity even on sub-facts at 300px, museum-grade balance | 809,737 B PNG | Yes | `01a20ace-3aab-75f5-8eb5-62267e2cfab7` | Round 2 pending (`scored`) | TBD | In Round 2 (latest) |
