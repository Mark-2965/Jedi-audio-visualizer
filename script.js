document.addEventListener("DOMContentLoaded", () => {
    // Access Gate Targets
    const loginOverlay = document.getElementById("loginOverlay");
    const mainContainer = document.getElementById("mainContainer");
    const userSelect = document.getElementById("userSelect");
    const userPassword = document.getElementById("userPassword");
    const loginBtn = document.getElementById("loginBtn");
    const loginError = document.getElementById("loginError");

    // Chat Interface Anchors
    const chatFeed = document.getElementById("chatFeed");
    const userInput = document.getElementById("userInput");
    const sendButton = document.querySelector(".send-btn");
    const userBadge = document.getElementById("userBadge");
    const welcomeMessage = document.getElementById("welcomeMessage");
    
    // Feature Infrastructure Graph Nodes
    const micBtn = document.getElementById("micBtn");
    const ecosystemSidebar = document.getElementById("ecosystemSidebar");
    const ecoButtons = document.querySelectorAll(".eco-btn");
    const avatarContainer = document.getElementById("avatarContainer");
    const avatarPicker = document.getElementById("avatarPicker");
    const profileImage = document.getElementById("profileImage");

    // Default corporate image baseline fall-back link
    const DEFAULT_AVATAR = "https://unsplash.com";

    let activeSessionToken = null;
    let activeIntentMode = null; 
    let pendingDestination = "";

    // Multi-Tenant Portal Access Check Gateway
    loginBtn.addEventListener("click", () => {
        const selectedUser = userSelect.value;
        const passwordInput = userPassword.value;

        if (!selectedUser) {
            loginError.innerText = "❌ Please select an authorized account profile.";
            return;
        }

        if ((selectedUser === "bismark" && passwordInput === "1234") || 
            (selectedUser === "peace" && passwordInput === "5678") ||
            (selectedUser === "john" && passwordInput === "8888") ||
            (selectedUser === "beatrice" && passwordInput === "9999")) {
            
            activeSessionToken = selectedUser;
            let displayTitle = selectedUser.toUpperCase();
            if (selectedUser === "john") displayTitle = "MR. JOHN MENSAH";
            if (selectedUser === "beatrice") displayTitle = "BEATRICE OKIM";
            
            userBadge.innerText = displayTitle;
            userBadge.style.background = (selectedUser === "bismark" || selectedUser === "john") ? "#b89730" : "#1e2d3d";
            welcomeMessage.innerText = `🔓 SESSION SECURED. Welcome back, ${displayTitle}. Your encrypted biometric lookup keys match. How can I query your bank files tonight?`;

            // 💾 ⚡ THE ABSOLUTE RETRIEVAL ENGINE FIX: Look up if this logged-in profile has a saved custom image inside our database
            const savedAvatar = localStorage.getItem(`jedi_avatar_${activeSessionToken}`);
            if (savedAvatar) {
                profileImage.src = savedAvatar; // Snaps their personal locked picture back on screen immediately!
            } else {
                profileImage.src = DEFAULT_AVATAR; // Fall-back to basic corporate layout if none uploaded yet
            }

            // Unveil the layout side-by-side cleanly
            loginOverlay.style.opacity = "0";
            setTimeout(() => {
                loginOverlay.style.display = "none";
                mainContainer.classList.remove("blurred");
                ecosystemSidebar.classList.remove("blurred");
                userInput.removeAttribute("disabled");
                sendButton.removeAttribute("disabled");
                micBtn.removeAttribute("disabled");
                userInput.focus();
            }, 400);

        } else {
            loginError.innerText = "❌ Invalid Authorization PIN. Security access gate denied.";
            userPassword.value = "";
        }
    });

    // 📸 LIVE PROFILE IMAGE AVATAR DECK PICKER LOGIC (With Database Syncing!)
    avatarContainer.addEventListener("click", () => { 
        if (activeSessionToken) avatarPicker.click(); 
    });

    avatarPicker.addEventListener("change", (event) => {
        const selectedFile = event.target.files[0];
        if (selectedFile) {
            const fileReader = new FileReader();
            fileReader.onload = function(e) {
                const base64ImageString = e.target.result;
                
                // Update the visual frame on the spot
                profileImage.src = base64ImageString; 
                
                // 💾 ⚡ LOCK THE IMAGE STRING PERMANENTLY: Store inside browser memory tied directly to this user's node name!
                localStorage.setItem(`jedi_avatar_${activeSessionToken}`, base64ImageString);
            };
            fileReader.readAsDataURL(selectedFile);
        }
    });

    function appendMessage(text, sender) {
        const msgDiv = document.createElement("div");
        msgDiv.classList.add("message", sender);
        msgDiv.innerText = text;
        chatFeed.appendChild(msgDiv);
        chatFeed.scrollTop = chatFeed.scrollHeight;
    }

    // 📡 TRANSMIT CHAT/TRANSACTION PACKETS TO PORT 5000
    async function processMessage() {
        const text = userInput.value.trim();
        if (text === "") return;

        if (activeIntentMode === "FLIGHT_PIN" || activeIntentMode === "UBER_PIN") {
            appendMessage("••••••••", "user");
        } else {
            appendMessage(text, "user");
        }
        
        userInput.value = "";

        if (activeIntentMode === "FLIGHT_DEST") {
            pendingDestination = text;
            appendMessage(`✈️ [TRANSACTION SECURITY LOCK]: You have requested a flight ticket to "${text.toUpperCase()}". Baseline charge is ₦1,200,000.00. Please enter your Account Transaction Verification PIN to authorize this deduction line:`, "bot");
            activeIntentMode = "FLIGHT_PIN";
            userInput.type = "password"; 
            return;
        }

        if (activeIntentMode === "UBER_DEST") {
            pendingDestination = text;
            appendMessage(`🚗 [TRANSACTION SECURITY LOCK]: You have requested an Uber logistics haul ride to "${text.toUpperCase()}". Baseline charge is ₦15,000.00. Please enter your Account Transaction Verification PIN to authorize this deduction line:`, "bot");
            activeIntentMode = "UBER_PIN";
            userInput.type = "password"; 
            return;
        }

        let fetchPayload = { message: text, user_session: activeSessionToken };
        
        if (activeIntentMode === "FLIGHT_PIN") {
            fetchPayload = {
                user_session: activeSessionToken,
                transaction_type: "FLIGHT",
                destination: pendingDestination,
                secure_pin: text
            };
            activeIntentMode = null;
            userInput.type = "text";
        } 
        else if (activeIntentMode === "UBER_PIN") {
            fetchPayload = {
                user_session: activeSessionToken,
                transaction_type: "UBER",
                destination: pendingDestination,
                secure_pin: text
            };
            activeIntentMode = null;
            userInput.type = "text";
        }

        try {
            const response = await fetch("http://127.0.0.1:5000/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(fetchPayload)
            });
            const data = await response.json();
            appendMessage(data.reply, "bot");
        } catch (error) {
            appendMessage("❌ [SERVER ERROR]: API transmission port bridge disconnected. Make sure bankbot.py is awake inside your console terminal panel!", "bot");
            activeIntentMode = null;
            userInput.type = "text";
        }
    }

    // Voice recognition binding
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.continuous = false; recognition.lang = 'en-US';
        micBtn.addEventListener("click", () => { try { recognition.start(); } catch(e) { recognition.stop(); } });
        recognition.onstart = () => { micBtn.classList.add("recording"); userInput.placeholder = "Listening..."; };
        recognition.onresult = (e) => { userInput.value = e.results.transcript; micBtn.classList.remove("recording"); processMessage(); };
        recognition.onend = () => { micBtn.classList.remove("recording"); };
    } else { micBtn.style.display = "none"; }

    // SHORTCUT BUTTON INTERCEPTORS
    ecoButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const buttonAction = btn.getAttribute("data-intent");
            userInput.type = "text";

            if (buttonAction.includes("flight")) {
                appendMessage("✈️ [JEDI TRAVEL VECTOR ENGAGED]: Which country or global terminal location are you booking a flight reservation ticket to today?", "bot");
                activeIntentMode = "FLIGHT_DEST";
                userInput.focus();
            } 
            else if (buttonAction.includes("Uber")) {
                appendMessage("🚗 [JEDI LOGISTICS PORTAL ENGAGED]: Where is your destination drop-off point location address for your premium logistics ride station haul today?", "bot");
                activeIntentMode = "UBER_DEST";
                userInput.focus();
            } 
            else {
                activeIntentMode = null;
                userInput.value = buttonAction;
                processMessage();
            }
        });
    });

    sendButton.addEventListener("click", () => processMessage());
    userInput.addEventListener("keypress", (e) => { if (e.key === "Enter") processMessage(); });
});
