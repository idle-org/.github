# Idle artwork and share card

## Existing identity

- `idle.png`: the original Idle organisation logo supplied through the maintainer's Gitea organisation.
- `canvas-pilot.png`: unchanged `crates/canvas-pilot/assets/app-icon.png` from Canvas Pilot.
- `pdf-presenter.png`: unchanged `crates/pdf-presenter/assets/app-icon.png` from PDF Presenter.
- `tiny-wb.png`: unchanged existing tiny-wb repository avatar, also added to that project's `docs/images/project-icon.png`.

The existing artwork was reused on 2026-11-20. This does not introduce a new license for project branding.

## Generated fox

`idle-share-fox.png` was generated on 2026-11-20 with the built-in image generation tool, using `idle.png` as an identity and palette reference. The illustration is used unchanged in the share-card layout. No CLI or API fallback was used.

Exact prompt:

> Use case: logo-brand. Create a new companion fox illustration for an Idle open-source software sharing card. Use the supplied existing Idle logo as identity and palette reference: elegant curled orange fox, deep ink navy ears and nose, cream chest, sweeping copper tail. Preserve the recognizable character but illustrate it as a friendly alert fox sitting with its generous tail curled around its feet, looking slightly left toward an adjacent QR code that will be placed separately in the final layout. Sophisticated clean sculptural paper-cut / softly shaded illustration, crisp silhouette, burnt orange, warm cream, deep ink navy. Center the whole fox comfortably in a square image with generous margins. Solid warm ivory background #fffaf2. No text, no letters, no QR code, no border, no watermark. This is the artwork only; a real machine-readable QR will be constructed separately without modifying this illustration.

## Share card

`idle-share-qr.svg` is a standalone 1200 × 720 layout with embedded fox artwork and a deterministic vector QR code. `idle-share-qr.png` is its 2400 × 1440 raster rendering. These are intended to be shared as links, images, or printed cards advertising Idle's public organisation page.

The QR payload is exactly `https://github.com/idle-org`. It uses error correction H and an unobstructed four-module quiet zone. No generated pixels are used for its modules, and the fox does not overlap it. There is no URL shortener, analytics service, or expiring redirect.

Build with `scripts/build-share-card.py` from the repository root, after installing the pinned packages in `scripts/requirements-share-card.txt`. The script renders the SVG with CairoSVG and checks the resulting card with ZXing at widths of 2400, 1200, 600, and 480 pixels. All four decoded the expected URL on 2026-11-20. Physical printed scans have not been tested.
