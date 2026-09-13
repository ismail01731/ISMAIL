class ISMAILVoiceAI {
    constructor() {
        this.isListening = false;
        this.websocket = null;
        this.mediaStream = null;
        this.audioContext = null;
        this.sourceNode = null;
        this.processorNode = null;
        this.textCallback = null;

        this.sampleRate = 16000;
        this.channels = 1;
        this.audioStarted = false;
    }

    async start() {
        if (this.isListening) {
            return true;
        }

        try {
            if (
                !navigator.mediaDevices ||
                !navigator.mediaDevices.getUserMedia
            ) {
                throw new Error(
                    "Microphone access is not supported."
                );
            }

            const session = await getSession();

            if (
                !session ||
                !session.token ||
                !session.user_id
            ) {
                throw new Error(
                    "Authentication session is unavailable."
                );
            }

            if (
                typeof currentChat === "undefined" ||
                !currentChat ||
                !currentChat.id
            ) {
                throw new Error(
                    "Active chat is unavailable."
                );
            }

            this.mediaStream =
                await navigator.mediaDevices.getUserMedia({
                    audio: {
                        channelCount: 1,
                        echoCancellation: true,
                        noiseSuppression: true,
                        autoGainControl: true
                    }
                });

            const wsUrl = new URL(
                "/ws/voice",
                window.location.origin
            );

            wsUrl.protocol =
                window.location.protocol === "https:"
                    ? "wss:"
                    : "ws:";

            this.websocket =
                new WebSocket(wsUrl.toString());

            await new Promise(
                (resolve, reject) => {
                    const timeout =
                        setTimeout(() => {
                            reject(
                                new Error(
                                    "Voice WebSocket connection timed out."
                                )
                            );
                        }, 10000);

                    this.websocket.onopen = () => {
                        clearTimeout(timeout);
                        resolve();
                    };

                    this.websocket.onerror = () => {
                        clearTimeout(timeout);
                        reject(
                            new Error(
                                "Voice WebSocket connection failed."
                            )
                        );
                    };
                }
            );

            this.websocket.onmessage =
                (event) => {
                    this.handleServerMessage(
                        event
                    );
                };

            this.websocket.onclose = () => {
                console.log(
                    "ISMAIL AI Voice: WebSocket closed"
                );

                this.audioStarted = false;

                if (this.isListening) {
                    this.stop(false);
                }
            };

            this.websocket.onerror = (
                error
            ) => {
                console.error(
                    "ISMAIL AI Voice WebSocket error:",
                    error
                );
            };

            this.websocket.send(
                JSON.stringify({
                    type: "auth",
                    token: session.token,
                    chat_id: String(
                        currentChat.id
                    )
                })
            );

            await this.waitForAuth();

            this.websocket.send(
                JSON.stringify({
                    type: "audio_start",
                    format: "pcm16",
                    sample_rate: this.sampleRate,
                    channels: this.channels
                })
            );

            await this.waitForAudioStart();

            this.audioContext =
                new AudioContext();

            if (
                this.audioContext.state ===
                "suspended"
            ) {
                await this.audioContext.resume();
            }

            this.sourceNode =
                this.audioContext.createMediaStreamSource(
                    this.mediaStream
                );

            this.processorNode =
                this.audioContext.createScriptProcessor(
                    4096,
                    1,
                    1
                );

            this.processorNode.onaudioprocess =
                (event) => {
                    if (
                        !this.isListening ||
                        !this.audioStarted ||
                        !this.websocket ||
                        this.websocket.readyState !==
                            WebSocket.OPEN
                    ) {
                        return;
                    }

                    const input =
                        event.inputBuffer.getChannelData(
                            0
                        );

                    const pcm16 =
                        this.convertToPCM16(
                            input,
                            this.audioContext.sampleRate
                        );

                    if (!pcm16.length) {
                        return;
                    }

                    const base64 =
                        this.arrayBufferToBase64(
                            pcm16.buffer
                        );

                    this.websocket.send(
                        JSON.stringify({
                            type: "audio",
                            format: "pcm16",
                            sample_rate:
                                this.sampleRate,
                            data: base64
                        })
                    );
                };

            this.sourceNode.connect(
                this.processorNode
            );

            this.processorNode.connect(
                this.audioContext.destination
            );

            this.isListening = true;

            console.log(
                "ISMAIL AI Voice: microphone started"
            );

            return true;

        } catch (error) {
            console.error(
                "ISMAIL AI Voice start error:",
                error
            );

            this.cleanup();

            return false;
        }
    }

    stop(sendAudioEnd = true) {
        if (!this.isListening && !this.mediaStream) {
            return;
        }

        this.isListening = false;

        if (
            sendAudioEnd &&
            this.audioStarted &&
            this.websocket &&
            this.websocket.readyState ===
                WebSocket.OPEN
        ) {
            this.websocket.send(
                JSON.stringify({
                    type: "audio_end"
                })
            );
        }

        this.audioStarted = false;

        this.cleanup();

        console.log(
            "ISMAIL AI Voice: microphone stopped"
        );
    }

    handleServerMessage(event) {
        let message;

        try {
            message = JSON.parse(
                event.data
            );
        } catch (error) {
            console.error(
                "Invalid voice server message:",
                error
            );
            return;
        }

        console.log(
            "ISMAIL AI Voice server:",
            message
        );

        if (message.type === "transcript") {
            if (
                message.final &&
                message.text &&
                this.textCallback
            ) {
                this.textCallback(
                    message.text
                );
            }

            return;
        }

        if (message.type === "error") {
            console.error(
                "ISMAIL AI Voice server error:",
                message.code,
                message.message
            );

            return;
        }

        if (message.type === "audio_committed") {
            console.log(
                "ISMAIL AI Voice audio committed:",
                message
            );
        }
    }

    waitForAuth() {
        return new Promise(
            (resolve, reject) => {
                const timeout =
                    setTimeout(() => {
                        reject(
                            new Error(
                                "Voice authentication timed out."
                            )
                        );
                    }, 10000);

                const handler = (
                    event
                ) => {
                    let message;

                    try {
                        message =
                            JSON.parse(
                                event.data
                            );
                    } catch (error) {
                        return;
                    }

                    if (
                        message.type ===
                        "auth_ok"
                    ) {
                        clearTimeout(
                            timeout
                        );

                        this.websocket.removeEventListener(
                            "message",
                            handler
                        );

                        resolve();
                    }

                    if (
                        message.type ===
                        "error"
                    ) {
                        clearTimeout(
                            timeout
                        );

                        this.websocket.removeEventListener(
                            "message",
                            handler
                        );

                        reject(
                            new Error(
                                message.message ||
                                "Voice authentication failed."
                            )
                        );
                    }
                };

                this.websocket.addEventListener(
                    "message",
                    handler
                );
            }
        );
    }

    waitForAudioStart() {
        return new Promise(
            (resolve, reject) => {
                const timeout =
                    setTimeout(() => {
                        reject(
                            new Error(
                                "Voice audio session start timed out."
                            )
                        );
                    }, 10000);

                const handler = (
                    event
                ) => {
                    let message;

                    try {
                        message =
                            JSON.parse(
                                event.data
                            );
                    } catch (error) {
                        return;
                    }

                    if (
                        message.type ===
                        "audio_started"
                    ) {
                        clearTimeout(
                            timeout
                        );

                        this.websocket.removeEventListener(
                            "message",
                            handler
                        );

                        this.audioStarted =
                            true;

                        resolve();
                    }

                    if (
                        message.type ===
                        "error"
                    ) {
                        clearTimeout(
                            timeout
                        );

                        this.websocket.removeEventListener(
                            "message",
                            handler
                        );

                        reject(
                            new Error(
                                message.message ||
                                "Voice audio start failed."
                            )
                        );
                    }
                };

                this.websocket.addEventListener(
                    "message",
                    handler
                );
            }
        );
    }

    convertToPCM16(
        float32Array,
        inputSampleRate
    ) {
        if (
            inputSampleRate ===
            this.sampleRate
        ) {
            const output =
                new Int16Array(
                    float32Array.length
                );

            for (
                let i = 0;
                i < float32Array.length;
                i++
            ) {
                const sample =
                    Math.max(
                        -1,
                        Math.min(
                            1,
                            float32Array[i]
                        )
                    );

                output[i] =
                    sample < 0
                        ? sample * 0x8000
                        : sample * 0x7fff;
            }

            return output;
        }

        const ratio =
            inputSampleRate /
            this.sampleRate;

        const outputLength =
            Math.floor(
                float32Array.length /
                ratio
            );

        const output =
            new Int16Array(
                outputLength
            );

        for (
            let i = 0;
            i < outputLength;
            i++
        ) {
            const position =
                i * ratio;

            const index =
                Math.floor(position);

            const nextIndex =
                Math.min(
                    index + 1,
                    float32Array.length - 1
                );

            const fraction =
                position - index;

            const sample =
                float32Array[index] *
                    (1 - fraction) +
                float32Array[nextIndex] *
                    fraction;

            const clamped =
                Math.max(
                    -1,
                    Math.min(
                        1,
                        sample
                    )
                );

            output[i] =
                clamped < 0
                    ? clamped * 0x8000
                    : clamped * 0x7fff;
        }

        return output;
    }

    arrayBufferToBase64(
        buffer
    ) {
        const bytes =
            new Uint8Array(buffer);

        const chunkSize = 0x8000;

        let binary = "";

        for (
            let i = 0;
            i < bytes.length;
            i += chunkSize
        ) {
            const chunk =
                bytes.subarray(
                    i,
                    Math.min(
                        i + chunkSize,
                        bytes.length
                    )
                );

            binary += String.fromCharCode(
                ...chunk
            );
        }

        return btoa(binary);
    }

    onText(callback) {
        if (
            typeof callback ===
            "function"
        ) {
            this.textCallback =
                callback;
        }
    }

    cleanup() {
        if (this.processorNode) {
            this.processorNode.onaudioprocess =
                null;

            try {
                this.processorNode.disconnect();
            } catch (error) {}

            this.processorNode = null;
        }

        if (this.sourceNode) {
            try {
                this.sourceNode.disconnect();
            } catch (error) {}

            this.sourceNode = null;
        }

        if (this.mediaStream) {
            this.mediaStream
                .getTracks()
                .forEach(
                    (track) => {
                        track.stop();
                    }
                );

            this.mediaStream = null;
        }

        if (this.audioContext) {
            try {
                this.audioContext.close();
            } catch (error) {}

            this.audioContext = null;
        }

        if (
            this.websocket &&
            (
                this.websocket.readyState ===
                    WebSocket.OPEN ||
                this.websocket.readyState ===
                    WebSocket.CONNECTING
            )
        ) {
            try {
                this.websocket.close();
            } catch (error) {}
        }

        this.websocket = null;
        this.audioStarted = false;
    }
}

window.ISMAILVoiceAI =
    ISMAILVoiceAI;
    