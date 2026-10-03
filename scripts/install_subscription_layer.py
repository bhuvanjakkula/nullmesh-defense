# install_subscription_layer.py
import re

# 1. Update backend/main.py
with open('backend/main.py', 'r', encoding='utf-8') as f:
    backend_code = f.read()

billing_backend = '''
class CheckoutRequest(BaseModel):
    email: Optional[str] = "bhuvanjakkula@gmail.com"
    tier: Optional[str] = "commandant"
    payment_method: Optional[str] = "direct_protocol"
    card_number: Optional[str] = None
    exp: Optional[str] = None
    cvv: Optional[str] = None


@app.get("/api/v1/billing/status")
def billing_status(email: Optional[str] = OWNER_EMAIL):
    user_email = (email or OWNER_EMAIL).lower().strip()
    is_owner = (user_email == OWNER_EMAIL)

    return {
        "user": user_email,
        "subscription_active": True,
        "plan_name": "DEFENSE COMMANDANT MAX // SOVEREIGN ENCLAVE" if is_owner else "TACTICAL OPERATOR",
        "billing_amount": "$0.00 / month (Authorized Defense Clearance)" if is_owner else "$49.00 / month",
        "renewal_date": "LIFETIME (NO EXPIRATION)" if is_owner else "2026-11-02",
        "payment_method": "Direct Defense Protocol Clearance" if is_owner else "Visa ending in •••• 4242",
        "status": "active",
        "features": [
            "Full Multi-Domain Access (Space, Air, Sea, Land)",
            "BB84 Quantum Key Distribution Channel (300km)",
            "NIST FIPS 203 ML-KEM-768 & ML-DSA-65 PQC",
            "Node D Hot Standby Autonomous Failover (<18ms)",
            "Disruption-Tolerant Store-and-Forward Mesh DTN",
            "Unlimited pLEO Optical Intersatellite Links (OISL)"
        ],
        "invoices": [
            {
                "id": "INV-2026-9041",
                "date": "2026-10-02",
                "description": "Defense Commandant Max Lifetime Subscription",
                "amount": "$0.00",
                "status": "PAID"
            },
            {
                "id": "INV-2026-8190",
                "date": "2026-09-02",
                "description": "Tactical Multi-Domain Enclave Allocation",
                "amount": "$0.00",
                "status": "PAID"
            }
        ]
    }


@app.post("/api/v1/billing/checkout")
def billing_checkout(req: CheckoutRequest):
    user_email = (req.email or OWNER_EMAIL).lower().strip()
    is_owner = (user_email == OWNER_EMAIL)
    import uuid
    inv_id = f"INV-2026-{uuid.uuid4().hex[:6].upper()}"

    return {
        "status": "success",
        "message": "Subscription tier confirmed and activated successfully",
        "invoice_id": inv_id,
        "tier": req.tier,
        "user": user_email,
        "amount_charged": "$0.00" if is_owner else ("$299.00" if req.tier == "commander" else "$49.00"),
        "receipt_hash": uuid.uuid4().hex
    }
'''

if '/api/v1/billing/status' not in backend_code:
    backend_code = backend_code.replace(
        '@app.post("/api/v1/analyze")',
        billing_backend + '\n\n@app.post("/api/v1/analyze")'
    )
    with open('backend/main.py', 'w', encoding='utf-8') as f:
        f.write(backend_code)
    print("backend/main.py updated with billing endpoints")

# 2. Update css/tactical.css with subscription & payment styles
with open('css/tactical.css', 'r', encoding='utf-8') as f:
    css = f.read()

sub_css = """
/* --- USER SUBSCRIPTION & PAYMENT WEB LAYER STYLES --- */
.subscription-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.sub-current-card {
  background: linear-gradient(135deg, rgba(10, 24, 48, 0.9) 0%, rgba(6, 12, 26, 0.95) 100%);
  border: 1px solid var(--accent-cyan);
  border-radius: 12px;
  padding: 22px;
  box-shadow: 0 0 30px rgba(0, 243, 255, 0.15);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.sub-current-info {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.sub-plan-badge {
  font-family: var(--font-display);
  font-size: 1.35rem;
  font-weight: 800;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 10px;
}

.sub-pricing-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 18px;
}

.sub-plan-card {
  background: rgba(10, 16, 32, 0.85);
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: all 0.25s ease;
  position: relative;
  backdrop-filter: blur(12px);
}

.sub-plan-card:hover {
  border-color: var(--border-bright);
  transform: translateY(-3px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
}

.sub-plan-card.featured {
  border-color: var(--accent-cyan);
  background: linear-gradient(180deg, rgba(0, 243, 255, 0.08) 0%, rgba(10, 16, 32, 0.9) 100%);
  box-shadow: 0 0 25px rgba(0, 243, 255, 0.2);
}

.plan-hdr {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.plan-name {
  font-family: var(--font-display);
  font-size: 1.15rem;
  font-weight: 800;
  color: #fff;
}

.plan-price {
  font-family: var(--font-mono);
  font-size: 1.6rem;
  font-weight: 800;
  color: #fff;
  margin-bottom: 12px;
}

.plan-price span {
  font-size: 0.8rem;
  color: var(--text-dim);
  font-weight: 400;
}

.plan-features {
  list-style: none;
  padding: 0;
  margin: 0 0 18px 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 0.76rem;
  color: var(--text-main);
  font-family: var(--font-mono);
}

.plan-features li {
  display: flex;
  align-items: center;
  gap: 8px;
}

.plan-features li::before {
  content: '✓';
  color: var(--accent-green);
  font-weight: 800;
}

.btn-plan-select {
  width: 100%;
  padding: 10px;
  border-radius: 6px;
  font-family: var(--font-display);
  font-size: 0.82rem;
  font-weight: 700;
  letter-spacing: 1px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
  border: 1px solid var(--border-subtle);
  background: rgba(14, 22, 40, 0.8);
  color: var(--text-dim);
}

.btn-plan-select:hover {
  background: var(--accent-cyan);
  color: #000;
  border-color: var(--accent-cyan);
  box-shadow: 0 0 15px rgba(0, 243, 255, 0.4);
}

.btn-plan-select.active-plan {
  background: rgba(0, 245, 155, 0.2);
  border-color: var(--accent-green);
  color: var(--accent-green);
  cursor: default;
}

/* Payment Terminal Box */
.payment-terminal-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}

.terminal-card {
  background: rgba(10, 16, 32, 0.85);
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  padding: 18px;
}

.table-invoices {
  width: 100%;
  border-collapse: collapse;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: var(--text-main);
}

.table-invoices th {
  text-align: left;
  padding: 8px 10px;
  border-bottom: 1px solid var(--border-subtle);
  color: var(--text-dim);
}

.table-invoices td {
  padding: 8px 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}
"""

if '.subscription-container' not in css:
    css += "\n" + sub_css
    with open('css/tactical.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("tactical.css updated with subscription styles")

# 3. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add view tab
nav_old = """      <button class="view-tab" data-view="layers">
        📚 ALL WEB & SYSTEM LAYERS (DECONSTRUCTED)
      </button>
    </nav>"""

nav_new = """      <button class="view-tab" data-view="layers">
        📚 ALL WEB & SYSTEM LAYERS (DECONSTRUCTED)
      </button>
      <button class="view-tab" data-view="subscription">
        💳 USER SUBSCRIPTION & PAYMENT LAYER
      </button>
    </nav>"""

if 'data-view="subscription"' not in html:
    html = html.replace(nav_old, nav_new)

# Add Top Header Button for subscription
btn_header_old = """        <button class="btn-tactical" id="btnSignOut" title="Return to Starting Sign In Gateway" style="border-color:var(--border-subtle); color:var(--text-dim);">
          🔑 SIGN OUT / RE-LOGIN
        </button>"""

btn_header_new = """        <button class="btn-tactical" id="btnHeaderSub" title="View User Subscription & Billing Layer" style="border-color:var(--accent-cyan); color:var(--accent-cyan);">
          💳 SUBSCRIPTION
        </button>
        <button class="btn-tactical" id="btnSignOut" title="Return to Starting Sign In Gateway" style="border-color:var(--border-subtle); color:var(--text-dim);">
          🔑 SIGN OUT / RE-LOGIN
        </button>"""

if 'id="btnHeaderSub"' not in html:
    html = html.replace(btn_header_old, btn_header_new)

# Add subscriptionWrapper view container
sub_wrapper_html = """
        <!-- View 7: User Subscription & Payment Web Layer (Separated View) -->
        <div style="display:none; padding:18px; overflow-y:auto; height:100%;" id="subscriptionWrapper">
          <div class="subscription-container">
            
            <!-- Section Header -->
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <div>
                <h2 style="font-family:var(--font-display); font-size:1.35rem; color:#fff; letter-spacing:1px; margin-bottom:4px;">
                  💳 USER SUBSCRIPTION, BILLING & DEFENSE PROCUREMENT PAYMENT LAYER
                </h2>
                <div style="font-family:var(--font-mono); font-size:0.75rem; color:var(--text-dim);">
                  ENTERPRISE COMMERCIAL & DEFENSE CLEARANCE LICENSING GATEWAY
                </div>
              </div>
              <span class="badge-version green" id="subBadgeState">SUBSCRIPTION ACTIVE</span>
            </div>

            <!-- Current Account & Subscription Status Card -->
            <div class="sub-current-card">
              <div class="sub-current-info">
                <div style="font-family:var(--font-mono); font-size:0.7rem; color:var(--text-dim); text-transform:uppercase;">
                  ACTIVE ACCOUNT CLEARANCE
                </div>
                <div class="sub-plan-badge">
                  <span style="color:var(--accent-cyan);">🛡️</span>
                  <span id="subPlanTitle">DEFENSE COMMANDANT MAX // SOVEREIGN ENCLAVE</span>
                </div>
                <div style="font-family:var(--font-mono); font-size:0.75rem; color:var(--text-main); margin-top:2px;">
                  Authorized User: <strong id="subUserEmail" style="color:#fff;">bhuvanjakkula@gmail.com</strong>
                </div>
                <div style="font-family:var(--font-mono); font-size:0.72rem; color:var(--accent-green); margin-top:4px;">
                  Billing Status: <strong>$0.00 / month (Authorized Defense Clearance // No Payment Required)</strong>
                </div>
              </div>

              <div style="display:flex; flex-direction:column; gap:8px; align-items:flex-end;">
                <span class="badge-version green" style="padding:4px 10px; font-size:0.75rem;">
                  ● LIFETIME ACTIVE (NO EXPIRATION)
                </span>
                <button class="btn-tactical" id="btnDownloadInvoice" style="border-color:var(--border-subtle); font-size:0.72rem;">
                  📄 DOWNLOAD OFFICIAL CLEARANCE RECEIPT
                </button>
              </div>
            </div>

            <!-- Subscription Tier Matrix (Separately Inspectable) -->
            <div style="margin-top:6px;">
              <h3 style="font-family:var(--font-display); font-size:1.05rem; color:#fff; margin-bottom:12px;">
                AVAILABLE SUBSCRIPTION & PROCUREMENT TIERS
              </h3>
              
              <div class="sub-pricing-grid">
                <!-- Tier 1: Operator -->
                <div class="sub-plan-card">
                  <div>
                    <div class="plan-hdr">
                      <div class="plan-name">TACTICAL OPERATOR</div>
                      <span class="badge-version">TIER 1</span>
                    </div>
                    <div class="plan-price">$49 <span>/ month</span></div>
                    <ul class="plan-features">
                      <li>Single-Domain Tactical MANET Access</li>
                      <li>10 Gbps Dynamic Mesh Bandwidth</li>
                      <li>Standard AES-256-GCM Encryption</li>
                      <li>Telemetry Logging (7-day Retention)</li>
                      <li>Community Support</li>
                    </ul>
                  </div>
                  <button class="btn-plan-select" data-tier="operator">SELECT TACTICAL OPERATOR</button>
                </div>

                <!-- Tier 2: Swarm Commander -->
                <div class="sub-plan-card">
                  <div>
                    <div class="plan-hdr">
                      <div class="plan-name">SWARM COMMANDER</div>
                      <span class="badge-version cyan">TIER 2</span>
                    </div>
                    <div class="plan-price">$299 <span>/ month</span></div>
                    <ul class="plan-features">
                      <li>All 4 Domains (Space, Air, Sea, Land)</li>
                      <li>Autonomous Node D Standby Failover (18ms)</li>
                      <li>CDT Consensus Horizon Engine (T* = ∞)</li>
                      <li>50 Gbps High-Throughput OISL Relay</li>
                      <li>Priority 24/7 Red-Team Support</li>
                    </ul>
                  </div>
                  <button class="btn-plan-select" data-tier="commander">SELECT SWARM COMMANDER</button>
                </div>

                <!-- Tier 3: Quantum Sovereign / Defense Commandant -->
                <div class="sub-plan-card featured">
                  <div>
                    <div class="plan-hdr">
                      <div class="plan-name" style="color:var(--accent-cyan);">QUANTUM SOVEREIGN</div>
                      <span class="badge-version" style="border-color:var(--accent-green); color:var(--accent-green);">CURRENT ACTIVE</span>
                    </div>
                    <div class="plan-price">$1,499 <span>/ mo (FREE FOR YOU)</span></div>
                    <ul class="plan-features">
                      <li>BB84 Entangled Photon QKD (300 km Channel)</li>
                      <li>NIST FIPS 203 ML-KEM-768 Lattice Cryptography</li>
                      <li>ML-DSA-65 Quantum-Resistant Digital Signatures</li>
                      <li>AEGIS IAMD Saturation Defense Grid</li>
                      <li>Sub-second Autonomous Self-Healing Mesh</li>
                      <li>Direct Python v0.1 Core Package Access</li>
                    </ul>
                  </div>
                  <button class="btn-plan-select active-plan" data-tier="commandant">CURRENT ACTIVE PLAN</button>
                </div>
              </div>
            </div>

            <!-- Payment Terminal & Invoicing History Section -->
            <div class="payment-terminal-grid">
              
              <!-- Payment Gateway Terminal Form -->
              <div class="terminal-card">
                <div style="font-family:var(--font-display); font-size:1rem; font-weight:700; color:#fff; margin-bottom:12px; display:flex; align-items:center; gap:8px;">
                  <span>💳</span> DEFENSE PAYMENT & CHECKOUT TERMINAL
                </div>

                <form id="paymentCheckoutForm" style="display:flex; flex-direction:column; gap:10px;">
                  <div class="form-group">
                    <label class="form-label">PAYMENT METHOD</label>
                    <select class="form-input" id="payMethodSelect">
                      <option value="protocol">Direct Protocol Clearance (Authorized for bhuvanjakkula@gmail.com)</option>
                      <option value="pcard">Government Defense P-Card / Commercial Visa/Mastercard</option>
                      <option value="qkd">QKD-Escrowed Quantum Crypto (USDC / BTC)</option>
                      <option value="contract">NATO / DoD Defense Contract Procurement Code</option>
                    </select>
                  </div>

                  <div class="form-group">
                    <label class="form-label">CARDHOLDER / PROCUREMENT AGENT NAME</label>
                    <input type="text" class="form-input" id="payAgentName" value="Commander Bhuvan Jakkula" required />
                  </div>

                  <div style="display:grid; grid-template-columns:2fr 1fr 1fr; gap:8px;">
                    <div class="form-group">
                      <label class="form-label">CARD / ID NUMBER</label>
                      <input type="text" class="form-input" id="payCardNum" value="•••• •••• •••• 9041" />
                    </div>
                    <div class="form-group">
                      <label class="form-label">EXPIRY</label>
                      <input type="text" class="form-input" id="payExp" value="12/30" />
                    </div>
                    <div class="form-group">
                      <label class="form-label">CVV / CODE</label>
                      <input type="text" class="form-input" id="payCvv" value="•••" />
                    </div>
                  </div>

                  <button type="submit" class="btn-auth-owner" id="btnSubmitPayment" style="margin-top:6px;">
                    AUTHORIZE SUBSCRIPTION & CONFIRM CLEARANCE
                  </button>

                  <div id="paymentResultMsg" style="display:none; font-family:var(--font-mono); font-size:0.75rem; padding:8px; border-radius:4px;"></div>
                </form>
              </div>

              <!-- Billing History & Invoice Records -->
              <div class="terminal-card">
                <div style="font-family:var(--font-display); font-size:1rem; font-weight:700; color:#fff; margin-bottom:12px; display:flex; align-items:center; gap:8px;">
                  <span>📋</span> INVOICING & PAYMENT HISTORY
                </div>

                <table class="table-invoices">
                  <thead>
                    <tr>
                      <th>INVOICE ID</th>
                      <th>DATE</th>
                      <th>PLAN / SERVICE</th>
                      <th>AMOUNT</th>
                      <th>STATUS</th>
                    </tr>
                  </thead>
                  <tbody id="invoiceTableBody">
                    <tr>
                      <td style="color:var(--accent-cyan);">INV-2026-9041</td>
                      <td>2026-10-02</td>
                      <td>Defense Commandant Max (Lifetime)</td>
                      <td><strong>$0.00</strong></td>
                      <td><span class="badge-version green" style="padding:1px 5px;">PAID</span></td>
                    </tr>
                    <tr>
                      <td style="color:var(--accent-cyan);">INV-2026-8190</td>
                      <td>2026-09-02</td>
                      <td>Quantum Enclave Channel Allocation</td>
                      <td><strong>$0.00</strong></td>
                      <td><span class="badge-version green" style="padding:1px 5px;">PAID</span></td>
                    </tr>
                    <tr>
                      <td style="color:var(--accent-cyan);">INV-2026-7023</td>
                      <td>2026-08-02</td>
                      <td>Tactical Multi-Domain Integration</td>
                      <td><strong>$0.00</strong></td>
                      <td><span class="badge-version green" style="padding:1px 5px;">PAID</span></td>
                    </tr>
                  </tbody>
                </table>
              </div>

            </div>

          </div>
        </div>
"""

if 'id="subscriptionWrapper"' not in html:
    html = html.replace('      </section>\n\n      <!-- Right Sidebar', sub_wrapper_html + '\n      </section>\n\n      <!-- Right Sidebar')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("index.html updated with subscriptionWrapper")

# Also add Layer 7 to the Deconstructed Layers list inside index.html if not already present
layer_7_card = """
            <!-- Layer 7: User Subscription, Billing & Defense Procurement Layer -->
            <div class="layer-deconstructor-card" style="border-left:4px solid #00f3ff;">
              <div class="layer-card-header">
                <div class="layer-card-title">
                  <span style="color:#00f3ff;">LAYER 7</span>
                  <span>// USER SUBSCRIPTION, BILLING & PAYMENT GATEWAY LAYER</span>
                </div>
                <span class="badge-version green">PAID // DEFENSE CLEARANCE ACTIVE</span>
              </div>
              <div class="layer-card-body">
                <div class="layer-desc-text">
                  Manages commercial subscription licensing, user accounts, government defense procurement cards (P-Cards), QKD-escrowed payment gateways, and automated zero-trust authorization.
                </div>
                <div class="layer-spec-list">
                  <div class="layer-spec-item">Account Status: <strong>bhuvanjakkula@gmail.com (Authorized)</strong></div>
                  <div class="layer-spec-item">Billing Tier: <strong>Commandant Max ($0.00/mo)</strong></div>
                  <div class="layer-spec-item">Payment Gateway: <strong>Direct Defense Protocol</strong></div>
                </div>
                <div>
                  <button class="btn-layer-isolate" data-target="subscription">ISOLATE LAYER</button>
                </div>
              </div>
            </div>
"""

if 'LAYER 7' not in html:
    html = html.replace('<!-- Layer 6: Backend Service', layer_7_card + '\n            <!-- Layer 6: Backend Service')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("index.html updated with Layer 7 in deconstructed view")
