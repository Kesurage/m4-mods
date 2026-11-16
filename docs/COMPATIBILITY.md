# Compatibility

## Games this build supports

The build writes every patch once, for one canonical executable (the European update's),
and carries it to your game version with its address maps — so the mod works on whatever
MH4U you give it:

| Game | Region | Built from your file | Notes |
|---|---|---|---|
| MH4U v1.0 (base) | EUR, USA | yes | `eur_base` / `usa_base` address maps |
| MH4U update (v1.1 / v1.3) | EUR, USA | yes | the version most players have; `usa_update` map, EUR update is the canonical |
| MH4G (Japan) | JPN | no | its code differs; no address map exists for it |
| Monster Hunter Generations / XX | — | no | different games |

The 4u-native port's own target is the USA v1.3.0 update — the most common case, and the
one to test first.

## Emulators and ports

| Platform | Supported | How |
|---|---|---|
| 4u-native (Android) | yes | docs/INSTALL-4U-NATIVE.md (mods folder + in-app code library build) |
| Azahar / AzaharPlus | yes | docs/INSTALL-AZAHAR.md |
| Citra and forks with mod support | yes | same as Azahar |
| Real 3DS with Luma3DS | in principle | the mod folder is the `luma/titles/<id>/` shape (`mod_title`); untested here — feedback welcome |

## Other mods and cheats

* **jM5557's single-screen mod** (or the port's built-in one-screen arrangement): no
  conflict — it moves menus (layouts of other archives); the damage numbers live in their
  own group of `core_quest.arc` and their own code blocks.
* **jM5557's QOL cheats**: different call sites; no conflict is known, but the built
  *code* cheats (their "Mods" exefs route) patch the same executable — order the Mods
  page so both build into the code library, and test before hunting.
* **Code-writing cheat lists** (HP, damage multipliers): those patch the same bytes. Use
  one or the other.
* **HD texture packs**: no conflict (different files entirely).

## Multiplayer

The numbers you see are your own hits (others' only with Show All Damage), and every
player's game keeps its own display choices — nothing the mod changes is sent online.
Online, the usual mod etiquette applies: it is a display-only mod, but agree on code mods
in the room as the port's own guide suggests.
