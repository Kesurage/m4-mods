# Installing into the 4u-native Android port

The [4u-native port](https://github.com/khorne-hub/4u-native) of Monster Hunter 4
Ultimate loads mods from a `mods` folder and rebuilds its code library from them — no new
APK, nothing on your phone is replaced. This mod is built for exactly that flow.

## 0. What you need

* The 4u-native port installed and your game working in it (its own guide's steps 1-4).
* Your decrypted game file (the `.cci` / `.3ds` / `.cia` you already own), on the phone or
  a PC. The build reads it; it is never modified.
* For a PC build: Python 3.10+ and `pip install zstandard`.
* For a phone-only build: the phone's browser. No PC needed.

## 1. Get the mod

**Easiest — download it built (no PC, no building at all):** if you play the **USA game
with the v1.3.0 update** (the code the port runs — the overwhelmingly common case), grab
**`mh4u-wilds-damage-usa-4u-native.zip`** from this repository's
[latest release](https://github.com/Kesurage/m4-mods/releases/latest) in the phone's
browser and skip to step 2. It is the built mod, for exactly that version (verified
against the port's own published code hash). European game or another version? Build
yours below — it reads your file and adapts.

**On a PC:**

```
python tools/build_wilds_mod.py --rom your-game.cci --out wilds-damage-mod --zip
```

**On the phone, no PC:** install [Termux](https://termux.dev) (free), then:

```
pkg install python git
pip install zstandard
git clone https://github.com/Kesurage/m4-mods
cd mh4u-wilds-damage
python tools/build_wilds_mod.py --rom /sdcard/Download/your-game.cci --out wilds-damage-mod --zip
```

The same Python, on the phone. It needs a few hundred megabytes of free space and a few
minutes.

The output is `wilds-damage-mod/0004000000126300/` (American) or `.../0004000000126100/`
(European), built for your game's own version — and `mh4u-wilds-damage-<region>.zip`
next to it with `--zip`.

## 2. Give it to the port

Either way works:

* **Import the zip:** in the game, gear > **Mods & Cheats** > **Mods** > **Add a mod
  (.zip)** — pick the zip you downloaded (`mh4u-wilds-damage-usa-4u-native.zip`, the
  release asset) or the one a build printed (`mh4u-wilds-damage-<region>.zip`). The port
  finds the mod inside the zip, even nested, and lists it on the Mods page.
* **Or the mods folder beside the game:** copy the `0004000000126300` (or `...126100`)
  folder into the `mods` folder that sits beside your game file (`MH4U/mods/`). The port
  lists the mods in that folder too.

The mod folder holds `exefs/code.bin` (the patched executable), `exheader.bin` and
`romfs/` (the layout and the digit picture the numbers draw with). Where two mods change
the same file, the one lower in the Mods page's list wins — if you also use the
single-screen mod, either order works: they touch different files.

## 3. Build the code library with the mod

The mod changes the game's code, so the port's code library has to be built with it once:

* **On the phone:** the first start after adding the mod says the library is missing —
  tap **Build on this phone**, then **Build**. Later: gear > **System** > **Game code** >
  **Build the game code**. The port's own guide has the details (it downloads its tools,
  needs about 1 GB free and 4 GB of memory, and takes about 30-90 minutes on a phone,
  once).
* **On a PC (faster):** the port's own PC build with the mod:
  `sh mh4n/tools/android/build-android-library.sh ~/MH4U/update.cia --mods ~/MH4U/mods`
  (see the port's README, step 3). Copy the two files it makes onto the phone.

The gear > **System** row **Code library** then says the library matches the mods that
are on.

## 4. Turn it on and tune it

1. Start the game. The mod adds the game's START menu a third page, **Mod Settings**.
2. Interface > **Damage Numbers**: on. From then on every hit shows its number.
3. The page also holds **Show All Damage** (other players' hits and damage no hit
   explains), the **Style** (Wilds / Rise / Classic), the **Size** (50%-400%) and the
   **Duration** (0.4-2.0 s). Every character keeps their own choices in their save.

## Check it works

Hunt something small and hit it a few times:

* a hit on a weak part (the head of most early monsters) shows **gold**, a hit elsewhere
  **white**, a bounce **grey**;
* a critical hit (positive affinity weapon, or just wait for luck) carries the **pink
  star** at the number's top left;
* a poisoned monster's ticks show **grey** numbers at it; a blast shows **gold**;
* numbers landing one after another on the same spot **stack upwards**;
* pause (the menu) stops the numbers' clocks; they do not run during item use.

If the game starts without the numbers showing at all, check that the Mods page lists the
mod **on**, that the **Code library** row says it matches, and that the quest's HUD is on
(the numbers only show in a quest with the HUD up).

## Removing it

Mods page: tap the mod, **Remove** — then rebuild the code library once more, since it
was built with the mod's code.
