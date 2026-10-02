# create_dashboard_page.py
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update title
html = html.replace(
    '<title>NULLMESH DEFENSE // Integrated C4ISR Tactical Architecture & Quantum Enclave</title>',
    '<title>NULLMESH DEFENSE // Standalone Main Function Platform</title>'
)

# 2. Add Top Page Switch Bar above <header class="top-header">
page_switch_bar = """
    <!-- ======================================================== -->
    <!-- TOP NAVIGATION: SWITCH SEPARATELY BETWEEN ALL 3 PAGES   -->
    <!-- ======================================================== -->
    <div style="background:rgba(6,10,22,0.95); border-bottom:1px solid rgba(0,243,255,0.25); padding:8px 24px; display:flex; justify-content:space-between; align-items:center; backdrop-filter:blur(12px); position:sticky; top:0; z-index:100000;">
      <div style="display:flex; align-items:center; gap:10px;">
        <span style="color:var(--accent-cyan, #00f3ff); font-size:1rem;">🛡️</span>
        <span style="font-family:var(--font-display, 'Outfit', sans-serif); font-weight:800; letter-spacing:1px; font-size:0.88rem; color:#fff;">
          NULLMESH DEFENSE PLATFORM
        </span>
      </div>

      <nav style="display:flex; gap:10px; align-items:center;">
        <span style="font-family:var(--font-mono); font-size:0.68rem; color:var(--text-dim); margin-right:4px;">
          SEPARATE WEB PAGES:
        </span>
        <a href="/signin.html" style="text-decoration:none; padding:5px 12px; border-radius:6px; font-family:var(--font-mono); font-size:0.72rem; font-weight:700; border:1px solid rgba(255,255,255,0.1); color:var(--text-dim); display:flex; align-items:center; gap:6px;">
          🔑 1. SIGN IN PAGE
        </a>
        <a href="/payment.html" style="text-decoration:none; padding:5px 12px; border-radius:6px; font-family:var(--font-mono); font-size:0.72rem; font-weight:700; border:1px solid rgba(255,255,255,0.1); color:var(--text-dim); display:flex; align-items:center; gap:6px;">
          💳 2. PAYMENT & SUBSCRIPTION PAGE
        </a>
        <a href="/dashboard.html" style="text-decoration:none; padding:5px 12px; border-radius:6px; font-family:var(--font-mono); font-size:0.72rem; font-weight:700; border:1px solid var(--accent-cyan); background:rgba(0,243,255,0.2); color:var(--accent-cyan); box-shadow:0 0 10px rgba(0,243,255,0.3); display:flex; align-items:center; gap:6px;">
          ⚡ 3. MAIN FUNCTION WEB PAGE (CURRENT)
        </a>
      </nav>
    </div>
"""

# Insert right after <body>
html = html.replace('<body>', '<body>\n' + page_switch_bar)

# Remove the authGatewayOverlay on the standalone dashboard so it opens directly!
html = html.replace('<div class="auth-gateway-overlay" id="authGatewayOverlay">', '<div class="auth-gateway-overlay" id="authGatewayOverlay" style="display:none !important;">')

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("dashboard.html created successfully")
