const chatContainer = document.getElementById("chatContainer");
const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const voiceButton =
document.getElementById("voiceButton");
const newChatButton = document.getElementById("newChatButton");
const clearChatButton =
    document.getElementById("clearChatButton");
const welcome = document.getElementById("welcome");

const exportChatButton =
    document.getElementById("exportChatButton");

const BACKEND_BASE_URL = "https://ismail-ai-api.onrender.com";
const API_URL = `${BACKEND_BASE_URL}/api/chat`;


const SESSION_KEY = "ismail_ai_session";

const HISTORY_KEY = "ismail_ai_chat_history";

let USER_ID = "";

let currentSession = null;


/* =========================================================
   ISMAIL AI ACCOUNT AUTHENTICATION
   ========================================================= */

const authScreen =
    document.getElementById("authScreen");

const authMessage =
    document.getElementById("authMessage");

const loginForm =
    document.getElementById("loginForm");

const registerForm =
    document.getElementById("registerForm");

const authToggleButton =
    document.getElementById("authToggleButton");

const loginUsername =
    document.getElementById("loginUsername");

const loginPassword =
    document.getElementById("loginPassword");

const registerUsername =
    document.getElementById("registerUsername");

const registerPassword =
    document.getElementById("registerPassword");



const registerPasswordConfirm =
    document.getElementById("registerPasswordConfirm");

const usernameSuggestions =
    document.getElementById("usernameSuggestions");

const passwordStrength =
    document.getElementById("passwordStrength");

const passwordMatch =
    document.getElementById("passwordMatch");

const passwordReqLength =
    document.getElementById("passwordReqLength");

const passwordReqLower =
    document.getElementById("passwordReqLower");

const passwordReqUpper =
    document.getElementById("passwordReqUpper");

const passwordReqNumber =
    document.getElementById("passwordReqNumber");

const passwordReqSpecial =
    document.getElementById("passwordReqSpecial");





function showAuthMessage(message = "") {
    if (authMessage) {
        authMessage.textContent = message;
    }
}


function showAuthScreen() {
    if (authScreen) {
        authScreen.style.display = "flex";
    }
}


function hideAuthScreen() {
    if (authScreen) {
        authScreen.style.display = "none";
    }
}


function setAuthenticatedSession(session) {

    if (
        !session ||
        !session.token ||
        !session.user_id ||
        !session.username
    ) {
        throw new Error(
            "Invalid authentication session."
        );
    }

    currentSession = session;
    USER_ID = String(session.user_id);

    localStorage.setItem(
        SESSION_KEY,
        JSON.stringify(session)
    );

    hideAuthScreen();
    showAuthMessage("");
}


function clearAuthenticatedSession() {

    currentSession = null;
    USER_ID = "";

    localStorage.removeItem(
        SESSION_KEY
    );

    showAuthScreen();
}


function getSavedSession() {

    const savedSession =
        localStorage.getItem(SESSION_KEY);

    if (!savedSession) {
        return null;
    }

    try {

        const session =
            JSON.parse(savedSession);

        if (
            !session ||
            !session.token ||
            !session.user_id ||
            !session.username
        ) {
            localStorage.removeItem(
                SESSION_KEY
            );

            return null;
        }

        return session;

    } catch (error) {

        localStorage.removeItem(
            SESSION_KEY
        );

        return null;
    }
}


async function getSession() {

    if (
        currentSession &&
        currentSession.token &&
        currentSession.user_id
    ) {
        return currentSession;
    }

    const savedSession =
        getSavedSession();

    if (savedSession) {

        currentSession =
            savedSession;

        USER_ID =
            String(savedSession.user_id);

        hideAuthScreen();

        return savedSession;
    }

    showAuthScreen();

    throw new Error(
        "Please login to continue."
    );
}



function updatePasswordRequirement(
    element,
    valid
) {
    if (!element) {
        return;
    }

    const icon =
        element.querySelector(".req-icon");

    if (valid) {
        element.classList.add(
            "valid"
        );

        if (icon) {
            icon.textContent = "✓";
        }
    } else {
        element.classList.remove(
            "valid"
        );

        if (icon) {
            icon.textContent = "○";
        }
    }
}


function updatePasswordValidation() {

    if (!registerPassword) {
        return false;
    }

    const password =
        registerPassword.value;

    const hasLength =
        password.length >= 8 &&
        password.length <= 128;

    const hasLower =
        /[a-z]/.test(password);

    const hasUpper =
        /[A-Z]/.test(password);

    const hasNumber =
        /[0-9]/.test(password);

    const hasSpecial =
        /[^A-Za-z0-9]/.test(password);


    updatePasswordRequirement(
        passwordReqLength,
        hasLength
    );

    updatePasswordRequirement(
        passwordReqLower,
        hasLower
    );

    updatePasswordRequirement(
        passwordReqUpper,
        hasUpper
    );

    updatePasswordRequirement(
        passwordReqNumber,
        hasNumber
    );

    updatePasswordRequirement(
        passwordReqSpecial,
        hasSpecial
    );


    const score =
        [
            hasLength,
            hasLower,
            hasUpper,
            hasNumber,
            hasSpecial
        ].filter(Boolean).length;


    if (passwordStrength) {

        if (!password) {
            passwordStrength.textContent =
                "Password strength: —";

            passwordStrength.className =
                "password-strength";

        } else if (score <= 2) {
            passwordStrength.textContent =
                "Password strength: Weak";

            passwordStrength.className =
                "password-strength weak";

        } else if (score <= 4) {
            passwordStrength.textContent =
                "Password strength: Medium";

            passwordStrength.className =
                "password-strength medium";

        } else {
            passwordStrength.textContent =
                "Password strength: Strong";

            passwordStrength.className =
                "password-strength strong";
        }
    }


    updatePasswordMatch();


    return (
        hasLength &&
        hasLower &&
        hasUpper &&
        hasNumber &&
        hasSpecial
    );
}


function updatePasswordMatch() {

    if (
        !registerPassword ||
        !registerPasswordConfirm ||
        !passwordMatch
    ) {
        return false;
    }

    const password =
        registerPassword.value;

    const confirmPassword =
        registerPasswordConfirm.value;


    if (!confirmPassword) {

        passwordMatch.textContent = "";

        passwordMatch.className =
            "password-match";

        return false;
    }


    if (
        password === confirmPassword
    ) {

        passwordMatch.textContent =
            "✓ Passwords match";

        passwordMatch.className =
            "password-match valid";

        return true;

    }


    passwordMatch.textContent =
        "✕ Passwords do not match";

    passwordMatch.className =
        "password-match invalid";

    return false;
}


function updateRegisterButton() {

    const passwordValid =
        updatePasswordValidation();

    const passwordsMatch =
        updatePasswordMatch();

    const username =
        registerUsername
            ? registerUsername.value.trim()
            : "";

    const usernameValid =
        /^[A-Za-z0-9._-]{3,50}$/
            .test(username);


    if (registerButton) {

        registerButton.disabled = !(
            usernameValid &&
            passwordValid &&
            passwordsMatch
        );
    }
}


if (registerPassword) {

    registerPassword.addEventListener(
        "input",
        updateRegisterButton
    );
}


if (registerPasswordConfirm) {

    registerPasswordConfirm
        .addEventListener(
            "input",
            updateRegisterButton
        );
}


if (registerUsername) {

    registerUsername.addEventListener(
        "input",
        updateRegisterButton
    );
}




function updateUsernameSuggestions() {

    if (
        !registerUsername ||
        !usernameSuggestions
    ) {
        return;
    }

    const username =
        registerUsername.value
            .trim()
            .toLowerCase();

    if (!username) {
        usernameSuggestions.innerHTML = "";
        return;
    }

    const base =
        username
            .replace(
                /[^a-z0-9]/g,
                ""
            )
            .slice(0, 42);

    if (!base) {
        usernameSuggestions.innerHTML = "";
        return;
    }

    const suggestions = [
        `${base}01`,
        `${base}123`,
        `${base}ai`
    ];

    usernameSuggestions.innerHTML = `
        <div class="suggestion-title">
            Username suggestions
        </div>

        ${suggestions
            .map(
                suggestion => `
                    <button
                        type="button"
                        class="username-suggestion"
                        data-username="${suggestion}"
                    >
                        ${suggestion}
                    </button>
                `
            )
            .join("")}
    `;

    usernameSuggestions
        .querySelectorAll(
            ".username-suggestion"
        )
        .forEach(button => {

            button.addEventListener(
                "click",
                function () {

                    registerUsername.value =
                        this.dataset.username;

                    updateUsernameSuggestions();
                    updateRegisterButton();

                    registerPassword.focus();
                }
            );

        });
}


if (registerUsername) {

    registerUsername.addEventListener(
        "input",
        updateUsernameSuggestions
    );

}






async function loginAccount(
    username,
    password
) {

    showAuthMessage(
        "Logging in..."
    );

    const response = await fetch(
        `${BACKEND_BASE_URL}/api/auth/login`,
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({
                username: username,
                password: password
            })
        }
    );

    let data = {};

    try {
        data = await response.json();
    } catch (error) {
        data = {};
    }

    if (!response.ok) {

        throw new Error(
            data.detail ||
            `Login failed: ${response.status}`
        );
    }

    setAuthenticatedSession(data);

    return data;
}


async function registerAccount(
    username,
    password
) {

    showAuthMessage(
        "Creating account..."
    );

    const response = await fetch(
        `${BACKEND_BASE_URL}/api/auth/register`,
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({
                username: username,
                password: password
            })
        }
    );

    let data = {};

    try {
        data = await response.json();
    } catch (error) {
        data = {};
    }

    if (!response.ok) {

        throw new Error(
            data.detail ||
            `Registration failed: ${response.status}`
        );
    }

    setAuthenticatedSession(data);

    return data;
}


/* Login */
if (loginForm) {

    loginForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            const username =
                loginUsername.value.trim();

            const password =
                loginPassword.value;

            if (!username || !password) {
                showAuthMessage(
                    "Please enter username and password."
                );
                return;
            }

            const button =
                document.getElementById(
                    "loginButton"
                );

            if (button) {
                button.disabled = true;
            }

            try {

                await loginAccount(
                    username,
                    password
                );

                await loadCentralChatHistory();

                startCentralHistorySync();

                loginPassword.value = "";

            } catch (error) {

                showAuthMessage(
                    error.message ||
                    "Login failed."
                );

            } finally {

                if (button) {
                    button.disabled = false;
                }
            }
        }
    );
}


/* Register */
if (registerForm) {

    registerForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            const username =
                registerUsername.value.trim();

            const password =
                registerPassword.value;

            if (!username || !password) {
                showAuthMessage(
                    "Please enter username and password."
                );
                return;
            }

            const button =
                document.getElementById(
                    "registerButton"
                );

            if (button) {
                button.disabled = true;
            }

            try {

                await registerAccount(
                    username,
                    password
                );

                await loadCentralChatHistory();

                startCentralHistorySync();

                registerPassword.value = "";

            } catch (error) {

                showAuthMessage(
                    error.message ||
                    "Account creation failed."
                );

            } finally {

                if (button) {
                    button.disabled = false;
                }
            }
        }
    );
}


/* Login <-> Register switch */
if (authToggleButton) {

    authToggleButton.addEventListener(
        "click",
        function () {

            const registerVisible =
                registerForm &&
                registerForm.style.display !== "none";

            showAuthMessage("");

            if (registerVisible) {

                registerForm.style.display =
                    "none";

                loginForm.style.display =
                    "flex";

                authToggleButton.textContent =
                    "Create a new account";

            } else {

                loginForm.style.display =
                    "none";

                registerForm.style.display =
                    "flex";

                authToggleButton.textContent =
                    "Back to login";
            }
        }
    );
}


/* Restore existing account session */
(function initializeAuthentication() {

    const savedSession =
        getSavedSession();

    if (savedSession) {

        try {

            setAuthenticatedSession(
                savedSession
            );

        } catch (error) {

            clearAuthenticatedSession();
        }

    } else {

        showAuthScreen();
    }

})();

/* =========================================================
   ISMAIL AI ACCOUNT AUTHENTICATION - END
   ========================================================= */

let currentChat = {
    id: Date.now(),
    title: "New chat",
    messages: []
};


async function loadCentralChatHistory() {

    try {

        const session = await getSession();

        const response = await fetch(
            `${BACKEND_BASE_URL}/api/chat/history`,
            {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${session.token}`
                }
            }
        );

        if (!response.ok) {
            console.error(
                "Central chat history load failed:",
                response.status
            );
            return;
        }

        const data = await response.json();

        const history = Array.isArray(data.history)
            ? data.history
            : [];

        if (history.length === 0) {
            return;
        }

        if (currentChat.messages.length > 0) {
            return;
        }

        if (currentChat.title === "New chat") {
            return;
        }

        currentChat.id =
            `central-${String(session.user_id)}`;

        currentChat.title = "Synced chat";

        history.forEach(item => {

            const role =
                item.role === "assistant"
                    ? "ai"
                    : "user";

            addMessage(
                String(item.message || ""),
                role
            );

        });

    } catch (error) {

        console.error(
            "Central chat history load error:",
            error
        );
    }
}



let centralHistorySyncTimer = null;


async function checkCentralChatHistory() {

    try {

        const session = await getSession();

        const response = await fetch(
            `${BACKEND_BASE_URL}/api/chat/history?chat_id=${encodeURIComponent(String(currentChat.id))}`,
            {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${session.token}`
                }
            }
        );

        if (!response.ok) {
            return;
        }

        const data = await response.json();

        const remoteHistory =
            Array.isArray(data.history)
                ? data.history
                : [];

        if (remoteHistory.length === 0) {
            return;
        }

        if (currentChat.title === "New chat") {
            return;
        }

        const localMessages =
            Array.isArray(currentChat.messages)
                ? currentChat.messages
                : [];

        /*
         * Only append messages when the existing local
         * messages match the beginning of the central history.
         * This prevents duplicate or unrelated chat data.
         */
        const commonLength =
            Math.min(
                localMessages.length,
                remoteHistory.length
            );

        for (let index = 0; index < commonLength; index++) {

            const localMessage =
                localMessages[index];

            const remoteMessage =
                remoteHistory[index];

            const remoteType =
                remoteMessage.role === "assistant"
                    ? "ai"
                    : "user";

            if (
                localMessage.type !== remoteType ||
                localMessage.text !==
                    String(remoteMessage.message || "")
            ) {
                return;
            }
        }

        if (
            remoteHistory.length <=
            localMessages.length
        ) {
            return;
        }

        for (
            let index = localMessages.length;
            index < remoteHistory.length;
            index++
        ) {

            const remoteMessage =
                remoteHistory[index];

            const remoteType =
                remoteMessage.role === "assistant"
                    ? "ai"
                    : "user";

            const remoteText =
                String(remoteMessage.message || "");

            if (!remoteText) {
                continue;
            }

            addMessage(
                remoteText,
                remoteType
            );
        }

    } catch (error) {

        console.error(
            "Central chat history polling error:",
            error
        );
    }
}


function startCentralHistorySync() {

    if (centralHistorySyncTimer) {
        clearInterval(
            centralHistorySyncTimer
        );
    }

    centralHistorySyncTimer =
        setInterval(
            checkCentralChatHistory,
            3000
        );
}



(function initializeCentralChatHistory() {

    const savedSession =
        getSavedSession();

    if (!savedSession) {
        return;
    }

    setTimeout(async function () {

        await loadCentralChatHistory();

        startCentralHistorySync();

    }, 0);

})();



async function syncChatMessage(role, message) {

    try {

        const session = await getSession();

        const response = await fetch(
            `${BACKEND_BASE_URL}/api/chat/history`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${session.token}`
                },

                body: JSON.stringify({
                    chat_id: String(currentChat.id),
                    role: role,
                    message: message
                })
            }
        );

        if (!response.ok) {
            console.error(
                "Chat history sync failed:",
                response.status
            );
        }

    } catch (error) {

        console.error(
            "Chat history sync error:",
            error
        );
    }
}


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
                message: question,
                user_id: USER_ID
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

    if (currentChat.title === "New chat") {
        currentChat.id = Date.now();
    }

    addMessage(message, "user");

    syncChatMessage("user", message);

    messageInput.value = "";
    messageInput.style.height = "auto";

    setLoading(true);
    showLoading();

    try {

        const session = await getSession();

        const response = await fetch(API_URL, {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${session.token}`
            },

            body: JSON.stringify({
                message: message,
                user_id: USER_ID
            })

        });



        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }


        const data = await response.json();

        if (data.action && data.action.action === "open_url" && data.action.url) {
            window.open(data.action.url, "_blank");
            removeLoading();
            return;
        }

        removeLoading();


        const assistantMessage =
            data.response ||
            "ISMAIL AI did not return a response.";

        addMessage(
            assistantMessage,
            "ai"
        );

        syncChatMessage(
            "assistant",
            assistantMessage
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




/* =========================================
   TOP RIGHT CHAT SEARCH
========================================= */

const topSearchButton =
    document.getElementById("topSearchButton");

const topSearchPopup =
    document.getElementById("topSearchPopup");

const topSearchInput =
    document.getElementById("topSearchInput");

const topSearchClose =
    document.getElementById("topSearchClose");

const topSearchResults =
    document.getElementById("topSearchResults");


/* -----------------------------------------
   GET SAVED CHAT HISTORY
----------------------------------------- */

function getTopSearchHistory() {
    try {

        const history =
            JSON.parse(
                localStorage.getItem(HISTORY_KEY) || "[]"
            );

        return Array.isArray(history)
            ? history
            : [];

    } catch (error) {

        console.error(
            "Search history error:",
            error
        );

        return [];
    }
}


/* -----------------------------------------
   OPEN SEARCH
----------------------------------------- */

function openTopSearch() {

    topSearchPopup.classList.add("open");

    setTimeout(() => {

        topSearchInput.focus();

    }, 50);
}


/* -----------------------------------------
   CLOSE SEARCH
----------------------------------------- */

function closeTopSearch() {

    topSearchPopup.classList.remove("open");

    topSearchInput.value = "";

    topSearchResults.innerHTML = "";
}


/* -----------------------------------------
   OPEN SELECTED CHAT
----------------------------------------- */

function openChatFromSearch(chat) {

    if (!chat) {
        return;
    }

    currentChat = chat;

    chatContainer.innerHTML = "";

    if (welcome) {
        welcome.style.display = "none";
    }


    if (
        Array.isArray(currentChat.messages)
    ) {

        currentChat.messages.forEach(
            message => {

                const messageElement =
                    document.createElement("div");

                messageElement.className =
                    `message ${message.type}-message`;


                const content =
                    document.createElement("div");

                content.className =
                    "message-content";

                content.textContent =
                    message.text || "";


                messageElement.appendChild(
                    content
                );

                chatContainer.appendChild(
                    messageElement
                );

            }
        );

    }


    closeTopSearch();

    messageInput.focus();
}


/* -----------------------------------------
   SEARCH CHATS
----------------------------------------- */

function renderTopSearchResults() {

    const searchText =
        topSearchInput.value
            .trim()
            .toLowerCase();


    topSearchResults.innerHTML = "";


    if (!searchText) {
        return;
    }


    const history =
        getTopSearchHistory();


    const filteredHistory =
        history.filter(chat => {

            const title =
                String(
                    chat.title || "New chat"
                );


            const messages =
                Array.isArray(chat.messages)
                    ? chat.messages
                        .map(
                            message =>
                                String(
                                    message.text || ""
                                )
                        )
                        .join(" ")
                    : "";


            return (
                title
                    .toLowerCase()
                    .includes(searchText)

                ||

                messages
                    .toLowerCase()
                    .includes(searchText)
            );

        });


    if (filteredHistory.length === 0) {

        const noResult =
            document.createElement("div");

        noResult.className =
            "top-search-no-result";

        noResult.textContent =
            "No matching chats found.";

        topSearchResults.appendChild(
            noResult
        );

        return;
    }


    filteredHistory
        .slice(0, 15)
        .forEach(chat => {

            const result =
                document.createElement("button");

            result.type = "button";

            result.className =
                "top-search-result";


            const title =
                document.createElement("div");

            title.className =
                "top-search-result-title";

            title.textContent =
                chat.title || "New chat";


            result.appendChild(title);


            /* Find matching message */

            let matchingMessage = null;


            if (
                Array.isArray(chat.messages)
            ) {

                matchingMessage =
                    chat.messages.find(
                        message =>
                            String(
                                message.text || ""
                            )
                            .toLowerCase()
                            .includes(searchText)
                    );

            }


            if (matchingMessage) {

                const message =
                    document.createElement("div");

                message.className =
                    "top-search-result-message";

                message.textContent =
                    String(
                        matchingMessage.text || ""
                    )
                    .replace(/\s+/g, " ")
                    .trim();


                result.appendChild(message);

            }


            result.addEventListener(
                "click",
                () => {

                    openChatFromSearch(chat);

                }
            );


            topSearchResults.appendChild(
                result
            );

        });

}


/* -----------------------------------------
   EVENTS
----------------------------------------- */

topSearchButton.addEventListener(
    "click",
    event => {

        event.stopPropagation();

        if (
            topSearchPopup.classList.contains(
                "open"
            )
        ) {

            closeTopSearch();

        } else {

            openTopSearch();

        }

    }
);


topSearchClose.addEventListener(
    "click",
    event => {

        event.stopPropagation();

        closeTopSearch();

    }
);


topSearchInput.addEventListener(
    "input",
    renderTopSearchResults
);


topSearchInput.addEventListener(
    "keydown",
    event => {

        if (event.key === "Escape") {

            closeTopSearch();

        }

    }
);


/* -----------------------------------------
   CLICK OUTSIDE
----------------------------------------- */

document.addEventListener(
    "click",
    event => {

        if (
            topSearchPopup.classList.contains(
                "open"
            )
            &&
            !topSearchPopup.contains(
                event.target
            )
            &&
            !topSearchButton.contains(
                event.target
            )
        ) {

            closeTopSearch();

        }

    }
);





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

    const filteredHistory = history.filter(chat => {
        const title = (chat.title || "New chat").toLowerCase();

        const messageText = Array.isArray(chat.messages)
            ? chat.messages
                .map(message => message.text || "")
                .join(" ")
                .toLowerCase()
            : "";

        return (
            title.includes(searchText) ||
            messageText.includes(searchText)
        );
    });

    
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



historySearchInput.addEventListener("input", renderHistory);





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



