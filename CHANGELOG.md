# MH4U Wilds Damage Numbers

## 1.0.1

- The builder accepts the game's **update** file directly (title id `0004000e00126300`
  and friends): the region resolver maps update titles to their base's region, and the
  build says which version it built from (`built from usa_update`).
- Fixed the builder's crash after a successful build (it summed the files' sizes after
  its own temp folder was deleted); sizes now come from the placed folder.
- docs/TROUBLESHOOTING.md: the "installed but nothing appears" case, read from a real
  phone log — a source zip imported as a mod (no `exefs/`, so no code library entry)
  looks exactly like a silent no-op; the checklist matches the port's log lines.
- README: the repository-is-the-builder warning up front.

## 1.0.0

First release: the Wilds damage numbers for MH4U, as a focused distribution of
Heavenfall Beta's damage numbers system (GPL-3.0-or-later, credited), retuned and
repackaged for the 4u-native Android port and Azahar.
