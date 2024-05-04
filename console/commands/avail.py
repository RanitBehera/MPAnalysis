import os

def get_available_boxes(boxbank_dir):
    files       = [f for f in os.listdir(boxbank_dir) if os.path.isfile(os.path.join(boxbank_dir, f))]
    boxfiles    = [f for f in files if f.endswith(".box")]
    box_list    = [f.split(".box")[0] for f in boxfiles]
    return box_list


def main(args:list[str],env:dict):
    if "-b" in args:
        boxes = get_available_boxes(env["BOXBANK_DIR"])
        [print(box,end="\t") for box in boxes]
        print("")
        