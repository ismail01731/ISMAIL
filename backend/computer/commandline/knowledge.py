COMMAND_LINE_KNOWLEDGE = [
    {
        "name": "command_line",
        "keywords": ["command line", "command-line", "কম্যান্ড লাইন", "কমান্ড লাইন"],
        "definition": "A command line is a text-based interface where users enter commands to interact with a computer.",
        "details": "It can be used to run programs, manage files, inspect systems, configure software, and automate tasks."
    },
    {
        "name": "cmd",
        "keywords": ["command prompt", "cmd", "কমান্ড প্রম্পট"],
        "definition": "Command Prompt is a Windows command-line interface for executing text-based commands.",
        "details": "It supports commands for files, directories, networking, diagnostics, and launching programs."
    },
    {
        "name": "powershell",
        "keywords": ["powershell", "power shell", "পাওয়ারশেল", "পাওয়ারশেল"],
        "definition": "PowerShell is a command-line shell and scripting environment from Microsoft.",
        "details": "It provides commands, scripting, automation, object-based pipelines, and Windows administration capabilities."
    },
    {
        "name": "terminal",
        "keywords": ["terminal", "টার্মিনাল"],
        "definition": "A terminal is an interface through which a user can interact with a command-line shell.",
        "details": "A terminal can host shells such as PowerShell, Command Prompt, Bash, and other command-line environments."
    },
    {
        "name": "command",
        "keywords": ["command", "কমান্ড"],
        "definition": "A command is an instruction entered into a command-line interface to perform an operation.",
        "details": "Commands can launch programs, manipulate files, inspect system information, and perform other tasks."
    },
    {
        "name": "argument",
        "keywords": ["command argument", "argument", "আর্গুমেন্ট"],
        "definition": "A command argument is a value supplied to a command that helps specify what the command should operate on.",
        "details": "For example, a filename supplied after a command can act as an argument."
    },
    {
        "name": "option_flag",
        "keywords": ["command option", "command flag", "option flag", "flag", "option", "ফ্ল্যাগ", "অপশন"],
        "definition": "A command option or flag changes or controls how a command behaves.",
        "details": "Options are commonly written using forms such as -r, --help, or other shell-specific syntax."
    },
    {
        "name": "pipe",
        "keywords": ["command pipe", "pipe", "পাইপ"],
        "definition": "A pipe sends the output of one command as input to another command.",
        "details": "In many command-line environments the pipe symbol is represented by |."
    },
    {
        "name": "redirect",
        "keywords": ["output redirect", "input redirect", "redirect", "redirection", "রিডাইরেক্ট", "রিডাইরেকশন"],
        "definition": "Command redirection sends command input or output to or from another location such as a file.",
        "details": "Common redirection operators include >, >>, and <, depending on the shell."
    },
    {
        "name": "environment_variable",
        "keywords": ["environment variable", "environment variables", "এনভায়রনমেন্ট ভ্যারিয়েবল", "এনভায়রনমেন্ট ভ্যারিয়েবল"],
        "definition": "An environment variable is a named value provided to processes by the operating system or shell environment.",
        "details": "Environment variables can store configuration values such as PATH and other application settings."
    },
    {
        "name": "path_variable",
        "keywords": ["path environment variable", "path variable", "environment path", "PATH variable", "path"],
        "definition": "PATH is an environment variable containing directories that the operating system or shell searches for executable commands.",
        "details": "Adding a program's directory to PATH can allow its executable to be invoked without specifying the full path."
    },
    {
        "name": "working_directory",
        "keywords": ["working directory", "current directory", "current working directory", "ওয়ার্কিং ডিরেক্টরি", "ওয়ার্কিং ডিরেক্টরি"],
        "definition": "The working directory is the directory a command-line process is currently operating in.",
        "details": "Relative paths are commonly interpreted from the current working directory."
    },
    {
        "name": "command_history",
        "keywords": ["command history", "shell history", "command history list", "কমান্ড হিস্ট্রি"],
        "definition": "Command history is a record of previously entered commands maintained by a shell.",
        "details": "History can help users review, reuse, or repeat commands."
    },
    {
        "name": "exit_code",
        "keywords": ["exit code", "return code", "status code", "এক্সিট কোড", "রিটার্ন কোড"],
        "definition": "An exit code is a numeric status returned by a program or command when it finishes.",
        "details": "A zero exit code commonly indicates success, while non-zero values commonly indicate an error or other condition."
    },
    {
        "name": "script",
        "keywords": ["command script", "shell script", "script", "স্ক্রিপ্ট"],
        "definition": "A script is a text file containing commands or program instructions that can be executed to automate tasks.",
        "details": "Scripts can automate repetitive operations and may contain variables, conditions, loops, and commands."
    },
    {
        "name": "batch_file",
        "keywords": ["batch file", "bat file", ".bat", "ব্যাচ ফাইল"],
        "definition": "A batch file is a Windows script file that contains commands to be executed by a command interpreter.",
        "details": "Batch files commonly use the .bat or .cmd extension."
    },
    {
        "name": "powershell_script",
        "keywords": ["powershell script", "ps1 script", ".ps1", "পাওয়ারশেল স্ক্রিপ্ট", "পাওয়ারশেল স্ক্রিপ্ট"],
        "definition": "A PowerShell script is a text file containing PowerShell commands and code.",
        "details": "PowerShell scripts commonly use the .ps1 extension and can automate administration and development tasks."
    }
]
def get_command_line_knowledge():
    return COMMAND_LINE_KNOWLEDGE
def search_command_line_knowledge(query):
    if not query:
        return []
    text = str(query).strip().lower()
    matches = []
    for item in COMMAND_LINE_KNOWLEDGE:
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
