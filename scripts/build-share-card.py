#!/usr/bin/env python3
"""Render the Idle share card with a deterministic QR and unchanged fox artwork."""
import base64
from pathlib import Path
import cairosvg
import qrcode
from PIL import Image
import zxingcpp

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'profile/assets'
URL = 'https://github.com/idle-org'


def build():
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, border=4)
    qr.add_data(URL)
    qr.make(fit=True)
    matrix = qr.get_matrix()
    modules = len(matrix)
    step = 10
    size = modules * step
    # Keep the full four-module quiet zone white. Artwork never overlaps the code.
    cells = ''.join(f'<rect x="{x*step}" y="{y*step}" width="{step}" height="{step}"/>'
                    for y, row in enumerate(matrix) for x, dark in enumerate(row) if dark)
    fox = base64.b64encode((ASSETS / 'idle-share-fox.png').read_bytes()).decode('ascii')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1200" height="720" viewBox="0 0 1200 720" role="img" aria-labelledby="title desc">
<title id="title">Share Idle — github.com/idle-org</title>
<desc id="desc">A curled orange fox beside a QR code linking directly to https://github.com/idle-org.</desc>
<defs><clipPath id="fox-panel"><rect x="604" y="88" width="552" height="552" rx="32"/></clipPath></defs>
<rect width="1200" height="720" fill="#fffaf2"/>
<rect x="36" y="38" width="7" height="106" rx="3" fill="#d56a35"/>
<g fill="#09212b" font-family="DejaVu Sans, sans-serif">
<text x="65" y="104" font-size="72" font-weight="bold">Idle</text>
<text x="68" y="147" font-size="24">Screens, shows, and signals.</text>
<text x="68" y="199" font-size="18" letter-spacing="2">OPEN-SOURCE TOOLS</text>
</g>
<image x="604" y="88" width="552" height="552" clip-path="url(#fox-panel)" xlink:href="data:image/png;base64,{fox}"/>
<g transform="translate(66 224)">
<rect width="{size}" height="{size}" fill="white"/>
<g fill="#09212b" shape-rendering="crispEdges">{cells}</g>
</g>
<g fill="#09212b" font-family="DejaVu Sans, sans-serif">
<text x="68" y="680" font-size="28" font-weight="bold">github.com/idle-org</text>
<text x="880" y="680" font-size="20" text-anchor="middle">Scan. Explore. Share.</text>
</g>
</svg>'''
    (ASSETS / 'idle-share-qr.svg').write_text(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(ASSETS / 'idle-share-qr.png'),
                    output_width=2400, output_height=1440)
    for width in [2400, 1200, 600, 480]:
        # Render each size directly from SVG to test the published card at common sizes.
        import io
        png = cairosvg.svg2png(bytestring=svg.encode(), output_width=width,
                              output_height=round(width * 0.6))
        decoded = zxingcpp.read_barcodes(Image.open(io.BytesIO(png)))
        assert any(result.text == URL for result in decoded), f'QR failed at {width}px'
        print(f'QR verified at {width}px: {URL}')


if __name__ == '__main__':
    build()
