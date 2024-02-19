import galspec,os
from galspec.navigation.MPGADGET.Sim import _Sim
from galspec.IO.RockstarCFG import _RockstarCFG

class _Config:
    def __init__(self) -> None:
        self.SNAPSORT_DIRECTORY = ""
        self.READ_BINARY_USING  = ""
    

    def FromFile(self,path:str):
        # Get list of class members.
        class_members = list(vars(self).keys())

        # Read external congif file.
        with open(path) as cfg:text = cfg.read()

        # Get all lines.
        lines = text.split("\n")

        # For each line:
        for i in range(len(lines)):
            line = lines[i].strip()

            # Filter out blank lines and comments.
            if line=="" or line.startswith("#"): continue       

            # Form key-value pair.
            tokens  = line.split("=")
            key     = tokens[0].strip()
            value   = tokens[1].strip()

            # Cast to appropiate types
            # - String
            if value.startswith('"') and value.endswith('"'):
                value = str(value[1:-1])
            # - Integer : Not implemented
            # - Float : Not implemented


            # Set values by validating keys with class member list
            if key in class_members:setattr(self,key,value)

            
def NavigationRoot(path:str):
    if path=="":
        return _Sim(galspec.CONFIG.SNAPSORT_DIRECTORY)
    else:
        return _Sim(path)


def RockstarCFG(path:str):
    return _RockstarCFG(os.path.join(path,"rockstar.cfg"))