document.getElementById('send-button').addEventListener('click', function() {
    const userInput = document.getElementById('user-input').value;
    if (userInput) {
        displayMessage(userInput, 'user');
        simulateApiResponse(userInput);
        document.getElementById('user-input').value = '';
    }
});

function displayMessage(message, sender) {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    messageElement.textContent = message;
    messageElement.className = sender === 'user' ? 'user-message' : 'bot-message';
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function simulateApiResponse(userInput) {
    // Simulate API call and response
    setTimeout(() => {
        // This is where you would normally handle the actual API call
        const botResponse = 'Simulated response for: ' + userInput;
        displayMessage(botResponse, 'bot');
    }, 1000);
}

