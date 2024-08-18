import os
import json
from options import TtetlOptions


def get_config(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            custom_options = json.load(f)

        return TtetlOptions(custom_options, source=path)

    return TtetlOptions()
