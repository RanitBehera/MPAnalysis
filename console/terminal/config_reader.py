
def get_config_value(config_file_path:str,key_name:str):
    # Read external congif file.
    with open(config_file_path) as cfg:text = cfg.read()

    # Get all lines.
    lines = text.split("\n")

    