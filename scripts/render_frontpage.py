"""Programmatic editorial broadsheet renderer for Monday, 23 November 2026 world news (v2)."""

from __future__ import annotations

import base64
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT.parent / "assets"
OUTPUT_PNG = ROOT / "entry.png"
PREVIEW_300 = ROOT / "preview_300.png"
RAW_PNG = ROOT.parent / "raw_1024_v2.png"


def encode_image_data_uri(path: Path) -> str:
    raw = path.read_bytes()
    b64 = base64.b64encode(raw).decode("ascii")
    mime = "image/jpeg" if path.suffix.lower() in {".jpg", ".jpeg"} else "image/png"
    return f"data:{mime};base64,{b64}"


def world_locator_svg() -> str:
    """Compact high-contrast stylized world map with 6 numbered regional pins matching the 6 stories."""
    return """
    <svg width="218" height="74" viewBox="0 0 218 74" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="Global coverage locator">
      <rect x="0.5" y="0.5" width="217" height="73" rx="3" fill="#0D1C2D" stroke="#2B425B" stroke-width="1"/>
      <!-- Minimalist latitude/longitude graticule -->
      <line x1="0" y1="37" x2="218" y2="37" stroke="#1E344B" stroke-width="0.7" stroke-dasharray="2 3"/>
      <line x1="109" y1="0" x2="109" y2="74" stroke="#1E344B" stroke-width="0.7" stroke-dasharray="2 3"/>
      <!-- Simplified world continent silhouettes -->
      <g fill="#2A445E">
        <!-- North America -->
        <path d="M16 14 L42 12 L56 19 L52 29 L40 34 L34 40 L28 36 L22 27 Z"/>
        <!-- South America -->
        <path d="M44 43 L56 44 L63 54 L56 67 L49 69 L45 57 Z"/>
        <!-- Europe -->
        <path d="M92 14 L116 12 L123 19 L118 26 L104 27 L94 24 Z"/>
        <!-- Africa -->
        <path d="M92 31 L114 31 L124 41 L118 59 L109 65 L100 54 L94 42 Z"/>
        <!-- Middle East & Asia -->
        <path d="M120 14 L164 13 L184 22 L177 35 L162 43 L149 41 L141 47 L133 39 L123 36 L119 27 Z"/>
        <!-- Maritime SE Asia & Japan -->
        <path d="M181 26 L187 24 L189 31 L183 32 Z"/>
        <path d="M164 46 L176 47 L179 51 L167 51 Z"/>
        <!-- Australia -->
        <path d="M174 55 L195 54 L199 64 L185 67 L174 63 Z"/>
      </g>
      <!-- Regional story pins: NY/Markets, Libya/Europe, Hormuz/Iran, COP31/Antalya, Asia-Pacific, N.Iraq/PKK -->
      <!-- 1. Americas / Wall St (Emerald) -->
      <circle cx="44" cy="24" r="6.5" fill="#10B981" fill-opacity="0.28"/>
      <circle cx="44" cy="24" r="3.6" fill="#34E0A1" stroke="#08131E" stroke-width="1"/>
      <!-- 2. Libya / Ukraine-Russia (Vermilion) -->
      <circle cx="107" cy="28" r="6.5" fill="#E04F3A" fill-opacity="0.28"/>
      <circle cx="107" cy="28" r="3.6" fill="#FF6B54" stroke="#08131E" stroke-width="1"/>
      <!-- 3. Strait of Hormuz (Amber) -->
      <circle cx="131" cy="34" r="6.5" fill="#F29F3D" fill-opacity="0.28"/>
      <circle cx="131" cy="34" r="3.6" fill="#FBBF5A" stroke="#08131E" stroke-width="1"/>
      <!-- 4. COP31 Antalya / Global Climate (Teal) -->
      <circle cx="118" cy="26" r="5.5" fill="#2DD4BF" fill-opacity="0.28"/>
      <circle cx="118" cy="26" r="3.3" fill="#2DD4BF" stroke="#08131E" stroke-width="1"/>
      <!-- 5. Asia-Pacific (Cobalt/Gold) -->
      <circle cx="166" cy="33" r="6.5" fill="#60A5FA" fill-opacity="0.28"/>
      <circle cx="166" cy="33" r="3.6" fill="#60A5FA" stroke="#08131E" stroke-width="1"/>
      <!-- 6. Northern Iraq / Turkey (Lavender-Gold) -->
      <circle cx="124" cy="29" r="3.0" fill="#F5D061" stroke="#08131E" stroke-width="0.9"/>
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
    background: #F6F1E6;
    color: #0D1520;
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
  }}
  .sheet {{
    width: 1024px;
    height: 1024px;
    display: flex;
    flex-direction: column;
    background:
      radial-gradient(circle at 15% 15%, rgba(255, 253, 248, 0.9), rgba(242, 235, 221, 0.85)),
      #F5EFE3;
  }}

  /* CLASSIC BROADSHEET MASTHEAD */
  .masthead {{
    height: 102px;
    background: #0B1522;
    color: #FBF7EE;
    border-top: 6px solid #C93B2B;
    border-bottom: 3px solid #D89B2B;
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
    font-size: 13.5px;
    font-weight: 800;
    letter-spacing: 2.8px;
    color: #F4BE52;
    text-transform: uppercase;
    margin-bottom: 2px;
  }}
  .mast-date {{
    font-family: Georgia, Cambria, "Times New Roman", serif;
    font-variant-numeric: lining-nums;
    font-size: 46px;
    font-weight: 900;
    letter-spacing: 0.4px;
    line-height: 0.98;
    color: #FFFFFF;
  }}
  .mast-date .accent-day {{
    color: #F7C25B;
  }}
  .mast-right {{
    display: flex;
    align-items: center;
    gap: 14px;
  }}
  .mast-meta {{
    text-align: right;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}
  .mast-edition {{
    font-family: Georgia, Cambria, "Times New Roman", serif;
    font-size: 20px;
    font-weight: 900;
    letter-spacing: 1px;
    color: #FFFFFF;
    line-height: 1.1;
  }}
  .mast-regions {{
    margin-top: 4px;
    font-size: 11.5px;
    font-weight: 700;
    letter-spacing: 1px;
    color: #AFC1D4;
    text-transform: uppercase;
    line-height: 1.3;
  }}

  /* EDITORIAL BROADSHEET GRID (NO WEB CARDS - HAIRLINE PRINT RULES) */
  .main-area {{
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 0 18px;
  }}

  /* HERO FEATURE BAND */
  .hero {{
    height: 274px;
    display: flex;
    padding: 13px 0 13px 0;
    border-bottom: 2.5px solid #122030;
    gap: 18px;
  }}
  .hero-art {{
    width: 458px;
    height: 100%;
    position: relative;
    flex-shrink: 0;
    background: #0D1B2A;
    border: 1.5px solid #1E3145;
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
    padding: 1px 0;
  }}
  .kicker-bar {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .tag-solid {{
    background: #0B7A54;
    color: #FFFFFF;
    font-size: 12.5px;
    font-weight: 900;
    letter-spacing: 1.3px;
    padding: 3px 9px;
    text-transform: uppercase;
  }}
  .tag-region {{
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 0.9px;
    color: #425466;
    text-transform: uppercase;
  }}
  .hero-headline {{
    font-family: Georgia, Cambria, "Times New Roman", serif;
    font-variant-numeric: lining-nums;
    font-size: 34px;
    font-weight: 900;
    line-height: 1.07;
    color: #09121C;
  }}
  .hero-stats {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
  }}
  .stat-cell {{
    background: #0C1B2A;
    padding: 6px 8px;
    text-align: center;
    border-bottom: 3.5px solid #18C386;
  }}
  .stat-name {{
    font-size: 11.5px;
    font-weight: 800;
    letter-spacing: 1.1px;
    color: #A4BCD2;
    text-transform: uppercase;
  }}
  .stat-num {{
    font-size: 23px;
    font-weight: 900;
    color: #38E4A6;
    line-height: 1.08;
    margin-top: 1px;
    font-variant-numeric: lining-nums;
  }}
  .hero-deck {{
    font-size: 17.5px;
    line-height: 1.24;
    color: #192634;
    font-weight: 600;
  }}

  /* 2x2 PRINT BROADSHEET COLUMNS */
  .stories-grid {{
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 1px 1fr;
    grid-template-rows: 1fr 1.5px 1fr;
    padding: 10px 0 10px 0;
  }}
  .v-rule {{
    background: #BEB4A0;
    grid-column: 2;
    grid-row: 1 / 4;
    margin: 2px 0;
  }}
  .h-rule {{
    background: #BEB4A0;
    grid-column: 1 / 4;
    grid-row: 2;
  }}
  .story {{
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }}
  .s-tl {{ grid-column: 1; grid-row: 1; padding: 0 14px 10px 0; }}
  .s-tr {{ grid-column: 3; grid-row: 1; padding: 0 0 10px 14px; }}
  .s-bl {{ grid-column: 1; grid-row: 3; padding: 10px 14px 0 0; }}
  .s-br {{ grid-column: 3; grid-row: 3; padding: 10px 0 0 14px; }}

  .story-art {{
    height: 168px;
    width: 100%;
    overflow: hidden;
    position: relative;
    border: 1px solid #C5BBA8;
    flex-shrink: 0;
  }}
  .story-art img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }}
  .art-libya {{ background: #182C40; }}
  .art-libya img {{ object-position: center 46%; }}
  .art-hormuz {{ background: #103542; }}
  .art-hormuz img {{ object-position: center 33%; }}
  .art-cop31 {{ background: #192B37; }}
  .art-cop31 img {{ object-fit: contain !important; object-position: center center; }}
  .art-asia {{ background: #13213C; }}
  .art-asia img {{ object-position: center 54%; }}

  .story-text {{
    flex: 1;
    padding-top: 6px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .story-meta {{
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .dot {{
    width: 9px;
    height: 9px;
    border-radius: 50%;
    display: inline-block;
    flex-shrink: 0;
  }}
  .dot-geo {{ background: #D13D2A; }}
  .dot-me {{ background: #C25D10; }}
  .dot-climate {{ background: #147E76; }}
  .dot-asia {{ background: #234C96; }}

  .story-kicker {{
    font-size: 12px;
    font-weight: 900;
    letter-spacing: 1.3px;
    text-transform: uppercase;
  }}
  .k-geo {{ color: #B82E1D; }}
  .k-me {{ color: #A64D0B; }}
  .k-climate {{ color: #0F6B64; }}
  .k-asia {{ color: #1B4185; }}

  .story-headline {{
    font-family: Georgia, Cambria, "Times New Roman", serif;
    font-variant-numeric: lining-nums;
    font-size: 22.5px;
    font-weight: 900;
    line-height: 1.12;
    color: #09121C;
    white-space: nowrap;
  }}
  .story-fact {{
    font-size: 16px;
    line-height: 1.22;
    color: #202F3E;
    font-weight: 600;
  }}

  /* BOTTOM WIRE FOOTER */
  .wire-footer {{
    height: 92px;
    background: #0D1B2B;
    border-top: 3px solid #D89B2B;
    padding: 9px 20px;
    display: grid;
    grid-template-columns: 1fr 1px 1fr;
    gap: 18px;
    align-items: center;
    color: #F7F3EA;
  }}
  .wire-sep {{
    width: 1px;
    height: 64px;
    background: rgba(255, 255, 255, 0.22);
  }}
  .wire-col {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}
  .wire-badge {{
    width: 44px;
    height: 44px;
    border-radius: 4px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  .wb-peace {{ background: #154549; border: 1.5px solid #4AC7B5; }}
  .wb-ai {{ background: #362348; border: 1.5px solid #C69CFF; }}
  .wire-copy {{
    display: flex;
    flex-direction: column;
    gap: 2px;
  }}
  .wire-tag {{
    font-size: 11.5px;
    font-weight: 900;
    letter-spacing: 1.3px;
    color: #F5C056;
    text-transform: uppercase;
  }}
  .wire-hl {{
    font-family: Georgia, Cambria, "Times New Roman", serif;
    font-variant-numeric: lining-nums;
    font-size: 20px;
    font-weight: 900;
    line-height: 1.1;
    color: #FFFFFF;
  }}
  .wire-sub {{
    font-size: 14px;
    line-height: 1.15;
    color: #C7D5E4;
    font-weight: 500;
  }}
</style>
</head>
<body>
  <div class="sheet">
    <header class="masthead">
      <div class="mast-left">
        <div class="mast-kicker">MONDAY · WORLD NEWS IN ONE IMAGE</div>
        <div class="mast-date"><span class="accent-day">23</span> NOVEMBER 2026</div>
      </div>
      <div class="mast-right">
        <div class="mast-meta">
          <div class="mast-edition">WORLD DISPATCH</div>
          <div class="mast-regions">GLOBAL FRONT PAGE<br/>6 REGIONS · 7 STORIES</div>
        </div>
        {world_locator_svg()}
      </div>
    </header>

    <main class="main-area">
      <section class="hero">
        <div class="hero-art">
          <img src="{images['hero']}" alt="Nvidia rally and Wall Street surge" />
        </div>
        <div class="hero-copy">
          <div class="kicker-bar">
            <span class="tag-solid">MARKETS · AI</span>
            <span class="tag-region">NEW YORK &amp; GLOBAL CHIPS</span>
          </div>
          <h1 class="hero-headline">Nvidia Reinstates Jensen Huang; Wall Street Surges</h1>
          <div class="hero-stats">
            <div class="stat-cell">
              <div class="stat-name">NVIDIA</div>
              <div class="stat-num">+31.5%</div>
            </div>
            <div class="stat-cell">
              <div class="stat-name">NASDAQ</div>
              <div class="stat-num">+6.5%</div>
            </div>
            <div class="stat-cell">
              <div class="stat-name">S&amp;P 500</div>
              <div class="stat-num">+4.7%</div>
            </div>
          </div>
          <p class="hero-deck">Unanimous board reversal adds $952B and ignites a global semiconductor rebound.</p>
        </div>
      </section>

      <section class="stories-grid">
        <div class="v-rule"></div>
        <div class="h-rule"></div>

        <article class="story s-tl">
          <div class="story-art art-libya">
            <img src="{images['libya']}" alt="Ukraine sea drones sink Russian warship Merkury in Benghazi" />
          </div>
          <div class="story-text">
            <div class="story-meta">
              <span class="dot dot-geo"></span>
              <span class="story-kicker k-geo">EUROPE · NORTH AFRICA</span>
            </div>
            <h2 class="story-headline">Ukraine Drones Sink Warship in Libya</h2>
            <p class="story-fact">7 sea drones sink Russia&rsquo;s <em>Merkury</em> in Benghazi, 2,400 km away.</p>
          </div>
        </article>

        <article class="story s-tr">
          <div class="story-art art-hormuz">
            <img src="{images['hormuz']}" alt="Strait of Hormuz U.S.-Iran naval blockade standoff" />
          </div>
          <div class="story-text">
            <div class="story-meta">
              <span class="dot dot-me"></span>
              <span class="story-kicker k-me">MIDDLE EAST · SECURITY</span>
            </div>
            <h2 class="story-headline">Iran Defies U.S. Blockade in Hormuz</h2>
            <p class="story-fact">Trump warns of new strikes; Israel&rsquo;s Eisenkot urges restraint.</p>
          </div>
        </article>

        <article class="story s-bl">
          <div class="story-art art-cop31">
            <img src="{images['cop31']}" alt="COP31 Antalya climate summit collapse" />
          </div>
          <div class="story-text">
            <div class="story-meta">
              <span class="dot dot-climate"></span>
              <span class="story-kicker k-climate">GLOBAL · CLIMATE</span>
            </div>
            <h2 class="story-headline">Global Dismay After COP31 Collapses</h2>
            <p class="story-fact">UN &amp; EU react to first climate summit failure since 2009.</p>
          </div>
        </article>

        <article class="story s-br">
          <div class="story-art art-asia">
            <img src="{images['asia']}" alt="Lowy 2026 Asia Power Index balance" />
          </div>
          <div class="story-text">
            <div class="story-meta">
              <span class="dot dot-asia"></span>
              <span class="story-kicker k-asia">ASIA-PACIFIC · POWER</span>
            </div>
            <h2 class="story-headline">U.S.&ndash;China Power Gap Hits Record Low</h2>
            <p class="story-fact">2026 Lowy Asia Index cuts gap to 5.3 pts as India rises 3rd.</p>
          </div>
        </article>
      </section>
    </main>

    <footer class="wire-footer">
      <div class="wire-col">
        <div class="wire-badge wb-peace">
          <svg width="26" height="26" viewBox="0 0 28 28" fill="none">
            <path d="M4 21L11.5 9.5L16.5 16L20 11L24 21H4Z" stroke="#5CE0CC" stroke-width="2.2" stroke-linejoin="round"/>
            <path d="M14 4V8.5M11.8 6.2H16.2" stroke="#F5C056" stroke-width="2.2" stroke-linecap="round"/>
          </svg>
        </div>
        <div class="wire-copy">
          <div class="wire-tag">TURKEY &amp; IRAQ · PEACE</div>
          <div class="wire-hl">PKK Vacates 14 Bases in N. Iraq</div>
          <div class="wire-sub">Ankara reports Hakurk pullout advancing disarmament.</div>
        </div>
      </div>

      <div class="wire-sep"></div>

      <div class="wire-col">
        <div class="wire-badge wb-ai">
          <svg width="26" height="26" viewBox="0 0 28 28" fill="none">
            <path d="M14 3L23 7V13.5C23 19.2 19.1 23.6 14 25C8.9 23.6 5 19.2 5 13.5V7L14 3Z" stroke="#D5B6FF" stroke-width="2.2" stroke-linejoin="round"/>
            <path d="M10.5 14L13 16.5L18 11.5" stroke="#F5C056" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <div class="wire-copy">
          <div class="wire-tag">BANKING · AI SAFETY</div>
          <div class="wire-hl">U.S. Banks Rein In AI Agents</div>
          <div class="wire-sub">Major lenders add kill switches after rogue-agent scares.</div>
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

    png_candidate = raw_png.with_name("candidate_opt_v2.png")
    img.save(png_candidate, format="PNG", optimize=True, compress_level=9)
    png_size = png_candidate.stat().st_size

    if png_size <= 950_000:
        out_path.write_bytes(png_candidate.read_bytes())
        chosen = f"PNG ({png_size:,} bytes)"
    else:
        for quality in (94, 92, 90, 88):
            jpg_candidate = raw_png.with_name("candidate_opt_v2.jpg")
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
