# kuiper-drawing-engine

Array drawing tool: https://ventusltd.github.io/kuiper-drawing-engine/

Choose a layout preset, enter module dimensions and tilt, then use Plan or 3D.
Plant opens the addressed virtual layout; select an array by number, use the
one-metre direction buttons, or enable Move array and drag. Save settings keeps
local placement edits. The default 1 GW DC example is synthetic.

The interface uses thin unfilled outlines. It does not supply an approved site,
structural design, protection design or SLD. See [scope and checks](docs/ARRAY-LAYOUT.md)
and [drawing source review](docs/DRAWING-SOURCE-REVIEW.md). Original array-tool
code is covered by `LICENSE-ARRAY`; retained third-party assets keep their terms.

## Symbol research

Kuiper's drawing work uses the shared open SLD library and education bench:

https://ventusltd.github.io/sld/

Reusable source catalogue:
https://ventusltd.github.io/sld/data/library.json

Source, pinned acquisition configuration and local GPU furnace:
https://github.com/Ventusltd/sld

The bench supports educational symbol assembly and JSON/SVG exports. Its
illustrative centre links are not validated electrical terminal connections.
Production symbols require a separate standards and approved-drawing review.

The earlier seven-symbol research pilot remains in `vendor/powsybl-symbols`;
the SLD owner now maintains the complete pinned ConvergenceLibrary acquisition.
