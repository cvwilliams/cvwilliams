"""Generate the profile banner SVGs (light + dark) in this folder.

Palette and font come from cameronwillia.ms. Libre Franklin (SIL OFL) is
embedded as base64 so the SVG renders the same everywhere, including
inside GitHub's <img> sandbox, which can't load external fonts.

Usage: python3 assets/build_banner.py [path/to/libre-franklin-latin-wght-normal.woff2]
"""

import base64
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
DEFAULT_FONT = (
    pathlib.Path.home()
    / "Projects/personal-website/dist/_astro/libre-franklin-latin-wght-normal.CLTz0ja0.woff2"
)

PALETTES = {
    "light": dict(bg="#f2ede4", text="#141414", muted="#5e5a53", ink="#141414",
                  blue="#1e4fa6", red="#ea4b35", yellow="#f4c12b", cell="#d9d2c5"),
    "dark": dict(bg="#121212", text="#f2ede4", muted="#a8a39a", ink="#f2ede4",
                 blue="#3f6fc6", red="#ea4b35", yellow="#f4c12b", cell="#2c2c2c"),
}

# A little "contribution graph" strip: 0 = empty cell, otherwise a palette key.
GRID = [
    "0b0y0r0b00y0br",
    "y0r0b0yy0r0b0y",
    "0by0r00b0yr0b0",
]
GRID_KEYS = {"b": "blue", "r": "red", "y": "yellow"}


def grid(p, x0, y0, size=18, gap=6):
    out = []
    for row, line in enumerate(GRID):
        for col, ch in enumerate(line):
            fill = p[GRID_KEYS[ch]] if ch in GRID_KEYS else p["cell"]
            x, y = x0 + col * (size + gap), y0 + row * (size + gap)
            out.append(f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="3" fill="{fill}"/>')
    return "\n    ".join(out)


def svg(p, font_b64):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="500" viewBox="0 0 1500 500" role="img" aria-label="Cameron Williams. Engineer, tinkerer, overthinker. New York. cameronwillia.ms">
  <style>
    @font-face {{
      font-family: "LF";
      src: url(data:font/woff2;base64,{font_b64}) format("woff2");
      font-weight: 100 900;
    }}
    text {{ font-family: "LF", "Libre Franklin", "Franklin Gothic Medium", "Helvetica Neue", Arial, sans-serif; }}
  </style>
  <rect width="1500" height="500" fill="{p['bg']}"/>

  <!-- shapes -->
  <g>
    <path d="M820 500a70 70 0 0 1 140 0Z" fill="{p['red']}"/>
    <rect x="900" y="170" width="220" height="330" fill="{p['blue']}"/>
    <circle cx="1150" cy="250" r="140" fill="{p['yellow']}"/>
    <path d="M1030 500L1175 245L1320 500Z" fill="{p['ink']}"/>
    <rect x="1350" y="0" width="150" height="190" fill="{p['ink']}"/>
    <circle cx="1395" cy="360" r="100" fill="{p['red']}"/>
    <circle cx="1395" cy="360" r="34" fill="{p['bg']}"/>
    <circle cx="1255" cy="80" r="22" fill="{p['blue']}"/>
    <circle cx="1010" cy="110" r="12" fill="{p['red']}"/>
  </g>

  <!-- text -->
  <text x="96" y="176" font-size="112" font-weight="800" letter-spacing="-4" fill="{p['text']}">Cameron</text>
  <text x="96" y="286" font-size="112" font-weight="800" letter-spacing="-4" fill="{p['text']}">Williams.</text>
  <text x="100" y="342" font-size="30" font-weight="500" letter-spacing="-0.3" fill="{p['text']}">Engineer, tinkerer, overthinker <tspan fill="{p['red']}">·</tspan> New York</text>
  <g>
    {grid(p, 100, 378)}
  </g>
  <text x="100" y="476" font-size="18" font-weight="600" letter-spacing="3" fill="{p['muted']}">CAMERONWILLIA.MS</text>
</svg>
"""


def main():
    font = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_FONT
    font_b64 = base64.b64encode(font.read_bytes()).decode()
    for name, p in PALETTES.items():
        out = HERE / f"banner-{name}.svg"
        out.write_text(svg(p, font_b64))
        print(f"wrote {out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
