# Installing into Azahar, Citra and forks

The same mod folder works in any 3DS emulator that loads mods the Azahar way.

1. Build it: `python tools/build_wilds_mod.py --rom your-game.cci --out wilds-damage-mod`
   (the `--zip` is only for the 4u-native port's import).
2. Copy the **contents** of the built title folder
   (`wilds-damage-mod/0004000000126300` for the American game, `0004000000126100` for the
   European one) into the emulator's `load/mods/<same title id>/` folder, so it reads:

   ```
   load/mods/0004000000126300/
   ├─ exefs/code.bin
   ├─ exheader.bin
   ├─ romfs/eng/data/core_quest.arc   (and the other archives the build lists)
   ├─ settings_.json
   └─ wilds_damage_mod.json
   ```

3. Start the game and turn the numbers on: START menu > **Mod Settings** > Interface >
   **Damage Numbers** > on. Style, Show All Damage, size and duration are on the same
   page.

## Notes

* The mod is built for the version of your game file (base or update — the build reads
  it and adapts). If you later update the game, build the mod again from the updated
  file.
* Cheats that patch the game's code (most damage- or HP-related cheat lists) fight over
  the same bytes this mod changes. Prefer turning such cheats off while the mod is on.
* The Mod Settings page is part of the mod: without it there is nothing to switch.
