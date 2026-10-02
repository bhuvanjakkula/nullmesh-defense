# update_app_layers.py
with open('js/app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# 1. Add layers wrapper to views
app_js = app_js.replace(
    'core: document.getElementById("coreWrapper")',
    'core: document.getElementById("coreWrapper"),\n    layers: document.getElementById("layersWrapper")'
)

# 2. Add title for layers view
title_hook = 'if (viewKey === "core") centerTitle.textContent = "📦 PYTHON v0.1 DISRUPTION-TOLERANT PROTOCOL";'
new_title_hook = 'if (viewKey === "core") centerTitle.textContent = "📦 PYTHON v0.1 DISRUPTION-TOLERANT PROTOCOL";\n      if (viewKey === "layers") centerTitle.textContent = "📚 SYSTEM & WEB LAYERS ARCHITECTURE (DECONSTRUCTED)";'
app_js = app_js.replace(title_hook, new_title_hook)

# 3. Add Layer Filter and Isolate button handlers right before DOMContentLoaded closing
handler_code = """
  // --- DOMAIN LAYER FILTER CONTROLLERS ---
  document.querySelectorAll(".domain-layer-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      playTacticalBlip(880, 0.04);
      document.querySelectorAll(".domain-layer-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const domain = btn.dataset.domain;
      renderer.activeDomainFilter = domain;
      engine.log("LAYER_FILTER", `Isolating tactical layer: ${domain.toUpperCase()}`, "info");

      // Sync with left sidebar pills
      document.querySelectorAll(".domain-pill").forEach(p => {
        p.classList.toggle("active", p.dataset.domain === domain);
      });
    });
  });

  // Sync left sidebar domain pills to canvas renderer
  document.querySelectorAll(".domain-pill").forEach(pill => {
    pill.addEventListener("click", () => {
      const domain = pill.dataset.domain;
      if (!domain) return;
      renderer.activeDomainFilter = domain;
      document.querySelectorAll(".domain-layer-btn").forEach(b => {
        b.classList.toggle("active", b.dataset.domain === domain);
      });
    });
  });

  // Deconstructed Layer Card "ISOLATE LAYER" Action Buttons
  document.querySelectorAll(".btn-layer-isolate").forEach(btn => {
    btn.addEventListener("click", () => {
      const target = btn.dataset.target;
      playTacticalBlip(1100, 0.08);
      if (target === "signout") {
        showAuthGateway();
      } else {
        const matchingTab = document.querySelector(`.view-tab[data-view="${target}"]`);
        if (matchingTab) matchingTab.click();
      }
    });
  });
"""

if 'domain-layer-btn' not in app_js:
    # Insert before the last lines
    app_js = app_js.replace('  // Initial render\n  updateUI();', handler_code + '\n  // Initial render\n  updateUI();')

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)

print("js/app.js updated successfully")
