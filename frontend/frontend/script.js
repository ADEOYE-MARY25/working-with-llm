    // Backend API URL
    const API_BASE = 'http://localhost:8000';
    let isConnected = false;

  
    const chatContainer = document.getElementById('chatContainer');
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const statusElement = document.getElementById('status');


    // Check API connection
    async function checkConnection() {
        try {
            const response = await fetch(`${API_BASE}/health`);
            if (response.ok) {
                isConnected = true;
                statusElement.textContent = 'Connected to API';
                statusElement.className = 'status connected';
            } else {
                throw new Error('API not responding');
            }
        } catch (error) {
            isConnected = false;
            statusElement.textContent = 'Disconnected from API';
            statusElement.className = 'status disconnected';
        }
    }








    // CUSTOMIZATIONS ===============================================================================

    // Add message to chat
    function addMessage(content, isUser = false, isError = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'ai-message'} ${isError ? 'error' : ''}`;
        messageDiv.textContent = content;
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Show typing indicator
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message ai-message typing-indicator';
        typingDiv.id = 'typingIndicator';
        typingDiv.innerHTML = 'AI is thinking<span class="typing-dots"></span>';
        chatContainer.appendChild(typingDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Hide typing indicator
    function hideTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }













    // ---------------------------------------------------------------------

    // Send message to API
    async function sendMessage() {
        if (!isConnected) {
            addMessage('Error: Not connected to API. Please check if the server is running.', false, true);
            return;
        }

        const message = messageInput.value.trim();
        if (!message) return;

        // Clear input and disable send button
        messageInput.value = '';
        sendButton.disabled = true;
        messageInput.disabled = true;

        // Add user message to chat
        addMessage(message, true);

        // Show typing indicator
        showTypingIndicator();

        try {
            const response = await fetch(`${API_BASE}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    model: 'gemini-2.5-flash'
                })
            });

            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }

            const data = await response.json();
            
            // Remove typing indicator and add AI response
            hideTypingIndicator();
            addMessage(data);

        } catch (error) {
            hideTypingIndicator();
            addMessage(`Error: ${error.message}`, false, true);
            console.error('Error:', error);
        } finally {
            // Re-enable input and send button
            sendButton.disabled = false;
            messageInput.disabled = false;
            messageInput.focus();
        }
    }

    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Auto-focus input
    messageInput.focus();

    // Check connection on load and every 30 seconds
    checkConnection();
    setInterval(checkConnection, 30000);