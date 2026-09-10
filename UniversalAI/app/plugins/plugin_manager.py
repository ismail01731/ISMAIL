from app.plugins.plugin_loader import plugins


async def execute(plugin_name, message):

    plugin = plugins.get(plugin_name)

    if plugin is None:
        plugin = plugins.get("general")

    return await plugin["run"](message)