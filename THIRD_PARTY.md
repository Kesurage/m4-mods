# Third-party code and assets in this repository

## Heavenfall Beta (the vendored `core/`)

* Project: **Heavenfall Beta — Monster Hunter 4 Ultimate on one screen**, by popzol and
  BlitzWOLF, with community contributors.
* Source this checkout was taken from:
  https://github.com/popzol/4u-heavenfall-mod-beta (the damage numbers system in
  `core/interface/damage_numbers/`, the executable machinery in `core/game/executable/`,
  the compiled code blocks in `core/game/executable/generated/`, and the supporting
  modules they need).
* License: **GNU General Public License v3.0 or later** — `LICENSE` in this repository is
  upstream's own copy. This repository is a derivative work: it distributes a focused
  subset of upstream (the damage numbers feature and its dependencies), retunes its
  curated damage numbers data, adds the focused build script and the documentation, and
  rebrands the edition metadata. All changes keep the same license, and the GPL's
  section 7 requirement to preserve legal notices is respected by this file and the
  headers upstream carried.

## Open Sans (the damage numbers' digits)

* The digit atlas `core/interface/damage_numbers/art/damage_numbers.png` sets digits from
  the **Open Sans** typeface, Copyright 2011-2015 Steve Matteson, under the **SIL Open
  Font License, Version 1.1**. Open Sans may be used, studied, modified and embedded by
  its terms; the OFL's text is at https://openfontlicense.org. The atlas file itself is
  upstream's, distributed here under the repository's GPL like the rest, while the
  typeface's own license continues to apply to the glyph shapes.

## Monster Hunter 4 Ultimate

* Capcom's game. Nothing in this repository includes game data that can play the game;
  the compiled code blocks are patches and injected code of our own, and the build
  transforms only the user's own copy, which is never modified or shared.

## Others referenced

* **4u-native** (khorne-hub) — the Android port this mod targets; its mod loader defines
  the folder layout docs/INSTALL-4U-NATIVE.md describes. GPL-3.0.
* **jM5557's MH4U mods** — the title-id folder conventions the install guides follow.
  Their repos are referenced only, not vendored.
