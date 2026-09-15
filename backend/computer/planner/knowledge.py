"""
ISMAIL AI - Computer Action Planner
Task 11A - Action Planner Knowledge Core
"""
COMPUTER_ACTION_PLANS = [
    {
        "name": "create_folder",
        "keywords": [
            "create folder",
            "make folder",
            "new folder",
            "folder বানাও",
            "folder তৈরি",
            "নতুন folder"
        ],
        "intent": "Create a new folder.",
        "actions": [
            "identify_target_directory",
            "verify_target_path",
            "check_permission",
            "create_folder",
            "verify_creation"
        ],
        "risk": "low"
    },
    {
        "name": "create_file",
        "keywords": [
            "create file",
            "make file",
            "new file",
            "make file",
            "new file",
            "file বানাও",
            "file তৈরি",
            "নতুন file"
        ],
        "intent": "Create a new file.",
        "actions": [
            "identify_target_directory",
            "identify_file_name",
            "verify_target_path",
            "check_permission",
            "create_file",
            "verify_creation"
        ],
        "risk": "low"
    },
    {
        "name": "read_file",
        "keywords": [
            "read file",
            "read this file",
            "open file",
            "open this file",
            "open file",
            "show file",
            "file পড়",
            "file দেখাও",
            "ফাইল খুলে"
        ],
        "intent": "Read or inspect a file.",
        "actions": [
            "identify_file",
            "verify_file_exists",
            "check_read_permission",
            "read_file",
            "return_content"
        ],
        "risk": "low"
    },
    {
        "name": "delete_file",
        "keywords": [
            "delete file",
            "delete this file",
            "remove file",
            "remove this file",
            "remove file",
            "file delete",
            "file মুছে",
            "ফাইল delete",
            "ফাইল মুছে ফেল"
        ],
        "intent": "Delete a file.",
        "actions": [
            "identify_file",
            "verify_file_exists",
            "confirm_target",
            "check_permission",
            "delete_file",
            "verify_deletion"
        ],
        "risk": "high"
    },
    {
        "name": "copy_file",
        "keywords": [
            "copy file",
            "copy this file",
            "file copy",
            "ফাইল copy",
            "ফাইল কপি"
        ],
        "intent": "Copy a file.",
        "actions": [
            "identify_source_file",
            "identify_destination",
            "verify_source_exists",
            "check_destination",
            "copy_file",
            "verify_copy"
        ],
        "risk": "low"
    },
    {
        "name": "move_file",
        "keywords": [
            "move file",
            "move this file",
            "file move",
            "ফাইল move",
            "ফাইল সরাও"
        ],
        "intent": "Move a file.",
        "actions": [
            "identify_source_file",
            "identify_destination",
            "verify_source_exists",
            "check_permission",
            "move_file",
            "verify_move"
        ],
        "risk": "medium"
    },
    {
        "name": "rename_file",
        "keywords": [
            "rename file",
            "rename this file",
            "file rename",
            "ফাইল rename",
            "ফাইলের নাম বদলাও"
        ],
        "intent": "Rename a file.",
        "actions": [
            "identify_file",
            "identify_new_name",
            "verify_file_exists",
            "check_permission",
            "rename_file",
            "verify_rename"
        ],
        "risk": "medium"
    },
    {
        "name": "open_application",
        "keywords": [
            "open app",
            "open chrome",
            "launch chrome",
            "start chrome",
            "open application",
            "launch app",
            "start application",
            "অ্যাপ খোল",
            "application খোল",
            "program খোল"
        ],
        "intent": "Open an application.",
        "actions": [
            "identify_application",
            "verify_application",
            "check_launch_permission",
            "launch_application",
            "verify_application_started"
        ],
        "risk": "low"
    },
    {
        "name": "close_application",
        "keywords": [
            "close app",
            "close application",
            "exit app",
            "stop application",
            "অ্যাপ বন্ধ",
            "application বন্ধ"
        ],
        "intent": "Close an application.",
        "actions": [
            "identify_application",
            "identify_running_process",
            "confirm_target_process",
            "request_termination",
            "verify_application_closed"
        ],
        "risk": "medium"
    },
    {
        "name": "open_website",
        "keywords": [
            "open website",
            "open site",
            "visit website",
            "website খোল",
            "site খোল",
            "ওয়েবসাইট খোল"
        ],
        "intent": "Open a website.",
        "actions": [
            "identify_destination",
            "validate_destination",
            "identify_browser",
            "open_browser",
            "navigate_to_destination",
            "verify_navigation"
        ],
        "risk": "low"
    },
    {
        "name": "search_web",
        "keywords": [
            "search web",
            "search google",
            "google search",
            "web search",
            "গুগলে search",
            "ওয়েবে search",
            "অনলাইনে খুঁজ"
        ],
        "intent": "Perform a web search.",
        "actions": [
            "identify_search_query",
            "identify_browser",
            "open_search_engine",
            "submit_search",
            "verify_results"
        ],
        "risk": "low"
    },
    {
        "name": "run_command",
        "keywords": [
            "run command",
            "execute command",
            "run powershell",
            "run cmd",
            "command চালাও",
            "command run",
            "powershell চালাও"
        ],
        "intent": "Execute a command.",
        "actions": [
            "identify_command",
            "validate_command",
            "classify_command_risk",
            "request_permission_if_required",
            "execute_command",
            "inspect_exit_code",
            "verify_result"
        ],
        "risk": "high"
    },
    {
        "name": "check_system",
        "keywords": [
            "check system",
            "check my computer",
            "check computer",
            "check computer",
            "system check",
            "computer check",
            "কম্পিউটার check",
            "system পরীক্ষা"
        ],
        "intent": "Inspect computer/system state.",
        "actions": [
            "identify_requested_information",
            "collect_system_information",
            "collect_resource_information",
            "analyze_state",
            "return_system_report"
        ],
        "risk": "low"
    },
    {
        "name": "check_network",
        "keywords": [
            "check network",
            "check internet",
            "test internet",
            "network check",
            "internet check",
            "ইন্টারনেট check",
            "নেট check"
        ],
        "intent": "Inspect network connectivity.",
        "actions": [
            "check_network_adapter",
            "check_local_configuration",
            "check_gateway",
            "check_dns",
            "test_connectivity",
            "return_network_report"
        ],
        "risk": "low"
    },
    {
        "name": "install_software",
        "keywords": [
            "install software",
            "install app",
            "install application",
            "software install",
            "app install",
            "software ইনস্টল",
            "app ইনস্টল"
        ],
        "intent": "Install software.",
        "actions": [
            "identify_software",
            "identify_trusted_source",
            "validate_package",
            "check_system_requirements",
            "request_install_permission",
            "install_software",
            "verify_installation"
        ],
        "risk": "high"
    },
    {
        "name": "uninstall_software",
        "keywords": [
            "uninstall software",
            "uninstall application",
            "uninstall app",
            "uninstall app",
            "remove application",
            "software uninstall",
            "app uninstall",
            "software uninstall কর",
            "app মুছে ফেল"
        ],
        "intent": "Uninstall software.",
        "actions": [
            "identify_software",
            "verify_installed_software",
            "confirm_target",
            "request_uninstall_permission",
            "uninstall_software",
            "verify_uninstallation"
        ],
        "risk": "high"
    },
    {
        "name": "shutdown_computer",
        "keywords": [
            "shutdown computer",
            "shut down computer",
            "turn off computer",
            "computer shutdown",
            "কম্পিউটার বন্ধ কর",
            "pc বন্ধ কর"
        ],
        "intent": "Shut down the computer.",
        "actions": [
            "identify_shutdown_request",
            "check_active_work",
            "warn_about_shutdown",
            "request_confirmation",
            "shutdown_computer",
            "verify_shutdown"
        ],
        "risk": "critical"
    },
    {
        "name": "restart_computer",
        "keywords": [
            "restart computer",
            "reboot computer",
            "restart pc",
            "reboot pc",
            "কম্পিউটার restart",
            "pc restart"
        ],
        "intent": "Restart the computer.",
        "actions": [
            "identify_restart_request",
            "check_active_work",
            "warn_about_restart",
            "request_confirmation",
            "restart_computer",
            "verify_restart"
        ],
        "risk": "critical"
    }
]
def get_computer_action_plans():
    """Return all computer action planner definitions."""
    return COMPUTER_ACTION_PLANS
def search_computer_action_plan(query):
    """
    Find the best computer action plan for a user request.
    Matching is word-aware so that:
    "install" does not incorrectly match
    "uninstall".
    """
    if not query:
        return []
    text = str(query).strip().lower()
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
    for index, item in enumerate(COMPUTER_ACTION_PLANS):
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
            if keyword_normalized in normalized:
                score = len(keyword_words) * 10
            elif len(keyword_words) > 1:
                matched_words = sum(
                    1
                    for word in keyword_words
                    if word in words
                )
                if matched_words == len(keyword_words):
                    score = len(keyword_words) * 7
            elif keyword_normalized in words:
                score = 5
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
    # Natural Bengali command fallbacks.
    # These rules classify common Bengali computer requests
    # without executing any real computer action.
    bengali_patterns = [
        ("create_folder", [
            "??????? ????",
            "??????? ?????",
            "??????? ????",
            "???? ???????",
            "???? ??????? ????",
            "???? ??????? ????",
        ]),
        ("create_file", [
            "???? ????",
            "???? ?????",
            "???? ????",
            "???? ????",
            "???? ???? ????",
            "???? ???? ????",
        ]),
        ("read_file", [
            "???? ???",
            "???? ??",
            "???? ?????",
            "???? ????",
            "???? ???",
            "???? ????",
        ]),
        ("delete_file", [
            "???? ????",
            "???? ???? ???",
            "???? ?????",
            "???? delete",
        ]),
        ("open_application", [
            "????? ???",
            "????? ????",
            "????? ????",
            "????????? ???",
            "????????? ????",
            "????? ???",
            "????? ????",
            "chrome ???",
            "chrome ????",
        ]),
        ("close_application", [
            "????? ????",
            "??????? ????",
            "??????? ????",
            "????????? ????",
            "????? ????",
            "chrome ????",
        ]),
        ("open_website", [
            "???????? ???",
            "???????? ????",
            "???????? ????",
            "???? ???",
            "???? ????",
        ]),
        ("search_web", [
            "????? ????",
            "????? ?????",
            "??????? ????",
            "????? ????",
            "????? ?????",
        ]),
        ("run_command", [
            "command ?????",
            "command ???? ??",
            "?????? ?????",
            "?????? ???? ??",
        ]),
        ("check_system", [
            "????????? ???????",
            "????????? ???",
            "??????? ???????",
            "??????? ???",
        ]),
        ("check_network", [
            "????????? ???????",
            "????????? ???",
            "??? ???",
            "????????? ???????",
            "????????? ???",
        ]),
        ("shutdown_computer", [
            "????????? shutdown",
            "????????? ???????",
            "????????? ???? ??",
            "????????? ???? ??? ???",
            "???? ???? ??",
        ]),
        ("restart_computer", [
            "????????? restart",
            "????????? ?????????",
            "????????? ???? ????",
            "????????? ?????? ????",
            "???? restart",
            "???? ?????????",
        ]),
    ]
    for action_name, patterns in bengali_patterns:
        if any(pattern in normalized for pattern in patterns):
            plan = next(
                (
                    item
                    for item in COMPUTER_ACTION_PLANS
                    if item.get("name") == action_name
                ),
                None
            )
            if plan is not None:
                already_matched = any(
                    item.get("name") == action_name
                    for _, _, _, item in matches
                )
                if not already_matched:
                    matches.append(
                        (
                            25,
                            max(
                                len(pattern)
                                for pattern in patterns
                                if pattern in normalized
                            ),
                            -1,
                            plan
                        )
                    )
    # Targeted fallback for requests such as:
    # "close Chrome", "close Notepad", etc.
    # A bare "close" request is intentionally not matched.
    if len(words) >= 2 and "close" in words:
        close_plan = next(
            (
                item
                for item in COMPUTER_ACTION_PLANS
                if item.get("name") == "close_application"
            ),
            None
        )
        if close_plan is not None:
            already_matched = any(
                item.get("name") == "close_application"
                for _, _, _, item in matches
            )
            if not already_matched:
                matches.append(
                    (
                        20,
                        len("close application"),
                        -1,
                        close_plan
                    )
                )
    # Natural Bengali action matches.
    # Unicode escapes are used here so Windows PowerShell
    # console encoding cannot corrupt Bengali source text.
    bengali_exact_actions = {
        "create_folder": [
            "\u09a8\u09a4\u09c1\u09a8 \u09ab\u09cb\u09b2\u09cd\u09a1\u09be\u09b0 \u09a4\u09c8\u09b0\u09bf",
            "\u09ab\u09cb\u09b2\u09cd\u09a1\u09be\u09b0 \u09a4\u09c8\u09b0\u09bf",
            "\u09ab\u09cb\u09b2\u09cd\u09a1\u09be\u09b0 \u09ac\u09be\u09a8\u09be\u0993",
            "\u09ab\u09cb\u09b2\u09cd\u09a1\u09be\u09b0 \u09a4\u09c8\u09b0\u09c0",
        ],
        "create_file": [
            "\u09a8\u09a4\u09c1\u09a8 \u09ab\u09be\u0987\u09b2 \u09a4\u09c8\u09b0\u09bf",
            "\u09ab\u09be\u0987\u09b2 \u09a4\u09c8\u09b0\u09bf",
            "\u09ab\u09be\u0987\u09b2 \u09ac\u09be\u09a8\u09be\u0993",
            "\u09ab\u09be\u0987\u09b2 \u09a4\u09c8\u09b0\u09c0",
        ],
        "read_file": [
            "\u09ab\u09be\u0987\u09b2 \u09aa\u09a1\u09bc",
            "\u09ab\u09be\u0987\u09b2 \u09aa\u09a1\u09bc\u09cb",
            "\u09ab\u09be\u0987\u09b2 \u09aa\u09a1\u09bc\u09be",
            "\u09ab\u09be\u0987\u09b2 \u09aa\u09dc",
            "\u09ab\u09be\u0987\u09b2 \u09a6\u09c7\u0996\u09be\u0993",
        ],
        "delete_file": [
            "\u09ab\u09be\u0987\u09b2 \u09ae\u09c1\u099b\u09c7",
            "\u09ab\u09be\u0987\u09b2 \u09ae\u09c1\u099b\u09c7 \u09ab\u09c7\u09b2",
            "\u09ab\u09be\u0987\u09b2 \u09a1\u09bf\u09b2\u09bf\u099f",
            "\u09ab\u09be\u0987\u09b2 delete",
        ],
        "open_application": [
            "chrome \u0996\u09c1\u09b2\u09c7",
            "chrome \u0996\u09cb\u09b2",
            "\u0995\u09cd\u09b0\u09cb\u09ae \u0996\u09c1\u09b2\u09c7",
            "\u0995\u09cd\u09b0\u09cb\u09ae \u0996\u09cb\u09b2",
            "\u0985\u09cd\u09af\u09be\u09aa \u0996\u09c1\u09b2\u09c7",
            "\u0985\u09cd\u09af\u09be\u09aa \u0996\u09cb\u09b2",
            "\u0985\u09cd\u09af\u09be\u09aa \u0993\u09aa\u09c7\u09a8",
            "\u09aa\u09cd\u09b0\u09cb\u0997\u09cd\u09b0\u09be\u09ae \u0996\u09c1\u09b2\u09c7",
            "\u09aa\u09cd\u09b0\u09cb\u0997\u09cd\u09b0\u09be\u09ae \u0996\u09cb\u09b2",
        ],
        "close_application": [
        "\u098f\u099f\u09be \u09ac\u09a8\u09cd\u09a7",
        "\u0993\u099f\u09be \u09ac\u09a8\u09cd\u09a7",
        "\u09b8\u09c7\u099f\u09be \u09ac\u09a8\u09cd\u09a7",
        "\u098f\u099f\u09be \u09ac\u09a8\u09cd\u09a7 \u0995\u09b0\u09cb",
        "\u0993\u099f\u09be \u09ac\u09a8\u09cd\u09a7 \u0995\u09b0\u09cb",
        "\u09b8\u09c7\u099f\u09be \u09ac\u09a8\u09cd\u09a7 \u0995\u09b0\u09cb",
        "\u098f\u099f\u09be \u09ac\u09a8\u09cd\u09a7 \u0995\u09b0",
        "\u0993\u099f\u09be \u09ac\u09a8\u09cd\u09a7 \u0995\u09b0",
        "\u09b8\u09c7\u099f\u09be \u09ac\u09a8\u09cd\u09a7 \u0995\u09b0",
            "chrome \u09ac\u09a8\u09cd\u09a7",
            "\u0995\u09cd\u09b0\u09cb\u09ae \u09ac\u09a8\u09cd\u09a7",
            "\u0985\u09cd\u09af\u09be\u09aa \u09ac\u09a8\u09cd\u09a7",
            "\u0985\u09cd\u09af\u09be\u09aa\u099f\u09bf \u09ac\u09a8\u09cd\u09a7",
            "\u0985\u09cd\u09af\u09be\u09aa\u099f\u09be \u09ac\u09a8\u09cd\u09a7",
            "\u09aa\u09cd\u09b0\u09cb\u0997\u09cd\u09b0\u09be\u09ae \u09ac\u09a8\u09cd\u09a7",
        ],
        "open_website": [
            "\u0993\u09df\u09c7\u09ac\u09b8\u09be\u0987\u099f \u0996\u09c1\u09b2\u09c7",
            "\u0993\u09df\u09c7\u09ac\u09b8\u09be\u0987\u099f \u0996\u09cb\u09b2",
            "\u0993\u09df\u09c7\u09ac\u09b8\u09be\u0987\u099f \u0993\u09aa\u09c7\u09a8",
            "\u09b8\u09be\u0987\u099f \u0996\u09c1\u09b2\u09c7",
            "\u09b8\u09be\u0987\u099f \u0996\u09cb\u09b2",
        ],
        "search_web": [
            "\u0993\u09df\u09c7\u09ac\u09c7 \u0996\u09c1\u0981\u099c",
            "\u0993\u09df\u09c7 \u09b8\u09be\u09b0\u09cd\u099a",
            "\u0985\u09a8\u09b2\u09be\u0987\u09a8\u09c7 \u0996\u09c1\u0981\u099c",
            "\u0997\u09c1\u0997\u09b2\u09c7 \u0996\u09c1\u0981\u099c",
            "\u0997\u09c1\u0997\u09b2\u09c7 \u09b8\u09be\u09b0\u09cd\u099a",
        ],
        "run_command": [
            "\u0995\u09ae\u09be\u09a8\u09cd\u09a1 \u099a\u09be\u09b2\u09be\u0993",
            "\u0995\u09ae\u09be\u09a8\u09cd\u09a1 \u099a\u09be\u09b2\u09c1 \u0995\u09b0",
            "command \u099a\u09be\u09b2\u09be\u0993",
            "command \u099a\u09be\u09b2\u09c1 \u0995\u09b0",
        ],
        "check_system": [
            "\u0995\u09ae\u09cd\u09aa\u09bf\u0989\u099f\u09be\u09b0 \u09aa\u09b0\u09c0\u0995\u09cd\u09b7\u09be",
            "\u0995\u09ae\u09cd\u09aa\u09bf\u0989\u099f\u09be\u09b0 \u099a\u09c7\u0995",
            "\u09b8\u09bf\u09b8\u09cd\u099f\u09c7\u09ae \u09aa\u09b0\u09c0\u0995\u09cd\u09b7\u09be",
            "\u09b8\u09bf\u09b8\u09cd\u099f\u09c7\u09ae \u099a\u09c7\u0995",
        ],
        "check_network": [
            "\u0987\u09a8\u09cd\u099f\u09be\u09b0\u09a8\u09c7\u099f \u09aa\u09b0\u09c0\u0995\u09cd\u09b7\u09be",
            "\u0987\u09a8\u09cd\u099f\u09be\u09b0\u09a8\u09c7\u099f \u099a\u09c7\u0995",
            "\u09a8\u09c7\u099f\u0993\u09df\u09be\u09b0\u09cd\u0995 \u09aa\u09b0\u09c0\u0995\u09cd\u09b7\u09be",
            "\u09a8\u09c7\u099f\u0993\u09df\u09be\u09b0\u09cd\u0995 \u099a\u09c7\u0995",
        ],
        "shutdown_computer": [
            "\u0995\u09ae\u09cd\u09aa\u09bf\u0989\u099f\u09be\u09b0 shutdown",
            "\u0995\u09ae\u09cd\u09aa\u09bf\u0989\u099f\u09be\u09b0 \u09b6\u09be\u099f\u09a1\u09be\u0989\u09a8",
            "\u0995\u09ae\u09cd\u09aa\u09bf\u0989\u099f\u09be\u09b0 \u09ac\u09a8\u09cd\u09a7 \u0995\u09b0",
            "\u0995\u09ae\u09cd\u09aa\u09bf\u0989\u099f\u09be\u09b0 \u09ac\u09a8\u09cd\u09a7 \u0995\u09b0\u09c7 \u09a6\u09be\u0993",
            "\u09aa\u09bf\u09b8\u09bf \u09ac\u09a8\u09cd\u09a7 \u0995\u09b0",
        ],
        "restart_computer": [
            "\u0995\u09ae\u09cd\u09aa\u09bf\u0989\u099f\u09be\u09b0 restart",
            "\u0995\u09ae\u09cd\u09aa\u09bf\u0989\u099f\u09be\u09b0 \u09b0\u09bf\u09b8\u09cd\u099f\u09be\u09b0\u09cd\u099f",
            "\u0995\u09ae\u09cd\u09aa\u09bf\u0989\u099f\u09be\u09b0 \u0986\u09ac\u09be\u09b0 \u099a\u09be\u09b2\u09c1",
            "\u0995\u09ae\u09cd\u09aa\u09bf\u0989\u099f\u09be\u09b0 \u09aa\u09c1\u09a8\u09b0\u09be\u09df \u099a\u09be\u09b2\u09c1",
            "\u09aa\u09bf\u09b8\u09bf restart",
            "\u09aa\u09bf\u09b8\u09bf \u09b0\u09bf\u09b8\u09cd\u099f\u09be\u09b0\u09cd\u200c\u099f",
        ],
    }
    for action_name, patterns in bengali_exact_actions.items():
        matched_patterns = [
            pattern
            for pattern in patterns
            if pattern in normalized
        ]
        if not matched_patterns:
            continue
        plan = next(
            (
                item
                for item in COMPUTER_ACTION_PLANS
                if item.get("name") == action_name
            ),
            None
        )
        if plan is None:
            continue
        matches = [
            item
            for item in matches
            if item[3].get("name") != action_name
        ]
        strongest_pattern = max(
            matched_patterns,
            key=len
        )
        matches.append(
            (
                1000,
                len(strongest_pattern),
                -1,
                plan
            )
        )
    matches.sort(
        key=lambda x: (x[0], x[1], -x[2]),
        reverse=True
    )
    return [
        item
        for _, _, _, item in matches
    ]

