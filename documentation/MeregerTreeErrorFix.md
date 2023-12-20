# Install sqlite3
While using mereger tree if following error comes
```
ModuleNotFoundError: No module named '_sqlite3'
```
While python build you find the same message as
```
The necessary bits to build these optional modules were not found:
_curses               _curses_panel         _tkinter           
nis                   readline              _sqlite3                   
To find the necessary bits, look in setup.py in detect_modules() for the module's name.
```

### Install sqlite as follows

1. Go to webpage https://www.sqlite.org/download.html
2. Download appropiate code. Here we use pre-release snapshot `sqlite-snapshot-202312141511.tar.gz`
    ```
    wget https://www.sqlite.org/snapshot/sqlite-snapshot-202312141511.tar.gz
    ```
3. Extract with `tar`
    ```
    tar -xzvf sqlite-snapshot-202312141511.tar.gz
    ```
4. Rrun `./configure --prefix="/home/user/.local"` and then `make`.
5. Find header file `sqlite3.h` and get path with `pwd`.
6. Find shared library `libsqlite3.so` in `.libs/libsqlite3.so`.
7. Run `make install` to copy it to `~/.local`.
8. Find header file `sqlite3.h` in `/home/user/.local/include`.
6. Find shared library `libsqlite3.so` in `/home/user/.local/lib`.

### Build Python with `_sqlite3` as follows.
1. In Python source package, open `setup.py`.
2. Serach for `def detect_sqlite()`.
3. In `sqlite_inc_paths=[...]` include `/home/user/.local/include`

Now python build shows
```
The necessary bits to build these optional modules were not found:
_curses               _curses_panel         _tkinter           
nis                   readline                                 
To find the necessary bits, look in setup.py in detect_modules() for the module's name.
```
Now `ete3` should no more show `_sqlite3` error.



### Error 2
If it show 
```
ImportError: cannot import name 'TreeStyle' from 'ete3'
```
install `PyQt5` as
```
pip install PyQt5
```
