import os
import importlib

model_dir = os.path.dirname(__file__)

for filename in os.listdir(model_dir):
    if filename.endswith(".py") and filename != "__init__.py" and filename != "BaseClass.py":
        module_name = f"{__name__}.{filename[:-3]}"
        importlib.import_module(module_name)