# makefun-news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/xyjk0511/makefun-news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/xyjk0511/makefun-news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

Programmatic editorial front-page generator summarizing Monday, 23 November 2026 world news into a single 1024×1024 visual dispatch engineered for instant readability at both full resolution and 300px thumbnail scale.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Architecture

- `main.ts`: Zero-dependency Node 22 entrypoint that deterministically validates and writes the verified 1024×1024 image (`entry.png`) to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png`).
- `scripts/render_frontpage.py`: Editorial layout composer using HTML/CSS/SVG + headless Chromium (Playwright) and Pillow thumbnail/size verification to generate and optimize the 1024×1024 front-page composition.
- `EXPERIMENTS.md`: Iterative visual design and server-round evaluation log.

---

<sub>Entered on [make.fun](https://make.fun/?ref=1wfaqr7c&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
