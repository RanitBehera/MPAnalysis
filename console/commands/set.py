
def main(args:list[str],env:dict):
    if "-b" in args:
        try:env["BOX"] = args[args.index("-b")+1]
        except:env["BOX"] = ""
    
    if "-s" in args:
        if env["BOX"]=="":
            print("Set a target box first")
            return
        try:env["SNAP"] = args[args.index("-s")+1]
        except:env["SNAP"] = ""

    if "-h" in args:
        if env["BOX"]=="":
            print("Set a target box first")
            return
        if env["SNAP"]=="":
            print("Set a target snap first")
            return
        try:env["HALO"] = args[args.index("-h")+1]
        except:env["HALO"] = ""