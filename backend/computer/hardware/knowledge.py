# =========================================================
# ISMAIL AI - HARDWARE KNOWLEDGE CORE
# TASK 2
# =========================================================
HARDWARE_KNOWLEDGE = {
    "cpu": {
        "name": "CPU",
        "keywords": ["cpu", "processor", "core", "cores", "thread", "threads", "clock speed"],
        "definition": "CPU (Central Processing Unit) is the main processor of a computer. It executes instructions and performs general-purpose calculations.",
        "details": "CPU performance can depend on factors such as cores, threads, clock speed, cache, architecture, and workload."
    },
    "ram": {
        "name": "RAM",
        "keywords": ["ram", "memory", "ddr", "ddr4", "ddr5", "memory usage"],
        "definition": "RAM (Random Access Memory) is temporary working memory used by the computer to store data and instructions that are actively being used.",
        "details": "More RAM can allow a computer to handle more applications and larger workloads simultaneously. RAM is volatile, so its contents are normally lost when power is removed."
    },
    "gpu": {
        "name": "GPU",
        "keywords": ["gpu", "graphics card", "graphics", "vram", "graphics processor"],
        "definition": "GPU (Graphics Processing Unit) is specialized hardware designed for graphics processing and highly parallel computations.",
        "details": "A GPU may be integrated into a processor or provided as a dedicated graphics card. Dedicated GPUs commonly have their own VRAM."
    },
    "storage": {
        "name": "Storage",
        "keywords": ["storage", "hdd", "ssd", "nvme", "sata ssd", "hard drive", "solid state drive"],
        "definition": "Computer storage permanently stores files, applications, operating system data, and other information.",
        "details": "Common storage technologies include HDD, SATA SSD, and NVMe SSD. SSDs generally provide much faster access than traditional HDDs."
    },
    "motherboard": {
        "name": "Motherboard",
        "keywords": ["motherboard", "mainboard", "system board"],
        "definition": "The motherboard is the main circuit board that connects the CPU, RAM, storage, GPU, and other hardware components.",
        "details": "It provides communication paths, connectors, expansion slots, power connections, and interfaces for computer components."
    },
    "psu": {
        "name": "PSU",
        "keywords": ["psu", "power supply", "power supply unit", "wattage"],
        "definition": "PSU (Power Supply Unit) converts electrical power from the wall into usable power for computer components.",
        "details": "A PSU must provide suitable power capacity and compatible connectors for the computer hardware."
    },
    "cooling": {
        "name": "Cooling",
        "keywords": ["cooling", "cpu cooler", "fan", "heatsink", "temperature", "thermal"],
        "definition": "Computer cooling removes heat produced by components such as the CPU and GPU.",
        "details": "Cooling systems can use heatsinks, fans, thermal interface material, or liquid cooling."
    },
    "monitor": {
        "name": "Monitor",
        "keywords": ["monitor", "display", "screen", "refresh rate", "resolution"],
        "definition": "A monitor is an output device that displays visual information from a computer.",
        "details": "Important monitor characteristics include resolution, refresh rate, panel technology, size, brightness, and response time."
    },
    "keyboard": {
        "name": "Keyboard",
        "keywords": ["keyboard", "key", "keys", "typing"],
        "definition": "A keyboard is an input device used to enter text, commands, shortcuts, and other instructions into a computer."
    },
    "mouse": {
        "name": "Mouse",
        "keywords": ["mouse", "cursor", "click", "pointer"],
        "definition": "A mouse is a pointing input device used to move the cursor and interact with graphical interfaces."
    },
    "usb": {
        "name": "USB",
        "keywords": ["usb", "usb-a", "usb-c", "usb 2", "usb 3"],
        "definition": "USB (Universal Serial Bus) is a standard used to connect devices and transfer data and power.",
        "details": "Different USB versions and connector types can support different data-transfer speeds and power capabilities."
    },
    "hdmi": {
        "name": "HDMI",
        "keywords": ["hdmi", "hdmi cable", "display cable"],
        "definition": "HDMI (High-Definition Multimedia Interface) is a digital interface commonly used to transmit video and audio between compatible devices."
    },
    "bluetooth": {
        "name": "Bluetooth",
        "keywords": ["bluetooth", "wireless peripheral"],
        "definition": "Bluetooth is a short-range wireless technology commonly used to connect peripherals such as keyboards, mice, headphones, and other devices."
    }
}
def get_hardware_knowledge():
    return HARDWARE_KNOWLEDGE
def search_hardware_knowledge(query: str):
    query_lower = query.lower().strip()
    if not query_lower:
        return []
    results = []
    for topic, data in HARDWARE_KNOWLEDGE.items():
        score = 0
        if topic in query_lower:
            score += 5
        for keyword in data.get("keywords", []):
            if keyword.lower() in query_lower:
                score += 2
        if data["name"].lower() in query_lower:
            score += 3
        if score > 0:
            results.append({
                "topic": topic,
                "name": data["name"],
                "definition": data["definition"],
                "details": data.get("details", ""),
                "score": score,
            })
    results.sort(key=lambda item: item["score"], reverse=True)
    return results
