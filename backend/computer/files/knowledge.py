# =========================================================
# ISMAIL AI - FILE & FOLDER INTELLIGENCE
# TASK 4 - KNOWLEDGE CORE
# =========================================================
FILE_FOLDER_KNOWLEDGE = [
    {
        "name": "file",
        "keywords": ["file", "ফাইল"],
        "definition": "A file is a named unit of data stored on a computer.",
        "details": "Files can contain text, images, videos, programs, documents, configuration data, and other information."
    },
    {
        "name": "folder",
        "keywords": ["folder", "ফোল্ডার", "directory", "ডিরেক্টরি"],
        "definition": "A folder is a container used to organize files and other folders.",
        "details": "Folders can contain files and subfolders and are used to organize a computer's data."
    },
    {
        "name": "file_extension",
        "keywords": ["file extension", "extension", "ফাইল এক্সটেনশন", "এক্সটেনশন"],
        "definition": "A file extension is the suffix of a filename that commonly indicates its file type.",
        "details": "Examples include .txt, .pdf, .jpg, .png, .mp4, .py, .exe, and .docx."
    },
    {
        "name": "file_path",
        "keywords": ["file path", "path", "ফাইল পাথ", "পাথ"],
        "definition": "A file path specifies the location of a file or folder in a filesystem.",
        "details": "A path can identify where a file or folder is located within a directory structure."
    },
    {
        "name": "absolute_path",
        "keywords": ["absolute path", "অ্যাবসোলিউট পাথ"],
        "definition": "An absolute path specifies the complete location of a file or folder from a filesystem root.",
        "details": "For example, Windows can use C:\\Users\\User\\Documents\\file.txt."
    },
    {
        "name": "relative_path",
        "keywords": ["relative path", "রিলেটিভ পাথ"],
        "definition": "A relative path specifies a location relative to the current working directory or another reference location.",
        "details": "For example, documents\\file.txt can be a relative path."
    },
    {
        "name": "file_name",
        "keywords": ["file name", "filename", "ফাইল নাম"],
        "definition": "A filename is the name assigned to a file.",
        "details": "A filename can contain a base name and, commonly, an extension such as report.pdf."
    },
    {
        "name": "file_size",
        "keywords": ["file size", "size of file", "ফাইল সাইজ", "ফাইলের আকার"],
        "definition": "File size represents how much storage space a file occupies.",
        "details": "File sizes are commonly measured in bytes, KB, MB, GB, or TB."
    },
    {
        "name": "file_type",
        "keywords": ["file type", "ফাইল টাইপ", "ফাইলের ধরন"],
        "definition": "A file type describes the format or kind of data stored in a file.",
        "details": "Examples include text files, image files, audio files, video files, documents, archives, and executable files."
    },
    {
        "name": "create_file",
        "keywords": ["create file", "new file", "ফাইল তৈরি", "নতুন ফাইল"],
        "definition": "Creating a file means making a new file in a filesystem.",
        "details": "A file can be created by applications, command-line tools, scripts, or operating-system interfaces."
    },
    {
        "name": "read_file",
        "keywords": ["read file", "open file", "ফাইল পড়া", "ফাইল খোলা"],
        "definition": "Reading a file means accessing its stored data.",
        "details": "Applications or system tools can read file contents when they have appropriate access."
    },
    {
        "name": "write_file",
        "keywords": ["write file", "edit file", "ফাইলে লেখা", "ফাইল এডিট"],
        "definition": "Writing a file means adding, changing, or replacing data stored in the file.",
        "details": "Writing normally requires suitable filesystem permissions."
    },
    {
        "name": "copy_file",
        "keywords": ["copy file", "copy", "ফাইল কপি"],
        "definition": "Copying a file creates another copy of the file's data at another location.",
        "details": "The original file normally remains unchanged after a copy operation."
    },
    {
        "name": "move_file",
        "keywords": ["move file", "move", "ফাইল সরানো"],
        "definition": "Moving a file changes its location within a filesystem.",
        "details": "The file normally remains the same while its directory location changes."
    },
    {
        "name": "rename_file",
        "keywords": ["rename file", "rename", "ফাইলের নাম পরিবর্তন", "ফাইল rename"],
        "definition": "Renaming a file changes its filename without normally changing its contents.",
        "details": "Renaming can also change the extension if the filename is edited incorrectly."
    },
    {
        "name": "delete_file",
        "keywords": ["delete file", "remove file", "delete", "ফাইল ডিলিট", "ফাইল মুছে ফেলা"],
        "definition": "Deleting a file removes its filesystem entry and may make its stored data inaccessible.",
        "details": "Depending on the operating system, deleted files may first be moved to a recycle bin or trash."
    },
    {
        "name": "hidden_file",
        "keywords": ["hidden file", "hidden files", "hidden", "হিডেন ফাইল", "গোপন ফাইল"],
        "definition": "A hidden file is a file that the operating system or file manager normally does not display by default.",
        "details": "Hidden files are often used for configuration or system-related data."
    },
    {
        "name": "directory_structure",
        "keywords": ["directory structure", "folder structure", "ডিরেক্টরি স্ট্রাকচার", "ফোল্ডার স্ট্রাকচার"],
        "definition": "A directory structure describes how folders and files are organized hierarchically.",
        "details": "A directory can contain files and child directories, creating a tree-like structure."
    },
    {
        "name": "windows_path",
        "keywords": ["windows path", "উইন্ডোজ পাথ"],
        "definition": "A Windows path identifies a file or folder location using Windows filesystem path conventions.",
        "details": "Windows commonly uses drive letters such as C: and backslashes in paths."
    },
    {
        "name": "linux_path",
        "keywords": ["linux path", "লিনাক্স পাথ"],
        "definition": "A Linux path identifies a file or folder location using Linux filesystem path conventions.",
        "details": "Linux paths normally use forward slashes and begin from the root directory / when absolute."
    }
]
def get_file_folder_knowledge():
    return FILE_FOLDER_KNOWLEDGE
def search_file_folder_knowledge(query):
    if not query:
        return []
    text = str(query).strip().lower()
    matches = []
    for item in FILE_FOLDER_KNOWLEDGE:
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
    # Most specific / longest matching keyword first.
    matches.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in matches]
