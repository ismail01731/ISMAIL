const chatContainer = document.getElementById("chatContainer");
const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const attachButton =
    document.getElementById("attachButton");

const fileInput =
    document.getElementById("fileInput");

const imageInput =
    document.getElementById("imageInput");

const attachmentPreview =
    document.getElementById("attachmentPreview");

const attachmentName =
    document.getElementById("attachmentName");

const removeAttachment =
    document.getElementById("removeAttachment");

const attachMenu =
    document.getElementById("attachMenu");

const fileOption =
    document.getElementById("fileOption");

const imageOption =
    document.getElementById("imageOption");

let selectedFile = null;
const voiceButton =
document.getElementById("voiceButton");

const voiceScreen =
    document.getElementById("voiceScreen");

const voiceCloseButton =
    document.getElementById("voiceCloseButton");

const voiceOption =
    document.getElementById("voiceOption");

const voiceStatus =
    document.getElementById("voiceStatus");

const voiceSubtitle =
    document.getElementById("voiceSubtitle");

const voiceMicButton =
    document.getElementById("voiceMicButton");

const voiceHint =
    document.getElementById("voiceHint");


if (
    window.location.hash === "#voice" ||
    window.name === "ISMAIL_AI_VOICE"
) {
    document.documentElement.classList.add("voice-window-mode");

    const initializeVoiceWindow = () => {
        if (!voiceScreen) return;

        voiceScreen.removeAttribute("hidden");
        voiceScreen.hidden = false;
        voiceScreen.setAttribute("aria-hidden", "false");

        voiceScreen.style.setProperty("display", "flex", "important");
        voiceScreen.style.setProperty("position", "fixed", "important");
        voiceScreen.style.setProperty("inset", "0", "important");
        voiceScreen.style.setProperty("width", "100vw", "important");
        voiceScreen.style.setProperty("height", "100vh", "important");
        voiceScreen.style.setProperty("background", "#000", "important");
        voiceScreen.style.setProperty("color", "#fff", "important");

        document.body.classList.add("voice-screen-open");

        if (voiceStatus) {
            voiceStatus.textContent = "Voice";
        }

        if (voiceSubtitle) {
            voiceSubtitle.textContent =
                "Tap the microphone to start a voice conversation.";
        }

        if (voiceHint) {
            voiceHint.textContent = "Ready when you are";
        }
    };

    if (document.readyState === "loading") {
        window.addEventListener(
            "DOMContentLoaded",
            initializeVoiceWindow
        );
    } else {
        initializeVoiceWindow();
    }
}






const newChatButton = document.getElementById("newChatButton");
const clearChatButton =
    document.getElementById("clearChatButton");
const welcome = document.getElementById("welcome");

const exportChatButton =
    document.getElementById("exportChatButton");

/* =========================================================
   ISMAIL AI BACKEND CONFIGURATION
   Localhost → LAN → Render fallback
   ========================================================= */

const BACKEND_URLS = [
    "http://127.0.0.1:8000",
    "http://192.168.0.103:8000",
    "https://ismail-ai-api.onrender.com"
];

let BACKEND_BASE_URL = BACKEND_URLS[0];

/* =========================================================
   ISMAIL AI AUTOMATIC BACKEND FAILOVER
   Localhost → LAN → Render
   ========================================================= */
async function requestBackend(url, options = {}) {
    let path = url;
    try {
        const parsed = new URL(url);
        path = parsed.pathname + parsed.search;
    } catch (error) {
        // Keep path unchanged
    }
    let lastError = null;
    for (const backend of BACKEND_URLS) {
        const targetUrl = `${backend}${path}`;
        try {
            const response = await fetch(
                targetUrl,
                options
            );
            BACKEND_BASE_URL = backend;
            console.log(
                '[ISMAIL AI] Backend connected:',
                backend
            );
            return response;
        } catch (error) {
            lastError = error;
            console.warn(
                '[ISMAIL AI] Backend unavailable:',
                backend
            );
        }
    }
    throw lastError || new Error(
        'No ISMAIL AI backend server is available.'
    );
}
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

const googleLoginButton =
    document.getElementById("googleLoginButton");

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

    const response = await requestBackend(
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

    const response = await requestBackend(
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



/* Google Login */
const GOOGLE_CLIENT_ID =
    "272446356006-nic51t1lo64sdf9v8m58rmhn6ha64kub.apps.googleusercontent.com";


async function loginWithGoogleCredential(credential) {

    showAuthMessage("Google Login হচ্ছে...");

    const response = await requestBackend(
        `${BACKEND_BASE_URL}/api/auth/google`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                credential: credential
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
            `Google Login failed: ${response.status}`
        );
    }

    setAuthenticatedSession(data);

    await loadCentralChatHistory();

    startCentralHistorySync();

    return data;
}


function handleGoogleCredentialResponse(response) {

    if (!response || !response.credential) {
        showAuthMessage(
            "Google Login credential পাওয়া যায়নি।"
        );
        return;
    }

    loginWithGoogleCredential(
        response.credential
    ).catch(function (error) {

        showAuthMessage(
            error.message ||
            "Google Login failed."
        );

    });
}


window.initializeGoogleLogin = function () {

    if (!googleLoginButton) {
        return;
    }

    if (
        !window.google ||
        !window.google.accounts ||
        !window.google.accounts.id
    ) {
        setTimeout(function () {
            window.initializeGoogleLogin();
        }, 1000);
        return;
    }

    window.google.accounts.id.initialize({
        client_id: GOOGLE_CLIENT_ID,
        callback: handleGoogleCredentialResponse
    });

    googleLoginButton.innerHTML = "";

    window.google.accounts.id.renderButton(
        googleLoginButton,
        {
            type: "standard",
            theme: "outline",
            size: "large",
            text: "continue_with",
            shape: "rectangular",
            width: 400
        }
    );
};


setTimeout(function () {
    window.initializeGoogleLogin();
}, 1500);


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

        const response = await requestBackend(
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

        const response = await requestBackend(
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

        const response = await requestBackend(
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

        const response = await requestBackend(API_URL, {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: question,
                user_id: USER_ID,
                chat_id: String(currentChat.id)
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
        speak(newAnswer);

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



// =========================================================
// VOICE SCREEN — TASK 1
// =========================================================

function openVoiceScreen() {
    const voiceUrl =
        `${window.location.origin}${window.location.pathname}#voice`;

    const voiceWindow = window.open(
        voiceUrl,
        "ISMAIL_AI_VOICE",
        "width=520,height=900,resizable=yes,scrollbars=no"
    );

    if (voiceWindow) {
        voiceWindow.focus();
    } else {
        console.warn(
            "[ISMAIL AI] Voice window was blocked by the browser."
        );
    }
}


function closeVoiceScreen() {
    if (window.location.hash === "#voice") {
        window.close();
        return;
    }

    if (!voiceScreen) return;

    voiceScreen.setAttribute("hidden", "");
    voiceScreen.setAttribute("aria-hidden", "true");

    document.body.classList.remove("voice-screen-open");
}


if (voiceOption) {
    voiceOption.addEventListener("click", function (event) {

        event.preventDefault();
        event.stopPropagation();

        openVoiceScreen();
    });
}


if (voiceCloseButton) {
    voiceCloseButton.addEventListener("click", function () {

        closeVoiceScreen();

    });
}

let ismailVoiceAI = null;

if (window.ISMAILVoiceAI) {
    ismailVoiceAI = new window.ISMAILVoiceAI();
}

if (voiceMicButton) {
    voiceMicButton.addEventListener("click", async function () {

        if (!ismailVoiceAI) {
            if (voiceStatus) {
                voiceStatus.textContent = "Unavailable";
            }

            if (voiceHint) {
                voiceHint.textContent =
                    "Voice engine is not available.";
            }

            return;
        }

        if (ismailVoiceAI.isListening) {
            ismailVoiceAI.stop();

            if (voiceStatus) {
                voiceStatus.textContent = "Ready";
            }

            if (voiceSubtitle) {
                voiceSubtitle.textContent =
                    "Tap the microphone to speak.";
            }

            if (voiceHint) {
                voiceHint.textContent =
                    "Microphone is off.";
            }

            return;
        }

        const started = await ismailVoiceAI.start();

        if (started) {
            if (voiceStatus) {
                voiceStatus.textContent = "Listening";
            }

            if (voiceSubtitle) {
                voiceSubtitle.textContent =
                    "Speak now...";
            }

            if (voiceHint) {
                voiceHint.textContent =
                    "Microphone is active.";
            }
        }

    });
}

document.addEventListener("keydown", function (event) {

    if (
        event.key === "Escape" &&
        voiceScreen &&
        !voiceScreen.hasAttribute("hidden")
    ) {
        closeVoiceScreen();
    }

});


// =========================================================
// FILE UPLOAD + ATTACH MENU
// =========================================================

const attachMenuElement =
    document.getElementById("attachMenu");

const fileOptionElement =
    document.getElementById("fileOption");



if (attachButton && attachMenuElement) {

    // + button
    attachButton.addEventListener("click", function (event) {

        event.preventDefault();
        event.stopPropagation();

        const isHidden =
            attachMenuElement.hasAttribute("hidden");

        if (isHidden) {
            attachMenuElement.removeAttribute("hidden");
        } else {
            attachMenuElement.setAttribute("hidden", "");
        }
    });


    // 📎 File / PDF
    if (fileOptionElement && fileInput) {

        fileOptionElement.addEventListener(
            "click",
            function (event) {

                event.preventDefault();
                event.stopPropagation();

                attachMenuElement.setAttribute(
                    "hidden",
                    ""
                );

                fileInput.accept =
                    ".pdf,.doc,.docx,.txt";

                fileInput.click();
            }
        );

    


        // File selected
        fileInput.addEventListener(
            "change",
            function () {

                const file =
                    fileInput.files &&
                    fileInput.files[0];

                if (!file) {
                    return;
                }


                const maxSize =
                    10 * 1024 * 1024;


                if (file.size > maxSize) {

                    alert(
                        "File is too large. Maximum size is 10 MB."
                    );

                    fileInput.value = "";

                    return;
                }


                // Keep file separately.
                // Never put PDF text into message box.
                selectedFile = file;


                // Show attachment preview
                if (attachmentPreview) {
                    attachmentPreview.hidden = false;
                }

                if (attachmentName) {
                    attachmentName.textContent =
                        file.name;
                }


                messageInput.style.height =
                    "auto";

                messageInput.focus();
            }
        );
    }







    // Image selected
    if (imageInput) {
        imageInput.addEventListener("change", function () {

            const file =
                imageInput.files &&
                imageInput.files[0];

            if (!file) {
                return;
            }

            const maxSize =
                10 * 1024 * 1024;

            if (file.size > maxSize) {
                alert(
                    "Image is too large. Maximum size is 10 MB."
                );
                imageInput.value = "";
                return;
            }

            selectedFile = file;

            if (attachmentPreview) {
                attachmentPreview.hidden = false;
            }

            if (attachmentName) {
                attachmentName.textContent =
                    file.name;
            }

            messageInput.style.height =
                "auto";

            messageInput.focus();
        });
    }


    // Outside click
    document.addEventListener(
        "click",
        function (event) {

            if (
                !attachMenuElement.contains(
                    event.target
                ) &&
                event.target !== attachButton
            ) {

                attachMenuElement.setAttribute(
                    "hidden",
                    ""
                );
            }
        }
    );
}




// =========================================================
// REMOVE ATTACHMENT
// =========================================================

if (removeAttachment) {

    removeAttachment.addEventListener(
        "click",
        function (event) {

            event.preventDefault();
            event.stopPropagation();

            selectedFile = null;

            if (fileInput) {
                fileInput.value = "";
            }

            if (attachmentPreview) {
                attachmentPreview.hidden = true;
            }

            if (attachmentName) {
                attachmentName.textContent = "";
            }
        }
    );
}




async function sendMessage() {

    const message =
        messageInput.value.trim();

    if (
        (!message && !selectedFile) ||
        sendButton.disabled
    ) {
        return;
    }

    if (currentChat.title === "New chat") {
        currentChat.id = Date.now();
    }

    setLoading(true);
    showLoading();

    try {

        const session =
            await getSession();

        let fileContext = "";
        let imageData = "";
        let imageType = "";
        let displayMessage = message;


// =================================================
// FILE MODE
// =================================================

if (selectedFile) {

    const isImage =
        selectedFile.type.startsWith("image/");


    // =================================================
    // IMAGE MODE
    // =================================================

    if (isImage) {

        imageType =
            selectedFile.type;

        imageData =
            await new Promise((resolve, reject) => {

                const reader =
                    new FileReader();

                reader.onload = () => {

                    const result =
                        String(reader.result || "");

                    const commaIndex =
                        result.indexOf(",");

                    resolve(
                        commaIndex >= 0
                            ? result.slice(commaIndex + 1)
                            : result
                    );
                };

                reader.onerror = () => {

                    reject(
                        new Error(
                            "Unable to read image."
                        )
                    );
                };

                reader.readAsDataURL(
                    selectedFile
                );
            });


        displayMessage =
            `🖼️ ${selectedFile.name}\n${message || "Analyze this image."}`;


        addMessage(
            displayMessage,
            "user"
        );


        syncChatMessage(
            "user",
            displayMessage
        );


        selectedFile = null;


        if (fileInput) {
            fileInput.value = "";
        }


        if (attachmentPreview) {
            attachmentPreview.hidden = true;
        }


    } else {


        // =================================================
        // DOCUMENT / FILE MODE
        // =================================================

        const formData =
            new FormData();


        formData.append(
            "file",
            selectedFile
        );


        const uploadResponse =
            await requestBackend(
                `${BACKEND_BASE_URL}/api/file/upload`,
                {
                    method: "POST",

                    headers: {
                        "Authorization":
                            `Bearer ${session.token}`
                    },

                    body: formData
                }
            );


        if (!uploadResponse.ok) {

            let errorMessage =
                "File upload failed.";

            try {

                const errorData =
                    await uploadResponse.json();

                errorMessage =
                    errorData.detail ||
                    errorMessage;

            } catch (error) {
                // Ignore JSON parsing error.
            }


            throw new Error(
                errorMessage
            );
        }


        const fileData =
            await uploadResponse.json();


        fileContext =
            String(fileData.text || "");


        displayMessage =
            `📎 ${fileData.filename}\n${message || "Analyze this file."}`;


        addMessage(
            displayMessage,
            "user"
        );


        syncChatMessage(
            "user",
            displayMessage
        );


        selectedFile = null;


        if (fileInput) {
            fileInput.value = "";
        }


        if (attachmentPreview) {
            attachmentPreview.hidden = true;
        }
    }


} else {

    addMessage(
        message,
        "user"
    );


    syncChatMessage(
        "user",
        message
    );
}


        messageInput.value = "";

        messageInput.style.height =
            "auto";


        // =================================================
        // SEND TO ISMAIL AI
        // =================================================

        const response =
            await requestBackend(
                API_URL,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json",

                        "Authorization":
                            `Bearer ${session.token}`
                    },

                    body: JSON.stringify({

                        message:
                            message ||
                            (imageData
                                ? "Analyze this image."
                                : "Analyze this file."),

                        user_id:
                            USER_ID,

                        chat_id:
                            String(currentChat.id),

                        file_context:
                            fileContext,

                        image_data:
                            imageData,

                        image_type:
                            imageType
                    })
                }
            );


        if (!response.ok) {

            let errorMessage =
                `Server error: ${response.status}`;

            try {

                const errorData =
                    await response.json();

                errorMessage =
                    errorData.detail ||
                    errorMessage;

            } catch (error) {
                // Ignore JSON parsing error.
            }

            throw new Error(
                errorMessage
            );
        }


        const data =
            await response.json();


        if (
            data.action &&
            data.action.action === "open_url" &&
            data.action.url
        ) {

            window.open(
                data.action.url,
                "_blank"
            );

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

        // Automatic AI voice disabled
        // speakAIResponse(assistantMessage);


        saveCurrentChat();


    } catch (error) {

        console.error(
            "File/Chat Error:",
            error
        );

        removeLoading();


        addMessage(
            `❌ ${error.message}`,
            "ai"
        );

    } finally {

        setLoading(false);

        messageInput.focus();
    }
}



/* Send button */

sendButton.addEventListener("click", sendMessage);


/* =========================
   ISMAIL AI VOICE SYSTEM
========================= */

let recognition = null;
let isListening = false;

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

if (voiceButton && SpeechRecognition) {

    console.log("SpeechRecognition:", window.SpeechRecognition);
    console.log("webkitSpeechRecognition:", window.webkitSpeechRecognition);

    alert(
        "SpeechRecognition = " +
        (window.SpeechRecognition ? "YES" : "NO") +
        "\nwebkitSpeechRecognition = " +
        (window.webkitSpeechRecognition ? "YES" : "NO")
    );

    recognition = new SpeechRecognition();

    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "bn-BD";

    recognition.onstart = function () {

        isListening = true;

        voiceButton.classList.add("recording");
        voiceButton.textContent = "🔴";
        voiceButton.title = "Listening...";
    };

    recognition.onresult = function (event) {

        const transcript =
            event.results[0][0].transcript;

        messageInput.value = transcript;

        messageInput.style.height = "auto";

        messageInput.style.height =
            `${Math.min(messageInput.scrollHeight, 150)}px`;

        voiceButton.classList.remove("recording");
        voiceButton.textContent = "🎙️";
        voiceButton.title = "Voice";

        isListening = false;

        /*
         * আপনার কথা বুঝে সরাসরি ISMAIL AI-তে পাঠাবে
         */
        sendMessage();
    };

    recognition.onerror = function (event) {

        if (window.AndroidVoice) return;

        console.error(
            "Voice recognition error:",
            event.error
        );

        isListening = false;

        voiceButton.classList.remove("recording");

        voiceButton.textContent = "🎙️";
        voiceButton.title = "Voice";
    };

    recognition.onend = function () {

        isListening = false;

        voiceButton.classList.remove("recording");

        voiceButton.textContent = "🎙️";
        voiceButton.title = "Voice";
    };

voiceButton.addEventListener(
    "click",
    function () {

        if (
            window.AndroidVoice &&
            window.AndroidVoice.startVoiceRecognition
        ) {

            window.AndroidVoice.startVoiceRecognition();
            return;

        }

        try {

            recognition.start();

        } catch (error) {

            console.error(error);

        }

    }
);

} else {

    if (voiceButton) {

        voiceButton.style.display = "none";
    }

}


/* =========================
   ISMAIL AI SPEAK RESPONSE
   DISABLED
========================= */

function speakAIResponse(text) {

    // Stop any speech that may already be playing
    if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel();
    }

    // Automatic AI response voice disabled
    return;
}




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


function speak(text) {
    if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel();
    }

    return;
}


window.receiveNativeVoice = function (text) {

    if (!text) return;

    messageInput.value = text;

    messageInput.style.height = "auto";
    messageInput.style.height =
        `${Math.min(messageInput.scrollHeight,150)}px`;

    sendMessage();

};





// IMAGE PICKER DEBUG
document.getElementById('imageOption')?.addEventListener('click', function () { console.log('IMAGE LABEL CLICKED'); });


