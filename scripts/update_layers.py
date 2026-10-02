# update_layers.py - Add domain filtering and layer deconstruction
import re

with open('js/canvas_renderer.js', 'r', encoding='utf-8') as f:
    code = f.read()

if 'activeDomainFilter' not in code:
    code = code.replace(
        'this.jamRings = [];',
        'this.jamRings = [];\n    this.activeDomainFilter = "all";'
    )
    code = code.replace(
        'const ty = tNode.yPct * this.height;\n\n      ctx.save();',
        'const ty = tNode.yPct * this.height;\n\n      ctx.save();\n      if (this.activeDomainFilter !== "all") {\n        if (sNode.domain !== this.activeDomainFilter && tNode.domain !== this.activeDomainFilter) {\n          ctx.globalAlpha = 0.06;\n        } else {\n          ctx.globalAlpha = 1.0;\n        }\n      }'
    )
    code = code.replace(
        'const isHovered = this.hoveredNode && this.hoveredNode.id === node.id;\n\n      ctx.save();',
        'const isHovered = this.hoveredNode && this.hoveredNode.id === node.id;\n\n      ctx.save();\n      if (this.activeDomainFilter !== "all") {\n        if (node.domain !== this.activeDomainFilter) {\n          ctx.globalAlpha = 0.12;\n        } else {\n          ctx.globalAlpha = 1.0;\n        }\n      }'
    )
    with open('js/canvas_renderer.js', 'w', encoding='utf-8') as f:
        f.write(code)
    print("canvas_renderer.js updated successfully")
else:
    print("Already updated")
