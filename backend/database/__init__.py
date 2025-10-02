import os
import importlib
from sqlalchemy.orm import declarative_base

models_folder = os.path.dirname(__file__)

for filename in os.listdir(models_folder):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = f"{__name__}.{filename[:-3]}"
        importlib.import_module(module_name)