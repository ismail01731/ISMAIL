from app.plugins.plugin_loader import plugins


def find_plugin(message):

    message = message.lower()

    for plugin in plugins.values():

        for capability in plugin["capabilities"]:

            if capability.lower() in message:

                return plugin["name"]

    return "general"