# PowSyBl SVG research candidates

Seven unmodified SVG source files from [PowSyBl Diagram](https://github.com/powsybl/powsybl-diagram), revision `952186b5b34d1e4e472a04fb663b3654b54e3022`, from its `ConvergenceLibrary`. The upstream project and its contributors are the source of this artwork; no authorship is claimed by this repository.

Upstream folder: `single-line-diagram/single-line-diagram-core/src/main/resources/ConvergenceLibrary/`.

These files are distributed under the included **Mozilla Public License 2.0**. Retain that licence and applicable notices, and meet its source-availability requirements when distributing covered files or modifications. The pinned repository tree contained no file with NOTICE or copyright in its path; the selected SVGs contained no separate copyright or licence notices. The upstream root LICENSE is preserved byte for byte. Exact paths, immutable raw source URLs and SHA-256 hashes are recorded in `manifest.json`.

Every entry has `standards_validation: "unverified"`, `approved_project_drawing: null`, and `production_enabled: false`. Display labels are tentative. These are research candidates, not an enabled production symbol palette. British-standard conformity and matching to an approved real-project drawing dated after 2012 have not been established.

The two transformer assets are winding fragments, not individually complete transformers. Anchor/assembly metadata and upstream styling have not been imported; preserve and review those before attempting production assembly. The generic ground graphic must not be silently labelled protective earth without an engineering review.

Verification: all seven SVGs parsed as XML; none contained script, foreignObject, image, use, event-handler attributes, href/src references or URL-valued attributes. SHA-256 hashes were computed on the unchanged downloaded bytes. This check establishes limited static-file hygiene, not symbol accuracy.

See [the research review](../../docs/OPEN-SYMBOL-LIBRARY-REVIEW.md) for alternatives and outstanding validation.
