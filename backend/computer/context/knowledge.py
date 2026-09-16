# =========================================================
# ISMAIL AI - COMPUTER CONTEXT KNOWLEDGE CORE
# TASK 10A
# =========================================================
COMPUTER_CONTEXT_KNOWLEDGE = [
    {
        "name": "computer_performance",
        "keywords": [
            "computer slow",
            "slow computer",
            "performance",
            "pc slow",
            "system slow",
            "very slow",
            "extremely slow"
        ],
        "definition": "Computer performance context describes situations where the system responds slowly or performs below expectations.",
        "domains": ["cpu", "ram", "storage", "process", "startup", "thermal"]
    },
    {
        "name": "cpu_context",
        "keywords": [
            "cpu",
            "processor",
            "cpu usage",
            "processor usage",
            "high cpu"
        ],
        "definition": "CPU context concerns processor workload, utilization, performance, temperature, and running tasks.",
        "domains": ["hardware", "process", "performance", "thermal"]
    },
    {
        "name": "memory_context",
        "keywords": [
            "ram",
            "memory",
            "memory usage",
            "high memory",
            "low memory"
        ],
        "definition": "Memory context concerns RAM availability, memory usage, applications consuming memory, and system responsiveness.",
        "domains": ["hardware", "process", "performance"]
    },
    {
        "name": "storage_context",
        "keywords": [
            "disk",
            "storage",
            "disk space",
            "low disk space",
            "hard drive",
            "ssd"
        ],
        "definition": "Storage context concerns available disk space, storage devices, disk activity, and storage performance.",
        "domains": ["hardware", "files", "performance"]
    },
    {
        "name": "network_context",
        "keywords": [
            "internet",
            "network",
            "wifi",
            "wi-fi",
            "ethernet",
            "connection",
            "online",
            "offline"
        ],
        "definition": "Network context concerns internet connectivity, local network connectivity, adapters, DNS, Wi-Fi, Ethernet, and related services.",
        "domains": ["network", "dns", "wifi", "ethernet", "firewall"]
    },
    {
        "name": "application_context",
        "keywords": [
            "application",
            "app",
            "software",
            "program",
            "application not opening",
            "app crashing",
            "program crashing"
        ],
        "definition": "Application context concerns software execution, application errors, crashes, startup, and compatibility.",
        "domains": ["software", "process", "files", "permissions"]
    },
    {
        "name": "file_context",
        "keywords": [
            "file",
            "folder",
            "directory",
            "file path",
            "folder path",
            "document"
        ],
        "definition": "File context concerns files, folders, paths, file types, storage locations, and file operations.",
        "domains": ["files", "storage", "permissions"]
    },
    {
        "name": "system_context",
        "keywords": [
            "system",
            "operating system",
            "windows",
            "linux",
            "system settings",
            "system information"
        ],
        "definition": "System context concerns the operating system, system configuration, system information, services, and system state.",
        "domains": ["os", "process", "hardware", "software"]
    },
    {
        "name": "boot_context",
        "keywords": [
            "boot",
            "startup",
            "start up",
            "computer not booting",
            "booting",
            "startup problem"
        ],
        "definition": "Boot context concerns the sequence and components involved in starting the computer and loading the operating system.",
        "domains": ["os", "hardware", "bios", "uefi", "storage"]
    },
    {
        "name": "thermal_context",
        "keywords": [
            "temperature",
            "overheating",
            "hot computer",
            "cpu temperature",
            "gpu temperature",
            "thermal"
        ],
        "definition": "Thermal context concerns computer temperature, cooling, overheating, thermal throttling, and heat-related performance issues.",
        "domains": ["cpu", "gpu", "cooling", "hardware"]
    },
    {
        "name": "device_context",
        "keywords": [
            "keyboard",
            "mouse",
            "printer",
            "monitor",
            "screen",
            "usb device",
            "device"
        ],
        "definition": "Device context concerns physical peripherals and their connection, detection, drivers, and operation.",
        "domains": ["hardware", "driver", "usb", "software"]
    },
    {
        "name": "security_context",
        "keywords": [
            "security",
            "antivirus",
            "firewall",
            "permission",
            "permissions",
            "access denied",
            "blocked",
            "firewall blocking",
            "security blocking"
        ],
        "definition": "Security context concerns permissions, access control, antivirus, firewall rules, and security restrictions.",
        "domains": ["os", "network", "software", "permissions"]
    },
    {
        "name": "user_context",
        "keywords": [
            "user account",
            "account",
            "administrator",
            "admin",
            "login",
            "sign in"
        ],
        "definition": "User context concerns the current user account, authentication, administrator privileges, and account-specific configuration.",
        "domains": ["os", "permissions", "security"]
    },
    {
        "name": "system_resource_context",
        "keywords": [
            "resource",
            "system resources",
            "cpu ram disk",
            "cpu ram and disk",
            "cpu ram disk usage",
            "resource usage",
            "resource consumption"
        ],
        "definition": "System resource context concerns CPU, memory, storage, processes, and other resources being consumed by the system.",
        "domains": ["cpu", "ram", "storage", "process"]
    },
    {
        "name": "error_context",
        "keywords": [
            "error",
            "error message",
            "failed",
            "failure",
            "crash",
            "problem",
            "issue"
        ],
        "definition": "Error context concerns failures, error messages, crashes, unexpected behavior, and diagnostic information.",
        "domains": ["troubleshooting", "software", "os", "hardware", "network"]
    }
]
def get_computer_context_knowledge():
    return COMPUTER_CONTEXT_KNOWLEDGE
def search_computer_context(query):
    if not query:
        return []
    text = str(query).strip().lower()
    # Normalize common punctuation.
    normalized = (
        text
        .replace("-", " ")
        .replace("_", " ")
        .replace(",", " ")
        .replace(".", " ")
        .replace(":", " ")
        .replace(";", " ")
    )
    words = set(normalized.split())
    matches = []
    for index, item in enumerate(COMPUTER_CONTEXT_KNOWLEDGE):
        best_score = 0
        best_keyword = None
        for keyword in item["keywords"]:
            keyword_lower = keyword.lower().strip()
            if not keyword_lower:
                continue
            keyword_normalized = (
                keyword_lower
                .replace("-", " ")
                .replace("_", " ")
            )
            keyword_words = keyword_normalized.split()
            score = 0
            # Single-word keywords must match a complete
            # token. This prevents "system" from matching
            # "System32".
            if len(keyword_words) == 1:
                if keyword_normalized in words:
                    score = 5
            else:
                # Multi-word keywords may match as a phrase.
                if keyword_normalized in normalized:
                    score = len(keyword_words) * 10
                else:
                    matched_words = sum(
                        1
                        for word in keyword_words
                        if word in words
                    )
                    if matched_words == len(keyword_words):
                        score = len(keyword_words) * 7
            if score > best_score:
                best_score = score
                best_keyword = keyword_lower
        if best_score > 0:
            matches.append(
                (
                    best_score,
                    len(best_keyword or ""),
                    index,
                    item
                )
            )
    # Higher semantic score first.
    # Longer keyword wins when scores are equal.
    # Original order is the final tie-breaker.
    matches.sort(
        key=lambda x: (x[0], x[1], -x[2]),
        reverse=True
    )
    return [item for _, _, _, item in matches]
