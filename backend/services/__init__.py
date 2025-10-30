import importlib
import pkgutil

package = __name__

for module_info in pkgutil.walk_packages(__path__, prefix=f"{package}."):
    if not module_info.ispkg:
        importlib.import_module(module_info.name)