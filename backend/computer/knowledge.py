"""
ISMAIL AI
Computer Knowledge Core

TASK 1:
Basic computer knowledge and concepts.
"""


COMPUTER_KNOWLEDGE = {

    "computer": {
        "name": "Computer",
        "category": "basic",
        "definition": (
            "A computer is an electronic system that accepts input, "
            "processes data, stores information, and produces output."
        ),
        "keywords": [
            "computer",
            "কম্পিউটার",
            "কম্পিউটার কী",
            "what is a computer",
        ],
    },

    "cpu": {
        "name": "CPU",
        "category": "hardware",
        "definition": (
            "CPU stands for Central Processing Unit. "
            "It executes instructions and performs calculations "
            "for computer programs."
        ),
        "keywords": [
            "cpu",
            "processor",
            "প্রসেসর",
            "cpu কী",
            "processor কী",
        ],
    },

    "ram": {
        "name": "RAM",
        "category": "hardware",
        "definition": (
            "RAM stands for Random Access Memory. "
            "It temporarily stores data and instructions that "
            "the computer is actively using."
        ),
        "keywords": [
            "ram",
            "র‍্যাম",
            "ram কী",
            "memory",
        ],
    },

    "storage": {
        "name": "Storage",
        "category": "hardware",
        "definition": (
            "Computer storage is used to permanently store "
            "files, programs, operating system data, and other information."
        ),
        "keywords": [
            "storage",
            "স্টোরেজ",
            "hard disk",
            "ssd",
            "hdd",
            "disk",
        ],
    },

    "gpu": {
        "name": "GPU",
        "category": "hardware",
        "definition": (
            "GPU stands for Graphics Processing Unit. "
            "It is specialized hardware used for graphics processing "
            "and highly parallel computations."
        ),
        "keywords": [
            "gpu",
            "graphics card",
            "গ্রাফিক্স কার্ড",
            "gpu কী",
        ],
    },

    "operating_system": {
        "name": "Operating System",
        "category": "software",
        "definition": (
            "An operating system is system software that manages "
            "computer hardware, software resources, files, processes, "
            "and provides services for applications."
        ),
        "keywords": [
            "operating system",
            "os",
            "অপারেটিং সিস্টেম",
            "windows",
            "linux",
            "macos",
        ],
    },

    "file": {
        "name": "File",
        "category": "data",
        "definition": (
            "A file is a named unit of data stored on a computer. "
            "Examples include documents, images, videos, programs, "
            "and configuration files."
        ),
        "keywords": [
            "file",
            "ফাইল",
            "file কী",
        ],
    },

    "folder": {
        "name": "Folder",
        "category": "data",
        "definition": (
            "A folder is a container used to organize files and "
            "other folders on a computer."
        ),
        "keywords": [
            "folder",
            "ফোল্ডার",
            "directory",
            "ডিরেক্টরি",
        ],
    },

    "application": {
        "name": "Application",
        "category": "software",
        "definition": (
            "An application is software designed to perform "
            "specific tasks for a user."
        ),
        "keywords": [
            "application",
            "app",
            "software",
            "অ্যাপ",
            "সফটওয়্যার",
        ],
    },

}


def get_computer_knowledge(topic: str):
    """
    Return computer knowledge for a known topic.
    """

    if not topic:
        return None

    text = topic.strip().lower()

    for key, item in COMPUTER_KNOWLEDGE.items():

        if text == key:
            return item

        for keyword in item["keywords"]:
            if text == keyword.lower():
                return item

    return None


def search_computer_knowledge(query: str):
    """
    Search the Computer Knowledge Core using keywords.
    """

    if not query:
        return []

    text = query.strip().lower()
    results = []

    for key, item in COMPUTER_KNOWLEDGE.items():

        score = 0

        if key.lower() in text:
            score += 3

        for keyword in item["keywords"]:
            if keyword.lower() in text:
                score += 2

        if score > 0:
            results.append({
                "topic": key,
                "name": item["name"],
                "category": item["category"],
                "definition": item["definition"],
                "score": score,
            })

    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return results