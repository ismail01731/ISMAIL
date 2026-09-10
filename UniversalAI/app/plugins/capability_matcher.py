from app.plugins.plugin_loader import plugins


def find_plugin(message):

    message = message.lower()

    for plugin in plugins.values():

        for capability in plugin["capabilities"]:

            if capability.lower() in message:
                return plugin["name"]

    return "general"


def find_plugins(message):

    message = message.lower()

    matched = []

    for plugin in plugins.values():

        for capability in plugin["capabilities"]:

            if capability.lower() in message:

                if plugin["name"] not in matched:
                    matched.append(plugin["name"])

                break

    if not matched:
        matched.append("general")

    return matched