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
