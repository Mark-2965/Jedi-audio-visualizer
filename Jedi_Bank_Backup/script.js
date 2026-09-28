const chatFeed = document.getElementById('chatFeed');
const userInput = document.getElementById('userInput');
const sendBtn = document.querySelector('.send-btn');
const loginOverlay = document.getElementById('loginOverlay');
const loginBtn = document.getElementById('loginBtn');
const loginError = document.getElementById('loginError');

let currentUsername = "";
let isAwaitingPin = false;
let pendingTransactionText = "";

// 🔐 GATEWAY API ACCESS ROUTING
loginBtn.addEventListener('click', async () => {
    const username = document.getElementById('userSelect').value;
    const pin = document.getElementById('userPassword').value;
    
    if(!username || !pin) {
        loginError.innerText = "Select a profile node and input security PIN.";
        return;
    }
    
    try {
        // Targets the Python backend server port 5000 directly
        const response = await fetch('http://127.0.0.1:5000/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, pin })
        });
        const data = await response.json();
        
        if(data.status === "success") {
            currentUsername = username;
            document.getElementById('userBadge').innerText = data.badge;
            document.getElementById('bankTitle').innerText = data.name;
            document.getElementById('mainContainer').classList.remove('blurred');
            loginOverlay.style.display = 'none';
            userInput.disabled = false;
            sendBtn.disabled = false;
            
            appendMessage(`System authorized. Session established for node: ${data.name}. Welcome back, leader. 🏛️⚡`, 'bot');
        } else {
            loginError.innerText = data.message;
        }
    } catch(err) {
        loginError.innerText = "Backend API server port 5000 offline.";
    }
});

// ⌨️ DISPATCH CORE ENGINE
async function sendMessage() {
    const text = userInput.value.trim();
    if(!text) return;
    
    userInput.value = "";
    
    // Check if security intercept layer is active
    if (isAwaitingPin) {
        appendMessage('••••', 'user'); // Visual masking layout
        try {
            const response = await fetch('http://127.0.0.1:5000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    username: currentUsername,
                    message: `pin:${text} action:${pendingTransactionText}`
                })
            });
            const data = await response.json();
            appendMessage(data.reply, 'bot');
            isAwaitingPin = false;
            pendingTransactionText = "";
        } catch(err) {
            appendMessage("❌ Network handshake failure.", 'bot');
        }
        return;
    }

    appendMessage(text, 'user');
    const lowerText = text.toLowerCase();
    
    // Trap financial transaction strings explicitly before firing
    if (lowerText.includes("flight") || lowerText.includes("book") || lowerText.includes("london")) {
        isAwaitingPin = true;
        pendingTransactionText = text;
        appendMessage("🔒 TRANSACTION SECURITY LOCK: Please input your 4-digit Account Security PIN to authorize this request.", 'bot');
        return;
    }
    
    try {
        const response = await fetch('http://127.0.0.1:5000/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: currentUsername, message: text })
        });
        const data = await response.json();
        appendMessage(data.reply, 'bot');
    } catch(err) {
        appendMessage("❌ Communication pipeline error.", 'bot');
    }
}

function appendMessage(text, sender) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}`;
    msgDiv.innerText = text;
    chatFeed.appendChild(msgDiv);
    chatFeed.scrollTop = chatFeed.scrollHeight;
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => { if(e.key === 'Enter') sendMessage(); });
