PROCESS_SYSTEM_KNOWLEDGE = [
    {
        "name": "process",
        "keywords": ["computer process", "system process", "process", "প্রসেস"],
        "definition": "A process is a running instance of a program.",
        "details": "A process has its own execution state and may use CPU, memory, files, network connections, and other system resources."
    },
    {
        "name": "pid",
        "keywords": ["process id", "process identifier", "pid", "প্রসেস আইডি"],
        "definition": "A Process ID, or PID, is a unique numeric identifier assigned to a running process.",
        "details": "Operating systems use PIDs to identify and manage individual processes."
    },
    {
        "name": "cpu_usage",
        "keywords": ["cpu usage", "processor usage", "cpu utilization", "সিপিইউ ব্যবহার"],
        "definition": "CPU usage represents how much of the processor's available computing capacity is being used.",
        "details": "High CPU usage can occur when applications or system processes are performing intensive computations."
    },
    {
        "name": "memory_usage",
        "keywords": ["memory usage", "ram usage", "memory utilization", "মেমোরি ব্যবহার"],
        "definition": "Memory usage represents how much system RAM is currently being used.",
        "details": "Applications and operating system processes consume RAM while they are running."
    },
    {
        "name": "system_memory",
        "keywords": ["system memory", "physical memory", "ram memory", "সিস্টেম মেমোরি"],
        "definition": "System memory generally refers to the computer's main RAM used by the operating system and applications.",
        "details": "Available system memory affects how many programs can run efficiently at the same time."
    },
    {
        "name": "disk_usage",
        "keywords": ["disk usage", "disk space usage", "storage usage", "ডিস্ক ব্যবহার"],
        "definition": "Disk usage describes how much storage space is currently occupied on a storage device or filesystem.",
        "details": "Disk usage can be monitored to identify low-storage conditions and large files or directories."
    },
    {
        "name": "system_uptime",
        "keywords": ["system uptime", "computer uptime", "uptime", "সিস্টেম আপটাইম"],
        "definition": "System uptime is the amount of time a computer has been running since its last boot or restart.",
        "details": "Uptime can help determine how long a system has remained continuously active."
    },
    {
        "name": "running_process",
        "keywords": ["running process", "active process", "চলমান প্রসেস"],
        "definition": "A running process is a program instance that is currently executing or scheduled to execute.",
        "details": "Operating systems maintain lists of running processes and their resource usage."
    },
    {
        "name": "background_process",
        "keywords": ["background process", "background task", "ব্যাকগ্রাউন্ড প্রসেস"],
        "definition": "A background process runs without requiring continuous direct interaction from the user.",
        "details": "Background processes may perform synchronization, updates, services, monitoring, or other tasks."
    },
    {
        "name": "service",
        "keywords": ["system service", "computer service", "service", "সিস্টেম সার্ভিস"],
        "definition": "A system service is a background software component that provides functionality to the operating system or applications.",
        "details": "Services can often start automatically and run without a visible user interface."
    },
    {
        "name": "windows_service",
        "keywords": ["windows service", "windows services", "উইন্ডোজ সার্ভিস"],
        "definition": "A Windows service is a background process managed by the Windows Service Control Manager.",
        "details": "Windows services can be configured to start automatically, manually, or under specific conditions."
    },
    {
        "name": "task_manager",
        "keywords": ["task manager", "windows task manager", "টাস্ক ম্যানেজার"],
        "definition": "Task Manager is a Windows system utility used to view and manage running applications, processes, performance, and services.",
        "details": "It can display CPU, memory, disk, network usage, process IDs, and other system information."
    },
    {
        "name": "system_information",
        "keywords": ["system information", "system info", "computer information", "সিস্টেম ইনফরমেশন"],
        "definition": "System information is a collection of details describing a computer's hardware, operating system, and configuration.",
        "details": "It can include the operating system version, processor, memory, architecture, hostname, and other configuration data."
    },
    {
        "name": "hostname",
        "keywords": ["computer hostname", "system hostname", "hostname", "host name", "কম্পিউটার নাম"],
        "definition": "A hostname is a name assigned to a computer or networked device for identification.",
        "details": "Hostnames can be used to identify systems on networks and in system administration."
    },
    {
        "name": "system_architecture",
        "keywords": ["system architecture", "cpu architecture", "computer architecture", "সিস্টেম আর্কিটেকচার"],
        "definition": "System architecture describes the processor and operating environment architecture of a computer.",
        "details": "Common architectures include x86, x64, ARM32, and ARM64."
    },
    {
        "name": "system_environment",
        "keywords": ["system environment", "computer environment", "environment", "সিস্টেম এনভায়রনমেন্ট", "সিস্টেম এনভায়রনমেন্ট"],
        "definition": "The system environment is the collection of configuration values, variables, services, and runtime conditions available to software on a computer.",
        "details": "Environment variables, operating system settings, installed software, and runtime configuration can form part of the system environment."
    }
]
def get_process_system_knowledge():
    return PROCESS_SYSTEM_KNOWLEDGE
def search_process_system_knowledge(query):
    if not query:
        return []
    text = str(query).strip().lower()
    matches = []
    for item in PROCESS_SYSTEM_KNOWLEDGE:
        best_keyword = None
        for keyword in item["keywords"]:
            keyword_lower = keyword.lower().strip()
            if not keyword_lower:
                continue
            if keyword_lower in text:
                if (
                    best_keyword is None
                    or len(keyword_lower) > len(best_keyword)
                ):
                    best_keyword = keyword_lower
        if best_keyword is not None:
            matches.append(
                (
                    len(best_keyword),
                    item
                )
            )
    matches.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in matches]
