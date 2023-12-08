# Module Design Structure

### Chained Notation

### Default Argument values
- Files for specific pupose like cube, rockstar.
- Unless special, these files should not have default argument values.

- Navigate File is to navigate the Folder structure for data files.
- This Navigate file should also take input from user and redirect it to corresponding code unit in corresponding folder.
- Default values should be in this navigate file, so that it is easier to track later.

- So structure is One root Navigate which has one further redirectin to corresponding code files.
- So the module structure has at most depth 2.