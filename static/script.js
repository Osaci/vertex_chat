async function sendMessage();
    const userMessage = document.getElementById("userMessage").value;
    if (userMessage.trim() === '') return;

    //Add message to the chat
    const chatBox = document.getElementById("chatBox");
    const userMessageBox = document.createElement('div');
    userMessageBox.className = 'user-message-box';
    const userMessageElem = document.createElement('p');
    userMessageElem.className = 'user-message';
    userMessageElem.textContent = userMessage;
    userMessageBox.appendChild(userMessageElem);
    chatBox.appendChild(userMessageBox);
    chatBox.scrollTop = chatBox.scrollHeight;

    
    //Send message to the backend
    const response = await fetch('/send-message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'-
        },
        body: JSON.stringify({ userMessage: userMessage })
    });

    const data = await response.json();
    
    //Add response to chat
    const botMessageElem = document.createElement('p');
    botMessageElem.className = 'bot-response';
    botMessageElem.textContent = data.reply;
    chatBox.appendChild(botMessageElem);
    chatBox.scrollTop = chatBox.scrollHeight;

    //Clear input field
    document.getElementById("userMessage").value = '';
}

//Send message when enter is pressed
document.addEventListener("DOMContentLoaded", function() {
    const inputField = document.getElementById("userMessage");
    inputField.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });
});
    
    
    
    