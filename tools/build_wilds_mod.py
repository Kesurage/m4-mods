#!/usr/bin/env python3
"""Build the MH4U Wilds Damage Numbers mod folder from your own game file.

    python tools/build_wilds_mod.py --rom game.3ds --out wilds-damage-mod
    python tools/build_wilds_mod.py --rom game.cia --out wilds-damage-mod --preset minimal --zip

This is the one command of this repository. It:

1. checks the tuning (the default curated one, or the preset you picked) with the same
   loader the build itself uses;
2. runs the vendored build (core, a focused fork of popzol and BlitzWOLF's Heavenfall Beta,
   GPL-3.0-or-later) with every other feature off, so the mod only adds the damage numbers;
3. checks what came out (the patched executable, its exheader, the interface archives);
4. puts it in the emulator's layout: OUT/<title id>/ (0004000000126300 for the American
   game, 0004000000126100 for the European one), optionally zipped for an emulator's
   "add a mod" page (--zip).

Your game file is only ever read, never written. The build is for your game's own version
and region (European or American, with or without the update): whatever you have, this
builds for it.

Afterwards, see docs/INSTALL-4U-NATIVE.md (the 4u-native Android port) or
docs/INSTALL-AZAHAR.md (Azahar, Citra and forks) for where the folder goes.
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

PRESETS = ("faithful", "vivid", "minimal")

# the build's flags: the damage numbers on, every other feature of the fork off.
# A flag here can be overridden on the command line (write it after the script's own).
BASE_FLAGS = [
    "--damage-numbers",
    "--no-single-screen", "--no-layered-equipment", "--no-quality-of-life",
    "--no-lock-on", "--no-hold-a", "--no-fast-text", "--no-box-equipment",
    "--hud-scale", "100",
    "--camera-speed", "10", "--camera-distance", "100",
    "--cheat-3d-mode", "off", "--no-cheat-no-bloom-dof", "--cheat-fps", "off",
    "--cheat-fov", "50", "--no-cheat-net-fix",
    "--cheat-aspect-ratio", "off", "--no-cheat-raw-unbloat",
]


def fail(message: str) -> None:
    print(f"build_wilds_mod: {message}", file=sys.stderr)
    sys.exit(1)


def preset_path(name: str) -> Path:
    if name == "faithful":
        return ROOT / "core/game/data/curated/damage_numbers.json"
    if name in ("vivid", "minimal"):
        return ROOT / f"docs/presets/wilds-{name}.json"
    path = Path(name).expanduser().resolve()
    if not path.is_file():
        fail(f"the preset {name} is not a file")
    return path


def apply_preset(path: Path) -> None:
    """The chosen tuning becomes the curated one the build reads."""
    target = ROOT / "core/game/data/curated/damage_numbers.json"
    data = path.read_bytes()
    target.write_bytes(data)
    from core.interface.damage_numbers.damage_numbers import load_tuning
    load_tuning(target)          # refuses anything the build could not pack
    print(f"tuning: {path.name} (checked: loads and packs)")


def region_of(rom: Path, forced: str) -> str:
    """The game's region, from its title id (the game file itself, never written). The
    update titles carry their base's region (the port runs the update's code)."""
    from core.game.executable.titles import MH4U_UPDATES, file_title, mh4u_region, normal
    seen = "auto"
    try:
        title = file_title(str(rom))
        if title:
            region = mh4u_region(title) or MH4U_UPDATES.get(normal(title))
            if region:
                seen = region
    except Exception as error:  # noqa: BLE001
        if forced == "auto":
            fail(f"cannot read the game's title id ({error}); pass --region usa or --region eur")
    if forced != "auto":
        if seen != "auto" and seen != forced:
            print(f"warning: the game file says {seen}, --region says {forced}; using {forced}")
        return forced
    if seen == "auto":
        fail("the game file's region is unknown; pass --region usa or --region eur")
    return seen


def check_output(mod_dir: Path) -> list[Path]:
    """What the build wrote must be there and sane; returns the files to place."""
    code = mod_dir / "exefs/code.bin"
    exheader = mod_dir / "exheader.bin"
    if not code.is_file() or code.stat().st_size < 1_000_000:
        fail(f"the build wrote no executable ({code}): did the command above print an error?")
    problems = []
    if not exheader.is_file():
        problems.append("exheader.bin is missing: the game's own header would run a shorter program and crash")
    elif exheader.stat().st_size < 0x800:
        problems.append(f"exheader.bin is {exheader.stat().st_size} bytes (a header is at least 0x800)")
    archives = sorted(mod_dir.glob("romfs/*/data/*.arc"))
    if not archives:
        problems.append("no romfs archive: the damage numbers draw through a layout the game loads from them")
    for problem in problems:
        print(f"warning: {problem}")
    return [code, exheader] + archives


def place(temp: Path, out: Path, title: str) -> Path:
    final = out / title
    if final.exists():
        shutil.rmtree(final)
    final.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(temp, final)
    return final


def make_zip(final: Path, out: Path, region: str) -> Path:
    zip_path = out / f"mh4u-wilds-damage-{region}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for file in sorted(final.rglob("*")):
            if file.is_file():
                archive.write(file, file.relative_to(final.parent))
    return zip_path


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="build_wilds_mod",
        description="MH4U Wilds Damage Numbers: the mod in a folder, from your own game file")
    parser.add_argument("--rom", type=Path, required=True, help="your decrypted game file (.3ds, .cia, .zcci...)")
    parser.add_argument("--out", type=Path, default=Path("wilds-damage-mod"), help="output folder (default %(default)s)")
    parser.add_argument("--preset", default="faithful",
                        help="faithful (Heavenfall's tested tuning), vivid, minimal, or a path to your own JSON")
    parser.add_argument("--region", choices=("auto", "usa", "eur"), default="auto",
                        help="only when the game file's title id cannot be read")
    parser.add_argument("--zip", action="store_true", help="also write OUT/mh4u-wilds-damage-<region>.zip")
    parser.add_argument("--code", type=Path, help="advanced: build from this executable instead of the game file")
    known, extra = parser.parse_known_args()
    if not known.rom.is_file():
        fail(f"the game file {known.rom} does not exist")

    preset = preset_path(known.preset)
    region = region_of(known.code if known.code else known.rom, known.region)
    title = {"usa": "0004000000126300", "eur": "0004000000126100"}[region]

    default_tuning = ROOT / "core/game/data/curated/damage_numbers.json"
    keep = default_tuning.read_bytes()
    try:
        apply_preset(preset)
        out = known.out.resolve()
        out.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="wilds_build_") as temp:
            command = [sys.executable, "-m", "core", "--rom", str(known.rom.resolve()),
                       "--out", temp, *BASE_FLAGS]
            if known.code:
                command += ["--code", str(known.code.resolve())]
            command += extra          # anything else the caller asked for, the build decides
            print("build:", " ".join(command[2:]))
            run = subprocess.run(command, cwd=ROOT)
            if run.returncode != 0:
                fail("the build did not finish (its error is above)")
            built = Path(temp)
            files = check_output(built)
            final = place(built, out, title)
    finally:
        default_tuning.write_bytes(keep)

    # sizes from the placed folder: the temp build folder is gone by now
    placed = [final.joinpath(file.relative_to(built)) for file in files]
    size_mb = sum(file.stat().st_size for file in placed) / 1_000_000
    print(f"\ndone: {final}")
    for file in placed:
        print(f"  {file.relative_to(final)}  ({file.stat().st_size:,} bytes)")
    print(f"  ({size_mb:.1f} MB of mod files, built for the {region.upper()} game {title})")
    if known.zip:
        zip_path = make_zip(final, out, region)
        print(f"zip:  {zip_path}")
    print("\nnext: docs/INSTALL-4U-NATIVE.md - copy the folder into the port's mods and build the code library "
          "in the app; docs/INSTALL-AZAHAR.md - copy it into the emulator's load/mods.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
