let currentChatId = 0;
const chats = {};

document.getElementById('send-button').addEventListener('click', sendMessage);
document.getElementById('new-chat-button').addEventListener('click', createNewChat);

function createNewChat() {
    currentChatId = Date.now();
    chats[currentChatId] = [];
    updateChatList();
    displayMessages();
}

function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (!userInput) return;

    addMessageToChat(currentChatId, { sender: 'user', text: userInput });
    simulateApiResponse(userInput); // Simulate bot response
    document.getElementById('user-input').value = '';
}

function addMessageToChat(chatId, message) {
    if (!chats[chatId]) {
        chats[chatId] = [];
    }
    chats[chatId].push(message);
    if (chatId === currentChatId) {
        displayMessages();
    }
}

function displayMessages() {
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML = '';
    (chats[currentChatId] || []).forEach(message => {
        const messageElement = document.createElement('div');
        messageElement.textContent = message.text;
        messageElement.className = message.sender === 'user' ? 'user-message' : 'bot-message';
        chatBox.appendChild(messageElement);
    });
    chatBox.scrollTop = chatBox.scrollHeight;
}

function updateChatList() {
    const chatList = document.getElementById('chat-list');
    chatList.innerHTML = '';
    Object.keys(chats).forEach(chatId => {
        const chatItem = document.createElement('button');
        chatItem.textContent = `Chat ${chatId}`;
        chatItem.onclick = () => selectChat(chatId);
        chatList.appendChild(chatItem);
    });
}

function selectChat(chatId) {
    currentChatId = chatId;
    displayMessages();
}

function simulateApiResponse(userInput) {
    // Only simulate response for non-empty input
    if (userInput.trim() !== '') {
        setTimeout(() => {
            const botResponse = 'Simulated response for: ' + userInput;
            addMessageToChat(currentChatId, { sender: 'bot', text: botResponse });
        }, 1000);
    }
}

createNewChat(); // Initialize the first chat
