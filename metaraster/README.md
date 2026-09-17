# MetaRaster

**Live demo:** https://darkwebdronedrops.github.io/torespar/metaraster/

MetaRaster is a working implementation of the **Transformer Native CRT-based Visual Encoding** research program — token-grid perception for transformers, expressed as readable text.

## Versions

- **MetaRaster.3** (`index.html`) — Alphabetical Chroma LC encoding. Static images → luminance+chroma character pairs. A–Z hue map (A=red 0°, Z=blue 240°), 9-level luma charset (`.:-=+*#%@`), saturation threshold for neutral grays. Client-only, no backend.
- **META.RASTER.DELTA** (`delta.html`) — Temporal frame differencing for motion. `_` = unchanged pixel; LC pair = new value. Webcam or built-in ball demo source, live delta mask, persistent-canvas decoder, keyframe interval control.

## Naming

| Context | Term |
|---|---|
| Formal / external (paper, funding) | Transformer Native CRT-based Visual Encoding |
| Product (public) | MetaRaster |
| In-house (family) | Kimi Vision |

## Research

- GitHub: https://github.com/darkwebdronedrops/Kimi-Vision
- Studio: https://darkwebdronedrops.github.io/torespar/

## License

- **MetaRaster** (this directory): proprietary — © 2026 Torespar Studios, Inc. All rights reserved. See [LICENSE](LICENSE).
- **Research** (Transformer Native CRT-based Visual Encoding): [MIT](https://github.com/darkwebdronedrops/Kimi-Vision/blob/main/LICENSE)
