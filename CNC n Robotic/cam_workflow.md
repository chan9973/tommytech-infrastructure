# 🔄 CAM (Computer-Aided Manufacturing) Workflow Guide

**Last updated:** 2026-08-17  
[[wikilink]] to this note: Open in Obsidian and use [[←backlinks]] or search for `cam`

---

## CAM Workflow Overview

```
CAD Design → Geometry Prep → Toolpath Selection → CAM Settings → G-code Output → CNC Machine
       ↓              ↓              ↓              ↓                ↓                  ↓
  (part         (fillets,        (mill/         (cut speeds,    (export .nc)      (post-processor
   drawing)    rounded edges)     rout/hold)     feed rates)                      specific to
                                        or          and           machine)              machine)
                                    plunge/peck    safety)
```

---

## Step-by-Step Workflow

### 1️⃣ **CAD Model Preparation**

- **Clean geometry**: Weld edges, remove unreferenced faces, fix normals
- **Add construction lines**: Define safe zones, machining limits, cutouts
- **Feature identification**: Which surfaces get cut? Which stay as bosses?

| CAD Tool | Notes | [[wikilink]] Reference |
|----------|-------|------------------------|
| Fusion 360 | Free tier available; cloud saves | Excellent CAM integration |
| SolidWorks | High-end, parametric | Steeper learning curve |
| FreeCAD | Open source, Linux/Windows | Good for hobbyists |

### 2️⃣ **Toolpath Strategy**

Choose based on material and tolerance needs:

- **Pocket**: 2+D, clears area with parallel or spiral toolpaths
- **Profile**: Follows contour of part perimeter (outline cut)
- **Contour**: Single-layer depth passes (clean finish)
- **3D Adaptive**: High material removal, follows surface curvature
- **Ramping**: Angled entry to avoid "plunge gouging"

### 3️⃣ **Cutting Parameters**

| Parameter | Typical Ranges | [[wikilink]] Notes |
|-----------|----------------|--------------------|
| Spindle RPM | 8000–24000 | Metal=6000–12k; Wood=12k–24k |
| Feed Rate (F) | 500–2500 mm/min | Depends on tool diameter, material hardness |
| Stepover | 10–30% of bit size | Roughing: 20–30%; Finishing: 3–8% |
| Plunge Feed | Slow first pass (avoid chip buildup) | Then accelerate to optimal |
| Peck Drill (G74/G83) | Q depth 50–60% of drill length | Prevents long chips in drilling thick blocks |

### 4️⃣ **Work Offset Setup**

- **G54-G59**: Work coordinate system offset points
- Machine → **Set Z-zero**: Touch tool tip to material top surface (using DRO or probe)
- Machine → **X/Y zero**: Align with part drawing origin (corner, boss, etc.)

### 5️⃣ **Simulation** (**Crucial Step!**)

Always simulate before running on real machine:

- Check for collisions (tool holder hitting gantry)
- Verify first cut depth matches material stock size
- Watch spindle speed ramps vs. rapid feed rates

### 6️⃣ **G-code Export & Post-processing**

Different CNC machines need different post-processors:

- **Fusion 360**: Select machine type (GRBL, Mach3/Mach4, LinuxCNC)
- **Mach3**: Standard `.nc` or `.ngc` extension for most controllers
- **GRBL**: Light-duty, hobby mill/router, G-code parser is minimal

---

## CAM Software Comparison

| Software | Cost | [[wikilink]] Pros | Cons |
|----------|------|------------------|------|
| Fusion 360 | Free/Pro ($50/mo) | Integrated CAD + CAM; cloud access | Steep learning curve for CAM tab |
| Mastercam | $$$$ | Industry standard, powerful | Expensive (~$6k–$12k license) |
| Carbide Motion (X-Carve) | Free | Easy, Inventables ecosystem | Limited toolpath types |
| Easel (Shapeoko) | Free/Paid apps | Tablet-friendly, intuitive | Basic features only |
| CamBam | Medium (~£30–$60) | Offline, good for 2.5D CAM | Less modern UI |

---

## Safety Checklist Before Cutting

- ✅ Z-axis: Tool tip at -Z material surface (or higher if using probe tool)
- ✅ Spindle RPM: Within machine limits (+tool holder rating)
- ✅ Vise/Clamp: Workpiece secured (not loose during cutting)
- ✅ Coolant: Active on spindle for metal cutting
- ✅ G-code preview: No collisions in first 30 seconds of motion

---

## Automation Idea with Hermes + Obsidian

Use Python to generate repeatable CAM presets or G-code snippets:

```python
# scripts/cam_automation.py (draft)
import os
from pathlib import Path

VARS = {
    "spindle_rpm": 12000,
    "feed_rate": 300,
    "stepover_percent": 25,
    "plunge_feed": 60,
}

def generate_gcode(python):
    lines = f"""%
O1 Program Header
G21 Metric units
G90 Absolute coordinates
G4 P1000 ; Delay for spindle warmup
"""
    # Add toolpath instructions...
    return "\n".join(lines) + "M30"
```

*See `scripts/cam_automation.py` for full implementation.*

---

## Tags & Cross-References

**Tags**: [[cam]], [[manufacturing]], [[tools]], [[python]]  
**Related notes**: [[cnc]] (G-code reference), [[material properties]] (cutting material data)

---

*Keep expanding this workflow as you automate with Python or refine CAM presets!*
