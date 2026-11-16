# The MH Wilds damage numbers, and what this mod ports of them

This is the design document behind the mod's defaults. It says what Monster Hunter Wilds
shows, what Monster Hunter 4 Ultimate can show through the same kind of system, and why
every value in `core/game/data/curated/damage_numbers.json` is what it is.

## What MH Wilds shows

When a hit lands in Monster Hunter Wilds, a number appears at the point of impact and
floats up briefly. Multiple community guides agree on the reading:

| What you see | What it means |
|---|---|
| White number | A normal hit on a part that takes neutral or little damage |
| Yellow / orange number | A hit on a weak spot (or a wound), the parts that take the most damage |
| A star-like burst at the number | The hit was a **critical** (positive affinity); its flare is bright with a lighter core |
| Blue-ish tint or marks on special parts | Parts with a state of their own (veils, membranes) react differently |
| Second, smaller numbers | Status and extra effects feed their own feedback beside the damage |

The features that make the Wilds system read at a glance:

1. **Colour = quality of the hit, at a threshold.** One look tells you whether the part
   you hit is a weak spot, without knowing hitzone tables.
2. **The crit mark is separate from the colour.** A critical hit keeps the same damage
   colour and gains a mark, so "weak spot" and "critical" never blur into one.
3. **Numbers pop in** (start slightly oversized and settle), **rise**, and **fade out**
   after most of their life, instead of blinking away.
4. **Consecutive hits stack**: numbers landing on the same spot within a short time climb
   one step each, so a combo reads as a column instead of a pile.
5. **Damage you do not explain yourself still shows** (poison ticks, blast, mounts and
   other sources), colour-coded so you can tell them from your hits.

## What MH4U gives the mod to work with

The vendored system (from Heavenfall Beta) hooks the game's real damage flow:

* `FUN_00be9c64` — a hit on a monster — hands over the hit's final damage, the hit record
  (where it landed, what made it, whether it bounced, whether it was a critical) and the
  hitzone value the hit met (cut, impact or shot);
* `FUN_00920104` — the monster's damage step — hands over poison ticks, blast detonations
  and the mount's finish, each with the health they took;
* the monster's health each frame lets the mod show damage no hook explains
  (the **Show All Damage** option): other players' hits, siege weapons, whatever is left.

So MH4U can produce, faithfully:

| Wilds feature | In this mod |
|---|---|
| White = normal hit | white for a physical hitzone below the threshold |
| Yellow / orange = weak spot | gold for a physical hitzone at or above the threshold (default 45) |
| Crit mark | the pink star with its bright core, drawn behind the digits (Wilds style) |
| Pop in, rise, fade | pop of 1.45x settling in 0.12 s, rise of 16 layout units, fade after 70% of the life |
| Stacking | numbers within 14 units of one younger than 0.35 s climb 1.05 digit heights each, up to 4 |
| Poison / blast / mount feedback | grey for poison and bounces, gold for blast and the mount's finish |
| Unexplained damage | Show All Damage shows it in white at the monster |

The styles selectable in the game's START menu (Mod Settings > Interface > Damage
Numbers > Style) each recreate one game's reading: **Wilds** (the star), **Rise** (the red
slash through the number) and **Classic** (MH4U's own small marks at the sides).

## Why the default colours are what they are

* **White** `[255, 255, 255, 255]` — Wilds' normal-hit number, and MH4U's own popup
  colour, so the familiar reading is kept.
* **Gold** `[255, 196, 64, 255]` — sits between Wilds' yellow weak-spot numbers and its
  orange wound numbers; on MH4U's small screen it stays readable over every area's
  background the tested value was iterated against.
* **Grey** `[150, 150, 150, 255]` — bounces and poison. A bounce is a hit that did nothing;
  poison ticks are the game's own damage over time. Both read "not a real swing".
* **The crit star** `[255, 80, 170, 255]` with core `[255, 240, 250, 255]` — Wilds reads
  its criticals through the pink-red burst at the number's top left, not through the
  number's colour.

Two shipped presets move the feel without moving the reading:

* `docs/presets/wilds-vivid.json` — deeper amber gold `[255, 176, 38]`, punchier pop
  (1.55x), one more stack step (5): for phones with room to spare.
* `docs/presets/wilds-minimal.json` — the "tiny real-time numbers" reading: digits at
  10.0 layout units, softer pop, shorter rise, calmer grey.

## What MH4U cannot give the mod (honestly)

* **Paralysis / sleep / stun buildup numbers.** Wilds counts status buildup with numbers;
  MH4U applies those statuses without a damage event, and no hook into their application
  exists in this system. Poison is shown because it takes health. Blast is shown because
  its detonation takes health. See docs/ROADMAP.md.
* **Wounds and focus strikes.** Wilds' wound system does not exist in MH4U; weak spots
  stand in for them through the hitzone threshold.
* **Element-breakdown numbers.** MH4U folds element into the hit's final damage before
  the hook sees it, so the mod shows the same number the game's own damage flow computed.

None of these are hidden: the mod shows what the game's damage system really carries,
and docs/ROADMAP.md says what a next version would need to add the rest.
