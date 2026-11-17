document.addEventListener("DOMContentLoaded", () => {
    const sendBtn = document.getElementById("send-btn");
    const userInput = document.getElementById("user-input");
    const chatContainer = document.getElementById("chat-container");

    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        // Mostrar mensagem do utilizador
        appendMessage(text, "user");
        userInput.value = "";

        // Indicador de carregamento
        const loadingId = appendMessage("A pensar...", "assistant loading");

        try {
            const response = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: text })
            });

            const data = await response.json();
            
            // Remover loading e mostrar resposta da Gaia
            document.getElementById(loadingId).remove();
            
            if (data.reply) {
                appendMessage(data.reply, "assistant");
            } else {
                appendMessage("Senti uma falha nos ramos digitais.", "assistant");
            }
        } catch (error) {
            document.getElementById(loadingId).remove();
            appendMessage("Erro de ligação ao servidor.", "assistant");
        }
    }

    function appendMessage(text, sender) {
        const msgDiv = document.createElement("div");
        msgDiv.className = `message ${sender}`;
        msgDiv.innerText = text;
        const id = "msg-" + Date.now();
        msgDiv.id = id;
        chatContainer.appendChild(msgDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
        return id;
    }

    sendBtn.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") sendMessage();
    });
});
