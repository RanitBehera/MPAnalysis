
class _Config:
    def __init__(self) -> None:
            self.SetUserConfig()

    def SetUserConfig(self):
        self.MPGADGET_OUTPUT_DIR    = "/home/ranitbehera/MyDrive/Data/MP-Gadget/L10N64" # Remove last '/' if input by validation
        # self.MPGADGET_OUTPUT_DIR    = "/home/ranitbehera/MyDrive/Data/MP-Gadget/L50N640" # Remove last '/' if input by validation
        self.READ_FIELD_WITH        = "numpy"   # numpy, bigfile
    
    def SetConfigFromFile(self,filename:str):
        pass

    # def GetTemplateConfig(self,dirpath:str):
        # members = [attr for attr in dir(_Config) if not callable(getattr(example, attr)) and not attr.startswith("__")]
        # print(dir(_Config))
        # pass



from galspec.mpgadget.Sim import _Sim
import galspec
def InitConfig():
    # Make it to work from a file,
    # and my be from dir path
    # or default
    sim = _Sim(galspec.CONFIG.MPGADGET_OUTPUT_DIR)
    return sim
