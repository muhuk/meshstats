# Changelog

## [Unreleased]

## [0.3] - 2020-05-24

### Added

- Display poles in overlay.  You can enable this overlay in `Item ->
  Meshstats` panel in 3D view.
- Display pole statistics (below face statistics).
- Added factory defaults for overlay colors.  Click `Reset Meshstats settings`
  button in addon preferences to return to factory defaults.
- Overlay settings are now also available in overlay pop-over.

### Changed

- Meshstats overlays are only visible if viewport overlays are enabled.
- Overlay colors are configured at addon level, not at scene level.

### Removed

- Changing of overlay colors is removed from 3D view panel.

## [0.2] - 2020-02-01

### Added
- Face budgets per mesh.  There are three algorithms for calculating face
  budget utilization.  `Tris` calculates utilization based on the
  triangulation of the mesh.  `Quads Only` disregards tris & ngons and counts
  only quads.  `Faces` counts each tri, quad and ngon as one.
- Customization of colors (with alpha) in overlay.

### Fixed
- Fixed visibility check for ngons.  When face center was not on the surface
  (when vertices are not co-planar) visibility check was always returning
  `False`.  Fix involves projecting the calculated center onto the mesh and
  using that as the ngon center.

## [0.1] - 2020-01-04

![screenshot_v0.1_1.jpeg](./img/screenshot_v0.1_1.jpeg)

### Added
- Display basic face statistics inside `Item -> Meshstats` panel in 3D view.
- Diplay in 3D view and overlay where tris & quads are outlined.
- Allow enabling & disabling the overlay.  This setting is saved with the
  scene.

[Unreleased]: https://github.com/muhuk/meshstats/compare/v0.3...HEAD
[0.3]: https://github.com/muhuk/meshstats/compare/v0.2...v0.3
[0.2]: https://github.com/muhuk/meshstats/compare/v0.1...v0.2
[0.1]: https://github.com/muhuk/meshstats/releases/tag/v0.1
