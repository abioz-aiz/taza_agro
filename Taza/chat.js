class ChatWidget {
    constructor() {
        this.widget = document.getElementById('chatWidget');
        this.messages = document.getElementById('chatMessages');
        this.input = document.getElementById('chatInput');
        this.sendButton = document.getElementById('sendMessage');
        this.toggleButton = document.getElementById('chatToggle');
        this.minimizeButton = document.querySelector('.minimize-chat');

        this.setupEventListeners();
        this.addWelcomeMessage();
    }

    setupEventListeners() {
        // Send message on button click
        this.sendButton.addEventListener('click', () => this.sendMessage());

        // Send message on Enter key
        this.input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });

        // Toggle chat widget
        this.toggleButton.addEventListener('click', () => {
            this.widget.classList.toggle('hidden');
            this.toggleButton.classList.toggle('hidden');
            if (!this.widget.classList.contains('hidden')) {
                this.input.focus();
            }
        });

        // Minimize chat widget
        this.minimizeButton.addEventListener('click', () => {
            this.widget.classList.add('minimized');
            this.toggleButton.classList.remove('hidden');
        });
    }

    async sendMessage() {
        const message = this.input.value.trim();
        if (!message) return;

        // Add user message to chat
        this.addMessage(message, 'user');
        this.input.value = '';

        try {
            // Show typing indicator
            this.addTypingIndicator();

            // Send message to server
            const response = await this.sendToServer(message);

            // Remove typing indicator and add bot response
            this.removeTypingIndicator();
            this.addMessage(response, 'bot');
        } catch (error) {
            this.removeTypingIndicator();
            this.addMessage('Sorry, I encountered an error. Please try again.', 'bot');
        }
    }

    async sendToServer(message) {
        try {
            const response = await fetch('http://localhost:1234/v1/chat/completions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    messages: [{ role: "user", content: message }],
                    max_tokens: 150
                })
            });

            if (!response.ok) throw new Error('Server response was not ok');

            const data = await response.json();
            return data.choices[0].message.content;
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    }

    addMessage(message, type) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${type}-message`);
        messageDiv.textContent = message;
        this.messages.appendChild(messageDiv);
        this.messages.scrollTop = this.messages.scrollHeight;
    }

    addTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'typingIndicator';
        indicator.classList.add('message', 'bot-message');
        indicator.textContent = 'Typing...';
        this.messages.appendChild(indicator);
        this.messages.scrollTop = this.messages.scrollHeight;
    }

    removeTypingIndicator() {
        const indicator = document.getElementById('typingIndicator');
        if (indicator) indicator.remove();
    }

    addWelcomeMessage() {
        this.addMessage('Hello! How can I help you today?', 'bot');
    }
}

// Initialize chat widget when document is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatWidget();
}); 