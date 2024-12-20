# meshstats

[Blender](https://www.blender.org/) addon that provides topological statistics
for meshes.

meshstats is released with [GPL license](./COPYING.txt), same as [Blender](https://www.blender.org/about/license/)

## Features

- Display counts for tris, quads & ngons.
- Display counts for e-poles (vertices connecting 5 edges), n-poles (vertices
  connecting 3 edges) and *-poles (vertices connecting 6 or more edges - fan
  center).
- Set a polygon budget for mesh objects and display how much of it is
  utilized.
- Highlight tris & ngons in the viewport. (in object mode only)
- Highlight e-poles, n-poles & *-poles in the viewport. (in object mode only)

See [CHANGELOG.md](./CHANGELOG.md) for release details.

## Installation

- Download the source zip [from releases
  page](https://github.com/muhuk/meshstats/releases).  You need to click to
  expand `Assets` under the correct version and download the file named
  `meshstats-#.#.zip` (where #.# is the version number).
- In Blender, open `Preferences` editor (`Edit -> Preferences`
  from the menu).
- Click `Install...` button and choose the zip file you have downloaded.
- Once the addon is installed, you **must** still enable it manually in
  `Preferences` view.  It is not automatically enabled.
- After installation, you can delete the zip file you have downloaded.

### Minimum Required Blender Versions

| Meshstats version | Blender version |
|-------------------|-----------------|
| 1.0 - 1.2         | 2.91            |
| 1.3               | 3.6.2           |

## Usage

Once you have enabled the addon, you should see a `Meshstats` panel under
`Item` tab in 3D view sidebar (default shortcut is `N`).

### How to View Face Counts

1. Select a mesh object.
2. You must be in `Object Mode`.
3. Open `3D Viewport`'s sidebar, `Item` tab.
4. If `disabled_by_default` is active in addon preferences you need to click
   `Enable` button in `Meshtats` panel.

![how_to_view_face_counts.png](./img/how_to_view_face_counts.png)

Note that even if you enable Meshtats for an object, if the mesh contains too
many faces (configurable in addon preferences) or modifiers that change
topology are active you won't see stats or overlays.

### How to Display Tri & Ngon Overlays

1. Overlays must be enabled.
2. Overlay options can be found in `Overlay` pop-up as well as in `Meshstats`
   panel.

![how_to_enable_overlays.png](./img/how_to_enable_overlays.png)

### How to Set Up a Face Budget

1. Select a mesh object.
2. You must be in `Object Mode`.
3. Open `3D Viewport`'s sidebar, `Item` tab.

![how_to_set_face_budget.png](./img/how_to_set_face_budget.png)
