import galspec
from galspec.snapshot.Sim import _Sim

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

            
def NavigationRoot():
    return _Sim(galspec.CONFIG.SNAPSORT_DIRECTORY)