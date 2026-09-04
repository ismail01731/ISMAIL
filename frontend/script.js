const chatContainer = document.getElementById("chatContainer");
const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const newChatButton = document.getElementById("newChatButton");
const clearChatButton =
    document.getElementById("clearChatButton");
const welcome = document.getElementById("welcome");

const exportChatButton =
    document.getElementById("exportChatButton");

const API_URL = "http://192.168.0.102:8000/api/chat";

const HISTORY_KEY = "ismail_ai_chat_history";

let currentChat = {
    id: Date.now(),
    title: "New chat",
    messages: []
};


function saveCurrentChat() {

    if (currentChat.messages.length === 0) {
        return;
    }

    const history =
        JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");

    const existingIndex =
        history.findIndex(chat => chat.id === currentChat.id);

    if (existingIndex >= 0) {
        history[existingIndex] = currentChat;
    } else {
        history.unshift(currentChat);
    }

    localStorage.setItem(
        HISTORY_KEY,
        JSON.stringify(history)
    );
}


function formatAIText(text, type) {

    const escapedText = String(text)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");

    if (type !== "ai") {
        return escapedText;
    }

    let formatted = escapedText;

    // Code blocks: ```code```
    formatted = formatted.replace(
        /```([\s\S]*?)```/g,
        '<pre class="code-block"><button class="code-copy-button" title="Copy code">⧉</button><code>$1</code></pre>'
    );

    // Important lines
    formatted = formatted.replace(
        /(^|\n)(\*{0,2}(Important|Key Point|Note|Warning|Summary|Answer|Conclusion):\*{0,2}[^\n]*)/gi,
        '$1<span class="important-heading"><span class="important-text">$2</span><button class="important-copy-button" title="Copy important text">⧉</button></span>'
    );

    // Bold: **text**
    formatted = formatted.replace(
        /\*\*(.+?)\*\*/g,
        '<strong>$1</strong>'
    );

    // Inline code: `code`
    formatted = formatted.replace(
        /`([^`]+)`/g,
        '<code>$1</code>'
    );

    return formatted;
}




function addMessage(text, type) {

    if (welcome) {
        welcome.style.display = "none";
    }

    const message = document.createElement("div");

    message.className = `message ${type}-message`;

    const content = document.createElement("div");

    content.className = "message-content";

    content.innerHTML = formatAIText(text, type);


    if (type === "ai") {

        


        const regenerateButton = document.createElement("button");

        regenerateButton.className = "regenerate-button";
        regenerateButton.textContent = "↻";
        regenerateButton.title = "Regenerate answer";

        regenerateButton.addEventListener("click", function () {

            const messageIndex = currentChat.messages.indexOf(
                currentChat.messages.find(
                    message =>
                        message.type === "ai" &&
                        message.text === text
                )
            );

            if (messageIndex <= 0) {
                return;
            }

            const question = currentChat.messages[messageIndex - 1];

            if (question.type !== "user") {
                return;
            }

            regenerateAnswer(question.text, message);
        });


        


                const codeCopyButtons =
                    content.querySelectorAll(".code-copy-button");

                codeCopyButtons.forEach(button => {

                    button.addEventListener("click", async function (event) {

                        event.stopPropagation();

                        const codeBlock =
                            button.parentElement.querySelector("code");

                        if (!codeBlock) {
                            return;
                        }

                        try {

                            const codeText = codeBlock.textContent;

                            if (navigator.clipboard && window.isSecureContext) {

                                await navigator.clipboard.writeText(codeText);

                            } else {

                                const textarea = document.createElement("textarea");

                                textarea.value = codeText;
                                textarea.style.position = "fixed";
                                textarea.style.left = "-9999px";
                                textarea.style.top = "0";

                                document.body.appendChild(textarea);

                                textarea.focus();
                                textarea.select();

                                document.execCommand("copy");

                                textarea.remove();
                            }

                            button.textContent = "✓";

                            setTimeout(() => {
                                button.textContent = "⧉";
                            }, 1500);

                        } catch (error) {

                            console.error("Code copy failed:", error);

                        }
                    });
                });


                const importantCopyButtons =
                    content.querySelectorAll(".important-copy-button");

                importantCopyButtons.forEach(button => {

                    button.addEventListener("click", async function (event) {

                        event.stopPropagation();

                        const importantText =
                            button.parentElement.querySelector(".important-text");

                        if (!importantText) {
                            return;
                        }

                        try {
                            await navigator.clipboard.writeText(
                                importantText.textContent
                            );

                            button.textContent = "✓";

                            setTimeout(() => {
                                button.textContent = "⧉";
                            }, 1500);

                        } catch (error) {
                            console.error("Important text copy failed:", error);
                        }
                    });
                });

        

                message.appendChild(content);

                const importantBox = content.querySelector(".important-heading");

                if (importantBox) {

                    const actions = document.createElement("span");
                    actions.className = "important-actions";

                    
                    actions.appendChild(regenerateButton);

                    importantBox.appendChild(actions);

                } else {

                    
                    message.appendChild(regenerateButton);
                }


    } else {

        message.appendChild(content);
    }

    currentChat.messages.push({
        type: type,
        text: text
    });

    if (
        currentChat.title === "New chat" &&
        type === "user"
    ) {
        currentChat.title =
            text.length > 30
                ? text.substring(0, 30) + "..."
                : text;
    }

    saveCurrentChat();



    chatContainer.appendChild(message);

    scrollToBottom();
}


function scrollToBottom() {

    chatContainer.scrollTo({
        top: chatContainer.scrollHeight,
        behavior: "smooth"
    });
}


function showLoading() {

    const message = document.createElement("div");

    message.className = "message ai-message";
    message.id = "loadingMessage";

    message.innerHTML = `
        <div class="loading-message">
            <span class="loading-dot"></span>
            <span class="loading-dot"></span>
            <span class="loading-dot"></span>
        </div>
    `;

    chatContainer.appendChild(message);

    scrollToBottom();
}


function removeLoading() {

    const loading = document.getElementById("loadingMessage");

    if (loading) {
        loading.remove();
    }
}


function setLoading(loading) {

    sendButton.disabled = loading;

    if (loading) {
        sendButton.textContent = "➤";
    } else {
        sendButton.textContent = "➤";
    }
}



async function regenerateAnswer(question, aiMessageElement) {

    if (!question || sendButton.disabled) {
        return;
    }

    sendButton.disabled = true;

    const oldContent =
        aiMessageElement.querySelector(".message-content");

    const oldAnswer = oldContent ? oldContent.textContent : "";

    if (oldContent) {
        oldContent.textContent = "Regenerating...";
    }

    try {

        const response = await fetch(API_URL, {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: question
            })
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();

        const newAnswer =
            data.response ||
            "ISMAIL AI did not return a response.";

        const messageIndex =
            currentChat.messages.findIndex(
                message =>
                    message.type === "ai" &&
                    message.text === oldAnswer
            );

        if (oldContent) {
            oldContent.textContent = newAnswer;
        }

        if (messageIndex >= 0) {
            currentChat.messages[messageIndex].text = newAnswer;
        }

        saveCurrentChat();

    } catch (error) {

        console.error("Regenerate Error:", error);

        if (oldContent) {
            oldContent.textContent =
                "Unable to regenerate the answer.";
        }

    } finally {

        sendButton.disabled = false;
        messageInput.focus();
    }
}


async function sendMessage() {

    const message = messageInput.value.trim();

    if (!message || sendButton.disabled) {
        return;
    }

    addMessage(message, "user");

    messageInput.value = "";
    messageInput.style.height = "auto";

    setLoading(true);
    showLoading();

    try {

        const response = await fetch(API_URL, {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })
        });


        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }


        const data = await response.json();

        removeLoading();


        addMessage(
            data.response || "ISMAIL AI did not return a response.",
            "ai"
        );


    } catch (error) {

        console.error("ISMAIL AI Error:", error);

        removeLoading();

        addMessage(
            "Unable to connect to ISMAIL AI. Please make sure the Python server is running.",
            "ai"
        );

    } finally {

        setLoading(false);

        messageInput.focus();
    }
}


/* Send button */

sendButton.addEventListener("click", sendMessage);


/* Enter = Send
   Shift + Enter = New line */

messageInput.addEventListener("keydown", function (event) {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        sendMessage();
    }
});


/* Auto resize textarea */

messageInput.addEventListener("input", function () {

    this.style.height = "auto";

    this.style.height =
        `${Math.min(this.scrollHeight, 150)}px`;
});


/* New Chat */

newChatButton.addEventListener("click", function () {

    chatContainer.innerHTML = "";

    currentChat = {
        id: Date.now(),
        title: "New chat",
        messages: []
    };

    if (welcome) {
        welcome.style.display = "flex";
        chatContainer.appendChild(welcome);
    }

    messageInput.value = "";

    messageInput.style.height = "auto";

    messageInput.focus();
});



/* =========================
   CHAT HISTORY
========================= */

const menuButton = document.querySelector(".menu-button");
const historyPanel = document.getElementById("historyPanel");
const closeHistoryButton =
    document.getElementById("closeHistoryButton");
const historyList =
    document.getElementById("historyList");


const historySearchInput =
    document.getElementById("historySearchInput");


const clearAllHistoryButton =
    document.getElementById("clearAllHistoryButton");


function renderHistory() {

    historyList.innerHTML = "";

    const history =
        JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");


    const searchText =
        historySearchInput.value.trim().toLowerCase();

    const filteredHistory = history.filter(chat =>
        (chat.title || "New chat")
            .toLowerCase()
            .includes(searchText)
    );

    
    if (history.length === 0) {

        const empty = document.createElement("div");

        empty.className = "history-empty";
        empty.textContent = "No chat history yet.";

            searchText
                    ? "No matching chats."
                    : "No chat history yet.";

        historyList.appendChild(empty);

        return;
    }

    filteredHistory.forEach(chat => {

        const item = document.createElement("div");

        item.className = "history-item";

        const title = document.createElement("span");

        title.textContent = chat.title || "New chat";


        const renameButton = document.createElement("button");

        renameButton.className = "history-rename-button";
        renameButton.textContent = "✎";
        renameButton.title = "Rename chat";

        renameButton.addEventListener("click", function (event) {

            event.stopPropagation();

            const newTitle = prompt(
                "Enter a new name for this chat:",
                chat.title || "New chat"
            );

            if (newTitle === null) {
                return;
            }

            const trimmedTitle = newTitle.trim();

            if (!trimmedTitle) {
                return;
            }

            const history =
                JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");

            const savedChat =
                history.find(savedChat => savedChat.id === chat.id);

            if (savedChat) {
                savedChat.title = trimmedTitle;

                localStorage.setItem(
                    HISTORY_KEY,
                    JSON.stringify(history)
                );
            }

            if (currentChat.id === chat.id) {
                currentChat.title = trimmedTitle;
            }

            renderHistory();
        });




        const deleteButton = document.createElement("button");

        deleteButton.className = "history-delete-button";
        deleteButton.textContent = "×";
        deleteButton.title = "Delete chat";

        deleteButton.addEventListener("click", function (event) {

            event.stopPropagation();

            const history =
                JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");

            const updatedHistory =
                history.filter(savedChat => savedChat.id !== chat.id);

            localStorage.setItem(
                HISTORY_KEY,
                JSON.stringify(updatedHistory)
            );

            if (currentChat.id === chat.id) {
                currentChat = {
                    id: Date.now(),
                    title: "New chat",
                    messages: []
                };
            }

            renderHistory();
        });

        item.appendChild(title);
        item.appendChild(renameButton);
        item.appendChild(deleteButton);

        item.addEventListener("click", function () {

            currentChat = chat;

            chatContainer.innerHTML = "";

            currentChat.messages.forEach(message => {

                if (welcome) {
                    welcome.style.display = "none";
                }

                const messageElement = document.createElement("div");

                messageElement.className =
                    `message ${message.type}-message`;

                const content = document.createElement("div");

                content.className = "message-content";
                content.textContent = message.text;

                messageElement.appendChild(content);

                chatContainer.appendChild(messageElement);
            });

            historyPanel.classList.remove("open");

            messageInput.focus();
        });

        historyList.appendChild(item);
    });
}





/* Close History */

closeHistoryButton.addEventListener("click", function () {

    historyPanel.classList.remove("open");
});


exportChatButton.addEventListener("click", function () {

    if (currentChat.messages.length === 0) {
        alert("There is no chat to export.");
        return;
    }

    let exportText = "";

    currentChat.messages.forEach(message => {

        const role =
            message.type === "user"
                ? "You"
                : "ISMAIL AI";

        exportText += `${role}:\n`;
        exportText += `${message.text}\n\n`;
    });

    const blob = new Blob(
        [exportText],
        { type: "text/plain;charset=utf-8" }
    );

    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");

    link.href = url;
    link.download =
        `${currentChat.title || "ISMAIL AI Chat"}.txt`;

    document.body.appendChild(link);

    link.click();

    link.remove();

    URL.revokeObjectURL(url);
});


clearChatButton.addEventListener("click", function () {

    if (currentChat.messages.length === 0) {
        return;
    }

    const confirmed = confirm(
        "Clear all messages from this chat?"
    );

    if (!confirmed) {
        return;
    }

    const history =
        JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");

    const updatedHistory =
        history.filter(chat => chat.id !== currentChat.id);

    localStorage.setItem(
        HISTORY_KEY,
        JSON.stringify(updatedHistory)
    );

    currentChat.messages = [];

    chatContainer.innerHTML = "";

    if (welcome) {
        welcome.style.display = "flex";
        chatContainer.appendChild(welcome);
    }

    saveCurrentChat();

    messageInput.value = "";
    messageInput.style.height = "auto";
    messageInput.focus();
});


clearAllHistoryButton.addEventListener("click", function () {

    const history =
        JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");

    if (history.length === 0) {
        return;
    }

    const confirmed = confirm(
        "Delete all chat history?"
    );

    if (!confirmed) {
        return;
    }

    localStorage.removeItem(HISTORY_KEY);

    currentChat = {
        id: Date.now(),
        title: "New chat",
        messages: []
    };

    chatContainer.innerHTML = "";

    if (welcome) {
        welcome.style.display = "flex";
        chatContainer.appendChild(welcome);
    }

    renderHistory();

    messageInput.value = "";
    messageInput.style.height = "auto";
    messageInput.focus();
});


// =========================
// MENU DROPDOWN
// =========================

const menuWrapper =
    document.querySelector(".menu-wrapper");

const menuDropdown =
    document.querySelector(".menu-dropdown");

const historyMenuButton =
    document.getElementById("historyMenuButton");

const clearAllHistoryMenuButton =
    document.getElementById("clearAllHistoryMenuButton");

menuButton.addEventListener("click", function (event) {

    event.stopPropagation();

    menuDropdown.classList.toggle("open");
});

document.addEventListener("click", function (event) {

    if (!menuWrapper.contains(event.target)) {
        menuDropdown.classList.remove("open");
    }
});

historyMenuButton.addEventListener("click", function () {

    renderHistory();

    historyPanel.classList.add("open");

    menuDropdown.classList.remove("open");
});

clearAllHistoryMenuButton.addEventListener("click", function () {

    menuDropdown.classList.remove("open");

    clearAllHistoryButton.click();
});
