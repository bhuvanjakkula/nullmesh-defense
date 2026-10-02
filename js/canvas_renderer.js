// NULLMESH DEFENSE - Multi-Domain Tactical Canvas Renderer
// Renders Land, Sea, Air, Space layers with animated laser links, ionospheric bounce, and particle flows

export class TacticalCanvasRenderer {
  constructor(canvas, engine) {
    this.canvas = canvas;
    this.ctx = canvas.getContext("2d");
    this.engine = engine;
    this.selectedNode = null;
    this.hoveredNode = null;

    this.particles = [];
    this.animTime = 0;
    this.jamRings = [];
    this.activeDomainFilter = "all";

    this.initCanvasSize();
    window.addEventListener("resize", () => this.initCanvasSize());
    this.setupInteraction();
    this.initParticles();
    this.animate();
  }

  initCanvasSize() {
    const rect = this.canvas.parentElement.getBoundingClientRect();
    this.canvas.width = rect.width * window.devicePixelRatio;
    this.canvas.height = rect.height * window.devicePixelRatio;
    this.ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
    this.width = rect.width;
    this.height = rect.height;
  }

  setupInteraction() {
    this.canvas.addEventListener("mousemove", (e) => {
      const rect = this.canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      let found = null;
      this.engine.nodes.forEach(node => {
        const nx = node.xPct * this.width;
        const ny = node.yPct * this.height;
        const dist = Math.hypot(x - nx, y - ny);
        if (dist < 18) found = node;
      });

      this.hoveredNode = found;
      this.canvas.style.cursor = found ? "pointer" : "default";
    });

    this.canvas.addEventListener("click", (e) => {
      if (this.hoveredNode) {
        this.selectedNode = this.hoveredNode;
        if (window.onNodeSelected) {
          window.onNodeSelected(this.selectedNode);
        }
      }
    });
  }

  initParticles() {
    for (let i = 0; i < 40; i++) {
      this.particles.push({
        linkIndex: Math.floor(Math.random() * this.engine.links.length),
        progress: Math.random(),
        speed: 0.003 + Math.random() * 0.005
      });
    }
  }

  animate() {
    this.animTime += 0.02;
    this.render();
    requestAnimationFrame(() => this.animate());
  }

  render() {
    const ctx = this.ctx;
    ctx.clearRect(0, 0, this.width, this.height);

    // 1. Draw Tactical Grid & Domain Horizon Bands
    this.drawDomainBands(ctx);
    this.drawIonosphericCurvature(ctx);

    // 2. Draw Network Links (Laser OISL, HF Bounce, Tactical MANET)
    this.drawLinks(ctx);

    // 3. Draw Traveling Data Packets
    this.drawPacketFlow(ctx);

    // 4. Draw Domain Nodes
    this.drawNodes(ctx);

    // 5. Draw Jamming & Strike Visual Effects
    this.drawThreatEffects(ctx);
  }

  drawDomainBands(ctx) {
    const domains = [
      { name: "SPACE DOMAIN (pLEO / MEO / GEO ORBITS)", y1: 0, y2: 0.22, color: "rgba(0, 243, 255, 0.02)" },
      { name: "AIR DOMAIN (DAF BATTLE NET / AEW&C / CCA)", y1: 0.22, y2: 0.48, color: "rgba(112, 161, 255, 0.02)" },
      { name: "SEA DOMAIN (CARRIER STRIKE GROUP / USV)", y1: 0.48, y2: 0.72, color: "rgba(0, 210, 211, 0.02)" },
      { name: "LAND DOMAIN (TACTICAL MANET / SUDARSHAN CHAKRA)", y1: 0.72, y2: 1.0, color: "rgba(46, 213, 115, 0.02)" }
    ];

    domains.forEach(d => {
      ctx.fillStyle = d.color;
      ctx.fillRect(0, d.y1 * this.height, this.width, (d.y2 - d.y1) * this.height);

      ctx.strokeStyle = "rgba(0, 243, 255, 0.08)";
      ctx.beginPath();
      ctx.moveTo(0, d.y2 * this.height);
      ctx.lineTo(this.width, d.y2 * this.height);
      ctx.stroke();

      ctx.fillStyle = "rgba(255, 255, 255, 0.25)";
      ctx.font = "9px 'JetBrains Mono'";
      ctx.fillText(d.name, 14, d.y1 * this.height + 16);
    });
  }

  drawIonosphericCurvature(ctx) {
    // Draws the F-Layer Ionosphere arc where STANAG-5066 bounces
    const ionoY = 0.06 * this.height;
    ctx.save();
    ctx.strokeStyle = "rgba(0, 243, 255, 0.18)";
    ctx.setLineDash([4, 6]);
    ctx.beginPath();
    ctx.moveTo(0, ionoY);
    ctx.bezierCurveTo(this.width * 0.3, ionoY - 10, this.width * 0.7, ionoY - 10, this.width, ionoY);
    ctx.stroke();

    ctx.fillStyle = "rgba(0, 243, 255, 0.4)";
    ctx.font = "8px 'JetBrains Mono'";
    ctx.fillText("IONOSPHERE F2 REFLECTION LAYER (BLOS HF BOUNCE BAND)", this.width - 290, ionoY + 12);
    ctx.restore();
  }

  drawLinks(ctx) {
    this.engine.links.forEach(link => {
      const sNode = this.engine.nodes.get(link.source);
      const tNode = this.engine.nodes.get(link.target);
      if (!sNode || !tNode) return;

      const sx = sNode.xPct * this.width;
      const sy = sNode.yPct * this.height;
      const tx = tNode.xPct * this.width;
      const ty = tNode.yPct * this.height;

      ctx.save();
      if (this.activeDomainFilter !== "all") {
        if (sNode.domain !== this.activeDomainFilter && tNode.domain !== this.activeDomainFilter) {
          ctx.globalAlpha = 0.06;
        } else {
          ctx.globalAlpha = 1.0;
        }
      }

      // Style link according to type and health
      if (link.status === "severed") {
        ctx.strokeStyle = "rgba(255, 51, 102, 0.2)";
        ctx.setLineDash([2, 6]);
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(sx, sy);
        ctx.lineTo(tx, ty);
        ctx.stroke();
        ctx.restore();
        return;
      }

      if (link.status === "jammed") {
        ctx.strokeStyle = "rgba(255, 183, 3, 0.35)";
        ctx.setLineDash([3, 3]);
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(sx, sy);
        ctx.lineTo(tx, ty);
        ctx.stroke();
        ctx.restore();
        return;
      }

      if (link.type === "hf-ionosphere") {
        // Curved ionospheric reflection arc
        ctx.strokeStyle = "rgba(0, 245, 155, 0.75)";
        ctx.lineWidth = 2;
        ctx.setLineDash([5, 4]);
        ctx.beginPath();
        ctx.moveTo(sx, sy);
        const midX = (sx + tx) / 2;
        const midY = 0.05 * this.height; // Ionosphere bounce apex
        ctx.quadraticCurveTo(midX, midY, tx, ty);
        ctx.stroke();
      } else if (link.type === "oisl") {
        // High-precision Optical Intersatellite Laser Beam
        ctx.strokeStyle = "rgba(0, 243, 255, 0.85)";
        ctx.shadowColor = "#00f3ff";
        ctx.shadowBlur = 8;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(sx, sy);
        ctx.lineTo(tx, ty);
        ctx.stroke();
      } else if (link.type.includes("laser")) {
        // Space-to-Earth Laser Downlink
        ctx.strokeStyle = "rgba(0, 243, 255, 0.6)";
        ctx.shadowColor = "#00f3ff";
        ctx.shadowBlur = 6;
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(sx, sy);
        ctx.lineTo(tx, ty);
        ctx.stroke();
      } else {
        // Standard RF / MANET mesh link
        ctx.strokeStyle = "rgba(112, 161, 255, 0.35)";
        ctx.lineWidth = 1.2;
        ctx.beginPath();
        ctx.moveTo(sx, sy);
        ctx.lineTo(tx, ty);
        ctx.stroke();
      }

      ctx.restore();
    });
  }

  drawPacketFlow(ctx) {
    ctx.save();
    this.particles.forEach(p => {
      const link = this.engine.links[p.linkIndex];
      if (!link || link.status !== "active") return;

      const sNode = this.engine.nodes.get(link.source);
      const tNode = this.engine.nodes.get(link.target);
      if (!sNode || !tNode) return;

      p.progress += p.speed;
      if (p.progress > 1) p.progress = 0;

      let px, py;
      if (link.type === "hf-ionosphere") {
        const sx = sNode.xPct * this.width;
        const sy = sNode.yPct * this.height;
        const tx = tNode.xPct * this.width;
        const ty = tNode.yPct * this.height;
        const midX = (sx + tx) / 2;
        const midY = 0.05 * this.height;

        const t = p.progress;
        px = (1 - t) * (1 - t) * sx + 2 * (1 - t) * t * midX + t * t * tx;
        py = (1 - t) * (1 - t) * sy + 2 * (1 - t) * t * midY + t * t * ty;
      } else {
        const sx = sNode.xPct * this.width;
        const sy = sNode.yPct * this.height;
        const tx = tNode.xPct * this.width;
        const ty = tNode.yPct * this.height;
        px = sx + (tx - sx) * p.progress;
        py = sy + (ty - sy) * p.progress;
      }

      ctx.fillStyle = link.type === "oisl" ? "#ffffff" : link.type === "hf-ionosphere" ? "#00f59b" : "#00f3ff";
      ctx.shadowColor = ctx.fillStyle;
      ctx.shadowBlur = 6;
      ctx.beginPath();
      ctx.arc(px, py, 2.5, 0, Math.PI * 2);
      ctx.fill();
    });
    ctx.restore();
  }

  drawNodes(ctx) {
    this.engine.nodes.forEach(node => {
      const x = node.xPct * this.width;
      const y = node.yPct * this.height;
      const isSelected = this.selectedNode && this.selectedNode.id === node.id;
      const isHovered = this.hoveredNode && this.hoveredNode.id === node.id;

      ctx.save();
      if (this.activeDomainFilter !== "all") {
        if (node.domain !== this.activeDomainFilter) {
          ctx.globalAlpha = 0.12;
        } else {
          ctx.globalAlpha = 1.0;
        }
      }

      // Node Status Color
      let nodeColor = "#00f3ff";
      if (node.status === "jammed") nodeColor = "#ffb703";
      if (node.status === "destroyed") nodeColor = "#ff3366";
      if (node.status === "rerouting") nodeColor = "#00f59b";

      // Outer Selection Ring
      if (isSelected || isHovered) {
        ctx.strokeStyle = nodeColor;
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.arc(x, y, 16, 0, Math.PI * 2);
        ctx.stroke();
      }

      // Orbital Drift / Pulse
      const pulseSize = Math.sin(this.animTime * 3 + node.xPct * 10) * 1.5;

      // Node Outer Glow
      ctx.fillStyle = nodeColor;
      ctx.shadowColor = nodeColor;
      ctx.shadowBlur = 10;
      ctx.beginPath();
      ctx.arc(x, y, 6 + pulseSize, 0, Math.PI * 2);
      ctx.fill();

      // Inner Core
      ctx.fillStyle = "#ffffff";
      ctx.beginPath();
      ctx.arc(x, y, 2.5, 0, Math.PI * 2);
      ctx.fill();

      // Domain Icon Indicator & Label
      ctx.fillStyle = "#f1f5f9";
      ctx.font = "10px 'JetBrains Mono'";
      ctx.fillText(node.id, x + 12, y + 3);

      ctx.fillStyle = "rgba(148, 163, 184, 0.8)";
      ctx.font = "8px 'Inter'";
      ctx.fillText(node.name, x + 12, y + 13);

      ctx.restore();
    });
  }

  drawThreatEffects(ctx) {
    // If broadband EW Jamming is active, draw electromagnetic interference ripples
    if (this.engine.activeThreats.has("EW_JAMMING")) {
      ctx.save();
      const waveY = (0.35 + 0.5 * Math.sin(this.animTime)) * this.height;
      ctx.strokeStyle = "rgba(255, 183, 3, 0.15)";
      ctx.lineWidth = 2;
      ctx.beginPath();
      for (let x = 0; x < this.width; x += 10) {
        const y = waveY + Math.sin(x * 0.05 + this.animTime * 5) * 15;
        if (x === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();
      ctx.restore();
    }
  }
}
