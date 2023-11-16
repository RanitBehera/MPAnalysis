# User Manual

The module **MPAnalysis** helps analyze the output of **MP-Gadget** simulation in Python.

## Navigating Directory
The MP-Gadget simulation outputs snapshots at different times under folder names "PART_###" and "PIG_###" with the snapshot number as a suffix. Inside these snapshots, there are multiple folders for different kinds of particles. For example, Gas particles under folder "0", Dark matter particles under folder "1", etc. Inside these folders are various fields of interest like "Position", "Velocity", "ID" etc. These folders contain the values of the corresponding fields in binary format with a header file for details of the binary data.

While analyzing the data, we frequently need to navigate different folders and use their path to read the binary files. The `Navigate` module makes this navigation easy with a `folder.subfolder.field` syntax. It has the following advantages:
- The MP-Gadget output directory structure is set up in this module. Using dot notation, one can quickly look at different available fields from the displayed *IntelliSense* if supported by the code editor. No need to use a file browser or list directory command.
- Selecting different fields from displayed IntelliSense makes one type less and hence code fast.

### Setup "Navigate" module
To use the `Navigate` module, one must import it and provide the path of the output directory containing the "PART" and "PIG" folders as the base directory.

```python
import Navigate as mpn
op=mpn.BaseDirectory("C:\MP-Gadget\Simulation\output")
```
In Windows, you might need the raw string to provide the path as `r"C:\directory\path"` instead of just `"C:\directory\path"`.

### Use "Navigate" module
After one sets up the `Navigate` module with a base directory using `Navigate.BaseDirecory()`, it is easy to use it to navigate the output directory structure with the chained dot notation as `folder.subfolder.field` syntax.

- **Example 1:**<br> 
    If one wants the path to the "Position" field of the "DarkMatter" particle for the snapshot "PART_005":
    ```python
    import Navigate as mpn
    op=mpn.BaseDirectory("C:\MP-Gadget\Simulation\output")
    print(op.PART(5).DarkMatter.Position.path)
    ```
    Output
    ```batch
    C:\MP-Gadget\Simulation\output\PART_005\1\Position
    ```

- **Example 2:**<br> 
    If one wants the path to the "GroupID" field of the "FOFGroup" representative particle for the snapshot "PIG_012":
    ```python
    import modules.Navigate as mpn
    op=mpn.BaseDirectory("C:\MP-Gadget\Simulation\output")
    print(op.PIG(12).FOFGroups.GroupID.path)
    ```
    Output
    ```batch
    C:\MP-Gadget\Simulation\output\PIG_012\FOFGroups\GroupID
    ```

### Chained Dot Notation
- If the beginning of a chain is a capital letter, then it has further chains. Use the dot to access them.
- If the beginning of a chain is a small letter, it returns valuable information or data. You can still use dot notation to use primitive functions of Python on them.

Hence, always finish the chain with a small letter chain.


## Reading Files


## VS Code intellisense not working
Command palette > Open Workspace Settings (JSON) 
```json
{

    "python.analysis.extraPaths": [
        "/home/ranitbehera/MyDrive/Repos/MPAnalysis/"
    ],
    "python.autoComplete.extraPaths": [
        "/home/ranitbehera/MyDrive/Repos/MPAnalysis/"
    ]

}
```


## Open3D
To visualize particle distribution in box we use `open3d` package. install it with `pip install open3d`.

Note that while developing this module, the lastest version of `open3d` v0.17.0 has bugs. So we tested it for v0.16.0. install it using `pip install open3d==0.16`. However future versions of `open3d` might get fixed.

To use `open3d` in this module, you have to follow three steps in order.
1. Get a `Open3DWindow`
2. Add items.
3. Show the window.

The first step is done easily with
```python
win=mp.Open3DWindow()
```
which abstracts the open3d python interface which is itself an wrapper for open3d c++ implementation.

The last step is done with
```
win.show()
```
Note that this function internally destroyes the open3d window when closed. so you can not show the window again after closed. So design code accordingly. This design decision might get changed.

The intermidiate steps to add items is displayed in next section.




### Add Items
Currently you can add following items.
- PointCloud
- LineSet
- Mesh

#### Adding Point Cloud



### Interactive Key Bindings
This window has following key-bindings for interactive purpose.

- Default Key Bindings (provided by open3d Visualizer window)
  - Mouse view control:
    - Left button + drag         : Rotate.
    - Ctrl + left button + drag  : Translate.
    - Wheel button + drag        : Translate.
    - Shift + left button + drag : Roll.
    - Wheel                      : Zoom in/out.
  - Keyboard view control --
    - [/]                         : Increase/decrease field of view.
    - R                           : Reset view point.
    - Ctrl/Cmd + C                : Copy current view status into the clipboard.
    - Ctrl/Cmd + V                : Paste view status from clipboard.
  - General control --
    - Q, Esc       : Exit window.
    - H            : Print help message.
    - P, PrtScn    : Take a screen capture.
    - D            : Take a depth capture.
    - O            : Take a capture of current rendering settings.
- Extra Key Bindings (by registering to callback functions)
  - Keyboard view contrtols
    - Arrow Keys    : Translate (with forqard and backward capability which is not present in ) 