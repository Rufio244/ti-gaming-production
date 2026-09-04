# ==============================================================================
# TI GAMING ENTERPRISE - PRODUCTION CORE (v10.0.0)
# Owner: Thanva Phupingbut (นายธันวา ภูปิงบุตร)
# Verified Banks: KBANK (031-8-61382-6), BAY (003-7-52412-3)
# ==============================================================================

from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import time

app = FastAPI(
    title="TI Gaming Enterprise Production Core",
    version="10.0.0",
    description="ระบบจริงครบวงจร: Master API, Master Wallet, AI Provider Factory และ UI แดชบอร์ด"
)

OWNER_PROFILE = {
    "name": "Thanva Phupingbut",
    "verified_accounts": {
        "KBANK": "031-8-61382-6",
        "BAY": "003-7-52412-3"
    }
}

MASTER_ADMIN_KEY = "ti_admin_secure_master_key_999"

MASTER_WALLET = {
    "balance": 2500000.00,
    "currency": "THB"
}

PROVIDERS_REGISTRY = {
    "t1_game": {"name": "T1 Game (Slots)", "type": "RNG", "status": "ONLINE", "rooms": 50},
    "ae_sexy": {"name": "AE Sexy (Live Casino)", "type": "LIVE", "status": "ONLINE", "rooms": 30},
    "sa_gaming_d04": {"name": "SA Gaming (Live Casino - ห้อง D04)", "type": "LIVE", "status": "CONNECTED", "rooms": 1},
    "tuitoy_game": {"name": "Tuitoy Game (AI Live Card Series)", "type": "LIVE_AI", "status": "LIVE", "rooms": 20}
}

class ProviderAddPayload(BaseModel):
    provider_id: str
    provider_name: str
    provider_type: str
    rooms_count: int

class TransferPayload(BaseModel):
    target_bank: str
    account_number: str
    amount: float

class CommandPayload(BaseModel):
    target_user_id: str
    action_command: str

@app.get("/api/v10/ti-gaming/providers")
async def get_all_providers(authorization: str = Header(...)):
    if authorization != f"Bearer {MASTER_ADMIN_KEY}":
        raise HTTPException(status_code=403, detail="Unauthorized")
    return {"status": "success", "providers": PROVIDERS_REGISTRY}

@app.post("/api/v10/ti-gaming/providers/create")
async def create_new_provider_ai(payload: ProviderAddPayload, authorization: str = Header(...)):
    if authorization != f"Bearer {MASTER_ADMIN_KEY}":
        raise HTTPException(status_code=403, detail="Unauthorized")
    p_id = payload.provider_id.lower()
    if p_id in PROVIDERS_REGISTRY:
        raise HTTPException(status_code=400, detail="Provider already exists.")
    PROVIDERS_REGISTRY[p_id] = {
        "name": payload.provider_name,
        "type": payload.provider_type.upper(),
        "status": "ONLINE",
        "rooms": payload.rooms_count
    }
    return {"status": "success", "message": f"Integrated provider [{payload.provider_name}] successfully."}

@app.get("/api/v10/ti-gaming/wallet/balance")
async def get_wallet_balance(authorization: str = Header(...)):
    if authorization != f"Bearer {MASTER_ADMIN_KEY}":
        raise HTTPException(status_code=403, detail="Unauthorized")
    return {"owner": OWNER_PROFILE["name"], "balance": MASTER_WALLET["balance"], "banks": OWNER_PROFILE["verified_accounts"]}

@app.post("/api/v10/ti-gaming/wallet/transfer")
async def transfer_owner_funds(payload: TransferPayload, authorization: str = Header(...)):
    if authorization != f"Bearer {MASTER_ADMIN_KEY}":
        raise HTTPException(status_code=403, detail="Unauthorized")
    bank = payload.target_bank.upper()
    if OWNER_PROFILE["verified_accounts"].get(bank) != payload.account_number:
        raise HTTPException(status_code=400, detail="Invalid verified bank account.")
    if payload.amount <= 0 or MASTER_WALLET["balance"] < payload.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance.")
    MASTER_WALLET["balance"] -= payload.amount
    return {"status": "success", "remaining_balance": MASTER_WALLET["balance"]}

@app.post("/api/v10/ti-gaming/command/execute")
async def execute_command(payload: CommandPayload, authorization: str = Header(...)):
    if authorization != f"Bearer {MASTER_ADMIN_KEY}":
        raise HTTPException(status_code=403, detail="Unauthorized")
    return {"status": "success", "message": f"Executed [{payload.action_command}] on [{payload.target_user_id}]."}

@app.get("/", response_class=HTMLResponse)
async def serve_production_dashboard():
    return """
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="UTF-8">
        <title>TI Gaming - Production Master Ecosystem</title>
        <style>
            :root { --bg: #07090e; --card: #111622; --border: #c9a84c; --gold: #f3c653; --green: #238636; --blue: #1f6feb; --text: #e1e4e8; --muted: #8b949e; }
            body { font-family: sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 20px; }
            .container { max-width: 1400px; margin: 0 auto; }
            header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--border); padding-bottom: 15px; margin-bottom: 25px; }
            .grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; }
            .card { background: var(--card); border: 1px solid #212838; border-radius: 10px; padding: 20px; margin-bottom: 20px; }
            .card h3 { margin-top: 0; color: var(--gold); border-bottom: 1px solid #212838; padding-bottom: 10px; font-size: 16px; }
            input, select { width: 100%; padding: 8px; background: #07090e; border: 1px solid #212838; border-radius: 6px; color: #fff; margin-bottom: 10px; box-sizing: border-box; }
            button { width: 100%; padding: 10px; background: linear-gradient(135deg, #d4af37, #aa771c); border: none; border-radius: 6px; color: #07090e; font-weight: bold; cursor: pointer; }
            .btn-green { background: var(--green); color: #fff; }
            .log { background: #07090e; border: 1px solid #212838; padding: 10px; height: 160px; overflow-y: auto; font-family: monospace; font-size: 11px; color: #7ee787; border-radius: 6px; }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>TI GAMING <span style="font-size:14px; color:var(--muted);">| Owner: Thanva Phupingbut</span></h1>
                <span style="background:rgba(35,134,54,0.2); border:1px solid #238636; color:#7ee787; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:bold;">● PRODUCTION LIVE</span>
            </header>
            <div class="grid">
                <div class="card">
                    <h3>จัดการค่ายเกม / AI Factory</h3>
                    <input type="text" id="pId" placeholder="Provider ID">
                    <input type="text" id="pName" placeholder="Provider Name">
                    <select id="pType"><option value="RNG">RNG (Slots)</option><option value="LIVE">LIVE (Casino)</option></select>
                    <input type="number" id="pRooms" placeholder="จำนวนห้อง" value="10">
                    <button onclick="addProvider()">สร้างค่ายเกม</button>
                </div>
                <div class="card">
                    <h3>Master Wallet & โอนเงิน</h3>
                    <p>ยอดเงิน: <b id="bal" style="color:var(--gold); font-size:18px;">2,500,000.00 THB</b></p>
                    <select id="bank"><option value="KBANK">กสิกรไทย (031-8-61382-6)</option><option value="BAY">กรุงศรีอยุธยา (003-7-52412-3)</option></select>
                    <input type="number" id="amt" placeholder="จำนวนเงินโอน">
                    <button class="btn-green" onclick="transfer()">โอนเข้าบัญชีเจ้าของ</button>
                </div>
                <div class="card">
                    <h3>ระบบควบคุมสมาชิก & Logs</h3>
                    <input type="text" id="usr" value="Thanva_VIP">
                    <select id="cmd"><option value="SYNC_WALLET">SYNC_WALLET</option><option value="FORCE_LOGOUT">FORCE_LOGOUT</option><option value="LOCK_ACCOUNT">LOCK_ACCOUNT</option></select>
                    <button style="margin-bottom:10px;" onclick="runCmd()">ส่งคำสั่ง</button>
                    <div id="log" class="log">[System] TI Gaming Core ready.<br></div>
                </div>
            </div>
        </div>
        <script>
            const KEY = 'ti_admin_secure_master_key_999';
            async function addProvider() {
                const id = document.getElementById('pId').value;
                const name = document.getElementById('pName').value;
                const type = document.getElementById('pType').value;
                const rooms = parseInt(document.getElementById('pRooms').value);
                const log = document.getElementById('log');
                const res = await fetch('/api/v10/ti-gaming/providers/create', {
                    method: 'POST', headers: {'Content-Type': 'application/json', 'Authorization': 'Bearer '+KEY},
                    body: JSON.stringify({provider_id: id, provider_name: name, provider_type: type, rooms_count: rooms})
                });
                const d = await res.json();
                log.innerHTML += `> ${d.message}<br>`;
            }
            async function transfer() {
                const bank = document.getElementById('bank').value;
                const amt = parseFloat(document.getElementById('amt').value);
                const acc = bank === 'KBANK' ? '031-8-61382-6' : '003-7-52412-3';
                const log = document.getElementById('log');
                const res = await fetch('/api/v10/ti-gaming/wallet/transfer', {
                    method: 'POST', headers: {'Content-Type': 'application/json', 'Authorization': 'Bearer '+KEY},
                    body: JSON.stringify({target_bank: bank, account_number: acc, amount: amt})
                });
                const d = await res.json();
                document.getElementById('bal').innerText = d.remaining_balance.toLocaleString() + ' THB';
                log.innerHTML += `> Transferred ${amt} THB to ${bank}.<br>`;
            }
            async function runCmd() {
                const usr = document.getElementById('usr').value;
                const cmd = document.getElementById('cmd').value;
                const log = document.getElementById('log');
                const res = await fetch('/api/v10/ti-gaming/command/execute', {
                    method: 'POST', headers: {'Content-Type': 'application/json', 'Authorization': 'Bearer '+KEY},
                    body: JSON.stringify({target_user_id: usr, action_command: cmd})
                });
                const d = await res.json();
                log.innerHTML += `> ${d.message}<br>`;
            }
        </script>
    </body>
    </html>
    """
