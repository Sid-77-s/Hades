document.addEventListener("DOMContentLoaded", () => {
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const chatContainer = document.getElementById('chat-container');
    const visualPresence = document.querySelector('.hades-visual-presence');
    const greetingText = document.getElementById('greeting-text');
    const userProfileContainer = document.getElementById('user-profile-container');
    const profileName = document.getElementById('profile-name');
    const userAvatar = document.getElementById('user-avatar');
    
    let sessionId = null;
    let userName = localStorage.getItem('user_name');
    let appState = 'IDLE'; // IDLE, AWAITING_NAME, PROCESSING, RESPONDING
    
    // Setup initial state
    if (userName) {
        setUserNameUI(userName);
    } else {
        appState = 'AWAITING_NAME';
        setTimeout(() => {
            appendMessage('hades', "Hey. I'm Hades.");
            setTimeout(() => {
                appendMessage('hades', "Before we start, what should I call you?");
                speakText("Hey. I'm Hades. Before we start, what should I call you?");
            }, 1000);
        }, 500);
    }

    // Auto-resize textarea
    chatInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
        if (this.value === '') {
            this.style.height = 'auto'; // reset
        }
    });

    // Handle Enter and Shift+Enter
    chatInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleUserInput();
        }
    });

    sendBtn.addEventListener('click', () => handleUserInput());

    function setUserNameUI(name) {
        greetingText.innerText = `Good evening, ${name}.`;
        profileName.innerText = name;
        userAvatar.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=random`;
        userProfileContainer.style.display = 'flex';
    }

    async function handleUserInput(text = null) {
        const messageText = text || chatInput.value.trim();
        if (!messageText) return;

        // Display user message
        appendMessage('user', messageText);
        if (!text) {
            chatInput.value = '';
            chatInput.style.height = 'auto';
        }

        visualPresence.classList.add('minimized');

        // Handle Onboarding Name Capture
        if (appState === 'AWAITING_NAME') {
            userName = messageText;
            localStorage.setItem('user_name', userName);
            setUserNameUI(userName);
            appState = 'IDLE';
            
            setTimeout(() => {
                appendMessage('hades', `Good to meet you, ${userName}.`);
                setTimeout(() => {
                    appendMessage('hades', "What are we working on?");
                    speakText(`Good to meet you, ${userName}. What are we working on?`);
                }, 1000);
            }, 500);
            return;
        }

        // Send to backend
        sendToPartnerBrain(messageText);
    }

    async function sendToPartnerBrain(text) {
        appState = 'PROCESSING';
        visualPresence.classList.add('processing');
        scrollToBottom();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: text,
                    session_id: sessionId,
                    user_name: userName
                })
            });

            if (!response.ok) {
                throw new Error("API Error");
            }

            const data = await response.json();
            sessionId = data.session_id;

            appState = 'RESPONDING';
            visualPresence.classList.remove('processing');
            
            // Check for specific graceful error
            if (data.is_error) {
                appendMessage('hades', data.response);
                appState = 'IDLE';
                return;
            }
            
            appendMessage('hades', data.response);
            speakText(data.response);
            
            if(data.mission_status === 'LOCKED') {
                updateContextPanel("Mission Locked. Hades is ready for execution phase.");
            } else if (data.action) {
                updateContextPanel(`Extracting requirements... Action: ${data.action}`);
            } else {
                updateContextPanel("Gathering mission requirements...");
            }

            appState = 'IDLE';

        } catch (error) {
            appState = 'ERROR';
            visualPresence.classList.remove('processing');
            appendMessage('hades', "I couldn't reach my reasoning service right now. Nothing was changed. Try again.");
            console.error(error);
        }
    }

    function appendMessage(sender, text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}`;
        
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        if (sender === 'user') {
            const nameToUse = userName || 'U';
            avatarDiv.innerHTML = `<img src="https://ui-avatars.com/api/?name=${encodeURIComponent(nameToUse)}&background=random" style="width:100%;height:100%;border-radius:50%;">`;
        } else {
            avatarDiv.innerHTML = '<i class="fa-solid fa-atom"></i>';
        }

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        const senderName = document.createElement('div');
        senderName.className = 'message-sender';
        senderName.innerText = sender === 'user' ? (userName || 'You') : 'HADES';
        
        const textBody = document.createElement('div');
        textBody.innerHTML = sender === 'hades' ? marked.parse(text) : escapeHTML(text);

        contentDiv.appendChild(senderName);
        contentDiv.appendChild(textBody);

        msgDiv.appendChild(avatarDiv);
        msgDiv.appendChild(contentDiv);

        chatContainer.appendChild(msgDiv);
        scrollToBottom();
    }

    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function escapeHTML(str) {
        const div = document.createElement('div');
        div.innerText = str;
        return div.innerHTML;
    }
    
    function updateContextPanel(text) {
        const contextPanel = document.querySelector('.panel-section .panel-content');
        if (contextPanel) {
            contextPanel.innerHTML = `<p class="text-subtle">${text}</p>`;
        }
    }

    // Text to Speech
    function speakText(text) {
        if ('speechSynthesis' in window) {
            // Remove markdown formatting before speaking
            const cleanText = text.replace(/[*_#`]/g, '');
            const utterance = new SpeechSynthesisUtterance(cleanText);
            utterance.rate = 1.0;
            utterance.pitch = 1.0;
            window.speechSynthesis.speak(utterance);
        }
    }

    // Voice Interaction ("Hey Hades")
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        
        recognition.continuous = true;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        let isListeningToCommand = false;

        recognition.onresult = function(event) {
            const resultIndex = event.resultIndex;
            const transcript = event.results[resultIndex][0].transcript.trim().toLowerCase();
            
            console.log("Heard:", transcript);

            if (!isListeningToCommand) {
                // Check for wake word
                if (transcript.includes('hey hades') || transcript.includes('hades')) {
                    isListeningToCommand = true;
                    visualPresence.classList.add('listening'); // Subtle UI feedback
                    
                    // See if the command was part of the same sentence
                    let command = transcript.replace(/hey hades/g, '').replace(/hades/g, '').trim();
                    if (command.length > 0) {
                        isListeningToCommand = false;
                        visualPresence.classList.remove('listening');
                        handleUserInput(command);
                    }
                }
            } else {
                // We are listening for the command
                if (transcript.length > 0) {
                    isListeningToCommand = false;
                    visualPresence.classList.remove('listening');
                    handleUserInput(transcript);
                }
            }
        };

        recognition.onerror = function(event) {
            console.log("Speech recognition error", event.error);
        };

        recognition.onend = function() {
            // Keep listening
            try {
                recognition.start();
            } catch(e) {}
        };

        // Start listening
        try {
            recognition.start();
        } catch(e) {}
    }
});
