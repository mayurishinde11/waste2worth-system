function sendMessage() {
    const input = document.getElementById("userInput").value;
    const chatBox = document.getElementById("chatBox");

    if (!input) {
        alert("Please enter a message");
        return;
    }

    chatBox.innerHTML += `<p><b>You:</b> ${input}</p>`;

    fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: input })
    })
    .then(res => res.json())
    .then(data => {
        chatBox.innerHTML += `<p><b>Bot:</b> ${data.reply}</p>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(err => console.error(err));
    
    document.getElementById("userInput").value = "";
}