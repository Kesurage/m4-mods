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
