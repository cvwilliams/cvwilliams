"""Generate the animated metal ID card (assets/id-card.svg).

A titanium-style card: soft studio lighting, fine grain, a punched
lanyard slot, a drop shadow, and laser-etched text. A faint glint
passes over it every few seconds, hidden for viewers who ask for
reduced motion. Libre Franklin (SIL OFL) is embedded so the text renders
the same inside GitHub's <img> sandbox.

Usage: python3 assets/build_card.py [path/to/libre-franklin-latin-wght-normal.woff2]
"""

import base64
import pathlib
import random
import sys

HERE = pathlib.Path(__file__).parent
DEFAULT_FONT = (
    pathlib.Path.home()
    / "Projects/personal-website/dist/_astro/libre-franklin-latin-wght-normal.CLTz0ja0.woff2"
)

NAME = "Cameron Williams"
BADGE_NAME = "CAMERON W."
FIELDS = [  # (label, value), laid out in two columns, row by row
    ("Role", "sw engineer"), ("Currently building", "bitkey @ block"),
    ("Based in", "new york city"), ("Learning", "rust + wasm"),
    ("Beverage of choice", "la croix"), ("Alter ego", "spiderman 4143"),
]

# Canvas has room around the card for its shadow.
W, H = 1000, 660
CX, CY, CW, CH, R = 30, 22, 940, 592, 30     # card rect
ETCH, LABEL, RULE = "#4f5459", "#6b7076", "#83888d"


def X(x):  # card-relative coords -> canvas
    return CX + x


def Y(y):
    return CY + y


def etched_line(x, y, w):
    return (f'<rect x="{X(x)}" y="{Y(y)}" width="{w}" height="1" fill="{RULE}" opacity=".9"/>'
            f'<rect x="{X(x)}" y="{Y(y) + 1}" width="{w}" height="1" fill="#fff" opacity=".45"/>')


def field(x, y, label, value, w=250):
    return (f'<text class="label" x="{X(x)}" y="{Y(y)}">{label.upper()}</text>'
            f'<text class="value" x="{X(x)}" y="{Y(y) + 36}">{value}</text>'
            + etched_line(x, y + 50, w))


def barcode(x, y, w, h):
    rng = random.Random(4143)  # fixed seed: same "barcode" every build
    out, cx = [], x
    while cx < x + w:
        bw = rng.choice([1.5, 1.5, 2.5, 3.5, 5])
        if cx + bw > x + w:
            break
        out.append(f'<rect x="{X(cx)}" y="{Y(y)}" width="{bw}" height="{h}"/>')
        cx += bw + rng.choice([2, 3, 4])
    return f'<g fill="{ETCH}" opacity=".75">{"".join(out)}</g>'


def svg(font_b64):
    fields = []
    for i, (label, value) in enumerate(FIELDS):
        col, row = i % 2, i // 2
        fields.append(field(56 + col * 290, 214 + row * 104, label, value))

    slot_w, slot_h = 96, 16
    slot_x, slot_y = X(CW / 2 - slot_w / 2), Y(28)
    px, py, pw, ph = 676, 92, 204, 240   # photo window, card-relative

    alt = f"ID card. Name: {NAME}. " + ". ".join(f"{l}: {v}" for l, v in FIELDS) + "."
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{alt}">
  <title>{alt}</title>
  <style>
    @font-face {{
      font-family: "LF";
      src: url(data:font/woff2;base64,{font_b64}) format("woff2");
      font-weight: 100 900;
    }}
    text {{ font-family: "LF", "Libre Franklin", "Helvetica Neue", Arial, sans-serif; }}
    .label {{ font-size: 13px; font-weight: 600; letter-spacing: 2.4px; fill: {LABEL}; }}
    .value {{ font-size: 27px; font-weight: 450; letter-spacing: -0.2px; fill: {ETCH}; }}
    .etched {{ filter: url(#etch); }}
    @media (prefers-reduced-motion: reduce) {{ .shine {{ display: none; }} }}
  </style>
  <defs>
    <!-- base metal: cool grey, a little lighter toward the top left -->
    <linearGradient id="metal" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#d3d5d7"/>
      <stop offset=".35" stop-color="#c2c5c8"/>
      <stop offset=".7" stop-color="#b1b4b8"/>
      <stop offset="1" stop-color="#a6a9ad"/>
    </linearGradient>
    <!-- soft window light falling across the card -->
    <radialGradient id="light" cx=".22" cy=".05" r=".9">
      <stop offset="0" stop-color="#fff" stop-opacity=".45"/>
      <stop offset=".55" stop-color="#fff" stop-opacity=".08"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="vignette" x1="0" y1="0" x2="0" y2="1">
      <stop offset=".6" stop-color="#000" stop-opacity="0"/>
      <stop offset="1" stop-color="#000" stop-opacity=".08"/>
    </linearGradient>
    <!-- edge: bright on the top lip, fading to a dark lower edge -->
    <linearGradient id="edge" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#fff" stop-opacity=".9"/>
      <stop offset=".15" stop-color="#fff" stop-opacity=".25"/>
      <stop offset=".85" stop-color="#000" stop-opacity=".05"/>
      <stop offset="1" stop-color="#000" stop-opacity=".25"/>
    </linearGradient>
    <linearGradient id="recess" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#000" stop-opacity=".1"/>
      <stop offset=".12" stop-color="#000" stop-opacity=".03"/>
      <stop offset="1" stop-color="#fff" stop-opacity=".12"/>
    </linearGradient>
    <linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset=".5" stop-color="#fff" stop-opacity=".22"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>

    <!-- fine grain plus a whisper of horizontal brushing -->
    <filter id="grain" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="3" result="g"/>
      <feTurbulence type="fractalNoise" baseFrequency=".006 .7" numOctaves="1" seed="9" result="b"/>
      <feBlend in="g" in2="b" mode="multiply"/>
      <feColorMatrix type="saturate" values="0"/>
      <feComponentTransfer><feFuncA type="linear" slope="0" intercept=".1"/></feComponentTransfer>
      <feComposite in2="SourceGraphic" operator="in"/>
    </filter>
    <!-- laser etch: darker mark with a hairline highlight underneath -->
    <filter id="etch" x="-5%" y="-20%" width="110%" height="140%">
      <feOffset in="SourceAlpha" dy="1" result="o"/>
      <feFlood flood-color="#fff" flood-opacity=".55"/>
      <feComposite in2="o" operator="in" result="hi"/>
      <feOffset in="SourceAlpha" dy="-.6" result="o2"/>
      <feFlood flood-color="#000" flood-opacity=".18"/>
      <feComposite in2="o2" operator="in" result="lo"/>
      <feMerge><feMergeNode in="hi"/><feMergeNode in="lo"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="shadow" filterUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">
      <feGaussianBlur in="SourceAlpha" stdDeviation="9"/>
      <feOffset dy="10"/>
      <feComponentTransfer><feFuncA type="linear" slope=".28"/></feComponentTransfer>
    </filter>
    <filter id="contact" filterUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">
      <feGaussianBlur in="SourceAlpha" stdDeviation="1.5"/>
      <feOffset dy="2"/>
      <feComponentTransfer><feFuncA type="linear" slope=".3"/></feComponentTransfer>
    </filter>

    <!-- card shape with the lanyard slot punched through -->
    <mask id="punch" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">
      <rect width="{W}" height="{H}" fill="#fff"/>
      <rect x="{slot_x}" y="{slot_y}" width="{slot_w}" height="{slot_h}" rx="{slot_h / 2}" fill="#000"/>
    </mask>
    <clipPath id="noSlot"><path clip-rule="evenodd" d="M0 0H{W}V{H}H0Z M{slot_x + slot_h / 2} {slot_y}h{slot_w - slot_h}a{slot_h / 2} {slot_h / 2} 0 0 1 0 {slot_h}h-{slot_w - slot_h}a{slot_h / 2} {slot_h / 2} 0 0 1 0 -{slot_h}Z"/></clipPath>
    <clipPath id="cardClip"><rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" rx="{R}"/></clipPath>
    <clipPath id="photo"><rect x="{X(px)}" y="{Y(py)}" width="{pw}" height="{ph}" rx="14"/></clipPath>
  </defs>

  <!-- shadows on the surface below (clip, not mask: WebKit crops masked
       filter output to the shape's box, which squares off the corners) -->
  <g clip-path="url(#noSlot)">
    <rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" rx="{R}" filter="url(#shadow)"/>
    <rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" rx="{R}" filter="url(#contact)"/>
  </g>

  <g mask="url(#punch)">
    <!-- metal -->
    <g clip-path="url(#cardClip)">
      <rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" rx="{R}" fill="url(#metal)"/>
      <rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" rx="{R}" fill="#000" filter="url(#grain)"/>
      <rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" rx="{R}" fill="url(#light)"/>
      <rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" rx="{R}" fill="url(#vignette)"/>
    </g>
    <rect x="{CX + .75}" y="{CY + .75}" width="{CW - 1.5}" height="{CH - 1.5}" rx="{R - .75}" fill="none" stroke="url(#edge)" stroke-width="1.5"/>
    <rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" rx="{R}" fill="none" stroke="#7d8287" stroke-opacity=".6"/>

    <!-- slot's inner wall -->
    <rect x="{slot_x}" y="{slot_y}" width="{slot_w}" height="{slot_h}" rx="{slot_h / 2}" fill="none" stroke="#6c7176" stroke-opacity=".7" stroke-width="2"/>
    <path d="M{slot_x + slot_h / 2} {slot_y + slot_h + 1}h{slot_w - slot_h}" stroke="#fff" stroke-opacity=".6"/>

    <g class="etched">
      <!-- name -->
      <text class="label" x="{X(56)}" y="{Y(96)}">NAME</text>
      <text x="{X(56)}" y="{Y(146)}" font-size="46" font-weight="500" letter-spacing="-0.8" fill="{ETCH}">{NAME}</text>
      {etched_line(56, 166, 540)}

      <!-- fields -->
      {''.join(fields)}

      <!-- badge name + barcode -->
      <text x="{X(px + pw / 2)}" y="{Y(py + ph + 42)}" text-anchor="middle" font-size="19" font-weight="600" letter-spacing="4.5" fill="{ETCH}">{BADGE_NAME}</text>
      {barcode(px, py + ph + 64, pw, 62)}
      <text x="{X(px + pw / 2)}" y="{Y(py + ph + 150)}" text-anchor="middle" font-size="11" font-weight="600" letter-spacing="3.2" fill="{LABEL}">CAMERONWILLIA.MS</text>
    </g>

    <!-- photo window: a shallow recess with an etched silhouette -->
    <rect x="{X(px)}" y="{Y(py)}" width="{pw}" height="{ph}" rx="14" fill="url(#recess)"/>
    <g clip-path="url(#photo)" class="etched" fill="none" stroke="{ETCH}" stroke-opacity=".55" stroke-width="1.5">
      <circle cx="{X(px + pw / 2)}" cy="{Y(py + 92)}" r="42"/>
      <path d="M{X(px + 14)} {Y(py + ph + 2)}c4-58 40-92 {pw / 2 - 14}-92s{pw / 2 - 18} 34 {pw / 2 - 14} 92"/>
    </g>
    <rect x="{X(px) + .5}" y="{Y(py) + .5}" width="{pw - 1}" height="{ph - 1}" rx="13.5" fill="none" stroke="#6c7176" stroke-opacity=".55"/>
    <path d="M{X(px) + 14} {Y(py + ph) + 1.5}h{pw - 28}" stroke="#fff" stroke-opacity=".55"/>

    <!-- glint: a faint, wide band of light that drifts across, then rests -->
    <g class="shine" clip-path="url(#cardClip)">
      <rect x="-560" y="-200" width="520" height="{H + 400}" fill="url(#shine)" transform="rotate(16 {W / 2} {H / 2})">
        <animateTransform attributeName="transform" type="translate" additive="sum"
          values="0 0; {W + 700} 0; {W + 700} 0" keyTimes="0; .4; 1" dur="7s"
          calcMode="spline" keySplines=".4 0 .3 1; 0 0 1 1" repeatCount="indefinite"/>
      </rect>
    </g>
  </g>
</svg>
"""


def main():
    font = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_FONT
    out = HERE / "id-card.svg"
    out.write_text(svg(base64.b64encode(font.read_bytes()).decode()))
    print(f"wrote {out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
