# Drawing source review

The local inventory scanned 20,645 tracked code files, excluding vendor/build
folders and files larger than 2 MB. It is not a complete history or semantic audit.
GPU literal-pattern results matched CPU searches. A similarity graph shortlisted
9,173 candidates; its ranking is discovery evidence, not a quality score.

One reviewed source is
`globalgrid2050/kuiper-grid/i0097/cartridges/009300000000-kuiper-programs.js`,
particularly the `build` routine around lines 692–800. It covers portrait versus
landscape dimensions, table rows, opposing faces, normalized junction positions,
and string traversal orders. The repository root declares CERN OHL-S v2; this
review does not relicense or copy that source into the independently authored
array tool.

Lessons applied to new code:

- Junction fractions belong to the physical short/long module axes and rotate
  with orientation. A test now checks this transform.
- Unknown junction geometry stays absent rather than acquiring plausible dots.
- Geometry can calculate the required reach of a cable. It cannot establish
  which lead lengths were supplied or approved.
- Presets remain editable; setting precedence must be explicit.

The top-ranked shortlist contains many related cartridge versions. It is not
100 independent drawing engines. Further source review must account for this
duplication and inspect other families before claiming broad coverage.

`electrical_reference_check.py` accepts local reference data and compares two
algebraic forms of a linear open-circuit voltage model on CPU/GPU. It separately
reports an equality tolerance band and STC current comparisons. It does not
establish installed variants, site temperatures, protection, cable sizing,
MPPT temperature behaviour or construction approval. Inputs and results may be
confidential and must stay outside the repository and served web directory.

A second reviewed family is `testcode/sandbox/202609052028/layer-apps/solar-bess-topology-v7/module-layout/module-layout-v5.js`, functions `mlPointFromOffset`, `mlRect` and `mlBuildLayout` (lines 74?145). It uses Turf destinations to place geographic rectangles, assigns per-module indices and explicitly caps rendering at 6,000 modules. Its useful distinction is total module count versus rendered count. The current tool similarly keeps the full addressed population separate from sampled display, and now checks every virtual module corner on GPU against CPU placement arithmetic. Geographic coordinates, terrain and routing are not supplied by the current tool. No source from this family was copied.

The discovery tool now emits a second shortlist with at most three candidates per normalized source directory (numeric version/date segments collapsed), and skips identical normalized-content hashes. This improves breadth but cannot prove that distinct directories contain independent implementations.
