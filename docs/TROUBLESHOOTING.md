# Troubleshooting

Written from a real failure on a real phone (an Infinix X6882, MT6789, Mali-G57), whose
log showed every one of these signs.

## The most common one: the mod installs but nothing appears

The port's log said:

```
[Info] Loader: code mod: .../load/mods/single-screen/exefs/code.ips
[Info] Mods: mods on, in load order: mh4u-wilds-damage-1.0.0, single-screen (code)
[Info] App: code library matches the code mods ...|.../load/mods/single-screen/:...
```

Read it: **only `single-screen` carries `(code)`** — the damage numbers mod had no
`exefs/code.bin`, so the port treated it as an empty mod and built its code library
without it. Nothing drew, and no error appears anywhere, because nothing was wrong with
what was installed — what was installed was not the mod.

That happens when the **repository zip** is imported instead of a **built mod zip**. This
repository is the *builder*; the mod itself comes out of running the builder on your own
game file:

```
python tools/build_wilds_mod.py --rom your-game-file --out wilds-damage-mod --zip
```

The zip to import is `wilds-damage-mod/mh4u-wilds-damage-<region>.zip` — the one the
builder prints. It holds `exefs/code.bin` (18.9 MB for the USA update), `exheader.bin`
and `romfs/<lang>/data/core_common.arc`.

## The checklist that matches the log's lines

1. The Mods page lists the mod **and shows it as a code mod** (the log's load order line
   names code mods with `(code)`).
2. gear > System > **Code library** says it **matches** the code mods — if it says it
   does not, build the code library once more (the mod changed the game's code; the
   library must be built with it, once, per mod change).
3. In a quest, START > **Mod Settings** > Interface > **Damage Numbers** > on. The page
   only exists when the mod's code is in the library.
4. Still nothing? Check the log (gear > System, the log screen): the load-order line
   should read `mh4u-wilds-damage..., single-screen (code)` with **your mod carrying
   `(code)`** (order does not matter; carrying the code does).

## "The port plays but the numbers never show" — the other causes

* The HUD is hidden (the numbers draw only with the quest's HUD up).
* The character's option is off: Mod Settings is per character; another hunter starts
  with it off.
* The mod was built from a different game file than the one the port runs (an update
  mismatch). Rebuild from the same file you gave the port; the builder prints the version
  it built for (`built from usa_update`, the USA v1.3.0 update the port runs).

## The startup refusal: "the code library ... does not match ... rebuild the code library"

After importing a code mod, the port refuses to start the game with the old code library
and says exactly this, with two crc32 values:

```
[Error] Runtime: the code library .../libmh4u_code_native.so does not match ...:
the program's code (..., crc32 71870D9F) is not the code ... was built from (..., crc32 9D682788):
rebuild the code library from this version of the game
```

That refusal is **correct and expected** — it proves the mod loaded (the loader's lines
above it name the mod's `exefs/code.bin` and its `exheader.bin in place of the game's`).
The first crc32 is the code as assembled **with** the mod; the second is what the library
on the phone was built from **before** it. The fix is the port's own step: gear >
System > **Build the game code** ("Build on this phone"), once, and let it finish.

## "The game stopped: a bad guest memory access" after the library matched

If the log shows the library accepted (`code library for usa_v130 …`, the mod in the load
order, its romfs files replaced) and then the game stops with

```
mh4n: bad guest memory access: access at 0x0131xxxx (guest thread 1, lr 0x0130xxxx)
```

at an address just past `0x1308000`, the mod's assets predate the fix of 2026-11-16: that
build's exheader declared the data segment 19 pages short of where its state variables
live (`mod_options_state` at `0x131AD70` was the first touch — the Mod Settings page's
options and Damage Numbers' own state sit in the extension's variables region, past the
code). The code itself was consistent; only the memory map was declared too small.

**Fix: re-download the release asset and import it again** (remove the old mod entry
first). The updated asset keeps every byte the code library was built from — the .text and
the extension's crc32s are unchanged — so **the library stays valid: no rebuild needed**.
The appended pages are the zeros the variables start as, and the exheader now declares the
segment out to `0x131B000`.

## One code mod at a time: this mod and jM5557's single-screen cannot compose

Both mods write code into the same unused space of the game's executable (the padding
before `.rodata`, around `0xDECEF0`): this mod puts its memory-split bootstrap there, the
single-screen mod puts its own stub. Applied together — a full `code.bin` first, then the
other mod's `code.ips` — the ips overwrites the bootstrap, and the assembled code is
broken (verified byte for byte: applying jM5557's ips over this mod's `code.bin` lands
`0xDECD00+732` of its bytes exactly on this mod's stub). They also both ship their own
`core_common.arc`, and only one of those can win.

So: **turn `single-screen` off on the Mods page** (or remove it) while this mod's code is
in the library. You lose nothing: the port has its **own** single-screen mode (gear >
Graphics & Audio > Screen and HUD), which needs no code mod. Switching between the two
mods later means one more library rebuild — each code mod needs the library built with
it.

## Building from the update

The builder accepts the update file directly and says so (`built from usa_update`): the
4u-native port runs the update's code, so a mod built from the update file is the closest
possible match. A base-game file works too (the builder adapts with its address maps).

## Verifying a build without a device

Compare your game file's code against the port's own published versions
(4u-native's `mh4n/config/versions.json`): the USA v1.3.0 update's decompressed code
SHA-1 is `c9225f87ca3f65e8537484d029b08b8b04c3717d`. The builder's game file that hashes
to it is exactly the code the port's library expects. `python tools/selftest.py` checks
everything else offline.
