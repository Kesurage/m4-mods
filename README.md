# MH4U Wilds Damage Numbers

**Monster Hunter Wilds' damage number system, ported to Monster Hunter 4 Ultimate.**

Every hit you land shows a number at the point of impact: white for a normal hit, gold
for a weak spot, grey for a bounce or a poison tick, gold for a blast — and a pink star
with its bright core for a critical, the way Wilds marks it. Numbers pop in, rise, fade,
and stack upwards when your combo lands on the same spot. A hit you did not make can show
too, with **Show All Damage**. It works with MH4U's own damage system — the real values
the game computes, read where the game applies them.

Built for the **4u-native Android port** (no new APK — it installs as the port's own mod
folder and the port rebuilds its code library with it) and for Azahar / Citra.

```
        * 17            <- a critical on a weak spot: the star, the gold number
        8               <- a normal hit, stacking a step lower
       (poison 5)       <- the monster's poison ticks, grey, at the monster
```

## What it does

* **Wilds-style numbers over monsters**, from the game's real damage flow (its hit
  records, hitzones and critical flags — no invented values).
* **Three styles in the game**: Wilds (the star), Rise (the red slash), Classic (MH4U's
  own side marks) — START menu > Mod Settings > Interface > Damage Numbers > Style.
* **Show All Damage**: other players' hits and damage no hit explains (sieges, the map).
* **Size 50%-400% and duration 0.4-2.0 s** per character, changed during play, kept in
  the save.
* Three tunings shipped: **faithful** (the tested default), **wilds-vivid** (deeper gold,
  punchier pop), **wilds-minimal** (the tiny real-time readout) — `docs/presets/`.

## Install (4u-native, the short version)

**No PC?** Playing the USA game with the v1.3.0 update: download
**`mh4u-wilds-damage-usa-4u-native.zip`** from the
[latest release](https://github.com/Kesurage/m4-mods/releases/latest) on your phone —
that is the built mod — and go to step 2 of **docs/INSTALL-4U-NATIVE.md**.

**This repository is the builder — the mod is its output.** Run the builder on your own
game file (the decrypted `.cci`/`.3ds`/`.cia`; the update file works too):

```
python tools/build_wilds_mod.py --rom your-game-file --out wilds-damage-mod --zip
```

then import the zip it prints (`mh4u-wilds-damage-<region>.zip` — **not** this
repository's zip): port > gear > **Mods & Cheats** > **Mods** > **Add a mod (.zip)**, and
build the code library with the mod (**Build on this phone**, once). The Mods page must
show your mod as a code mod and the **Code library** row must say it matches — that is
the whole game. Full details, the Azahar route, the Termux-on-phone route and the
checklist that diagnoses "installed but nothing appears": **docs/INSTALL-4U-NATIVE.md**,
**docs/INSTALL-AZAHAR.md**, **docs/TROUBLESHOOTING.md**.

Your game file is only ever read, never written; the mod is built for your game's own
version and region (EUR/USA, base or update). The damage numbers are turned on in the
game: START > Mod Settings > Interface > Damage Numbers > on.

## Check it works

* weak spot -> gold, elsewhere -> white, bounce -> grey;
* critical -> the pink star at the number's top left;
* poison ticks -> grey at the monster, blast -> gold, mount finish -> gold;
* numbers one after another on a spot -> stack upwards;
* open the menu -> the numbers freeze (the game's pause).

## Compatibility

EUR and USA, base game and update. No conflict with the single-screen mods or HD texture
packs; code-writing cheat lists fight over the same bytes — use one or the other. Details
and the real-3DS note: **docs/COMPATIBILITY.md**.

## How it works (one paragraph)

A focused build of popzol and BlitzWOLF's **Heavenfall Beta** (GPL-3.0): its damage
numbers feature hooks the two functions of MH4U's damage flow — a hit's final damage
being added to the monster (`FUN_00be9c64` -> `FUN_00921f74`), and the monster's damage
step (poison tick, blast, mount finish) — measures what each call added, and draws
numbers through the game's own 2D layout system from a small Open Sans digit atlas
registered as the quest layout `hf_dmg`. The patched executable (`exefs/code.bin`), its
exheader and the layout archives (`romfs/`) are what the mod folder carries; the build
adapts every patch to your game's version with address maps. The long version:
**docs/WILDS-SPEC.md** (what Wilds shows and what MH4U can carry), the vendored
**docs/HOW-IT-WORKS-upstream.md** (the upstream system in full).

## Honest limits

Paralysis, sleep and stun buildup numbers (Wilds' status counters) are not in this
version — MH4U applies those statuses without a damage event, and no hook exists for
them yet (docs/ROADMAP.md). Element is not split out: MH4U folds it into the final
damage before the mod sees it. Wounds and focus strikes do not exist in MH4U.

## Credits and license

* **popzol** and **BlitzWOLF** — Heavenfall Beta, whose damage numbers system this mod
  builds and builds on (GPL-3.0-or-later). This repository is a focused, retuned
  distribution of that work for the 4u-native port; all its source is here and stays
  under the GPL.
* **Open Sans** — the digits' typeface (SIL Open Font License 1.1).
* The **4u-native** port team — the mod loader this targets.
* **jM5557** — the mod conventions the install paths follow.

MH4U Wilds Damage Numbers: GPL-3.0-or-later, like upstream. Monster Hunter 4 Ultimate is
Capcom's; this mod never includes, distributes or modifies your game file.

## Verify your checkout

```
python -m pip install zstandard
python tools/selftest.py
```

11 checks: the tunings load and pack, the compiled code blocks are present, the version
maps are there, the atlas covers the styles, and a mod folder fits the 4u-native loader's
expectations.
