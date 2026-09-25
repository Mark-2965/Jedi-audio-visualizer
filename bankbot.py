from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Establishes the secure network bridge to your Chrome browser window

# 📊 THE ENCRYPTED JEDI MULTI-TENANT LEDGER DATABASE (Dynamic Balance Tracking Matrix)
CUSTOMER_DATABASE = {
    "bismark": {
        "name": "Bismark",
        "pin": "1234",
        "account_type": "Premium Diamond Savings",
        "balance_naira": 75000000.00,  # ₦75 Million Naira portfolio asset!
        "last_transaction": "-₦150,000.00 (Solar Inverter Upgrade Maintenance Setup)"
    },
    "peace": {
        "name": "Peace",
        "pin": "5678",
        "account_type": "Standard Savings Tier-1",
        "balance_naira": 14500.00,     # ₦14,500 Naira balance track (Will cause Insufficient Funds!)
        "last_transaction": "-₦2,500.00 (Campus Bookstore Resource Materials)"
    },
    "john": {
        "name": "Mr. John Mensah",
        "pin": "8888",
        "account_type": "Enterprise Business Current",
        "balance_naira": 12450000.00,  # ₦12.45 Million Naira capital liquidity track
        "last_transaction": "+₦1,850,000.00 (Corporate Invoiced Product Sales Inflow Receipt)"
    },
    "beatrice": {
        "name": "Beatrice Okim",
        "pin": "9999",
        "account_type": "Gold VIP High-Yield Savings",
        "balance_naira": 3400000.00,   # ₦3.4 Million Naira savings balance
        "last_transaction": "-₦45,000.00 (ZARA Luxury Fashion Apparel Delivery)"
    }
}

# 📡 SEAMLESS WEB TERMINAL ENTRY ENDPOINT
@app.route('/chat', methods=['POST'])
def chat_endpoint():
    data = request.json
    user_prompt = data.get("message", "").lower()
    session_user = data.get("user_session", "").lower()
    
    # Extract additional transaction payload validation keys from frontend JavaScript
    transaction_type = data.get("transaction_type", None)
    destination_target = data.get("destination", "").upper()
    provided_pin = data.get("secure_pin", "")

    # Security Check: Ensure the user session is valid inside our ledger array
    if session_user not in CUSTOMER_DATABASE:
        return jsonify({"reply": "❌ [SECURITY ERROR]: No active authenticated tenant session context discovered."})
    
    client_profile = CUSTOMER_DATABASE[session_user]
    
    # 🔐 PHASE A: TRANSACTION SECURE PIN SIGNING VERIFICATION ENGINE
    if transaction_type:
        if provided_pin != client_profile["pin"]:
            return jsonify({
                "status": "PIN_DENIED",
                "reply": f"❌ [TRANSACTION BLOCKED]: Authorization Security PIN verification failed for {client_profile['name']}. Transaction signature access denied."
            })
        
        # Assign baseline costs for our dynamic simulation activities
        transaction_cost = 1200000.00 if transaction_type == "FLIGHT" else 15000.00
        service_label = f"Flight Ticket to {destination_target}" if transaction_type == "FLIGHT" else f"Uber Ride to {destination_target}"

        # 🛑 BALANCE MATRIX THRESHOLD VALIDATION (The Overdraft/Insufficient Funds Shield)
        if client_profile["balance_naira"] < transaction_cost:
            return jsonify({
                "status": "INSUFFICIENT_FUNDS",
                "reply": f"⛔ [TRANSACTION DECLINED]: Insufficient Funds! {client_profile['name']}, your current balance is ₦{client_profile['balance_naira']:,.2f}, which cannot clear the required invoice charge of ₦{transaction_cost:,.2f} for this {service_label}."
            })
            
        # 💸 STATE MANAGEMENT MODIFICATION: EXECUTE BALANCE SUBTRACTION IN MEMORY
        client_profile["balance_naira"] -= transaction_cost
        client_profile["last_transaction"] = f"-₦{transaction_cost:,.2f} ({service_label})"
        
        return jsonify({
            "status": "SUCCESS",
            "reply": f"✅ [TRANSACTION SUCCESFULLY CLEARED]: Authorization approved, {client_profile['name']}! ₦{transaction_cost:,.2f} has been deducted from your account. Remaining available ledger balance is now: ₦{client_profile['balance_naira']:,.2f} Naira."
        })

    # 🏁 PHASE B: GENERAL BALANCE/STATEMENT INQUIRY ROUTING LOGIC PATTERN MATCHING
    if "balance" in user_prompt or "money" in user_prompt or "how much" in user_prompt:
        response = f"💳 [BALANCE TRACKER]: Hello {client_profile['name']}, your current available balance on your {client_profile['account_type']} is ₦{client_profile['balance_naira']:,.2f} Naira."
        
    elif "statement" in user_prompt or "transaction" in user_prompt or "last" in user_prompt or "audit" in user_prompt:
        response = f"📜 [ACCOUNT MATRIX]: Your absolute last recorded ledger transaction execution was: {client_profile['last_transaction']}."
        
    elif "status" in user_prompt or "profile" in user_prompt or "bvn" in user_prompt or "security" in user_prompt:
        response = f"🎖️ [JEDI SECURITY SECURE CORE]: Profile Master Node: {client_profile['name']} | Status Vector: VERIFIED AUTHENTICATED LOCK."
        
    else:
        response = f"🤖 [JEDI ASSISTANT]: Query analyzed, {client_profile['name']}. Please specify an action prompt request for your 'balance', 'last transaction', or 'profile status'."

    return jsonify({"reply": response})

if __name__ == "__main__":
    print("🚀 JEDI PREMIUM MULTI-TENANT BACKEND SERVER RUNNING LIVE ON PORT 5000...")
    app.run(host="127.0.0.1", port=5000, debug=True)
