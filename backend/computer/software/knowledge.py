SOFTWARE_KNOWLEDGE = [
    {
        "name": "software",
        "keywords": ["software", "সফটওয়্যার", "সফটওয়্যার"],
        "definition": "Software is a collection of programs and instructions that tell a computer what to do.",
        "details": "Software includes operating systems, applications, utilities, development tools, and other programs."
    },
    {
        "name": "application",
        "keywords": ["application", "app", "অ্যাপ্লিকেশন", "অ্যাপ"],
        "definition": "An application is software designed to perform specific tasks for users.",
        "details": "Examples include web browsers, media players, text editors, office applications, and communication apps."
    },
    {
        "name": "web_browser",
        "keywords": ["web browser", "browser", "ব্রাউজার"],
        "definition": "A web browser is software used to access and interact with websites and web applications.",
        "details": "Examples include Chrome, Microsoft Edge, Firefox, and Safari."
    },
    {
        "name": "chrome",
        "keywords": ["google chrome", "chrome", "গুগল ক্রোম", "ক্রোম"],
        "definition": "Google Chrome is a web browser developed by Google.",
        "details": "It is used to browse websites, run web applications, manage browser tabs, and use browser-based services."
    },
    {
        "name": "edge",
        "keywords": ["microsoft edge", "edge", "মাইক্রোসফট এজ", "এজ"],
        "definition": "Microsoft Edge is a web browser developed by Microsoft.",
        "details": "It is used for browsing websites and running web applications."
    },
    {
        "name": "firefox",
        "keywords": ["mozilla firefox", "firefox", "মজিলা ফায়ারফক্স", "ফায়ারফক্স"],
        "definition": "Mozilla Firefox is a web browser developed by Mozilla.",
        "details": "It is used to browse websites and provides privacy, customization, and extension features."
    },
    {
        "name": "vs_code",
        "keywords": ["visual studio code", "vs code", "vscode", "ভিএস কোড"],
        "definition": "Visual Studio Code is a source-code editor developed by Microsoft.",
        "details": "It supports many programming languages and can be extended with plugins, debuggers, terminals, and development tools."
    },
    {
        "name": "android_studio",
        "keywords": ["android studio", "অ্যান্ড্রয়েড স্টুডিও"],
        "definition": "Android Studio is the official integrated development environment for Android application development.",
        "details": "It provides code editing, debugging, build tools, emulators, and Android project management."
    },
    {
        "name": "terminal",
        "keywords": ["terminal", "টার্মিনাল"],
        "definition": "A terminal is a text-based interface used to interact with a computer by entering commands.",
        "details": "Terminals can be used to run programs, manage files, inspect systems, and perform development tasks."
    },
    {
        "name": "powershell",
        "keywords": ["powershell", "power shell", "পাওয়ারশেল", "পাওয়ারশেল"],
        "definition": "PowerShell is a command-line shell and scripting environment developed by Microsoft.",
        "details": "It is commonly used for Windows administration, automation, scripting, file management, and system tasks."
    },
    {
        "name": "command_prompt",
        "keywords": ["command prompt", "cmd", "কমান্ড প্রম্পট"],
        "definition": "Command Prompt is a Windows command-line interface used to execute text-based commands.",
        "details": "It can be used for file operations, diagnostics, networking commands, and running programs."
    },
    {
        "name": "python",
        "keywords": ["python programming", "python language", "python", "পাইথন"],
        "definition": "Python is a high-level programming language used to build software, automate tasks, analyze data, and develop AI systems.",
        "details": "Python has a large ecosystem of libraries and is widely used in web development, automation, data science, and artificial intelligence."
    },
    {
        "name": "git",
        "keywords": ["git version control", "git", "গিট"],
        "definition": "Git is a distributed version control system used to track changes in source code and other files.",
        "details": "Git supports commits, branches, merges, history tracking, and collaboration workflows."
    },
    {
        "name": "github",
        "keywords": ["github", "গিটহাব"],
        "definition": "GitHub is a platform for hosting Git repositories and collaborating on software projects.",
        "details": "It provides repository hosting, pull requests, issues, code review, and other development collaboration features."
    },
    {
        "name": "database_software",
        "keywords": ["database software", "database", "ডাটাবেস সফটওয়্যার", "ডাটাবেস"],
        "definition": "Database software is used to store, organize, retrieve, and manage structured data.",
        "details": "Examples include PostgreSQL, MySQL, SQLite, and Microsoft SQL Server."
    },
    {
        "name": "antivirus",
        "keywords": ["antivirus software", "antivirus", "অ্যান্টিভাইরাস"],
        "definition": "Antivirus software is designed to detect, prevent, and help remove malicious software.",
        "details": "It can scan files and systems for malware and may provide real-time protection."
    },
    {
        "name": "media_player",
        "keywords": ["media player", "video player", "মিডিয়া প্লেয়ার", "মিডিয়া প্লেয়ার"],
        "definition": "A media player is software used to play audio and video files.",
        "details": "Media players may support different audio and video formats and playback controls."
    },
    {
        "name": "office_software",
        "keywords": ["office software", "office suite", "অফিস সফটওয়্যার", "অফিস সফটওয়্যার"],
        "definition": "Office software is a collection of applications used for common productivity tasks.",
        "details": "Typical office software includes word processing, spreadsheets, presentations, email, and document tools."
    }
]
def get_software_knowledge():
    return SOFTWARE_KNOWLEDGE
def search_software_knowledge(query):
    if not query:
        return []
    text = str(query).strip().lower()
    matches = []
    for item in SOFTWARE_KNOWLEDGE:
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
