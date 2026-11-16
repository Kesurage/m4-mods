#!/usr/bin/env python3
"""Make the curated tuning files from the upstream defaults plus per-preset overrides.

The default curated file (core/game/data/curated/damage_numbers.json) is Heavenfall Beta's
tested tuning, kept as the "faithful" preset. The presets in docs/presets/ change only the
values listed here; everything else stays. Every produced file is checked with the same
loader and packer the build uses (core.interface.damage_numbers.damage_numbers).
"""
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.interface.damage_numbers.damage_numbers import load_tuning  # noqa: E402

CURATED = ROOT / "core/game/data/curated/damage_numbers.json"
PRESETS = ROOT / "docs/presets"

# value overrides per preset: dotted path into the tuning dict
OVERRIDES = {
    "wilds-vivid": {
        "colours.gold": [255, 176, 38, 255],
        "styles.wilds.effects.0.colour": [255, 58, 140, 255],
        "styles.wilds.effects.1.colour": [255, 244, 255, 255],
        "pop.scale": 1.55,
        "stack.max": 5,
    },
    "wilds-minimal": {
        "digit_height": 10.0,
        "pop.scale": 1.3,
        "rise": 12.0,
        "colours.grey": [140, 140, 140, 255],
        "stack.radius": 12.0,
    },
}

DESCRIPTIONS = {
    "faithful": (
        "MH4U Wilds Damage Numbers (core/interface/damage_numbers/damage_numbers.py): the default tuning, kept "
        "exactly as Heavenfall Beta ships it (popzol and BlitzWOLF, GPL-3.0-or-later) - the values they iterated on "
        "in game. Sizes and distances are in the top screen's layout units (400 x 240 at 5:3), times are seconds. "
        "The presets in docs/presets/ change only some values."
    ),
    "vivid": (
        "wilds-vivid preset (docs/presets/wilds-vivid.json): the faithful tuning with a deeper amber-orange gold "
        "for weak spots, a punchier pop and one more stack step. Apply it with "
        "tools/build_wilds_mod.py --preset vivid."
    ),
    "minimal": (
        "wilds-minimal preset (docs/presets/wilds-minimal.json): smaller, calmer numbers - the tiny real-time "
        "readout. A digit's cell is 10 layout units instead of 11.25, the pop is softer, numbers rise less. "
        "Apply it with tools/build_wilds_mod.py --preset minimal."
    ),
}


def set_path(raw: dict, dotted: str, value) -> None:
    """Dotted path through the tuning's {"value": ..., "description": ...} wrappers: `colours.gold` lands in
    colours["value"]["gold"], `pop.scale` in pop["value"]["scale"], `styles.wilds.effects.0.colour` in
    styles["value"]["wilds"]["effects"][0]["colour"] (styles' entries are not wrapped)."""
    def descend(node, key):
        if isinstance(node, list):
            return node[int(key)]
        if isinstance(node, dict) and key in node:
            return node[key]
        if isinstance(node, dict) and isinstance(node.get("value"), dict) and key in node["value"]:
            return node["value"][key]
        raise KeyError(f"{dotted}: no '{key}' in {type(node).__name__}")

    keys = dotted.split(".")
    target = raw
    for key in keys[:-1]:
        target = descend(target, key)
    last = keys[-1]
    if isinstance(target, list):
        target[int(last)] = value
    elif isinstance(target, dict) and isinstance(target.get(last), dict) and "value" in target[last] \
            and not isinstance(target[last].get("description"), dict):
        target[last]["value"] = value            # a wrapper: digit_height -> digit_height["value"]
    elif isinstance(target, dict) and last in target:
        target[last] = value
    elif isinstance(target, dict) and isinstance(target.get("value"), dict) and last in target["value"]:
        target["value"][last] = value
    else:
        raise KeyError(f"{dotted}: cannot place the value")


def main() -> int:
    default_raw = json.loads(CURATED.read_text(encoding="utf-8"))

    # the curated default keeps the upstream values; refresh its description
    default_raw["description"] = DESCRIPTIONS["faithful"]
    CURATED.write_text(json.dumps(default_raw, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    PRESETS.mkdir(parents=True, exist_ok=True)
    for name, overrides in OVERRIDES.items():
        raw = copy.deepcopy(default_raw)
        raw["description"] = DESCRIPTIONS[name.split("-")[1]]
        for dotted, value in overrides.items():
            set_path(raw, dotted, value)
        path = PRESETS / f"{name}.json"
        path.write_text(json.dumps(raw, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)} ({len(overrides)} overrides)")

    # every tuning the repo ships must load and pack
    files = [CURATED] + sorted(PRESETS.glob("*.json"))
    ok = True
    for path in files:
        try:
            tuning = load_tuning(path)
            from core.interface.damage_numbers.damage_numbers import data_block
            block = data_block(tuning)
            print(f"OK  {path.relative_to(ROOT)}: loads, data block {len(block)} bytes")
        except Exception as error:  # noqa: BLE001
            ok = False
            print(f"FAIL {path.relative_to(ROOT)}: {error}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
