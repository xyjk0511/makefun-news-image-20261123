"""Programmatic editorial poster renderer for Monday, 23 November 2026 world news (v3)."""

from __future__ import annotations

import base64
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT.parent / "assets"
OUTPUT_PNG = ROOT / "entry.png"
PREVIEW_300 = ROOT / "preview_300.png"
RAW_PNG = ROOT.parent / "raw_1024_v3.png"


def encode_image_data_uri(path: Path) -> str:
    raw = path.read_bytes()
    b64 = base64.b64encode(raw).decode("ascii")
    mime = "image/jpeg" if path.suffix.lower() in {".jpg", ".jpeg"} else "image/png"
    return f"data:{mime};base64,{b64}"


def world_locator_svg() -> str:
    """Compact high-contrast world locator with 5 color-matched regional news beacons."""
    return """
    <svg width="212" height="72" viewBox="0 0 218 74" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="Global news locator">
      <rect x="0.5" y="0.5" width="217" height="73" rx="3" fill="#0B1928" stroke="#2D4661" stroke-width="1"/>
      <line x1="0" y1="37" x2="218" y2="37" stroke="#1C3248" stroke-width="0.7" stroke-dasharray="2 3"/>
      <line x1="109" y1="0" x2="109" y2="74" stroke="#1C3248" stroke-width="0.7" stroke-dasharray="2 3"/>
      <g fill="#2C4966">
        <path d="M16 14 L42 12 L56 19 L52 29 L40 34 L34 40 L28 36 L22 27 Z"/>
        <path d="M44 43 L56 44 L63 54 L56 67 L49 69 L45 57 Z"/>
        <path d="M92 14 L116 12 L123 19 L118 26 L104 27 L94 24 Z"/>
        <path d="M92 31 L114 31 L124 41 L118 59 L109 65 L100 54 L94 42 Z"/>
        <path d="M120 14 L164 13 L184 22 L177 35 L162 43 L149 41 L141 47 L133 39 L123 36 L119 27 Z"/>
        <path d="M181 26 L187 24 L189 31 L183 32 Z"/>
        <path d="M164 46 L176 47 L179 51 L167 51 Z"/>
        <path d="M174 55 L195 54 L199 64 L185 67 L174 63 Z"/>
      </g>
      <circle cx="44" cy="24" r="7" fill="#10B981" fill-opacity="0.32"/>
      <circle cx="44" cy="24" r="3.8" fill="#34E0A1" stroke="#08131E" stroke-width="1"/>
      <circle cx="107" cy="28" r="7" fill="#E04F3A" fill-opacity="0.32"/>
      <circle cx="107" cy="28" r="3.8" fill="#FF6B54" stroke="#08131E" stroke-width="1"/>
      <circle cx="131" cy="34" r="7" fill="#F29F3D" fill-opacity="0.32"/>
      <circle cx="131" cy="34" r="3.8" fill="#FBBF5A" stroke="#08131E" stroke-width="1"/>
      <circle cx="118" cy="25" r="6" fill="#2DD4BF" fill-opacity="0.32"/>
      <circle cx="118" cy="25" r="3.4" fill="#2DD4BF" stroke="#08131E" stroke-width="1"/>
      <circle cx="166" cy="33" r="7" fill="#60A5FA" fill-opacity="0.32"/>
      <circle cx="166" cy="33" r="3.8" fill="#60A5FA" stroke="#08131E" stroke-width="1"/>
    </svg>
    """


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
    background: #F5EFE2;
    color: #0B131E;
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
  }}
  .poster {{
    width: 1024px;
    height: 1024px;
    display: flex;
    flex-direction: column;
    background: #F6F1E6;
  }}

  /* BOLD COLLECTOR MASTHEAD */
  .masthead {{
    height: 102px;
    background: linear-gradient(180deg, #09131F 0%, #102033 100%);
    color: #FFFBF2;
    border-top: 6px solid #D13D2A;
    border-bottom: 3.5px solid #DDA02C;
    padding: 0 22px;
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
    font-size: 14px;
    font-weight: 800;
    letter-spacing: 2.8px;
    color: #F6C255;
    text-transform: uppercase;
    margin-bottom: 2px;
  }}
  .mast-date {{
    font-family: Georgia, Cambria, "Times New Roman", serif;
    font-variant-numeric: lining-nums;
    font-size: 48px;
    font-weight: 900;
    letter-spacing: 0.4px;
    line-height: 0.96;
    color: #FFFFFF;
  }}
  .mast-date .day-accent {{
    color: #F7C25B;
  }}
  .mast-right {{
    display: flex;
    align-items: center;
    gap: 14px;
  }}
  .mast-meta {{
    text-align: right;
  }}
  .mast-title {{
    font-family: Georgia, Cambria, "Times New Roman", serif;
    font-size: 21px;
    font-weight: 900;
    letter-spacing: 1px;
    color: #FFFFFF;
    line-height: 1.1;
  }}
  .mast-sub {{
    margin-top: 4px;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.1px;
    color: #B4C6D8;
    text-transform: uppercase;
    line-height: 1.3;
  }}

  /* BODY CONTAINER */
  .content {{
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 0 18px;
  }}

  /* HERO FEATURE (LARGE CINEMATIC ART + ULTRA-LEGIBLE HEADLINE & STATS) */
  .hero {{
    height: 292px;
    display: flex;
    padding: 13px 0;
    border-bottom: 3px solid #0F1D2D;
    gap: 18px;
  }}
  .hero-art {{
    width: 472px;
    height: 100%;
    flex-shrink: 0;
    background: #0D1B2A;
    border: 1.5px solid #1C3147;
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
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .hero-kicker-row {{
    display: flex;
    align-items: center;
    gap: 9px;
  }}
  .badge-solid {{
    background: #0B7A54;
    color: #FFFFFF;
    font-size: 13.5px;
    font-weight: 900;
    letter-spacing: 1.3px;
    padding: 4px 10px;
    text-transform: uppercase;
  }}
  .hero-region {{
    font-size: 13.5px;
    font-weight: 800;
    letter-spacing: 0.9px;
    color: #3E5063;
    text-transform: uppercase;
  }}
  .hero-hl {{
    font-family: Georgia, Cambria, "Times New Roman", serif;
    font-variant-numeric: lining-nums;
    font-size: 36px;
    font-weight: 900;
    line-height: 1.06;
    color: #08111B;
  }}
  .hero-stats {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 9px;
  }}
  .stat-box {{
    background: #0B1927;
    padding: 7px 8px;
    text-align: center;
    border-bottom: 4px solid #1AC88A;
  }}
  .stat-k {{
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.1px;
    color: #A7BFD5;
    text-transform: uppercase;
  }}
  .stat-v {{
    font-size: 25px;
    font-weight: 900;
    color: #3BE8A9;
    line-height: 1.08;
    margin-top: 1px;
    font-variant-numeric: lining-nums;
  }}
  .hero-deck {{
    font-size: 18.5px;
    line-height: 1.22;
    color: #162330;
    font-weight: 600;
  }}

  /* 2x2 LARGE-ART BROADSHEET GRID */
  .grid {{
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 1.5px 1fr;
    grid-template-rows: 1fr 1.5px 1fr;
    padding: 10px 0 8px 0;
  }}
  .v-line {{
    background: #C2B8A3;
    grid-column: 2;
    grid-row: 1 / 4;
  }}
  .h-line {{
    background: #C2B8A3;
    grid-column: 1 / 4;
    grid-row: 2;
  }}
  .cell {{
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }}
  .c-tl {{ grid-column: 1; grid-row: 1; padding: 0 14px 9px 0; }}
  .c-tr {{ grid-column: 3; grid-row: 1; padding: 0 0 9px 14px; }}
  .c-bl {{ grid-column: 1; grid-row: 3; padding: 9px 14px 0 0; }}
  .c-br {{ grid-column: 3; grid-row: 3; padding: 9px 0 0 14px; }}

  .cell-art {{
    height: 192px;
    width: 100%;
    overflow: hidden;
    border: 1px solid #C0B6A2;
    flex-shrink: 0;
  }}
  .cell-art img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }}
  .art-libya {{ background: #182C40; }}
  .art-libya img {{ object-position: center 46%; }}
  .art-hormuz {{ background: #103542; }}
  .art-hormuz img {{ object-position: center 35%; }}
  .art-cop31 {{ background: #192B37; }}
  .art-cop31 img {{ object-fit: contain !important; object-position: center center; }}
  .art-asia {{ background: #13213C; }}
  .art-asia img {{ object-position: center 54%; }}

  .cell-copy {{
    flex: 1;
    padding-top: 6px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .cell-kicker-row {{
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
  }}
  .dot-geo {{ background: #D13D2A; }}
  .dot-me {{ background: #C25D10; }}
  .dot-climate {{ background: #147E76; }}
  .dot-asia {{ background: #234C96; }}

  .cell-kicker {{
    font-size: 13px;
    font-weight: 900;
    letter-spacing: 1.3px;
    text-transform: uppercase;
  }}
  .k-geo {{ color: #B42B1A; }}
  .k-me {{ color: #A14A09; }}
  .k-climate {{ color: #0E6A63; }}
  .k-asia {{ color: #193E80; }}

  .cell-hl {{
    font-family: Georgia, Cambria, "Times New Roman", serif;
    font-variant-numeric: lining-nums;
    font-size: 24px;
    font-weight: 900;
    line-height: 1.08;
    color: #08111B;
    white-space: nowrap;
  }}
  .cell-fact {{
    font-size: 17.5px;
    line-height: 1.16;
    color: #1C2A38;
    font-weight: 600;
    white-space: nowrap;
  }}

  /* ULTRA-CRISP COMPACT WIRE RIBBON */
  .ribbon {{
    height: 50px;
    background: #0C1A2A;
    border-top: 3px solid #DDA02C;
    padding: 0 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: #F7F3EA;
  }}
  .ribbon-item {{
    display: flex;
    align-items: center;
    gap: 9px;
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 0.2px;
  }}
  .ribbon-tag {{
    background: #1C3550;
    color: #F7C25B;
    font-size: 12px;
    font-weight: 900;
    letter-spacing: 1.2px;
    padding: 3px 8px;
    text-transform: uppercase;
    border-radius: 2px;
  }}
  .ribbon-sep {{
    width: 2px;
    height: 24px;
    background: rgba(255, 255, 255, 0.24);
  }}
</style>
</head>
<body>
  <div class="poster">
    <header class="masthead">
      <div class="mast-left">
        <div class="mast-kicker">MONDAY · WORLD NEWS IN ONE IMAGE</div>
        <div class="mast-date"><span class="day-accent">23</span> NOVEMBER 2026</div>
      </div>
      <div class="mast-right">
        <div class="mast-meta">
          <div class="mast-title">WORLD DISPATCH</div>
          <div class="mast-sub">6 REGIONS · MARKETS<br/>WAR · CLIMATE · TECH</div>
        </div>
        {world_locator_svg()}
      </div>
    </header>

    <main class="content">
      <section class="hero">
        <div class="hero-art">
          <img src="{images['hero']}" alt="Nvidia rally and Wall Street surge" />
        </div>
        <div class="hero-copy">
          <div class="hero-kicker-row">
            <span class="badge-solid">MARKETS · AI</span>
            <span class="hero-region">NEW YORK &amp; GLOBAL CHIPS</span>
          </div>
          <h1 class="hero-hl">Nvidia Reinstates Jensen Huang; Wall Street Surges</h1>
          <div class="hero-stats">
            <div class="stat-box">
              <div class="stat-k">NVIDIA</div>
              <div class="stat-v">+31.5%</div>
            </div>
            <div class="stat-box">
              <div class="stat-k">NASDAQ</div>
              <div class="stat-v">+6.5%</div>
            </div>
            <div class="stat-box">
              <div class="stat-k">S&amp;P 500</div>
              <div class="stat-v">+4.7%</div>
            </div>
          </div>
          <p class="hero-deck">Unanimous board reversal adds $952B and sparks global chip rebound.</p>
        </div>
      </section>

      <section class="grid">
        <div class="v-line"></div>
        <div class="h-line"></div>

        <article class="cell c-tl">
          <div class="cell-art art-libya">
            <img src="{images['libya']}" alt="Ukraine sea drones sink Russian warship Merkury in Libya" />
          </div>
          <div class="cell-copy">
            <div class="cell-kicker-row">
              <span class="dot dot-geo"></span>
              <span class="cell-kicker k-geo">EUROPE · NORTH AFRICA</span>
            </div>
            <h2 class="cell-hl">Ukraine Sinks Warship in Libya</h2>
            <p class="cell-fact">7 sea drones sink Russia&rsquo;s <em>Merkury</em> 2,400 km away.</p>
          </div>
        </article>

        <article class="cell c-tr">
          <div class="cell-art art-hormuz">
            <img src="{images['hormuz']}" alt="Strait of Hormuz U.S.-Iran naval blockade" />
          </div>
          <div class="cell-copy">
            <div class="cell-kicker-row">
              <span class="dot dot-me"></span>
              <span class="cell-kicker k-me">MIDDLE EAST · SECURITY</span>
            </div>
            <h2 class="cell-hl">Iran Defies Hormuz Blockade</h2>
            <p class="cell-fact">Trump warns of strikes; Israel&rsquo;s Eisenkot urges calm.</p>
          </div>
        </article>

        <article class="cell c-bl">
          <div class="cell-art art-cop31">
            <img src="{images['cop31']}" alt="COP31 climate talks collapse in Antalya" />
          </div>
          <div class="cell-copy">
            <div class="cell-kicker-row">
              <span class="dot dot-climate"></span>
              <span class="cell-kicker k-climate">GLOBAL · CLIMATE</span>
            </div>
            <h2 class="cell-hl">Fallout After COP31 Collapses</h2>
            <p class="cell-fact">UN &amp; EU react to first climate summit failure since 2009.</p>
          </div>
        </article>

        <article class="cell c-br">
          <div class="cell-art art-asia">
            <img src="{images['asia']}" alt="Lowy 2026 Asia Power Index balance" />
          </div>
          <div class="cell-copy">
            <div class="cell-kicker-row">
              <span class="dot dot-asia"></span>
              <span class="cell-kicker k-asia">ASIA-PACIFIC · POWER</span>
            </div>
            <h2 class="cell-hl">U.S.&ndash;China Gap Hits Asia Low</h2>
            <p class="cell-fact">2026 Lowy Index narrows gap to 5.3 pts; India rises 3rd.</p>
          </div>
        </article>
      </section>
    </main>

    <footer class="ribbon">
      <div class="ribbon-item">
        <span class="ribbon-tag">IRAQ · PEACE</span>
        <span>PKK vacates 14 bases in N. Iraq</span>
      </div>
      <div class="ribbon-sep"></div>
      <div class="ribbon-item">
        <span class="ribbon-tag">BANKS · AI</span>
        <span>U.S. lenders add AI agent kill switches</span>
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

    png_candidate = raw_png.with_name("candidate_opt_v3.png")
    img.save(png_candidate, format="PNG", optimize=True, compress_level=9)
    png_size = png_candidate.stat().st_size

    if png_size <= 950_000:
        out_path.write_bytes(png_candidate.read_bytes())
        chosen = f"PNG ({png_size:,} bytes)"
    else:
        for quality in (94, 92, 90, 88):
            jpg_candidate = raw_png.with_name("candidate_opt_v3.jpg")
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
