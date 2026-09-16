# KiCad Adapter, BoardState, ChangeSet, and Ownership

## 1. KiCad integration evidence

The bundled studies show several viable local KiCad access paths, each with different authority/freshness properties:

| Mechanism | Evidence-backed use | Current treatment |
|---|---|---|
| `pcbnew.ActionPlugin`, `pcbnew.GetBoard()` | active live PCB, native object creation/removal, UI refresh | strong adapter reference |
| kipy/IPC | live PCB save/reload/actions | adapt; exact KiCad-10 role unresolved |
| direct `.kicad_pcb` S-expression | bulk PCB query/mutation | adapt behind adapter; version/fidelity tests required |
| `.kicad_pro` JSON | net classes/design settings | adapt |
| `.kicad_dru` S-expression | custom rules | adapt |
| `kicad-cli` | DRC/ERC/export/oracle-style validation | candidate authority/secondary oracle; final status unresolved |
| DSN/SES | FreeRouting workflow | reference only for native target |

KRT also demonstrates a live path `pcbnew.GetBoard() -> routing-oriented model -> route -> board.Add/RemoveNative -> pcbnew.Refresh()`. The useful lesson is the integration path, not coupling Core Router APIs directly to `pcbnew`.

### Version evidence must remain separated

- KCAA declared `kicad-python>=0.7.1` with KiCad 9+ GUI context; its CI used KiCad 10 in inspected Linux/Windows jobs.
- KRT parser/writer evidence covers KiCad 9/10 PCB syntax, while inspected PCM metadata declared KiCad 9.0.
- Therefore file-format support does **not** establish end-to-end live plugin support for KiCad 10.

**BLOCKING UNKNOWN:** final KiCad version/API support matrix and authority for each operation.

## 2. Canonical BoardState

KCAA currently separates raw S-expressions/project files/live objects, query dictionaries, and a routing `WorldModel`. No current donor representation is sufficient as the cross-component contract.

`WorldModel(obstacles, board_bbox)` should remain a derived routing view, not BoardState.

### Required canonical domains

A product BoardState/BoardSnapshot needs, at minimum:

```text
Board
├── exact validated outer outline + cutouts/openings
├── layers / authoritative copper order / stackup metadata
├── footprints / bodies / courtyards as required
├── pads + access geometry
├── nets / net classes / connectivity graph
├── tracks / arcs / vias / zones
├── via type/span/manufacturing constraints
├── keepouts / rule areas
├── resolved rules + rule provenance
├── stable object identity
├── KiCad lock state
├── ownership/protection/provenance
└── source + freshness metadata
```

Current extraction evidence is relatively strong for footprints, pads, nets, tracks, copper layers, rules/netclasses/custom rules, and basic vias. It is incomplete/weak for full stackup, exact authoritative outline usage, stable identity/provenance, complete via-span semantics, lock state, canonical connectivity, filled-zone freshness, and ownership.

### Board boundary invariant

Valid `Edge.Cuts` is mandatory for automated routing/placement. Existing fallback behavior in donors—default board bounds, footprint-union bounds, skipping bounds checks, or using only the `Edge.Cuts` AABB—must not become the product legality contract. Concave/non-rectangular outlines require actual validated outline geometry.

## 3. Ownership and object protection

KRT already provides useful **net/source-state** protection patterns: pre-existing copper is normally non-rip-eligible; selected pre-existing nets can be explicitly authorized; locked-segment/via nets can be excluded; diff-pair members are protected together; and protected-net invariants can be persisted in `.kicad_pro`.

This is not enough for safe selective automation. The product requires object-level identity/provenance capable of distinguishing, conceptually:

```text
USER_PROTECTED
USER_EDITABLE
ROUTER_GENERATED
ROUTER_TEMPORARY
IMPORTED_UNKNOWN
```

These category names are a research recommendation, not a finalized schema. The required behavior is the important part: a manually edited segment on an otherwise router-owned net must be independently protectable; a generated via must be attributable to a run; deletion/replacement must target identity rather than only coordinate tolerance.

**BLOCKING UNKNOWN:** how ownership/identity persists (KiCad UUID/group/property, `.kicad_pro`, sidecar manifest, other local state).

## 4. Router-neutral ChangeSet

Routing and analysis computation should not opportunistically mutate KiCad. A controlled boundary is expected:

```text
Core Router
  -> ChangeSet candidate
  -> safety/validation gate
  -> KiCad Adapter
       - resolve stable identities
       - verify freshness/preconditions
       - begin native transaction or equivalent
       - add/remove/update authorized objects
       - rollback/reject on failure
       - refresh/re-read authoritative state
```

The exact ChangeSet schema is not available in the bundled sources. It should not be guessed before the missing dedicated BoardState/ChangeSet study or an explicit design decision.

## 5. Transaction and freshness evidence

KCAA provides strong project/file-level safety patterns: automatic snapshots before protected mutations, coherent project-version archives, restore backups, `.bak` files, temp-write + `os.replace()`, dirty-file tracking, and reload after mutation even when failure may have partially changed state.

KRT live mutation shows precompute-before-apply and can reject a route before touching the live board, but the inspected code did not establish `BOARD_COMMIT` grouping or a general atomic multi-object ChangeSet contract.

**REQUIREMENT implied by safety direction:** failed/rejected/partial mutation must have a defined recovery path; file state and live editor state must not be treated as automatically identical.

## 6. Adapter design rule

KiCad-specific objects and runtime semantics terminate at the Adapter/Model/Rule layers. Core Router and Analyzer should consume normalized product models rather than `pcbnew` objects or parser-specific syntax trees. This preserves replaceability of file/live/IPC mechanisms and keeps KiCad version compatibility localized.
