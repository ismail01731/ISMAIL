from app.memory.session import memory


def save_user(message):
    memory.add("user", message)


def save_assistant(message):
    memory.add("assistant", message)


def get_history():
    return memory.history()