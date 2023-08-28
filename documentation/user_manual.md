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

