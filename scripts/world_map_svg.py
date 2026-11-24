"""Accurate equirectangular world map SVG generator with 29 real city lat/lon pins."""

from __future__ import annotations

from dataclasses import dataclass

# Simplified yet geographically faithful continent polygons in (lon, lat) degrees.
LAND_POLYGONS: tuple[list[tuple[float, float]], ...] = (
    # North America
    [
        (-168, 66), (-160, 71), (-135, 70), (-115, 68), (-95, 69), (-80, 62),
        (-64, 60), (-55, 52), (-60, 46), (-67, 45), (-70, 41), (-76, 35),
        (-81, 31), (-80, 25), (-83, 29), (-90, 29), (-97, 26), (-97, 19),
        (-87, 21), (-84, 10), (-78, 8), (-83, 9), (-92, 14), (-105, 20),
        (-110, 24), (-117, 32), (-124, 41), (-124, 49), (-136, 58), (-152, 60),
        (-162, 55), (-166, 60),
    ],
    # Greenland
    [(-52, 60), (-42, 60), (-22, 70), (-18, 81), (-46, 83), (-68, 76), (-56, 68)],
    # Cuba / Hispaniola
    [(-84, 22), (-75, 20), (-77, 22), (-83, 23)],
    # South America
    [
        (-78, 9), (-72, 12), (-62, 10), (-50, 1), (-35, -6), (-38, -14),
        (-41, -23), (-48, -28), (-54, -35), (-63, -41), (-68, -54), (-74, -52),
        (-73, -40), (-71, -30), (-70, -18), (-81, -5), (-79, 2),
    ],
    # Europe (mainland)
    [
        (-9, 37), (-9, 43), (-2, 43), (-4, 48), (2, 51), (9, 54), (8, 57),
        (11, 58), (6, 61), (14, 68), (28, 71), (42, 67), (58, 69), (60, 56),
        (48, 46), (40, 45), (30, 46), (28, 41), (23, 37), (19, 40), (15, 38),
        (12, 44), (7, 44), (3, 42), (-5, 36),
    ],
    # Great Britain & Ireland
    [(-6, 50), (2, 51), (1, 55), (-3, 59), (-6, 57), (-5, 52)],
    [(-10, 52), (-6, 52), (-6, 55), (-10, 54)],
    # Iceland
    [(-24, 64), (-14, 64), (-14, 66), (-23, 66)],
    # Africa
    [
        (-17, 15), (-13, 28), (-6, 36), (10, 37), (12, 33), (20, 32), (25, 32),
        (33, 31), (38, 22), (43, 12), (51, 11), (48, 5), (41, -2), (40, -15),
        (35, -24), (28, -33), (18, -34), (14, -22), (12, -6), (9, 4), (2, 6),
        (-8, 5), (-15, 10),
    ],
    # Madagascar
    [(44, -25), (47, -25), (50, -13), (47, -15), (44, -20)],
    # Middle East & Asia
    [
        (27, 41), (36, 42), (41, 41), (48, 46), (60, 56), (60, 69), (80, 73),
        (110, 74), (140, 73), (175, 67), (170, 60), (158, 52), (142, 54),
        (135, 44), (129, 35), (126, 38), (122, 40), (122, 31), (120, 23),
        (110, 20), (109, 12), (104, 10), (102, 13), (103, 2), (99, 8),
        (96, 17), (90, 22), (80, 15), (77, 8), (72, 20), (67, 25), (56, 26),
        (60, 22), (53, 16), (44, 13), (39, 21), (35, 29), (36, 36), (27, 37),
    ],
    # Sri Lanka
    [(80, 6), (82, 7), (81, 10), (79, 8)],
    # Japan
    [(130, 31), (136, 34), (141, 36), (145, 44), (140, 41), (136, 37), (131, 34)],
    # Taiwan
    [(120.2, 22), (121.9, 25.2), (121.3, 25.3), (120, 23.2)],
    # Philippines
    [(120, 18), (123, 14), (126, 7), (122, 7), (120, 14)],
    # Indonesia (Sumatra, Java, Borneo)
    [(95, 5), (105, -6), (104, -7), (95, 3)],
    [(106, -6), (114, -8), (114, -9), (106, -7)],
    [(109, 2), (118, 5), (117, -3), (110, -3)],
    # New Guinea
    [(131, -1), (141, -3), (150, -10), (145, -9), (136, -5)],
    # Australia
    [
        (114, -22), (123, -17), (131, -12), (136, -12), (142, -11), (146, -18),
        (153, -27), (150, -37), (141, -38), (135, -35), (129, -32), (115, -34),
        (113, -27),
    ],
    # New Zealand
    [(167, -46), (173, -41), (178, -37), (174, -35), (174, -41), (170, -46)],
)


@dataclass(frozen=True)
class MapPin:
    num: int
    lon: float
    lat: float
    color: str
    major: bool = False
    dx: float = 0.0
    dy: float = 0.0


STORY_PINS: tuple[MapPin, ...] = (
    # 5 Major Visual Stories (zero overlap with subtle visual offsets where Mediterranean cities cluster)
    MapPin(1, -74.0, 40.7, "#10B981", major=True),
    MapPin(2, 20.1, 32.1, "#E04532", major=True, dx=-3.0, dy=2.5),
    MapPin(3, 56.2, 26.6, "#EB8C28", major=True, dx=2.0, dy=1.0),
    MapPin(4, 30.7, 36.9, "#17A89E", major=True, dx=2.5, dy=-4.0),
    MapPin(5, 114.0, 22.0, "#3B82F6", major=True),
    # 24 Regional Briefings (6-29)
    MapPin(6, -79.0, 35.8, "#10B981"),   # US NC House 258
    MapPin(7, -87.6, 41.8, "#10B981"),   # US Banks AI
    MapPin(8, -72.5, 7.9, "#10B981"),    # Cucuta, Colombia
    MapPin(9, -58.0, -30.0, "#10B981"),  # Argentina-Brazil gas
    MapPin(10, 19.0, 52.2, "#E04532"),   # Poland / NATO AWACS
    MapPin(11, -0.1, 51.5, "#E04532"),   # London UK PM
    MapPin(12, -2.2, 53.5, "#E04532"),   # Manchester
    MapPin(13, 2.3, 48.8, "#E04532"),    # Paris / EU
    MapPin(14, 44.3, 37.1, "#EB8C28"),   # N. Iraq / PKK
    MapPin(15, 35.2, 31.8, "#EB8C28"),   # Israel
    MapPin(16, 35.5, 33.4, "#EB8C28"),   # Gaza / Lebanon
    MapPin(17, 50.6, 26.1, "#EB8C28"),   # Persian Gulf oil/shipping
    MapPin(18, 13.2, 32.9, "#D94F70"),   # Libya UN complaint
    MapPin(19, 30.2, 1.5, "#D94F70"),    # Ituri, DR Congo
    MapPin(20, 6.6, 12.1, "#D94F70"),    # NW Nigeria (Zamfara)
    MapPin(21, -6.8, 34.0, "#D94F70"),   # Morocco/Egypt AfDB
    MapPin(22, 139.7, 35.7, "#3B82F6"),  # Tokyo/Seoul/Taipei rally
    MapPin(23, 90.0, 23.4, "#3B82F6"),   # Bangladesh
    MapPin(24, 123.9, 10.3, "#3B82F6"),  # Philippines Visayas
    MapPin(25, 121.5, 25.0, "#3B82F6"),  # Taiwan elections
    MapPin(26, 8.5, 47.4, "#17A89E"),    # FIFA Zurich -> 2031/2035
    MapPin(27, 174.8, -41.3, "#17A89E"), # Wellington NZ Cricket
    MapPin(28, -67.8, -23.0, "#17A89E"), # ALMA Chile
    MapPin(29, -155.5, 19.6, "#17A89E"), # Hawaii core carbon
)


def _project(lon: float, lat: float, width: float, height: float) -> tuple[float, float]:
    x = (lon + 180.0) / 360.0 * width
    y = (82.0 - lat) / 140.0 * height
    return round(x, 1), round(y, 1)


def render_world_map_svg(width: int = 398, height: int = 204) -> str:
    map_h = height - 24
    poly_elems: list[str] = []
    for ring in LAND_POLYGONS:
        pts = " ".join(f"{_project(lon, lat, width, map_h)[0]},{_project(lon, lat, width, map_h)[1]}" for lon, lat in ring)
        poly_elems.append(f'<polygon points="{pts}" />')

    graticule = []
    for lat in (-30, 0, 30, 60):
        _, y = _project(0, lat, width, map_h)
        dash = "" if lat == 0 else 'stroke-dasharray="2 3"'
        op = "0.28" if lat == 0 else "0.16"
        graticule.append(f'<line x1="0" y1="{y}" x2="{width}" y2="{y}" stroke="#6FA3C7" stroke-opacity="{op}" stroke-width="0.8" {dash}/>')
    for lon in (-120, -60, 0, 60, 120):
        x, _ = _project(lon, 0, width, map_h)
        graticule.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{map_h}" stroke="#6FA3C7" stroke-opacity="0.16" stroke-width="0.8" stroke-dasharray="2 3"/>')

    minor_elems: list[str] = []
    major_elems: list[str] = []
    for pin in STORY_PINS:
        cx, cy = _project(pin.lon, pin.lat, width, map_h)
        cx = round(cx + pin.dx, 1)
        cy = round(cy + pin.dy, 1)
        if pin.major:
            major_elems.append(
                f'<g>'
                f'<circle cx="{cx}" cy="{cy}" r="10.2" fill="{pin.color}" fill-opacity="0.28"/>'
                f'<circle cx="{cx}" cy="{cy}" r="6.7" fill="{pin.color}" stroke="#FFFFFF" stroke-width="1.35"/>'
                f'<text x="{cx}" y="{cy + 3.0}" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" '
                f'font-size="9.2" font-weight="900" fill="#FFFFFF">{pin.num}</text>'
                f'</g>'
            )
        else:
            minor_elems.append(
                f'<circle cx="{cx}" cy="{cy}" r="3.2" fill="{pin.color}" stroke="#091523" stroke-width="1.05"/>'
            )

    legend_y = map_h + 15.5
    legend = (
        f'<rect x="0" y="{map_h}" width="{width}" height="24" fill="#081320"/>'
        f'<line x1="0" y1="{map_h}" x2="{width}" y2="{map_h}" stroke="#27435E" stroke-width="1"/>'
        f'<text x="10" y="{legend_y}" font-family="Segoe UI, Arial, sans-serif" font-size="10.2" font-weight="800" letter-spacing="0.8" fill="#F4C155">GLOBAL ATLAS</text>'
        f'<circle cx="107" cy="{legend_y - 3.5}" r="3.5" fill="#10B981"/><text x="114" y="{legend_y}" font-size="9.5" font-weight="700" fill="#CBD8E6">AM</text>'
        f'<circle cx="144" cy="{legend_y - 3.5}" r="3.5" fill="#E04532"/><text x="151" y="{legend_y}" font-size="9.5" font-weight="700" fill="#CBD8E6">EU</text>'
        f'<circle cx="179" cy="{legend_y - 3.5}" r="3.5" fill="#EB8C28"/><text x="186" y="{legend_y}" font-size="9.5" font-weight="700" fill="#CBD8E6">ME</text>'
        f'<circle cx="217" cy="{legend_y - 3.5}" r="3.5" fill="#D94F70"/><text x="224" y="{legend_y}" font-size="9.5" font-weight="700" fill="#CBD8E6">AF</text>'
        f'<circle cx="252" cy="{legend_y - 3.5}" r="3.5" fill="#3B82F6"/><text x="259" y="{legend_y}" font-size="9.5" font-weight="700" fill="#CBD8E6">AS</text>'
        f'<circle cx="287" cy="{legend_y - 3.5}" r="3.5" fill="#17A89E"/><text x="294" y="{legend_y}" font-size="9.5" font-weight="700" fill="#CBD8E6">OC/SCI</text>'
        f'<text x="{width - 10}" y="{legend_y}" text-anchor="end" font-size="9.5" font-weight="800" fill="#8FB3D4">29 PINS</text>'
    )

    return (
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'
        f'<defs><linearGradient id="oceanGrad" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="#0C1D30"/><stop offset="100%" stop-color="#122B42"/></linearGradient></defs>'
        f'<rect width="{width}" height="{map_h}" fill="url(#oceanGrad)"/>'
        f'{"".join(graticule)}'
        f'<g fill="#2C4D6B" stroke="#456E92" stroke-width="0.65" stroke-linejoin="round">{"".join(poly_elems)}</g>'
        f'{"".join(minor_elems)}'
        f'{"".join(major_elems)}'
        f'{legend}'
        f'</svg>'
    )
