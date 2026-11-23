# Bounty: news-image-20261123 | Goal: Top Win Rate (#1)

- **Competition**: Sum up 23 November's world news in one image (`news-image-20261123`)
- **Deadline (UTC)**: `2026-11-25T00:00:00.000Z`
- **Blind Rounds**:
  - Round 1: `2026-11-23T12:00:00Z` (judged, 7,226 entries)
  - Round 2: `2026-11-24T00:00:00Z` (target for v1/v2)
  - Round 3: `2026-11-24T12:00:00Z`
  - Round 4 (Final): `2026-11-25T00:00:00Z`
- **Judge**: `z-ai/glm-5.3-flash` on OpenRouter (5-criterion priority: 1. Specific single day + date; 2. Selection & breadth across regions/fields; 3. Reads clearly from picture + short labels, zero falsehoods; 4. Faithful, no hype; 5. Craft, one clear composition, legible at ~300px)
- **Current Best Submission**: _Pending v1_
- **Quota Status**: day 0/10 (resets `2026-11-24T00:00:00Z`), total 0/20, hard 0/40

## Experiment Log

| Ver | Commit | Hypothesis / Key Design Change | Local 1024px & 300px Check | File Size | Uploaded? | Sub ID | Round / Win Rate | Rank | Action |
| :-- | :----- | :----------------------------- | :------------------------- | :-------- | :-------- | :----- | :--------------- | :--- | :----- |
| v1a | -      | Initial magazine front page: 1 Hero + 4 Illustrated Cards + 2 Wire Strips | Good base; COP31 gavel cropped, badges overlapped top-left of art, masthead numerals slightly uneven | 723,296 B PNG | No | - | - | - | Refined locally |
| v1  | pending | Unobstructed editorial illustrations, `contain` + matched `#192B37` for COP31 gavel, lining numerals on `23 NOVEMBER 2026`, crisp 4px top color bars & kickers in white text zones | 1024px & 300px verified: zero text overlap/clipping, razor-sharp date/headlines/metrics, all 5 art scenes unobstructed | 725,772 B PNG | Pending | - | - | - | Ready for Round 2 |
