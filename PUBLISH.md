# Updating the published repository

This repository is published at https://github.com/Kesurage/m4-mods. To publish changes:

## Push new commits

```
git add -A && git commit -m "..." && git push
```

(Git will ask for credentials when you push; a fine-grained token with only
"Contents: read and write" on this repository is all the job needs.)

## Make a release

```
gh release create v1.x.y --title "MH4U Wilds Damage Numbers 1.x.y" --notes "..."
```

or Releases > Draft a new release > tag `v1.x.y` > notes > Publish. Bump
`core/__init__.py`'s `__version__` and CHANGELOG.md in the same commit.

## What not to attach to a release

Do **not** upload a built mod folder (`exefs/code.bin`) as a release asset: it is derived
from your own game file — distributing it publicly is distributing game code. The
community-standard alternative is a patch form (like code.ips), which this build
deliberately does not produce (the port's own loader guidance prefers the whole
executable, built per player). The builder is one command for anyone who wants the mod.

## If you ever need a new token

Create it at https://github.com/settings/tokens (fine-grained, this repository only),
and never paste it into a chat or a file: a token that has been in a conversation must
be treated as leaked and revoked.
