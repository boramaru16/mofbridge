# Blender MOF Bridge

Unwrap your objects with MINISTRY OF FLAT. Hail Ministry of Flat, your flatness!!!

This Blender addon integrates Ministry of Flat (MOF) UV unwrapping tool into Blender, allowing automatic UV unwrapping of selected objects.

## Features

- Automatic UV unwrapping using Ministry of Flat
- Option to separate hard edges
- Automatic UV packing after unwrapping
- Switch to UV edit mode after completion
- Sidebar panel for easy access

## Requirements

- Blender 2.80 or later
- Ministry of Flat installed on your system

## Installation

1. Download the `mofbridge.py` file
2. In Blender, go to Edit > Preferences > Add-ons
3. Click "Install..." and select the `mofbridge.py` file
4. Enable the addon "Blender MOF Bridge"
5. In the addon preferences, set the path to the folder containing `UnWrapConsole3.exe` from Ministry of Flat

## Usage

1. Select the objects you want to unwrap
2. In the 3D Viewport, go to the "MOF Bridge" tab in the sidebar (N key)
3. Click "Unwrap in Ministry of Flat"
4. Or use Object > Unwrap in Ministry of Flat from the menu

## Configuration

In the addon preferences (Edit > Preferences > Add-ons > Blender MOF Bridge):

- **MOF folder**: Path to the folder containing Ministry of Flat executable
- **Separate edges**: Guarantees that all hard edges are separated (useful for lightmapping and normal mapping)
- **Pack after unwrap**: Automatically pack UV islands in Blender
- **Show UV when done**: Switch to edit mode and show UV editor after unwrapping

## License

This addon is released under the same license as the original mofbridge by rentanek0.

## Credits

- Original author: rentanek0
- Ministry of Flat: https://www.quelsolaar.com/ministry_of_flat/
- Repository: https://github.com/garanovich/mofbridge/


---

## Addon Settings

The addon provides several settings to customize its behavior:

### `MOF folder`
- **Description**: The path to the folder containing the Ministry of Flat executable (`UnWrapConsole3.exe`).
- **Purpose**: Specifies where the addon should look for the Ministry of Flat tool.

### `Separate edges`
- **Description**: Guarantees that all hard edges are separated. Useful for lightmapping and normal mapping.
- **Default**: `True`
- **Purpose**: Ensures clean UV seams for specific use cases like baking.

### `Pack after unwrap`
- **Description**: Automatically packs UV islands after unwrapping. This uses Blender's built-in UV packing functionality.
- **Default**: `True`
- **Purpose**: Optimizes UV space usage by packing the islands efficiently.

### `Show UV when done`
- **Description**: Switches to UV editing mode after the process is complete.
- **Default**: `True`
- **Purpose**: Allows you to immediately inspect the UV maps in the UV Editor.

---

## Workflow

1. **Export**: The selected objects are exported to a temporary `.obj` file.
2. **Unwrap**: Ministry of Flat processes the `.obj` file and generates a new file with unwrapped UVs.
3. **Import**: The unwrapped objects are imported back into Blender.
4. **Copy UVs**: The UV maps from the imported objects are copied to the original objects.
5. **Cleanup**: Temporary files and imported objects are removed.

---

## Notes

- **Ministry of Flat**: This addon relies on the Ministry of Flat tool, which must be downloaded and installed separately from [https://www.quelsolaar.com/ministry_of_flat/](https://www.quelsolaar.com/ministry_of_flat/).
- **Blender Compatibility**: The addon is designed for Blender 2.80 and above.
- **Feedback**: For questions or feedback, contact me on X (formerly Twitter): [@rentaneko3d](https://x.com/rentaneko3d).

---

## Credits

- **Ministry of Flat**: Developed by [Quel Solaar](https://www.quelsolaar.com/).
- **Inspiration**: The initial version for this addon was written in the article [https://techracho.bpsinc.jp/ecn/2024_08_22/144348](https://techracho.bpsinc.jp/ecn/2024_08_22/144348).
- **Developer**: [@rentaneko3d](https://x.com/rentaneko3d).

Make The Earth Flat Again.
---

## License

This addon is provided under the MIT License. Feel free to modify and distribute it as needed.
