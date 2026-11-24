"""Dual-scale editorial front-page & 6-continent world dispatch renderer for 23 Nov 2026 (v4)."""

from __future__ import annotations

import base64
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

from world_map_svg import render_world_map_svg

ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT.parent / "assets"
OUTPUT_PNG = ROOT / "entry.png"
PREVIEW_300 = ROOT / "preview_300.png"
RAW_PNG = ROOT.parent / "raw_1024_v4.png"


def encode_image_data_uri(path: Path) -> str:
    raw = path.read_bytes()
    b64 = base64.b64encode(raw).decode("ascii")
    mime = "image/jpeg" if path.suffix.lower() in {".jpg", ".jpeg"} else "image/png"
    return f"data:{mime};base64,{b64}"


def build_brief_item(num: int, lead: str, body: str, color: str) -> str:
    return (
        f'<li class="brief-item">'
        f'<span class="b-num" style="background:{color}">{num}</span>'
        f'<span class="b-text"><strong>{lead}</strong> {body}</span>'
        f'</li>'
    )


def build_html(images: dict[str, str], map_svg: str) -> str:
    americas_items = "".join([
        build_brief_item(6, "U.S. House:", "Democrats clinch 258 seats after NC recount&mdash;largest majority since 1992.", "#0C7C55"),
        build_brief_item(7, "Wall St. AI:", "JPMorgan, BofA &amp; Citi add kill switches and strict walls on AI agents.", "#0C7C55"),
        build_brief_item(8, "Colombia:", "Drone attack hits C&uacute;cuta police base, injuring civilians &amp; damaging homes.", "#0C7C55"),
        build_brief_item(9, "Argentina&ndash;Brazil:", "PAE signs Vaca Muerta shale gas supply deal to Rio via Bolivia.", "#0C7C55"),
    ])

    europe_items = "".join([
        build_brief_item(10, "NATO / Poland:", "Emergency Brussels session deploys AWACS after Russian missile incursion.", "#C83E2B"),
        build_brief_item(11, "UK Parliament:", "PM Andy Burnham defends EU reset deal; rules out rejoin without vote.", "#C83E2B"),
        build_brief_item(12, "Manchester:", "Irritant gas evacuates 12,000 fans at Co-op Live concert; 80+ treated.", "#C83E2B"),
        build_brief_item(13, "EU / Paris:", "EU tightens AI chip export controls; Paris summit backs 2% wealth tax.", "#C83E2B"),
    ])

    middle_east_items = "".join([
        build_brief_item(14, "Turkey / N. Iraq:", "Ankara reports PKK vacated 14 Hakurk bases in disarmament push.", "#B85914"),
        build_brief_item(15, "Israel:", "PM-designate Eisenkot sees no imminent Iran threat, tempering strike calls.", "#B85914"),
        build_brief_item(16, "Gaza &amp; Lebanon:", "Localized IDF raids in Gaza &amp; West Bank; south Lebanon truce strained.", "#B85914"),
        build_brief_item(17, "Energy / Gulf:", "Oil steadies as Hormuz tanker fires &amp; shipping risks offset slowdown fears.", "#B85914"),
    ])

    africa_items = "".join([
        build_brief_item(18, "Libya / UN:", "Eastern Libyan government files formal UN complaint over Benghazi strike.", "#9C3D54"),
        build_brief_item(19, "DR Congo:", "Heavy fighting near Ituri hospitals forces WHO emergency teams to shelter.", "#9C3D54"),
        build_brief_item(20, "Nigeria:", "Northwest security worsens with Zamfara/Niger abductions &amp; fatal boat capsize.", "#9C3D54"),
        build_brief_item(21, "North Africa:", "AfDB launches MSME investment push in Morocco &amp; Egypt; mineral race grows.", "#9C3D54"),
    ])

    asia_items = "".join([
        build_brief_item(22, "Asia Markets:", "Tech relief rally lifts Taiwan +9%, KOSPI +7.5% and Nikkei +4.5%.", "#264B8A"),
        build_brief_item(23, "Bangladesh:", "Factional clashes in Jhenaidah &amp; Gopalganj injure 35+ with crude bombs.", "#264B8A"),
        build_brief_item(24, "Philippines:", "Visayas power grid hits red alert; Quad maritime talks held in Manila.", "#264B8A"),
        build_brief_item(25, "China / Taiwan:", "Taipei flags cross-strait travel before Nov 28 vote; IAEA AUKUS query.", "#264B8A"),
    ])

    oceania_sci_items = "".join([
        build_brief_item(26, "FIFA 2031/35:", "Congress confirms U.S.-led Americas host 2031 Women&rsquo;s World Cup; UK 2035.", "#157770"),
        build_brief_item(27, "NZ / India Cricket:", "India&rsquo;s 720/9 d. sets NZ record; Black Caps bat 120 overs for draw.", "#157770"),
        build_brief_item(28, "ALMA Space:", "Chile array detects first gaseous rock-forming TiO around young star Orion I.", "#157770"),
        build_brief_item(29, "Earth &amp; Health:", "PNAS finds ancient core carbon in Hawaii lava; WHO flags EU climate distress.", "#157770"),
    ])

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
  .page {{
    width: 1024px;
    height: 1024px;
    display: flex;
    flex-direction: column;
    background: #F6F1E6;
  }}

  /* 1. MASTHEAD (76px) */
  .masthead {{
    height: 76px;
    background: linear-gradient(180deg, #09131F 0%, #102033 100%);
    color: #FFFFFF;
    border-top: 5px solid #D13D2A;
    border-bottom: 3px solid #DDA02C;
    padding: 0 18px;
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
    font-size: 11.5px;
    font-weight: 800;
    letter-spacing: 2.4px;
    color: #F6C255;
    text-transform: uppercase;
    margin-bottom: 1px;
  }}
  .mast-date {{
    font-family: Georgia, Cambria, "Times New Roman", serif;
    font-variant-numeric: lining-nums;
    font-size: 36px;
    font-weight: 900;
    letter-spacing: 0.4px;
    line-height: 0.98;
    color: #FFFFFF;
  }}
  .mast-date .day-accent {{ color: #F7C25B; }}
  .mast-right {{
    text-align: right;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    justify-content: center;
  }}
  .mast-brand {{
    font-family: Georgia, Cambria, "Times New Roman", serif;
    font-size: 23px;
    font-weight: 900;
    letter-spacing: 0.9px;
    color: #FFFFFF;
    line-height: 1.05;
  }}
  .mast-badge {{
    margin-top: 4px;
    background: #1B334D;
    border: 1px solid #DDA02C;
    color: #F8D17B;
    font-size: 11.5px;
    font-weight: 800;
    letter-spacing: 1.2px;
    padding: 2px 9px;
    border-radius: 2px;
    text-transform: uppercase;
  }}

  /* BODY WRAPPER */
  .main {{
    flex: 1;
    padding: 10px 14px 10px 14px;
    display: flex;
    flex-direction: column;
    gap: 9px;
  }}

  /* 2. TOP ROW: HERO + ANNOTATED WORLD ATLAS (206px) */
  .top-row {{
    height: 206px;
    display: grid;
    grid-template-columns: 586px 398px;
    gap: 12px;
  }}
  .hero {{
    background: #FFFDF8;
    border: 1.5px solid #C8BFA9;
    border-left: 5px solid #0C7C55;
    display: flex;
    overflow: hidden;
  }}
  .hero-art {{
    width: 248px;
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
  .art-pin {{
    position: absolute;
    top: 7px;
    left: 7px;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    color: #FFFFFF;
    font-size: 13px;
    font-weight: 900;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px solid #FFFFFF;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.45);
  }}
  .hero-copy {{
    flex: 1;
    padding: 9px 12px 9px 13px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .hero-kicker {{
    display: flex;
    align-items: center;
    gap: 7px;
  }}
  .pill {{
    background: #0C7C55;
    color: #FFFFFF;
    font-size: 11px;
    font-weight: 900;
    letter-spacing: 1px;
    padding: 2px 7px;
    text-transform: uppercase;
  }}
  .hero-loc {{
    font-size: 11px;
    font-weight: 800;
    color: #4A5C6E;
    letter-spacing: 0.7px;
    text-transform: uppercase;
  }}
  .hero-hl {{
    font-family: Georgia, Cambria, "Times New Roman", serif;
    font-variant-numeric: lining-nums;
    font-size: 24.5px;
    font-weight: 900;
    line-height: 1.08;
    color: #09121C;
  }}
  .hero-stats {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 6px;
  }}
  .stat-cell {{
    background: #0C1B2A;
    padding: 4px 5px;
    text-align: center;
    border-bottom: 3px solid #18C386;
  }}
  .stat-k {{
    font-size: 9.8px;
    font-weight: 800;
    letter-spacing: 0.8px;
    color: #A2BAD0;
    text-transform: uppercase;
  }}
  .stat-v {{
    font-size: 18.5px;
    font-weight: 900;
    color: #38E4A6;
    line-height: 1.08;
    font-variant-numeric: lining-nums;
  }}
  .hero-deck {{
    font-size: 13px;
    line-height: 1.22;
    color: #162330;
    font-weight: 600;
  }}

  .map-box {{
    border: 1.5px solid #1E3650;
    background: #0B1928;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
  }}

  /* 3. MIDDLE ROW: 4 ILLUSTRATED MAJOR STORIES (222px) */
  .mid-row {{
    height: 222px;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
  }}
  .mcard {{
    background: #FFFDF8;
    border: 1.3px solid #C8BFA9;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }}
  .mc-geo {{ border-top: 4px solid #C83E2B; }}
  .mc-me {{ border-top: 4px solid #B85914; }}
  .mc-cli {{ border-top: 4px solid #157770; }}
  .mc-asia {{ border-top: 4px solid #264B8A; }}

  .mcard-art {{
    height: 114px;
    width: 100%;
    position: relative;
    overflow: hidden;
    flex-shrink: 0;
  }}
  .mcard-art img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }}
  .ma-libya {{ background: #182C40; }}
  .ma-libya img {{ object-position: center 46%; }}
  .ma-hormuz {{ background: #103542; }}
  .ma-hormuz img {{ object-position: center 35%; }}
  .ma-cop31 {{ background: #192B37; }}
  .ma-cop31 img {{ object-fit: contain !important; object-position: center center; }}
  .ma-asia {{ background: #13213C; }}
  .ma-asia img {{ object-position: center 54%; }}

  .mcard-body {{
    flex: 1;
    padding: 6px 9px 7px 9px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .mcard-kicker {{
    font-size: 10.2px;
    font-weight: 900;
    letter-spacing: 0.9px;
    text-transform: uppercase;
  }}
  .mk-geo {{ color: #B82E1D; }}
  .mk-me {{ color: #A64D0B; }}
  .mk-cli {{ color: #0F6B64; }}
  .mk-asia {{ color: #1B4185; }}

  .mcard-hl {{
    font-family: Georgia, Cambria, "Times New Roman", serif;
    font-variant-numeric: lining-nums;
    font-size: 17.5px;
    font-weight: 900;
    line-height: 1.09;
    color: #08111B;
  }}
  .mcard-desc {{
    font-size: 12px;
    line-height: 1.18;
    color: #1F2D3B;
    font-weight: 500;
  }}

  /* 4. BOTTOM MATRIX: SYMMETRIC 6 CONTINENTS x 4 BRIEFS = 24 REGIONAL STORIES (482px) */
  .continent-grid {{
    flex: 1;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: 1fr 1fr;
    gap: 9px 10px;
  }}
  .region-box {{
    background: #FFFDF9;
    border: 1.2px solid #CCC3AE;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }}
  .region-hdr {{
    height: 26px;
    padding: 0 9px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: #FFFFFF;
    font-size: 12.8px;
    font-weight: 900;
    letter-spacing: 1px;
    text-transform: uppercase;
    flex-shrink: 0;
  }}
  .rh-am {{ background: #0C7C55; }}
  .rh-eu {{ background: #C83E2B; }}
  .rh-me {{ background: #B85914; }}
  .rh-af {{ background: #9C3D54; }}
  .rh-as {{ background: #264B8A; }}
  .rh-oc {{ background: #157770; }}

  .region-count {{
    font-size: 9.8px;
    font-weight: 800;
    opacity: 0.92;
    letter-spacing: 0.6px;
  }}
  .brief-list {{
    list-style: none;
    flex: 1;
    padding: 5px 8px 5px 8px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .brief-item {{
    display: flex;
    align-items: flex-start;
    gap: 6px;
    padding-bottom: 4px;
    border-bottom: 1px solid #EAE3D5;
  }}
  .brief-item:last-child {{
    border-bottom: none;
    padding-bottom: 0;
  }}
  .b-num {{
    min-width: 18px;
    height: 17px;
    border-radius: 3px;
    color: #FFFFFF;
    font-size: 10.2px;
    font-weight: 900;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 1px;
    font-variant-numeric: lining-nums;
  }}
  .b-text {{
    font-size: 12.2px;
    line-height: 1.19;
    color: #121E2B;
    font-weight: 500;
  }}
  .b-text strong {{
    color: #060D16;
    font-weight: 800;
  }}
</style>
</head>
<body>
  <div class="page">
    <header class="masthead">
      <div class="mast-left">
        <div class="mast-kicker">MONDAY · WORLD NEWS IN ONE IMAGE</div>
        <div class="mast-date"><span class="day-accent">23</span> NOVEMBER 2026</div>
      </div>
      <div class="mast-right">
        <div class="mast-brand">WORLD DISPATCH</div>
        <div class="mast-badge">6 CONTINENTS · 29 VERIFIED STORIES · GLOBAL ATLAS</div>
      </div>
    </header>

    <main class="main">
      <section class="top-row">
        <article class="hero">
          <div class="hero-art">
            <img src="{images['hero']}" alt="Nvidia rally and Wall Street rebound" />
            <span class="art-pin" style="background:#0C7C55">1</span>
          </div>
          <div class="hero-copy">
            <div class="hero-kicker">
              <span class="pill">MARKETS · AI</span>
              <span class="hero-loc">NEW YORK &amp; GLOBAL</span>
            </div>
            <h1 class="hero-hl">Nvidia Reinstates Jensen Huang; Wall Street Surges</h1>
            <div class="hero-stats">
              <div class="stat-cell">
                <div class="stat-k">NVIDIA</div>
                <div class="stat-v">+31.5%</div>
              </div>
              <div class="stat-cell">
                <div class="stat-k">NASDAQ</div>
                <div class="stat-v">+6.5%</div>
              </div>
              <div class="stat-cell">
                <div class="stat-k">S&amp;P 500</div>
                <div class="stat-v">+4.7%</div>
              </div>
            </div>
            <p class="hero-deck">Unanimous board reversal adds $952B after White House assurances; Dow surges +1,448 pts (+3.0%).</p>
          </div>
        </article>

        <div class="map-box">
          {map_svg}
        </div>
      </section>

      <section class="mid-row">
        <article class="mcard mc-geo">
          <div class="mcard-art ma-libya">
            <img src="{images['libya']}" alt="Ukraine sea drones sink Russian warship Merkury in Benghazi" />
            <span class="art-pin" style="background:#C83E2B">2</span>
          </div>
          <div class="mcard-body">
            <div class="mcard-kicker mk-geo">EUROPE · N. AFRICA</div>
            <h2 class="mcard-hl">Ukraine Sinks Russian Warship in Libya</h2>
            <p class="mcard-desc">7 sea drones sink <em>Merkury</em> in Benghazi (2,400 km away); refineries hit.</p>
          </div>
        </article>

        <article class="mcard mc-me">
          <div class="mcard-art ma-hormuz">
            <img src="{images['hormuz']}" alt="Strait of Hormuz U.S.-Iran blockade standoff" />
            <span class="art-pin" style="background:#B85914">3</span>
          </div>
          <div class="mcard-body">
            <div class="mcard-kicker mk-me">MIDDLE EAST · CRISIS</div>
            <h2 class="mcard-hl">Iran Defies U.S. Blockade in Hormuz</h2>
            <p class="mcard-desc">Tehran vows &ldquo;all means&rdquo;; Trump threatens ships &amp; new strikes.</p>
          </div>
        </article>

        <article class="mcard mc-cli">
          <div class="mcard-art ma-cop31">
            <img src="{images['cop31']}" alt="COP31 climate talks collapse in Antalya" />
            <span class="art-pin" style="background:#157770">4</span>
          </div>
          <div class="mcard-body">
            <div class="mcard-kicker mk-cli">GLOBAL · CLIMATE</div>
            <h2 class="mcard-hl">Fallout After COP31 Collapses</h2>
            <p class="mcard-desc">UN, EU &amp; Pacific states react to 1st climate breakdown since 2009.</p>
          </div>
        </article>

        <article class="mcard mc-asia">
          <div class="mcard-art ma-asia">
            <img src="{images['asia']}" alt="Lowy 2026 Asia Power Index balance" />
            <span class="art-pin" style="background:#264B8A">5</span>
          </div>
          <div class="mcard-body">
            <div class="mcard-kicker mk-asia">ASIA-PACIFIC · POWER</div>
            <h2 class="mcard-hl">U.S.&ndash;China Gap Hits Record Asia Low</h2>
            <p class="mcard-desc">2026 Lowy Index narrows gap to 5.3 pts as India rises as 3rd pole.</p>
          </div>
        </article>
      </section>

      <section class="continent-grid">
        <div class="region-box">
          <div class="region-hdr rh-am"><span>AMERICAS</span><span class="region-count">NORTH &amp; LATIN</span></div>
          <ul class="brief-list">{americas_items}</ul>
        </div>

        <div class="region-box">
          <div class="region-hdr rh-eu"><span>EUROPE</span><span class="region-count">SECURITY &amp; POLICY</span></div>
          <ul class="brief-list">{europe_items}</ul>
        </div>

        <div class="region-box">
          <div class="region-hdr rh-me"><span>MIDDLE EAST</span><span class="region-count">DIPLOMACY &amp; ENERGY</span></div>
          <ul class="brief-list">{middle_east_items}</ul>
        </div>

        <div class="region-box">
          <div class="region-hdr rh-af"><span>AFRICA</span><span class="region-count">NORTH, WEST &amp; CENTRAL</span></div>
          <ul class="brief-list">{africa_items}</ul>
        </div>

        <div class="region-box">
          <div class="region-hdr rh-as"><span>ASIA</span><span class="region-count">MARKETS &amp; SOCIETY</span></div>
          <ul class="brief-list">{asia_items}</ul>
        </div>

        <div class="region-box">
          <div class="region-hdr rh-oc"><span>OCEANIA · SCIENCE · SPORTS</span><span class="region-count">GLOBAL</span></div>
          <ul class="brief-list">{oceania_sci_items}</ul>
        </div>
      </section>
    </main>
  </div>
</body>
</html>
"""


def optimize_output(raw_png: Path, out_path: Path, preview_path: Path) -> None:
    img = Image.open(raw_png).convert("RGB")
    if img.size != (1024, 1024):
        img = img.resize((1024, 1024), Image.Resampling.LANCZOS)

    png_candidate = raw_png.with_name("candidate_opt_v4.png")
    img.save(png_candidate, format="PNG", optimize=True, compress_level=9)
    png_size = png_candidate.stat().st_size

    if png_size <= 950_000:
        out_path.write_bytes(png_candidate.read_bytes())
        chosen = f"PNG ({png_size:,} bytes)"
    else:
        for quality in (94, 92, 90, 88):
            jpg_candidate = raw_png.with_name("candidate_opt_v4.jpg")
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
    map_svg = render_world_map_svg(width=398, height=204)
    html = build_html(images, map_svg)

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
