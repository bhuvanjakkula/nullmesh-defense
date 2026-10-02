# install_layer_views.py
import re

# 1. Update css/tactical.css
with open('css/tactical.css', 'r', encoding='utf-8') as f:
    css = f.read()

layer_css = """
/* --- DOMAIN LAYER FILTER BAR ON CANVAS --- */
.canvas-layer-filter-bar {
  position: absolute;
  top: 12px;
  left: 16px;
  z-index: 25;
  display: flex;
  align-items: center;
  gap: 6px;
  background: rgba(6, 10, 22, 0.85);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  padding: 4px 8px;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
}

.filter-bar-title {
  font-family: var(--font-mono);
  font-size: 0.65rem;
  color: var(--text-dim);
  font-weight: 700;
  margin-right: 4px;
}

.domain-layer-btn {
  background: rgba(14, 22, 40, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--text-dim);
  font-family: var(--font-mono);
  font-size: 0.68rem;
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.domain-layer-btn:hover {
  border-color: var(--accent-cyan);
  color: #fff;
}

.domain-layer-btn.active {
  background: rgba(0, 243, 255, 0.2);
  border-color: var(--accent-cyan);
  color: #fff;
  box-shadow: 0 0 10px rgba(0, 243, 255, 0.3);
}

/* --- SYSTEM LAYERS DECONSTRUCTOR STYLES --- */
.layers-deconstructor-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-width: 1200px;
  margin: 0 auto;
}

.layer-deconstructor-card {
  background: rgba(10, 16, 32, 0.88);
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  padding: 16px 20px;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(12px);
  transition: all 0.25s ease;
}

.layer-deconstructor-card:hover {
  border-color: var(--border-bright);
  box-shadow: 0 0 25px rgba(0, 243, 255, 0.15);
  transform: translateY(-2px);
}

.layer-deconstructor-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
}

.layer-card-1::before { background: var(--accent-cyan); }
.layer-card-2::before { background: var(--domain-air); }
.layer-card-3::before { background: var(--accent-green); }
.layer-card-4::before { background: var(--accent-amber); }
.layer-card-5::before { background: var(--accent-qkd); }
.layer-card-6::before { background: #a855f7; }

.layer-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.layer-card-title {
  font-family: var(--font-display);
  font-size: 1.15rem;
  font-weight: 700;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 10px;
}

.layer-card-body {
  display: grid;
  grid-template-columns: 2fr 1fr 150px;
  gap: 16px;
  align-items: center;
}

.layer-desc-text {
  font-size: 0.78rem;
  color: var(--text-dim);
  line-height: 1.5;
}

.layer-spec-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: var(--text-muted);
}

.layer-spec-item strong {
  color: #fff;
}

.btn-layer-isolate {
  background: rgba(14, 22, 40, 0.8);
  border: 1px solid var(--accent-cyan);
  color: var(--accent-cyan);
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 700;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  text-align: center;
  transition: all 0.2s ease;
}

.btn-layer-isolate:hover {
  background: var(--accent-cyan);
  color: #000;
  box-shadow: 0 0 15px rgba(0, 243, 255, 0.4);
}
"""

if '.canvas-layer-filter-bar' not in css:
    css += "\n" + layer_css
    with open('css/tactical.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("tactical.css updated with layer styles")

# 2. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add view tab
old_nav = """      <button class="view-tab" data-view="core">
        📦 PYTHON v0.1 PROTOCOL & SUITE
      </button>
    </nav>"""

new_nav = """      <button class="view-tab" data-view="core">
        📦 PYTHON v0.1 PROTOCOL & SUITE
      </button>
      <button class="view-tab" data-view="layers">
        📚 ALL WEB & SYSTEM LAYERS (DECONSTRUCTED)
      </button>
    </nav>"""

if 'data-view="layers"' not in html:
    html = html.replace(old_nav, new_nav)

# Add domain filter bar inside canvas-wrapper
old_canvas_wrap = """        <!-- View 1: Multi-Domain 2.5D Canvas -->
        <div class="canvas-wrapper" id="multidomainWrapper">
          <canvas id="tacticalCanvas"></canvas>"""

new_canvas_wrap = """        <!-- View 1: Multi-Domain 2.5D Canvas -->
        <div class="canvas-wrapper" id="multidomainWrapper">
          <!-- Interactive Domain Layer Filter Bar -->
          <div class="canvas-layer-filter-bar">
            <span class="filter-bar-title">ISOLATE DOMAIN LAYER:</span>
            <button class="domain-layer-btn active" data-domain="all">ALL DOMAINS</button>
            <button class="domain-layer-btn" data-domain="space">🛰️ SPACE LAYER</button>
            <button class="domain-layer-btn" data-domain="air">✈️ AIR LAYER</button>
            <button class="domain-layer-btn" data-domain="sea">⚓ SEA LAYER</button>
            <button class="domain-layer-btn" data-domain="land">🛡️ LAND LAYER</button>
          </div>
          <canvas id="tacticalCanvas"></canvas>"""

if 'canvas-layer-filter-bar' not in html:
    html = html.replace(old_canvas_wrap, new_canvas_wrap)

# Add layersWrapper
layers_wrapper_html = """
        <!-- View 6: Complete Web & System Layers Breakdown (Separated View) -->
        <div style="display:none; padding:18px; overflow-y:auto; height:100%;" id="layersWrapper">
          <div class="layers-deconstructor-container">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
              <h2 style="font-family:var(--font-display); font-size:1.35rem; color:#fff; letter-spacing:1px;">
                📚 COMPLETE SYSTEM & WEB LAYERS ARCHITECTURE (SEPARATED)
              </h2>
              <span class="badge-version green">6/6 LAYERS ACTIVE & SYNCHRONIZED</span>
            </div>
            <p style="font-size:0.78rem; color:var(--text-dim); margin-bottom:12px; font-family:var(--font-mono);">
              Each layer operates autonomously with strict abstraction boundaries, unified by Zero-Trust Causality & Disruption-Tolerant (CDT) consensus. Click "INSPECT LAYER" to isolate any layer.
            </p>

            <!-- Layer 1: Gateway & UI -->
            <div class="layer-deconstructor-card layer-card-1">
              <div class="layer-card-header">
                <div class="layer-card-title">
                  <span style="color:var(--accent-cyan);">LAYER 1</span>
                  <span>// CLIENT COMMAND GATEWAY & TACTICAL HUD LAYER</span>
                </div>
                <span class="badge-version cyan">AUTHENTICATED (ZERO-TRUST)</span>
              </div>
              <div class="layer-card-body">
                <div class="layer-desc-text">
                  Handles user identity, defense DEFCON status, starting sign-in authorization, Web Audio API tactical sound synthesis, and real-time operator situational awareness HUD.
                </div>
                <div class="layer-spec-list">
                  <div class="layer-spec-item">Protocol: <strong>HTTP/2 + Web Audio + JWT</strong></div>
                  <div class="layer-spec-item">Security: <strong>Zero-Trust Session Tokens</strong></div>
                  <div class="layer-spec-item">Clearance: <strong>COMMANDANT_MAX</strong></div>
                </div>
                <div>
                  <button class="btn-layer-isolate" data-target="signout">SIGN IN FLOW</button>
                </div>
              </div>
            </div>

            <!-- Layer 2: Multi-Domain Physical & Link Layer -->
            <div class="layer-deconstructor-card layer-card-2">
              <div class="layer-card-header">
                <div class="layer-card-title">
                  <span style="color:var(--domain-air);">LAYER 2</span>
                  <span>// MULTI-DOMAIN PHYSICAL & DATA LINK LAYER (SPACE · AIR · SEA · LAND)</span>
                </div>
                <span class="badge-version green">14 ACTIVE LINKS (100% HEALTH)</span>
              </div>
              <div class="layer-card-body">
                <div class="layer-desc-text">
                  Controls the kinetic domain nodes across low-earth orbit (SDA pLEO laser OISL), airborne high-bandwidth data links (MADL / TTNT), naval acoustic / VLF submarine relays, and ground tactical MANETs.
                </div>
                <div class="layer-spec-list">
                  <div class="layer-spec-item">Optical Media: <strong>100 Gbps Laser OISL</strong></div>
                  <div class="layer-spec-item">RF Media: <strong>STANAG-5066 HF Ionosphere</strong></div>
                  <div class="layer-spec-item">Tactical Mesh: <strong>Link-16 / MANET Swarm</strong></div>
                </div>
                <div>
                  <button class="btn-layer-isolate" data-target="multidomain">ISOLATE LAYER</button>
                </div>
              </div>
            </div>

            <!-- Layer 3: Core Tactical Mesh & Failover Routing Layer -->
            <div class="layer-deconstructor-card layer-card-3">
              <div class="layer-card-header">
                <div class="layer-card-title">
                  <span style="color:var(--accent-green);">LAYER 3</span>
                  <span>// CORE TACTICAL MESH & NODE D HOT-STANDBY FAILOVER LAYER</span>
                </div>
                <span class="badge-version green">18ms AUTONOMOUS REROUTING</span>
              </div>
              <div class="layer-card-body">
                <div class="layer-desc-text">
                  Executes deterministic packet routing (CMD ➔ A ➔ B ➔ C ➔ RECON). Under jamming or node destruction, instantaneously promotes Node D from standby to active relay with zero packet loss.
                </div>
                <div class="layer-spec-list">
                  <div class="layer-spec-item">Topology: <strong>5-Node BFT-Protected Mesh</strong></div>
                  <div class="layer-spec-item">Recovery Limit: <strong>&lt;50ms Sub-second Healing</strong></div>
                  <div class="layer-spec-item">Packet Loss: <strong>0.00% Guaranteed</strong></div>
                </div>
                <div>
                  <button class="btn-layer-isolate" data-target="architecture">ISOLATE LAYER</button>
                </div>
              </div>
            </div>

            <!-- Layer 4: Consensus & CDT Temporal Horizon Layer -->
            <div class="layer-deconstructor-card layer-card-4">
              <div class="layer-card-header">
                <div class="layer-card-title">
                  <span style="color:var(--accent-amber);">LAYER 4</span>
                  <span>// CAUSALITY & DISRUPTION-TOLERANT (CDT) CONSENSUS LAYER</span>
                </div>
                <span class="badge-version amber">T* DIVERGENCE BOUNDED</span>
              </div>
              <div class="layer-card-body">
                <div class="layer-desc-text">
                  Maintains causal ordering across partitioned networks with high propagation delay. Guarantees eventual swarm convergence without centralized clocks using vector-time horizons and Byzantine isolation.
                </div>
                <div class="layer-spec-list">
                  <div class="layer-spec-item">Algorithm: <strong>CDT-Lamport Horizon Engine</strong></div>
                  <div class="layer-spec-item">Convergence: <strong>T* = ∞ Guaranteed Secure</strong></div>
                  <div class="layer-spec-item">Tolerance: <strong>f &lt; n/3 Byzantine Nodes</strong></div>
                </div>
                <div>
                  <button class="btn-layer-isolate" data-target="cdt">ISOLATE LAYER</button>
                </div>
              </div>
            </div>

            <!-- Layer 5: Quantum Enclave & Post-Quantum Cryptography -->
            <div class="layer-deconstructor-card layer-card-5">
              <div class="layer-card-header">
                <div class="layer-card-title">
                  <span style="color:var(--accent-qkd);">LAYER 5</span>
                  <span>// QUANTUM KEY DISTRIBUTION (QKD) & PQC CRYPTOGRAPHIC ENCLAVE</span>
                </div>
                <span class="badge-version" style="border-color:var(--accent-qkd); color:var(--accent-qkd);">NIST FIPS 203 CERTIFIED</span>
              </div>
              <div class="layer-card-body">
                <div class="layer-desc-text">
                  Employs BB84 polarized entangled photons for physical layer eavesdropping detection (QBER &lt; 11%) combined with NIST ML-KEM-768 Kyber and ML-DSA-65 Dilithium for post-quantum defense against Shor's algorithm.
                </div>
                <div class="layer-spec-list">
                  <div class="layer-spec-item">Key Exchange: <strong>ML-KEM-768 (Module-LWE)</strong></div>
                  <div class="layer-spec-item">Signatures: <strong>ML-DSA-65 (Lattice)</strong></div>
                  <div class="layer-spec-item">QKD Channel: <strong>BB84 Dual-Basis (X / +)</strong></div>
                </div>
                <div>
                  <button class="btn-layer-isolate" data-target="quantum">ISOLATE LAYER</button>
                </div>
              </div>
            </div>

            <!-- Layer 6: Backend Service & Protocol Transport Layer -->
            <div class="layer-deconstructor-card layer-card-6">
              <div class="layer-card-header">
                <div class="layer-card-title">
                  <span style="color:#a855f7;">LAYER 6</span>
                  <span>// BACKEND RUNTIME, WEBSOCKET STREAM & PYTHON v0.1 PROTOCOL</span>
                </div>
                <span class="badge-version green">PORT 8001 LIVE STREAMING</span>
              </div>
              <div class="layer-card-body">
                <div class="layer-desc-text">
                  FastAPI high-performance ASGI service, bidirectional WebSockets (/api/v1/mesh/stream), and immutable mesh-object protocol serialization with full pytest validation.
                </div>
                <div class="layer-spec-list">
                  <div class="layer-spec-item">Core Engine: <strong>Python 3.12 + FastAPI</strong></div>
                  <div class="layer-spec-item">Stream: <strong>WebSocket RFC 6455 (Full Duplex)</strong></div>
                  <div class="layer-spec-item">Test Suite: <strong>9/9 Pytest Verified</strong></div>
                </div>
                <div>
                  <button class="btn-layer-isolate" data-target="core">ISOLATE LAYER</button>
                </div>
              </div>
            </div>

          </div>
        </div>
"""

# Insert layersWrapper before closing </section>
if 'id="layersWrapper"' not in html:
    html = html.replace('      </section>\n\n      <!-- Right Sidebar', layers_wrapper_html + '\n      </section>\n\n      <!-- Right Sidebar')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html updated successfully")
