# wire_all_separate_pages.py
import re

# 1. Update index.html to redirect to /signin.html if opened as root, or provide clean navigation
with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

# Add meta refresh redirect to /signin.html or instant JS redirect
if 'window.location.href = "/signin.html"' not in idx:
    idx = idx.replace(
        '<head>',
        '<head>\n    <script>if (window.location.pathname === "/" || window.location.pathname === "/index.html") { window.location.href = "/signin.html"; }</script>'
    )
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(idx)
    print("index.html updated to redirect to /signin.html")

# 2. Update js/app.js to redirect btnSignOut to /signin.html
with open('js/app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

app_js = app_js.replace(
    'if (btnSignOut) {\n    btnSignOut.addEventListener("click", () => {\n      showAuthGateway();\n    });\n  }',
    'if (btnSignOut) {\n    btnSignOut.addEventListener("click", () => {\n      window.location.href = "/signin.html";\n    });\n  }'
)

app_js = app_js.replace(
    'if (target === "signout") {\n        showAuthGateway();\n      }',
    'if (target === "signout") {\n        window.location.href = "/signin.html";\n      } else if (target === "subscription") {\n        window.location.href = "/payment.html";\n      }'
)

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
print("js/app.js updated")

# 3. Update dashboard.html with updated app.js sync
with open('dashboard.html', 'r', encoding='utf-8') as f:
    dash = f.read()

# Make sure dashboard does NOT redirect to signin.html
dash = dash.replace(
    '<script>if (window.location.pathname === "/" || window.location.pathname === "/index.html") { window.location.href = "/signin.html"; }</script>',
    ''
)
with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(dash)
print("dashboard.html checked")

# 4. Update index.v0.html with navigation to all 3 separate pages
with open('index.v0.html', 'r', encoding='utf-8') as f:
    v0 = f.read()

v0_nav = """    <!-- Floating Quick Navigation Bar to all 3 separated pages -->
    <div style="position:fixed; top:12px; left:16px; z-index:999999; display:flex; align-items:center; gap:10px; background:rgba(10,16,32,0.92); border:1px solid rgba(0,243,255,0.4); border-radius:8px; padding:6px 14px; backdrop-filter:blur(10px); box-shadow:0 4px 20px rgba(0,0,0,0.5);">
      <a href="/signin.html" style="color:#94a3b8; text-decoration:none; font-family:'Courier New', monospace; font-size:11px; font-weight:700;">
        🔑 1. SIGN IN PAGE
      </a>
      <span style="color:#475569;">|</span>
      <a href="/payment.html" style="color:#94a3b8; text-decoration:none; font-family:'Courier New', monospace; font-size:11px; font-weight:700;">
        💳 2. PAYMENT PAGE
      </a>
      <span style="color:#475569;">|</span>
      <a href="/dashboard.html" style="color:#00f3ff; text-decoration:none; font-family:'Courier New', monospace; font-size:11px; font-weight:700; display:flex; align-items:center; gap:4px;">
        ⚡ 3. MAIN FUNCTION WEB PAGE
      </a>
    </div>"""

# Replace floating nav in v0
old_v0_bar = re.search(r'<!-- Floating Quick Navigation Bar -->.*?</div>', v0, re.DOTALL)
if old_v0_bar:
    v0 = v0.replace(old_v0_bar.group(0), v0_nav)
    with open('index.v0.html', 'w', encoding='utf-8') as f:
        f.write(v0)
    print("index.v0.html updated with 3-page navigation")
