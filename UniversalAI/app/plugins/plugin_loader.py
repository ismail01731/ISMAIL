import importlib
import pkgutil

plugins = {}


def load_plugins():

    import app.plugins

    for _, module_name, _ in pkgutil.iter_modules(app.plugins.__path__):

        if module_name in ["plugin_loader", "__init__"]:
            continue

        module = importlib.import_module(
            f"app.plugins.{module_name}"
        )

        if hasattr(module, "plugin"):

            plugins[module.plugin["name"]] = module.plugin


load_plugins()