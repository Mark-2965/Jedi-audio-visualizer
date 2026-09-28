import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Unlocks total CORS origin connection clearance

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "bissboi2@gmail.com"
SENDER_PASSWORD = "jdgijaxdicyhokur"

def send_transaction_email(recipient_email, customer_name, transaction_detail, transaction_amount, remaining_balance):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = "🏛️ JEDI PREMIUM BANK - LIVE TRANSACTION SECURITY ALERT"

        html_content = f"""
        <html>
        <body style="font-family: 'Segoe UI', Arial, sans-serif; background-color: #0d131a; color: #f4f6f8; padding: 20px; margin: 0;">
            <div style="max-width: 500px; margin: 0 auto; background: #141d26; border: 1px solid rgba(212, 175, 55, 0.3); border-radius: 16px; padding: 30px; box-shadow: 0 12px 40px rgba(0,0,0,0.5);">
                <div style="text-align: center; margin-bottom: 20px;">
                    <span style="font-size: 40px;">🏛️</span>
                    <h2 style="color: #d4af37; margin: 10px 0 5px 0; font-size: 22px; letter-spacing: 1px;">JEDI PREMIUM BANK</h2>
                    <p style="color: #8ca3ba; margin: 0; font-size: 12px; text-transform: uppercase;">Secure Account Telemetry Ledger</p>
                </div>
                <table style="width: 100%; font-size: 14px; border-collapse: collapse; margin-bottom: 25px;">
                    <tr style="border-bottom: 1px solid rgba(250,250,250,0.05);">
                        <td style="color: #8ca3ba; padding: 10px 0; font-weight: 500;">Action Type</td>
                        <td style="color: #f4f6f8; padding: 10px 0; text-align: right; font-weight: 600;">{transaction_detail}</td>
                    </tr>
                    <tr style="border-bottom: 1px solid rgba(250,250,250,0.05);">
                        <td style="color: #8ca3ba; padding: 10px 0; font-weight: 500;">Debited Amount</td>
                        <td style="color: #ff4a4a; padding: 10px 0; text-align: right; font-weight: 700;">₦{transaction_amount:,.2f}</td>
                    </tr>
                    <tr>
                        <td style="color: #8ca3ba; padding: 10px 0; font-weight: 500;">Available Balance</td>
                        <td style="color: #00ff87; padding: 10px 0; text-align: right; font-weight: 700;">₦{remaining_balance:,.2f}</td>
                    </tr>
                </table>
            </div>
        </body>
        </html>
        """
        msg.attach(MIMEText(html_content, 'html'))
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        server.quit()
        print(f"📬 [LIVE NETWORK DISPATCH] Success out to: {recipient_email}")
        return True
    except Exception as e:
        print(f"❌ SMTP Failure Node: {e}")
        return False

# =====================================================================
# 🏛️ SYSTEM ACCOUNT DATABASE ENTITIES (Perfect Alignment Keys)
# =====================================================================
ACCOUNTS = {
    "bismark": {"name": "Bismark", "pin": "1234", "balance": 45000000.0, "badge": "Premium Diamond", "email": "bissboi2@gmail.com"},
    "peace": {"name": "Peace", "pin": "5678", "balance": 125000.0, "badge": "Standard Tier-1", "email": "peace-test@gmail.com"},
    "john": {"name": "Mr. John Mensah", "pin": "8888", "balance": 75000000.0, "badge": "Enterprise Business", "email": "bissboi2@gmail.com"}
}

@app.route('/login', methods=['POST'])
def handle_login():
    data = request.json or {}
    username = data.get("username")
    pin = data.get("pin")
    
    if username in ACCOUNTS and ACCOUNTS[username]["pin"] == pin:
        return jsonify({
            "status": "success",
            "name": ACCOUNTS[username]["name"],
            "balance": ACCOUNTS[username]["balance"],
            "badge": ACCOUNTS[username]["badge"]
        })
    return jsonify({"status": "error", "message": "Access Denied: Invalid Security Credential Node PIN verification failure."})

@app.route('/chat', methods=['POST'])
def handle_chat():
    data = request.json or {}
    username = data.get("username")
    message = data.get("message", "")
    
    if username not in ACCOUNTS:
        return jsonify({"reply": "System core authentication database fault."})
        
    user_data = ACCOUNTS[username]
    
    # ⚡ CRASH-PROOF POSITION INDEX SELECTION (Cannot break on string operations)
    if "pin:" in message:
        try:
            start_pos = message.find("pin:") + 4
            submitted_pin = message[start_pos:start_pos+4].strip()
            
            if submitted_pin == user_data["pin"]:
                flight_cost = 1200000.0
                if user_data["balance"] >= flight_cost:
                    user_data["balance"] -= flight_cost
                    
                    send_transaction_email(
                        recipient_email=user_data["email"],
                        customer_name=user_data["name"],
                        transaction_detail="Flight Ticket Reservation (London Corporate Hub)",
                        transaction_amount=flight_cost,
                        remaining_balance=user_data["balance"]
                    )
                    return jsonify({"reply": f"✅ TRANSACTION SIGNED & AUTHORIZED: Flight booking confirmed. ₦{flight_cost:,.2f} debited from database tier. New balance: ₦{user_data['balance']:,.2f}.", "balance": user_data["balance"]})
                else:
                    return jsonify({"reply": f"❌ DECLINED: Insufficient liquidity parameters. Required: ₦{flight_cost:,.2f}.", "balance": user_data["balance"]})
            else:
                return jsonify({"reply": "❌ INVALID SECURITY TOKEN: The transaction authentication PIN string did not match our records.", "balance": user_data["balance"]})
        except Exception as e:
            return jsonify({"reply": f"❌ Logic structure parsing fault exception: {str(e)}", "balance": user_data["balance"]})

    message_lower = message.lower()
    if "balance" in message_lower or "statement" in message_lower:
        return jsonify({"reply": f"Hello {user_data['name']}, available asset liquidity volume sits at ₦{user_data['balance']:,.2f}.", "balance": user_data["balance"]})
        
    return jsonify({"reply": f"Prompt recorded string line node for authorized user: {user_data['name']}.", "balance": user_data["balance"]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
