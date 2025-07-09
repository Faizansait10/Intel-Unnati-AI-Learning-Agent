// Get references to DOM elements
const chatBox = document.getElementById('chatBox');
const textInput = document.getElementById('textInput');
const sendTextButton = document.getElementById('sendTextButton');
const recordButton = document.getElementById('recordButton');
const stopRecordingButton = document.getElementById('stopRecordingButton');
const statusDiv = document.createElement('div'); // Create a status div dynamically
statusDiv.id = 'status';
statusDiv.style.textAlign = 'center';
statusDiv.style.marginTop = '10px';
statusDiv.style.fontSize = '0.9em';
statusDiv.style.color = '#888'; // Adjust color for dark theme
document.querySelector('.chat-container').insertBefore(statusDiv, chatBox); // Insert before chatBox


let mediaRecorder;
let audioChunks = [];
let audioStream; // To hold the media stream so we can stop tracks later

// --- Event Listeners ---
sendTextButton.addEventListener('click', sendTextInput);
textInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendTextInput();
    }
});

recordButton.addEventListener('click', startRecording);
stopRecordingButton.addEventListener('click', stopRecording);

// --- Functions ---

// Function to update the status message
function setStatus(message) {
    statusDiv.textContent = message;
}

// Function to append messages to the chat box
function appendMessage(sender, text, audioBlobUrl = null) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${sender}-message`);

    const p = document.createElement('p');
    // Replace newline characters with <br> tags for proper HTML rendering
    // Use innerHTML instead of textContent when inserting HTML content
    p.innerHTML = text.replace(/\n/g, '<br>');
    messageDiv.appendChild(p);

    if (audioBlobUrl) {
        const audio = document.createElement('audio');
        audio.controls = true;
        audio.src = audioBlobUrl;
        messageDiv.appendChild(audio);
    }
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to latest message
}

// Function to send text input to backend
async function sendTextInput() {
    const text = textInput.value.trim();
    if (text) {
        appendMessage('user', text); // Display user's text message immediately
        textInput.value = ''; // Clear input field

        setStatus('Thinking...');
        try {
            const formData = new FormData();
            formData.append('text_input', text);

            const response = await fetch('/chat', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.response || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            const botResponseText = data.response;
            const audioResponseBase64 = data.audio_response_base64;

            let botAudioBlobUrl = null;
            if (audioResponseBase64) {
                const audioBlob = base64toBlob(audioResponseBase64, 'audio/mpeg'); // MP3 is audio/mpeg
                botAudioBlobUrl = URL.createObjectURL(audioBlob);
            }
            appendMessage('bot', botResponseText, botAudioBlobUrl);
            setStatus('Ready');

        } catch (error) {
            console.error('Error sending text to backend:', error);
            appendMessage('bot', `Error communicating with AI: ${error.message}`);
            setStatus('Error');
        }
    }
}

// Function to start audio recording
async function startRecording() {
    try {
        audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(audioStream, { mimeType: 'audio/webm; codecs=opus' }); // Specify codec

        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm; codecs=opus' });
            audioChunks = []; // Clear for next recording
            const audioBlobUrl = URL.createObjectURL(audioBlob);

            appendMessage('user', 'Recording finished. Sending audio...', audioBlobUrl); // Show user's audio
            await sendAudioToBackend(audioBlob);

            // Stop all tracks in the stream to release microphone
            if (audioStream) {
                audioStream.getTracks().forEach(track => track.stop());
            }
        };

        mediaRecorder.start();
        console.log('Recording started');
        recordButton.style.display = 'none'; // Hide Start button
        stopRecordingButton.style.display = 'inline-block'; // Show Stop button
        setStatus('Recording...');
    } catch (error) {
        console.error('Error starting recording:', error);
        setStatus('Error starting recording. Please check microphone permissions.');
        // Ensure buttons are reset if recording fails to start
        recordButton.style.display = 'inline-block';
        stopRecordingButton.style.display = 'none';
    }
}

// Function to stop audio recording
function stopRecording() {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        console.log('Recording stopped');
        recordButton.style.display = 'inline-block'; // Show Start button
        stopRecordingButton.style.display = 'none'; // Hide Stop button
        setStatus('Processing audio...');
    }
}

// Function to send audio blob to backend
async function sendAudioToBackend(audioBlob) {
    try {
        const formData = new FormData();
        formData.append('audio_input', audioBlob, 'recording.webm'); // Ensure correct filename and type

        const response = await fetch('/chat', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.response || `HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        const botResponseText = data.response;
        const audioResponseBase64 = data.audio_response_base64;

        let botAudioBlobUrl = null;
        if (audioResponseBase64) {
            const audioBlob = base64toBlob(audioResponseBase64, 'audio/mpeg'); // MP3 is audio/mpeg
            botAudioBlobUrl = URL.createObjectURL(audioBlob);
        }
        appendMessage('bot', botResponseText, botAudioBlobUrl);
        setStatus('Ready');

    } catch (error) {
        console.error('Error sending audio to backend:', error);
        appendMessage('bot', `Error communicating with AI: ${error.message}`);
        setStatus('Error');
    }
}

// Helper function to convert base64 to Blob
function base64toBlob(base64, mimeType) {
    const byteCharacters = atob(base64);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray], { type: mimeType });
}

// Initial status
setStatus('Ready');