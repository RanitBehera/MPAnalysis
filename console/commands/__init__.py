# from .avail import *
# from .set import *

# import commands.avail
# import commands.set
# import commands.rockstar.halo
# import commands.rockstar.varun
# import commands.rockstar.anirban

# from commands.rockstar import *

from importlib import import_module

module_names = ['avail', 'set']

for mname in module_names:
    import_module("commands."+mname)

