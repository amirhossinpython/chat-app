document.addEventListener('DOMContentLoaded', function() {
    const socket = io();
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');
    
    // اسکرول به پایین هنگام لود صفحه
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // ارسال پیام
    function sendMessage() {
        const message = messageInput.value.trim();
        if (message) {
            socket.emit('send_message', { message: message });
            messageInput.value = '';
        }
    }
    
    sendButton.addEventListener('click', sendMessage);
    
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // دریافت پیام جدید
    socket.on('receive_message', function(data) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        
        messageElement.innerHTML = `
            <span class="message-username">${data.username}</span>
            <span class="message-text">${data.text}</span>
            <span class="message-time">${data.timestamp}</span>
        `;
        
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    });
});