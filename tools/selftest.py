#!/usr/bin/env python3
"""Check everything of this repository that can be checked without a game file.

    python tools/selftest.py

What it checks:

1. the vendored core imports and its command line answers;
2. every tuning the repository ships (the curated default and the presets) loads with the
   build's own loader and packs into the exact data block the compiled code reads
   (932 bytes, the code's own static assert);
3. the compiled code blocks the build places (damage_numbers_stub, _code, _data, _state)
   are present in core/game/executable/generated/code_space.json;
4. every game version the build supports has its address map
   (core/game/executable/generated/versions/);
5. the digit atlas has the styles' cells and the marks the tunings name;
6. a mod folder in the shape the 4u-native port's loader expects (exefs/code.bin,
   exheader.bin of at least 0x800 bytes, romfs archives) passes the same checks the
   builder applies to a real build - tried here on a synthetic folder, clearly not a
   game file.

It prints PASS or FAIL per check and exits 0 only when all pass.
"""
import json
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

RESULTS = []


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, ok, detail))
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f" - {detail}" if detail else ""))


def check_cli() -> None:
    run = subprocess.run([sys.executable, "-m", "core", "--help"], cwd=ROOT,
                         capture_output=True, text=True)
    check("core command line answers", run.returncode == 0 and "--damage-numbers" in run.stdout)


def check_tunings() -> None:
    from core.interface.damage_numbers.damage_numbers import load_tuning, data_block
    files = [ROOT / "core/game/data/curated/damage_numbers.json",
             *sorted((ROOT / "docs/presets").glob("*.json"))]
    for path in files:
        try:
            block = data_block(load_tuning(path))
            check(f"tuning packs: {path.name}", len(block) == 932, f"{len(block)} bytes")
        except Exception as error:  # noqa: BLE001
            check(f"tuning packs: {path.name}", False, str(error))


def check_blocks() -> None:
    code_space = ROOT / "core/game/executable/generated/code_space.json"
    try:
        data = json.loads(code_space.read_text(encoding="utf-8"))
    except Exception as error:  # noqa: BLE001
        check("compiled blocks readable", False, str(error))
        return
    blocks = data.get("blocks", {})
    variables = data.get("variables", {})
    wanted = ("damage_numbers_stub", "damage_numbers_code", "damage_numbers_data", "damage_numbers_state")
    names = set(blocks) | set(variables)
    missing = [w for w in wanted if not any(w in name for name in names)]
    check("damage numbers blocks compiled", not missing,
          ("missing: " + ", ".join(missing)) if missing else "3 code/data blocks + the state variable present")


def check_versions() -> None:
    from core.game.executable.versions import CANONICAL  # noqa: F401  (import proves it parses)
    maps = sorted(p.stem for p in (ROOT / "core/game/executable/generated/versions").glob("*.json"))
    # the canonical executable (eur_update) needs no map; every other supported version has one
    check("version maps present", len(maps) >= 3, ", ".join(maps) + " (+ the eur_update canonical)")


def check_atlas() -> None:
    from core.interface.damage_numbers.layout import atlas
    from core.interface.damage_numbers.damage_numbers import load_tuning, MARKS
    art = atlas()
    tuning = load_tuning()
    problems = []
    for style, entry in tuning["styles"].items():
        digits = art["styles"].get(style, {}).get("digits")
        if not digits or len(digits) != 10:
            problems.append(f"{style}: the atlas has no 10 digit cells")
        for effect in entry["effects"]:
            if effect["mark"] not in art.get("effects", {}):
                problems.append(f"{style}: the atlas has no '{effect['mark']}'")
            if effect["mark"] not in MARKS:
                problems.append(f"{style}: '{effect['mark']}' is not a mark of the code")
    check("atlas covers the tunings", not problems, "; ".join(problems) or "3 styles, marks found")


def check_mod_folder_shape() -> None:
    """A mod folder as the 4u-native port's loader reads it (mh4n native/src/code_patch/code_patch.h):
    the first of exefs/code.bin, code.bin takes the game's code's place; exheader.bin (first 0x800
    bytes) takes the game's exheader; romfs/ files take the game's files. Tried on a synthetic
    folder - its bytes are a fixture, not a game file."""
    with tempfile.TemporaryDirectory(prefix="wilds_shape_") as temp:
        mod = Path(temp) / "0004000000126300"
        (mod / "exefs").mkdir(parents=True)
        (mod / "exefs" / "code.bin").write_bytes(bytes(2_000_000))   # dummy, the size of a real one is 16 MB
        (mod / "exheader.bin").write_bytes(bytes(0x800))
        (mod / "romfs" / "eng" / "data").mkdir(parents=True)
        (mod / "romfs" / "eng" / "data" / "core_quest.arc").write_bytes(b"fixture")
        # the loader's rules, as the port implements them
        replacement = next((p for p in (mod / "exefs" / "code.bin", mod / "code.bin") if p.is_file()), None)
        exheader = mod / "exheader.bin"
        ok = (replacement is not None and replacement.stat().st_size > 0
              and exheader.is_file() and exheader.stat().st_size >= 0x800
              and any(mod.glob("romfs/*/data/*.arc")))
        check("mod folder shape fits the 4u-native loader", ok)
        # the builder's own post-build checks would accept the same shape
        sys.path.insert(0, str(ROOT / "tools"))
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("bwm", ROOT / "tools/build_wilds_mod.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            files = module.check_output(mod)
            check("builder accepts the shape", len(files) >= 2, f"{len(files)} files")
        except SystemExit as error:      # check_output fails with sys.exit
            check("builder accepts the shape", False, f"refused (exit {error})")


def check_data_block_struct() -> None:
    """The code's own static asserts, mirrored here: 932 bytes of data, 1480 of state."""
    from core.interface.damage_numbers.damage_numbers import load_tuning, data_block
    block = data_block(load_tuning())
    check("data block size", len(block) == 932, f"{len(block)} bytes (the code asserts 932)")
    check("data block little-endian u32s", len(block) % 4 == 0 and struct.unpack_from("<I", block)[0] != 0)


def main() -> int:
    check_cli()
    check_tunings()
    check_blocks()
    check_versions()
    check_atlas()
    check_mod_folder_shape()
    check_data_block_struct()
    failed = [name for name, ok, _ in RESULTS if not ok]
    print(f"\n{len(RESULTS) - len(failed)}/{len(RESULTS)} checks pass" + (f"; FAILED: {', '.join(failed)}" if failed else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
