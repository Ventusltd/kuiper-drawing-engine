# Open electrical symbol sources

Reviewed 25 September 2026. Seven exact-byte PowSyBl research SVGs have been imported under `vendor/powsybl-symbols`, with the upstream MPL 2.0 licence and a source/hash manifest. None is production-enabled or approved for production by this research task.

## Finding

No inspected source establishes the complete combination of unrestricted/open licensing, comprehensive UK power-grid SLD coverage, and independently demonstrated British-standard compliance. Open licensing and correct engineering representation are separate tests.

The strongest practical grid-SLD source is **PowSyBl Diagram**, with actual SVG component libraries under MPL 2.0 and network-driven SLD generation. The strongest verified university-backed framework is **pandapower**, from University of Kassel and Fraunhofer IEE, under BSD-3-Clause; its main value is network modelling, analysis and plotting. For electronics-oriented symbols, evaluate **KiCad's official library**, accepting attribution/share-alike for redistributed collections. For the least restrictive individual SVG assets, use the **CC0 subset of basverdoes/ElectricalSymbolLibrary**. None is ready to label “British-standard compliant” without the required symbol-by-symbol review.

## First choice: grid and university sources

**PowSyBl Diagram** is directly useful for reuse. Its [official SLD documentation](https://github.com/powsybl/powsybl-diagram/blob/main/docs/single_line_diagrams/index.md) describes SVG generation for voltage levels, substations and zones, supporting node/breaker and bus/breaker topologies and replaceable component libraries.

Pinned revision: `952186b5b34d1e4e472a04fb663b3654b54e3022`. The repository's [actual LICENSE](https://github.com/powsybl/powsybl-diagram/blob/952186b5b34d1e4e472a04fb663b3654b54e3022/LICENSE) is Mozilla Public License 2.0. The [ConvergenceLibrary SVG directory](https://github.com/powsybl/powsybl-diagram/tree/952186b5b34d1e4e472a04fb663b3654b54e3022/single-line-diagram/single-line-diagram-core/src/main/resources/ConvergenceLibrary) contains actual breaker-open/closed, disconnector-open/closed, ground, ground-disconnector, transformer windings, generator, load, battery, capacitor, inductor, load-break switch, LCC and VSC graphics. The parallel FlatDesignLibrary offers another visual style. Inspected the SVG source of breaker, disconnector, ground and transformer files in both directories: no separate or conflicting licence statements found. These SVGs inherit the repository licence on the evidence inspected. MPL is open source with file-level source-sharing requirements, not a noncommercial or no-ML licence. Keep notices and the source of covered distributed modifications available as required.

**Recommended pilot:** ConvergenceLibrary breaker-open/closed, disconnector-open/closed, ground, and the two transformer-winding SVGs, together with the library's component/anchor metadata. Inspect rendered output and assembly rather than treating each winding fragment as a complete device. This is the most directly relevant source found for a utility-grid SLD. It remains a source/licence screen, with no British compliance or post-2012 approved-drawing match claimed. CT, VT, inverter and low-voltage protective-device requirements need a separate coverage review.

**pandapower** provides the verified university connection the user prefers. [Fraunhofer's official account](https://www.iee.fraunhofer.de/de/presse-infothek/Presse-Medien/2024/pandapower-open-source-tool-erreicht-500k-downloads.html) and the [project contact page](https://www.pandapower.org/contact/) identify joint development by University of Kassel and Fraunhofer IEE. Its [official licence](https://pandapower.readthedocs.io/en/latest/about/license.html) is BSD-3-Clause. Use it for reusable network models, engineering calculations and network visualisation; university provenance does not make its plotting glyphs a verified British symbol catalogue. A sensible architecture is pandapower for network analysis and a reviewed PowSyBl-derived symbol layer for drawings, subject to implementing the data mapping.

BSI identifies [BS EN 60617](https://landingpage.bsigroup.com/LandingPage/Series?UPI=BS+EN+60617) as the graphical-symbol family; [BS ISO 14084-2:2015](https://knowledge.bsigroup.com/products/process-diagrams-for-power-plants-graphical-symbols) expressly points to IEC 60617 for electrotechnical diagrams. This supports the reference family, not certification of a third-party library or permission to redistribute IEC database artwork.

## Licence and source audit

| Candidate | Inspected licence and scope | Practical assessment |
|---|---|---|
| KiCad official symbols | CC-BY-SA 4.0 with exception for electronic designs and their generated files. Redistributing modified symbol collections retains attribution and share-alike. No ML-specific exclusion in inspected licence. | Mature candidate; electronics emphasis. Four relevant classes found: circuit breakers, fuses, transformers, earth. IEC and US alternatives coexist; never import by name alone. |
| basverdoes/ElectricalSymbolLibrary | `src/symbols/` explicitly CC0 1.0; all other repository files, including the assembled SVG, are CC-BY-NC-SA 4.0. Four inspected individual IEC SVGs also carry embedded CC0 metadata. | Strongest unrestricted SVG subset, but analog/electronics coverage rather than complete utility switchgear. Preserve provenance even though attribution is not a CC0 condition. |
| Schematika | Standard MIT licence at pinned revision. Inspected every Python file in `src/schematika/electrical/symbols/`; no separate copyright/licence/QElectroTech notice found. | IEC claims are author's claims. Breaker, fuse, CT, contacts, motors available; no dedicated utility transformer, VT or inverter located in that package. Alpha API. |
| Schemdraw | Standard MIT licence; inspected resistor/fuse/breaker, switch, and earth definition files. | Useful drawing engine, SVG output and explicitly selectable IEC style. Style selection affects a subset; do not assume every element becomes IEC-compliant. |
| Powston electrical-symbols | README and package metadata say MIT, but no LICENSE/NOTICE file found in pinned repository tree. | Especially relevant solar SLD React/SVG coverage, but Australian conventions. Four component files inspected; no conflicting per-file notice. Needs proper licence text and independent symbol review before adoption. |
| QElectroTech current collection | `ELEMENTS.LICENSE` includes CC-BY 3.0 terms plus an explicit restriction on using associated files as sample data for building ML models. | Does not meet this task's unrestricted-use criterion. A downstream wrapper claiming MIT or plain CC-BY does not by itself resolve upstream provenance. |

Pinned primary sources:

- KiCad inspected historical GitHub mirror revision `4e17d7595f9691d45d97aea8ad64572652fb5bed`: [licence](https://github.com/KiCad/kicad-symbols/blob/4e17d7595f9691d45d97aea8ad64572652fb5bed/LICENSE.md), [Device.lib](https://github.com/KiCad/kicad-symbols/blob/4e17d7595f9691d45d97aea8ad64572652fb5bed/Device.lib), [power.lib](https://github.com/KiCad/kicad-symbols/blob/4e17d7595f9691d45d97aea8ad64572652fb5bed/power.lib). This mirror uses legacy `.lib` files; it is not evidence of the current release's exact inventory. [Current official licensing policy](https://www.kicad.org/libraries/license/) confirms the same licensing structure.
- basverdoes revision `ed1c2a3a910969b6de2483249515cce10cfd0a07`: [scope of licence](https://github.com/basverdoes/ElectricalSymbolLibrary/blob/ed1c2a3a910969b6de2483249515cce10cfd0a07/README.md), [individual IEC symbols](https://github.com/basverdoes/ElectricalSymbolLibrary/tree/ed1c2a3a910969b6de2483249515cce10cfd0a07/src/symbols/analog-iec/core). Files inspected: `ground-earth.svg`, `transformer.svg`, `resistor.svg`, `capacitor.svg`; embedded CC0 metadata credits Filip Dominec and contributors.
- Schematika revision `d883ff975722d4cf9f40651f489831b11276eb4b`: [MIT licence](https://github.com/OleJBondahl/Schematika/blob/d883ff975722d4cf9f40651f489831b11276eb4b/LICENSE), [symbol package](https://github.com/OleJBondahl/Schematika/tree/d883ff975722d4cf9f40651f489831b11276eb4b/src/schematika/electrical/symbols).
- Schemdraw revision `e140437dac9b681e9f7eb1accdd462fef2433864`: [MIT licence](https://github.com/cdelker/schemdraw/blob/e140437dac9b681e9f7eb1accdd462fef2433864/LICENSE.txt), [element sources](https://github.com/cdelker/schemdraw/tree/e140437dac9b681e9f7eb1accdd462fef2433864/schemdraw/elements), [IEC style documentation](https://schemdraw.readthedocs.io/en/stable/elements/electrical.html).
- Powston revision `0f7cc28e209a74427ba479bb5a20bcfc77b81ebe`: [README](https://github.com/powston/electrical-symbols/blob/0f7cc28e209a74427ba479bb5a20bcfc77b81ebe/README.md), [components](https://github.com/powston/electrical-symbols/tree/0f7cc28e209a74427ba479bb5a20bcfc77b81ebe/src/components). Inspected CircuitBreaker, Fuse, EarthSymbol and Transformer TSX. Claimed IEC IDs are unverified. Breaker comment says cross but geometry contains a square and horizontal internal stroke; this is a concrete reason to check graphics independently.
- QElectroTech revision `1932150ea6a93a89200f391af1fe89c6aaebfc45`: [actual collection terms](https://github.com/qelectrotech/qelectrotech-source-mirror/blob/1932150ea6a93a89200f391af1fe89c6aaebfc45/ELEMENTS.LICENSE). [Example downstream SLD project's notice](https://github.com/synergycodes/ng-diagram-single-line-diagram/blob/main/NOTICE.md) explicitly identifies QElectroTech-derived artwork despite its MIT application code.

## Additional electronics candidates

Evaluate KiCad `Device:CircuitBreaker_1P`, `Device:Fuse`, `Device:Transformer_1P_1S`, and `power:Earth_Protective`. These names and definitions exist in the pinned source. This is a **source and licence screen only**, not a standards approval. The transformer is an electronics winding representation, not automatically the preferred utility SLD glyph. Preserve variants for functional earth versus protective earth and breaker versus disconnector; an generic switch must not silently stand in for an isolator.

Alternatively, the four CC0 SVGs above are a clean extraction starting point if unrestricted assets take priority, but they leave the utility switchgear problem unresolved.

Before a part becomes production-ready, record upstream revision/path/licence, intended function, applicable IEC reference, and the matching **approved real-project drawing dated after 2012**, including drawing ID, revision, date, sheet, and reviewer. No such project drawing was supplied to this research agent, so that user's validation requirement remains outstanding for every part. No geometry was certified or visually approved here.

## SPICE

SPICE describes electrical models and simulation; it does not define a British-compliant graphical symbol bank. **ngspice** is a good open simulation candidate: its [official FAQ](https://ngspice.sourceforge.io/faq.html) identifies modified BSD licensing, and its [developer page](https://ngspice.sourceforge.io/devel.html) explicitly notes exceptions. Review the selected distribution and third-party models separately. A model's pin mapping and parameters can be associated with a drawing symbol, but model validity and symbol conformance are separate.

**LTspice is not an unrestricted symbol source merely because it is free to download.** Analog Devices points users to the installed [LTspice EULA](https://support.analog.com/en-US/knowledgebase/article/ka-16982). Do not assume ngspice's licence covers LTspice, PSpice, manufacturer models, or bundled artwork.

## Grid foundations and manufacturers

[OpenSCD](https://openscd.org/) is an open IEC 61850 SCL configuration tool; its [resource page](https://openscd.org/resources.html) connects it with LF Energy CoMPAS. This is valuable grid engineering infrastructure, but not evidence of a complete British-compliant artwork library. A separate audit of any SLD plugin's actual graphics is required. Likewise [SunSpec](https://sunspec.org/specifications/) supplies DER interoperability specifications and information models, not a universal SLD artwork bank. Shared equipment models can support a future symbol catalogue but do not confer artwork rights or conformance.

Manufacturer drawings from Schneider Electric, ABB, Victron, SMA, or Control Techniques should be treated as product-specific references until the exact asset licence is established. Schneider's [official CAD-download guidance](https://www.se.com/us/en/faqs/FA344563/) establishes availability, while its [UK terms](https://www.se.com/uk/en/about-us/legal/terms-of-use/) identify technical drawings and graphics as protected content. This audit did not establish an unrestricted manufacturer-wide symbol licence for any of those five vendors. Publicly downloadable CAD/EPLAN material is not sufficient proof. An open manufacturer software repository would only cover the material within its stated licence scope.

Recommendation: use a small reviewed open core with explicit source and licence records, add missing utility symbols through a documented implementation and standards review, and keep manufacturer part metadata separate from the generic electrical glyphs. There is no verified all-grids, all-manufacturers, fully open, pre-approved British SLD library in this review.

## Working groups and interoperability

LF Energy (https://lfenergy.org/grid-operators/) provides shared open software developed with grid operators, including PowSyBl. UCA International Users Group (https://ucaiug.org/about-ucaiug/) supports IEC 61850 and CIM interoperability. CIGRE working groups (https://www.cigre.org/article/home/cigre-active-working-groups--call-for-experts) address engineering topics including information exchange and digital twins. These are different outputs: executable software, exchange conventions and engineering guidance. None alone establishes a freely reusable, validated British drawing-symbol library. UK/IEC conventions are the intended default; alternative conventions must be explicitly labelled.

## Drawing conventions and honest document status

BS EN 61082-1:2015 covers preparation and presentation of electrotechnical documents, including diagrams (https://knowledge.bsigroup.com/products/preparation-of-documents-used-in-electrotechnology-rules). IEC 60617 supplies graphical symbols; its official database is subscription-based (https://webstore.iec.ch/en/publication/2723). These references do not constitute an open-source artwork licence or evidence that this implementation complies with every applicable clause.

Proposed application acceptance rules, not a quotation of either standard:

- A concept block view must be labelled as such. Do not equate appearance or animation with engineering approval.
- An SLD view must represent electrical equipment and circuit connectivity at an explicitly stated scope and design stage, with identifiable devices and unambiguous connection/junction semantics.
- Required voltage levels, equipment/circuit ratings, switching/protection and earthing information depend on the view's purpose. Unknown information stays explicitly unknown; the renderer must not invent it.
- A high-level SLD may legitimately omit detail held in linked schedules, protection drawings and lower-level SLDs. Missing detail alone is not evidence of deception.
- Approved status requires an actual review record, drawing identity/revision and referenced evidence. A preliminary SLD must remain preliminary.
- Connect symbols to typed equipment and terminal/node records. Derive the picture and exports from those same records so lines have electrical meaning, rather than being arbitrary graphics.
