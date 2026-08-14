document.addEventListener('DOMContentLoaded', () => {
    // --- State & DOM Elements ---
    let sessionId = localStorage.getItem('hades_session_id') || null;
    let userName = localStorage.getItem('hades_user_name') || null;
    let isProcessing = false;
    let activeMissionId = null;

    // Settings State
    let devMode = localStorage.getItem('hades_dev_mode') === 'true';
    let wakeWord = localStorage.getItem('hades_wake_word') || 'Hades';

    const firstLaunchOverlay = document.getElementById('first-launch-overlay');
    const launchText2 = document.getElementById('launch-text-2');
    const nameInputContainer = document.getElementById('name-input-container');
    const userNameInput = document.getElementById('user-name-input');
    const saveNameBtn = document.getElementById('save-name-btn');
    const chatContainer = document.getElementById('chat-container');
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const hadesCore = document.getElementById('hades-core');
    const voiceStatus = document.getElementById('voice-status-indicator');
    
    // UI Elements for Execution & Settings
    const contextualMissionWidget = document.getElementById('contextual-mission-widget');
    const widgetMissionTitle = document.getElementById('widget-mission-title');
    const executionLog = document.getElementById('widget-execution-log');
    
    const navSettings = document.getElementById('nav-settings');
    const settingsModal = document.getElementById('settings-modal');
    const closeSettingsBtn = document.getElementById('close-settings-btn');
    const saveSettingsBtn = document.getElementById('save-settings-btn');
    const testApiBtn = document.getElementById('test-api-btn');
    const apiTestStatus = document.getElementById('api-test-status');

    // Load initial settings UI state
    document.getElementById('setting-wake-word').value = wakeWord;
    document.getElementById('setting-dev-mode').checked = devMode;

    // --- Visual State Management ---
    function setHadesState(state) {
        hadesCore.className = `hades-visual-presence large ${state}`;
    }

    // --- Settings UI ---
    navSettings.addEventListener('click', (e) => {
        e.preventDefault();
        settingsModal.style.display = 'flex';
    });

    closeSettingsBtn.addEventListener('click', () => {
        settingsModal.style.display = 'none';
        apiTestStatus.innerText = '';
    });

    testApiBtn.addEventListener('click', async () => {
        const geminiKey = document.getElementById('setting-gemini-key').value;
        if (!geminiKey) {
            apiTestStatus.className = 'test-status error';
            apiTestStatus.innerText = "Key is required to test.";
            return;
        }

        apiTestStatus.className = 'test-status';
        apiTestStatus.innerText = "Testing connection...";

        try {
            const res = await fetch('/api/settings/ai/test', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ gemini_key: geminiKey })
            });
            const data = await res.json();
            
            if (data.status === "CONNECTED") {
                apiTestStatus.className = 'test-status';
                apiTestStatus.innerText = "Connection Successful.";
            } else {
                apiTestStatus.className = 'test-status error';
                apiTestStatus.innerText = `${data.status}: ${data.reason}`;
            }
        } catch (e) {
            apiTestStatus.className = 'test-status error';
            apiTestStatus.innerText = `Network Error.`;
        }
    });

    saveSettingsBtn.addEventListener('click', async () => {
        const geminiKey = document.getElementById('setting-gemini-key').value;
        
        wakeWord = document.getElementById('setting-wake-word').value.trim() || 'Hades';
        devMode = document.getElementById('setting-dev-mode').checked;
        
        localStorage.setItem('hades_wake_word', wakeWord);
        localStorage.setItem('hades_dev_mode', devMode);

        try {
            if (geminiKey) {
                await fetch('/api/settings/ai', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ gemini_key: geminiKey })
                });
            }
            settingsModal.style.display = 'none';
            appendMessage('hades', 'Systems updated. New configuration applied.');
        } catch (e) {
            console.error(e);
        }
    });

    // --- SSE Event Listener ---
    function initSSE() {
        const evtSource = new EventSource('/api/events');
        
        evtSource.onmessage = (e) => {
            const data = JSON.parse(e.data);
            handleBackgroundEvent(data);
        };
    }

    function logExecutionEvent(text, type = "info") {
        const div = document.createElement('div');
        div.className = `execution-event ${type}`;
        div.innerHTML = `<i class="fa-solid fa-chevron-right"></i> ${text}`;
        executionLog.appendChild(div);
        executionLog.scrollTop = executionLog.scrollHeight;
    }

    function handleBackgroundEvent(event) {
        const type = event.type;
        const payload = event.data;
        
        if (type === 'MISSION_STATUS_UPDATED') {
            activeMissionId = payload.mission_id;
            if (payload.status === 'EXECUTING') {
                setHadesState('executing');
                contextualMissionWidget.style.display = 'block';
                widgetMissionTitle.innerText = `Mission Executing`;
                logExecutionEvent("Execution Brain took control.", "info");
            }
        } else if (type === 'PLAN_CREATED') {
            logExecutionEvent(`Plan created with ${payload.tasks} task(s).`);
        } else if (type === 'TASK_STARTED') {
            logExecutionEvent(`Started task: ${payload.objective}`);
        } else if (type === 'CAPABILITY_SELECTED') {
            logExecutionEvent(`Using capability: ${payload.adapter}`);
        } else if (type === 'TASK_COMPLETED') {
            logExecutionEvent(`Task completed: ${payload.result}`);
        } else if (type === 'TASK_FAILED') {
            logExecutionEvent(`Task failed: ${payload.error}`, "error");
        } else if (type === 'USER_INTERVENTION_REQUIRED') {
            logExecutionEvent(`Blocker Hit: ${payload.details}`, "error");
            setHadesState('error');
            appendMessage('hades', `**I've hit a blocker.**\n\n${payload.details}\n\nFallback protocols available.`);
        } else if (type === 'MISSION_COMPLETED') {
            setHadesState('idle');
            appendMessage('hades', `**Mission Complete.**\n\n${payload.result}`);
            logExecutionEvent(`Mission Delivered.`, "info");
            setTimeout(() => {
                contextualMissionWidget.style.display = 'none';
                executionLog.innerHTML = '';
            }, 8000); // Hide after 8s
        }
    }

    // --- First Launch Experience ---
    function checkFirstLaunch() {
        if (!userName) {
            firstLaunchOverlay.style.display = 'flex';
            setTimeout(() => { launchText2.style.display = 'block'; }, 1500);
            setTimeout(() => { nameInputContainer.style.display = 'flex'; userNameInput.focus(); }, 3000);
        } else {
            initWorkspace();
        }
    }

    saveNameBtn.addEventListener('click', saveName);
    userNameInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') saveName();
    });

    function saveName() {
        const val = userNameInput.value.trim();
        if (val) {
            userName = val;
            localStorage.setItem('hades_user_name', userName);
            firstLaunchOverlay.style.opacity = '0';
            setTimeout(() => {
                firstLaunchOverlay.style.display = 'none';
                initWorkspace();
                appendMessage('hades', `Good to meet you, ${userName}.\n\nWhat are we working on?`);
            }, 1000);
        }
    }

    function initWorkspace() {
        initSSE(); // Connect to Event Bus
        initVoice(); // Connect continuous listener
    }

    // --- Chat Logic ---
    function appendMessage(sender, text, isError = false, devError = null) {
        const div = document.createElement('div');
        div.className = `message msg-${sender}`;
        div.innerHTML = marked.parse(text);
        
        if (isError && devMode && devError) {
            const errDiv = document.createElement('div');
            errDiv.className = 'dev-error-block';
            errDiv.innerHTML = `<strong>Developer Mode Exception:</strong><br/>Type: ${devError.type}<br/>Provider: ${devError.provider}<br/>Reason: ${devError.reason}`;
            div.appendChild(errDiv);
        }

        chatContainer.appendChild(div);
        scrollToBottom();
    }

    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    async function sendMessage(text) {
        if (!text.trim() || isProcessing) return;
        
        isProcessing = true;
        appendMessage('user', text);
        chatInput.value = '';
        
        setHadesState('processing');

        try {
            const payload = { message: text, user_name: userName };
            if (sessionId) payload.session_id = sessionId;

            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await res.json();
            
            if (data.session_id) {
                sessionId = data.session_id;
                localStorage.setItem('hades_session_id', sessionId);
            }

            appendMessage('hades', data.response, data.is_error, data.developer_error);
            
            if (data.mission_status !== "LOCKED" && data.mission_status !== "EXECUTING") {
                setHadesState('idle');
            }
            
            isProcessing = false;
        } catch (err) {
            console.error("API Error", err);
            setHadesState('error');
            appendMessage('hades', "I encountered an error connecting to my core processing system.");
            isProcessing = false;
        }
    }

    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage(chatInput.value);
        }
    });

    // Handle send btn if they manually type and click it
    chatInput.addEventListener('input', () => {
        sendBtn.style.display = chatInput.value.trim().length > 0 ? 'block' : 'none';
    });
    sendBtn.addEventListener('click', () => {
        sendMessage(chatInput.value);
        sendBtn.style.display = 'none';
    });

    // --- Voice Recognition & TTS ---
    let recognition = null;
    let shouldListen = true;
    
    function speakText(text) {
        if (!('speechSynthesis' in window)) return;
        const cleanText = text.replace(/[*_#`~]/g, '');
        window.speechSynthesis.cancel(); // Barge-in: Stop whatever is currently playing
        const utterance = new SpeechSynthesisUtterance(cleanText);
        utterance.rate = 1.05;
        utterance.pitch = 0.9;
        const voices = window.speechSynthesis.getVoices();
        const enVoice = voices.find(v => v.lang.startsWith('en') && v.name.includes('Male')) || voices.find(v => v.lang.startsWith('en'));
        if (enVoice) utterance.voice = enVoice;
        
        window.speechSynthesis.speak(utterance);
    }

    // Auto-Listening continuous loop
    function initVoice() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = false;
            
            recognition.onstart = () => {
                if (!isProcessing && hadesCore.className.indexOf('executing') === -1) {
                    setHadesState('idle');
                }
                voiceStatus.classList.add('visible');
                voiceStatus.innerHTML = `<div class="pulse-dot"></div> Listening for "${wakeWord}"`;
            };
            
            recognition.onresult = (event) => {
                const results = event.results;
                const transcript = results[results.length - 1][0].transcript.trim();
                
                // Barge-in if the user speaks while TTS is playing
                if (transcript.length > 0) {
                    window.speechSynthesis.cancel();
                }

                // Check for wake word
                const lowerTranscript = transcript.toLowerCase();
                const lowerWake = wakeWord.toLowerCase();
                
                if (lowerTranscript.includes(lowerWake)) {
                    // Extract command after wake word
                    const wakeIndex = lowerTranscript.indexOf(lowerWake);
                    const command = transcript.substring(wakeIndex + wakeWord.length).trim();
                    
                    if (command.length > 0) {
                        chatInput.value = command;
                        sendMessage(command);
                    }
                }
            };
            
            recognition.onend = () => {
                if (shouldListen) {
                    // Automatically restart listening if we shouldn't have stopped
                    try {
                        recognition.start();
                    } catch (e) {
                        // ignore if already started
                    }
                } else {
                    voiceStatus.classList.remove('visible');
                }
            };

            // Start it
            try {
                recognition.start();
            } catch (e) {}
        }
    }

    // Wrap the send message response to trigger TTS
    const originalAppend = appendMessage;
    appendMessage = function(sender, text, isErr, devErr) {
        originalAppend(sender, text, isErr, devErr);
        if (sender === 'hades') {
            speakText(text);
        }
    };

    // --- Init ---
    checkFirstLaunch();
});

