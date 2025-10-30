import pkgutil
import importlib

package_name = __name__
# Dynamically import all repository modules in the current package
for _, module_name, is_pkg in pkgutil.iter_modules(__path__):
    if not is_pkg:
        full_module_name = f"{package_name}.{module_name}"
        importlib.import_module(full_module_name)