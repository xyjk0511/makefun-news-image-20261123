"""Programmatic editorial front-page renderer for 23 November 2026 world news."""

from __future__ import annotations

import base64
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT.parent / "assets"
OUTPUT_PNG = ROOT / "entry.png"
PREVIEW_300 = ROOT / "preview_300.png"
RAW_PNG = ROOT.parent / "raw_1024.png"


def encode_image_data_uri(path: Path) -> str:
    raw = path.read_bytes()
    b64 = base64.b64encode(raw).decode("ascii")
    mime = "image/jpeg" if path.suffix.lower() in {".jpg", ".jpeg"} else "image/png"
    return f"data:{mime};base64,{b64}"


def build_html(images: dict[str, str]) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<style>
  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}
  html, body {{
    width: 1024px;
    height: 1024px;
    overflow: hidden;
    background: #F4EFE4;
    color: #0E1724;
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
  }}
  .page {{
    width: 1024px;
    height: 1024px;
    display: flex;
    flex-direction: column;
    background: #F4EFE4;
  }}

  /* MASTHEAD */
  .masthead {{
    height: 100px;
    background: linear-gradient(135deg, #0A1522 0%, #13253A 100%);
    color: #FAF6EE;
    border-top: 5px solid #D1432F;
    border-bottom: 3px solid #D99B29;
    padding: 0 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .mast-left {{
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}
  .mast-kicker {{
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 2.6px;
    color: #F2B84B;
    text-transform: uppercase;
    margin-bottom: 2px;
  }}
  .mast-date {{
    font-family: Georgia, Cambria, "Times New Roman", serif;
    font-variant-numeric: lining-nums;
    font-size: 42px;
    font-weight: 900;
    letter-spacing: 0.6px;
    line-height: 1.02;
    color: #FFFFFF;
  }}
  .mast-date .day-num {{
    color: #F7C25B;
  }}
  .mast-right {{
    text-align: right;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    justify-content: center;
  }}
  .mast-brand {{
    font-family: Georgia, Cambria, "Times New Roman", serif;
    font-size: 24px;
    font-weight: 900;
    letter-spacing: 1px;
    color: #FFFFFF;
    line-height: 1.1;
  }}
  .mast-sub {{
    margin-top: 5px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1.4px;
    color: #B8C7D9;
    text-transform: uppercase;
  }}

  /* CONTENT BODY */
  .body {{
    flex: 1;
    padding: 14px 18px 12px 18px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }}

  /* HERO STORY */
  .hero {{
    height: 256px;
    background: #FFFDF8;
    border: 1.5px solid #CFC6B4;
    border-left: 6px solid #0E8A5F;
    border-radius: 6px;
    display: flex;
    overflow: hidden;
    box-shadow: 0 3px 10px rgba(10, 21, 34, 0.08);
  }}
  .hero-art {{
    width: 438px;
    height: 100%;
    position: relative;
    flex-shrink: 0;
    background: #0D1B2A;
    overflow: hidden;
  }}
  .hero-art img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center 46%;
    display: block;
  }}
  .hero-copy {{
    flex: 1;
    padding: 13px 18px 13px 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .tag-row {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .pill {{
    display: inline-block;
    padding: 3px 9px;
    border-radius: 3px;
    font-size: 12.5px;
    font-weight: 800;
    letter-spacing: 1.1px;
    text-transform: uppercase;
    color: #FFFFFF;
    line-height: 1.2;
  }}
  .pill-hero {{ background: #0C7C55; }}
  .pill-geo {{ background: #C83E2B; }}
  .pill-me {{ background: #B85914; }}
  .pill-climate {{ background: #157770; }}
  .pill-asia {{ background: #264B8A; }}

  .loc-tag {{
    font-size: 12.5px;
    font-weight: 700;
    letter-spacing: 0.8px;
    color: #546476;
    text-transform: uppercase;
  }}
  .hero-title {{
    font-family: Georgia, Cambria, "Times New Roman", serif;
    font-variant-numeric: lining-nums;
    font-size: 31px;
    font-weight: 900;
    line-height: 1.1;
    color: #0B1522;
  }}
  .hero-metrics {{
    display: flex;
    gap: 8px;
  }}
  .metric-box {{
    flex: 1;
    background: #0E1F2E;
    border-radius: 4px;
    padding: 5px 8px;
    text-align: center;
    border-bottom: 3px solid #16B87F;
  }}
  .metric-label {{
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
    color: #A6BCD0;
    text-transform: uppercase;
  }}
  .metric-val {{
    font-size: 21px;
    font-weight: 900;
    color: #34E0A1;
    line-height: 1.1;
    margin-top: 1px;
  }}
  .hero-summary {{
    font-size: 16.5px;
    line-height: 1.25;
    color: #1F2D3B;
    font-weight: 500;
  }}

  /* 2x2 REGIONAL GRID */
  .grid {{
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 12px;
  }}
  .card {{
    background: #FFFDF8;
    border: 1.5px solid #CFC6B4;
    border-radius: 6px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow: 0 2px 8px rgba(10, 21, 34, 0.06);
  }}
  .card-geo {{ border-top: 4px solid #C83E2B; }}
  .card-me {{ border-top: 4px solid #B85914; }}
  .card-climate {{ border-top: 4px solid #157770; }}
  .card-asia {{ border-top: 4px solid #264B8A; }}
  .card-art {{
    height: 146px;
    width: 100%;
    position: relative;
    overflow: hidden;
    background: #102030;
    flex-shrink: 0;
  }}
  .card-art img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }}
  .img-libya {{ object-position: center 48%; }}
  .img-hormuz {{ object-position: center 34%; }}
  .img-cop31 {{ object-fit: contain !important; object-position: center center; }}
  .img-cop31-wrap {{ background: #192B37; }}
  .img-asia {{ object-position: center 54%; }}
  .card-body {{
    flex: 1;
    padding: 7px 13px 8px 13px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .card-kicker {{
    font-size: 11.5px;
    font-weight: 900;
    letter-spacing: 1.25px;
    text-transform: uppercase;
    line-height: 1.1;
  }}
  .kicker-geo {{ color: #B83220; }}
  .kicker-me {{ color: #A64E0E; }}
  .kicker-climate {{ color: #116963; }}
  .kicker-asia {{ color: #1E4282; }}
  .card-title {{
    font-family: Georgia, Cambria, "Times New Roman", serif;
    font-variant-numeric: lining-nums;
    font-size: 21.5px;
    font-weight: 900;
    line-height: 1.11;
    color: #0B1522;
  }}
  .card-desc {{
    font-size: 15px;
    line-height: 1.22;
    color: #202E3D;
    font-weight: 500;
  }}

  /* BOTTOM WIRE STRIP */
  .wire-bar {{
    height: 106px;
    background: #0F1E2F;
    border-top: 3px solid #D99B29;
    padding: 10px 18px;
    display: grid;
    grid-template-columns: 1fr 1px 1fr;
    gap: 16px;
    align-items: center;
    color: #F6F2EA;
  }}
  .wire-divider {{
    width: 1px;
    height: 76px;
    background: rgba(255, 255, 255, 0.18);
  }}
  .wire-item {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}
  .wire-icon {{
    width: 48px;
    height: 48px;
    border-radius: 6px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  .wire-icon-peace {{ background: #1D4D4F; border: 1.5px solid #48B5A3; }}
  .wire-icon-bank {{ background: #3B284D; border: 1.5px solid #C59BFF; }}
  .wire-text {{
    display: flex;
    flex-direction: column;
    gap: 3px;
  }}
  .wire-kicker {{
    font-size: 11.5px;
    font-weight: 800;
    letter-spacing: 1.3px;
    text-transform: uppercase;
    color: #F5BE54;
  }}
  .wire-title {{
    font-family: Georgia, Cambria, "Times New Roman", serif;
    font-size: 19px;
    font-weight: 800;
    line-height: 1.14;
    color: #FFFFFF;
  }}
  .wire-sub {{
    font-size: 13.5px;
    line-height: 1.2;
    color: #C4D2E0;
  }}
</style>
</head>
<body>
  <div class="page">
    <header class="masthead">
      <div class="mast-left">
        <div class="mast-kicker">MONDAY · WORLD NEWS SUMMARY</div>
        <div class="mast-date"><span class="day-num">23</span> NOVEMBER 2026</div>
      </div>
      <div class="mast-right">
        <div class="mast-brand">GLOBAL DISPATCH</div>
        <div class="mast-sub">AMERICAS · EUROPE · MIDDLE EAST · AFRICA · ASIA</div>
      </div>
    </header>

    <main class="body">
      <section class="hero">
        <div class="hero-art">
          <img src="{images['hero']}" alt="Nvidia rally illustration" />
        </div>
        <div class="hero-copy">
          <div class="tag-row">
            <span class="pill pill-hero">MARKETS · TECH</span>
            <span class="loc-tag">WALL STREET &amp; GLOBAL CHIPS</span>
          </div>
          <h1 class="hero-title">Nvidia Reinstates Jensen Huang; Wall Street Roars Back</h1>
          <div class="hero-metrics">
            <div class="metric-box">
              <div class="metric-label">NVIDIA</div>
              <div class="metric-val">+31.5%</div>
            </div>
            <div class="metric-box">
              <div class="metric-label">NASDAQ</div>
              <div class="metric-val">+6.5%</div>
            </div>
            <div class="metric-box">
              <div class="metric-label">S&amp;P 500</div>
              <div class="metric-val">+4.7%</div>
            </div>
          </div>
          <p class="hero-summary">Board restores CEO after White House backing, adding $952B and sparking a broad tech and chip surge.</p>
        </div>
      </section>

      <section class="grid">
        <article class="card card-geo">
          <div class="card-art">
            <img class="img-libya" src="{images['libya']}" alt="Benghazi naval drone strike" />
          </div>
          <div class="card-body">
            <div class="card-kicker kicker-geo">EUROPE · NORTH AFRICA · WAR</div>
            <h2 class="card-title">Ukraine Sea Drones Sink Russian Warship in Libya</h2>
            <p class="card-desc">Kyiv confirms 7 drones sank corvette <em>Merkury</em> in Benghazi, 2,400 km away; drones also hit Russian refineries.</p>
          </div>
        </article>

        <article class="card card-me">
          <div class="card-art">
            <img class="img-hormuz" src="{images['hormuz']}" alt="Strait of Hormuz naval blockade" />
          </div>
          <div class="card-body">
            <div class="card-kicker kicker-me">MIDDLE EAST · SECURITY</div>
            <h2 class="card-title">Iran Defies U.S. Blockade; Trump Warns of Strikes</h2>
            <p class="card-desc">Tehran vows &ldquo;all means&rdquo; in Strait of Hormuz; Trump threatens blockade runners as Israel&rsquo;s Eisenkot urges restraint.</p>
          </div>
        </article>

        <article class="card card-climate">
          <div class="card-art img-cop31-wrap">
            <img class="img-cop31" src="{images['cop31']}" alt="COP31 climate collapse" />
          </div>
          <div class="card-body">
            <div class="card-kicker kicker-climate">GLOBAL · CLIMATE</div>
            <h2 class="card-title">Global Dismay After COP31 Collapses Without Deal</h2>
            <p class="card-desc">UN chief &amp; EU react after Antalya talks ended with no fossil-fuel pact&mdash;first UN climate collapse since 2009.</p>
          </div>
        </article>

        <article class="card card-asia">
          <div class="card-art">
            <img class="img-asia" src="{images['asia']}" alt="Asia Power Index balance" />
          </div>
          <div class="card-body">
            <div class="card-kicker kicker-asia">ASIA-PACIFIC · GEOPOLITICS</div>
            <h2 class="card-title">U.S.&ndash;China Power Gap Hits Record Low in Asia</h2>
            <p class="card-desc">2026 Lowy Asia Power Index narrows gap to 5.3 points as India rises as third pole and allies weigh shifts.</p>
          </div>
        </article>
      </section>
    </main>

    <footer class="wire-bar">
      <div class="wire-item">
        <div class="wire-icon wire-icon-peace">
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
            <path d="M5 21L12 10L16.5 16L20 11.5L24 21H5Z" stroke="#6BE0CC" stroke-width="2.2" stroke-linejoin="round"/>
            <path d="M14 4V9M11.5 6.5H16.5" stroke="#F5BE54" stroke-width="2.2" stroke-linecap="round"/>
          </svg>
        </div>
        <div class="wire-text">
          <div class="wire-kicker">TURKEY &amp; IRAQ · DISARMAMENT</div>
          <div class="wire-title">PKK Vacates 14 More Bases in N. Iraq</div>
          <div class="wire-sub">Ankara reports Hakurk pullout advancing peace process.</div>
        </div>
      </div>

      <div class="wire-divider"></div>

      <div class="wire-item">
        <div class="wire-icon wire-icon-bank">
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
            <path d="M14 3L23 7V13.5C23 19.2 19.1 23.6 14 25C8.9 23.6 5 19.2 5 13.5V7L14 3Z" stroke="#D3B3FF" stroke-width="2.2" stroke-linejoin="round"/>
            <path d="M10.5 14L13 16.5L18 11.5" stroke="#F5BE54" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <div class="wire-text">
          <div class="wire-kicker">BANKING · AI GOVERNANCE</div>
          <div class="wire-title">U.S. Banks Rein In Internal AI Agents</div>
          <div class="wire-sub">Major lenders add kill switches after Hugging Face breach.</div>
        </div>
      </div>
    </footer>
  </div>
</body>
</html>
"""


def optimize_output(raw_png: Path, out_path: Path, preview_path: Path) -> None:
    img = Image.open(raw_png).convert("RGB")
    if img.size != (1024, 1024):
        img = img.resize((1024, 1024), Image.Resampling.LANCZOS)

    # Save crisp high-quality JPEG (kept named entry.png per rules) or PNG under 1 MiB.
    # Prefer lossless PNG if <= 900 KB; otherwise crisp JPEG quality 93 (subsampling=0 for razor-sharp text).
    png_candidate = raw_png.with_name("candidate_opt.png")
    img.save(png_candidate, format="PNG", optimize=True, compress_level=9)
    png_size = png_candidate.stat().st_size

    if png_size <= 950_000:
        out_path.write_bytes(png_candidate.read_bytes())
        chosen = f"PNG ({png_size:,} bytes)"
    else:
        for quality in (94, 92, 90, 88):
            jpg_candidate = raw_png.with_name("candidate_opt.jpg")
            img.save(jpg_candidate, format="JPEG", quality=quality, subsampling=0, optimize=True)
            jpg_size = jpg_candidate.stat().st_size
            if jpg_size <= 950_000:
                out_path.write_bytes(jpg_candidate.read_bytes())
                chosen = f"JPEG q={quality} 4:4:4 ({jpg_size:,} bytes)"
                break
        else:
            raise RuntimeError("Could not compress image under 950 KB")

    thumb = img.resize((300, 300), Image.Resampling.LANCZOS)
    thumb.save(preview_path, format="PNG", optimize=True)
    print(f"Wrote {out_path} as {chosen}; 300px preview -> {preview_path}")


def main() -> None:
    images = {
        "hero": encode_image_data_uri(ASSETS_DIR / "hero_nvidia_rally.jpg"),
        "libya": encode_image_data_uri(ASSETS_DIR / "card_libya_warship.jpg"),
        "hormuz": encode_image_data_uri(ASSETS_DIR / "card_hormuz_blockade.jpg"),
        "cop31": encode_image_data_uri(ASSETS_DIR / "card_cop31_climate.jpg"),
        "asia": encode_image_data_uri(ASSETS_DIR / "card_asia_power.jpg"),
    }
    html = build_html(images)
    with sync_playwright() as p:
        browser = None
        for kwargs in (
            {"channel": "chrome"},
            {"channel": "msedge"},
            {},
        ):
            try:
                browser = p.chromium.launch(**kwargs)
                break
            except Exception:
                continue
        if browser is None:
            raise RuntimeError("No Chromium/Chrome/Edge browser available for Playwright")
        page = browser.new_page(viewport={"width": 1024, "height": 1024}, device_scale_factor=1)
        page.set_content(html, wait_until="load")
        page.screenshot(path=str(RAW_PNG), type="png", clip={"x": 0, "y": 0, "width": 1024, "height": 1024})
        browser.close()

    optimize_output(RAW_PNG, OUTPUT_PNG, PREVIEW_300)


if __name__ == "__main__":
    main()
