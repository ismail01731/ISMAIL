class ISMAILVoiceAI {
    constructor() {
        this.recognition = null;
        this.isListening = false;
        this.supported = false;
        this.textCallback = null;
        const SpeechRecognition =
            window.SpeechRecognition ||
            window.webkitSpeechRecognition;
        if (SpeechRecognition) {
            this.supported = true;
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = "bn-BD";
            this.recognition.onstart = () => {
                this.isListening = true;
                console.log(
                    "ISMAIL AI Voice: microphone started"
                );
            };
            this.recognition.onresult = (event) => {
                const result =
                    event.results[0][0].transcript;
                console.log(
                    "ISMAIL AI Voice heard:",
                    result
                );
                if (this.textCallback) {
                    this.textCallback(result);
                }
            };
            this.recognition.onerror = (event) => {
                console.error(
                    "ISMAIL AI Voice error:",
                    event.error
                );
                this.isListening = false;
            };
            this.recognition.onend = () => {
                this.isListening = false;
                console.log(
                    "ISMAIL AI Voice: microphone stopped"
                );
            };
        }
    }
    start() {
        if (!this.supported) {
            console.error(
                "Speech Recognition is not supported by this browser."
            );
            return false;
        }
        if (this.isListening) {
            return true;
        }
        try {
            this.recognition.start();
            return true;
        } catch (error) {
            console.error(
                "ISMAIL AI Voice start error:",
                error
            );
            return false;
        }
    }
    stop() {
        if (
            !this.supported ||
            !this.recognition ||
            !this.isListening
        ) {
            return;
        }
        this.recognition.stop();
    }
    setLanguage(language) {
        if (this.recognition && language) {
            this.recognition.lang = language;
        }
    }
    onText(callback) {
        if (typeof callback === "function") {
            this.textCallback = callback;
        }
    }
}
window.ISMAILVoiceAI = ISMAILVoiceAI;
