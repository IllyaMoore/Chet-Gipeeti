const chatDiv = document.getElementById("chat");
const input = document.getElementById("input");
const send = document.getElementById("send");

function addMessage(text, sender = "bot") {
  const msg = document.createElement("div");
  msg.className = `message ${sender}`;
  msg.innerHTML = `
    <div class="avatar">${sender === "user" ? "U" : "B"}</div>
    <div class="bubble">${text}</div>
  `;
  chatDiv.appendChild(msg);
  chatDiv.scrollTop = chatDiv.scrollHeight;
}

async function sendMessage() {
  const prompt = input.value.trim();
  if (!prompt) return;

  addMessage(prompt, "user");
  input.value = "";

  const typingMsg = document.createElement("div");
  typingMsg.className = "message bot";
  typingMsg.innerHTML = `
    <div class="avatar">B</div>
    <div class="bubble"><span class="typing">...</span></div>`;
  chatDiv.appendChild(typingMsg);
  chatDiv.scrollTop = chatDiv.scrollHeight;

  try {
    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({prompt})
    });
    const data = await res.json();

    typingMsg.remove();
    addMessage(data.reply, "bot");
  } catch (err) {
    typingMsg.remove();
    addMessage("Не вдалося отримати відповідь від сервера.", "bot");
  }
}

send.onclick = sendMessage;

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});
і