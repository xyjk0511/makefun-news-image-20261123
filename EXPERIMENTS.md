# Bounty: news-image-20261123 | Goal: Top Win Rate (#1)

- **Competition**: Sum up 23 November's world news in one image (`news-image-20261123`)
- **Deadline (UTC)**: `2026-11-25T00:00:00.000Z`
- **Blind Rounds**:
  - Round 1: `2026-11-23T12:00:00Z` (judged, 7,226 entries)
  - Round 2: `2026-11-24T00:00:00Z` (v1 & v2 both entered for head-to-head A/B validation!)
  - Round 3: `2026-11-24T12:00:00Z`
  - Round 4 (Final): `2026-11-25T00:00:00Z`
- **Judge**: `z-ai/glm-5.3-flash` on OpenRouter (5-criterion priority: 1. Specific single day + date; 2. Selection & breadth across regions/fields; 3. Reads clearly from picture + short labels, zero falsehoods; 4. Faithful, no hype; 5. Craft, one clear composition, legible at ~300px)
- **Current Best Submission**: `01a20abc-a71a-7108-8140-33809f86215a` (v1, awaiting Round 2 judging)
- **Quota Status**: day 1/10 (resets `2026-11-24T00:00:00Z`), total 1/20, hard 1/40

## Experiment Log

| Ver | Commit | Hypothesis / Key Design Change | Local 1024px & 300px Check | File Size | Uploaded? | Sub ID | Round / Win Rate | Rank | Action |
| :-- | :----- | :----------------------------- | :------------------------- | :-------- | :-------- | :----- | :--------------- | :--- | :----- |
| v1a | -      | Initial magazine front page: 1 Hero + 4 Illustrated Cards + 2 Wire Strips | Good base; COP31 gavel cropped, badges overlapped top-left of art, masthead numerals slightly uneven | 723,296 B PNG | No | - | - | - | Refined locally |
| v1  | `2c6d9d6` | Unobstructed editorial illustrations, `contain` + matched `#192B37` for COP31 gavel, lining numerals on `23 NOVEMBER 2026`, crisp 4px top color bars & kickers in white text zones | 1024px & 300px verified: zero text overlap/clipping, razor-sharp date/headlines/metrics | 725,772 B PNG | Yes | `01a20abc-a71a-7108-8140-33809f86215a` | Round 2 pending (`scored`) | TBD | Baseline live |
| v2a | -      | Paradigm shift to Print Broadsheet: remove web cards/shadows, add hairline print grid, add stylized World Locator SVG with 6 color-coded regional pins in masthead, enlarge art & headlines | Much stronger cohesive poster feel; spotted orphan words on 3 sub-headlines & COP31 deck | 835,889 B PNG | No | - | - | - | Refined locally |
| v2  | pending | Eliminate all orphan words via tight balanced single-line headlines (22.5px) + single-line crisp facts (16px), expand 4 regional artworks to 168px height, remove July Hugging Face date reference to prevent stale-event misread | 1024px & 300px verified: zero orphans/overlaps, every headline & metric crystal clear at 300px, museum-grade broadsheet cohesion | 859,311 B PNG | Pending | - | Round 2 target | TBD | Ready to submit |
