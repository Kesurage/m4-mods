# Publishing this repository on GitHub

You publish this under your own account. Nothing here needs a token from a chat: create
one on GitHub only when the commands below ask for it, keep it in `gh`'s own storage, and
**revoke any token you have ever pasted into a chat** (https://github.com/settings/tokens
- if a token is in a conversation, treat it as leaked and delete it).

## 1. Create the repository

On https://github.com/new: name it `mh4u-wilds-damage`, description
"Monster Hunter Wilds' damage numbers, ported to MH4U - for the 4u-native Android port
and Azahar", public, **empty** (no README, no license: this folder has both).

## 2. Push this folder

```
cd mh4u-wilds-damage
git init
git add -A
git commit -m "MH4U Wilds Damage Numbers 1.0.0"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/mh4u-wilds-damage.git
git push -u origin main
```

Before pushing, one small edit so the repo is yours:

* `core/game/data/curated/edition.json`: replace `your-username/mh4u-wilds-damage` in
  `repository` with your real `user/repo` (it is only used for update checks; a wrong
  value is harmless but pointless).
* `docs/INSTALL-4U-NATIVE.md`: the `git clone` line, same replacement.

## 3. Make the release

```
gh auth login                      # or: export GH_TOKEN=... in the shell of THIS command only
gh release create v1.0.0 --title "MH4U Wilds Damage Numbers 1.0.0" --notes-from-tag
```

Or without `gh`: GitHub > your repo > **Releases** > **Draft a new release** > tag
`v1.0.0` > fill the notes > Publish. Suggested release notes:

> First release. Wilds-style damage numbers for MH4U: white / gold / grey by hit quality,
> the pink star for criticals, pop-rise-fade, stacking, poison and blast numbers, Show
> All Damage, three styles in the game's Mod Settings. Builds from your own game file for
> EUR/USA, base or update. Install: docs/INSTALL-4U-NATIVE.md (4u-native) or
> docs/INSTALL-AZAHAR.md.

Optionally attach a built example mod folder only if it is yours to attach — a build is
derived from your game file, so treat it like the game: the release page is cleaner
without it.

## 4. After publishing

* Re-check `edition.json`'s `repository` matches the real repo, so self-update checks
  point at your releases.
* Issues: point people at docs/COMPATIBILITY.md for "does it work with X".
* Screenshots: a short clip of a hunt with the numbers showing is the best README
  addition; capture it from your own game and drop it into the README's top.
