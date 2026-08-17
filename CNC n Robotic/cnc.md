# 🖥️ CNC (Computer Numerical Control) — Quick Reference

**Last updated:** 2026-08-17  
[[wikilink]] to this note: Open in Obsidian and use [[←backlinks]] or search for `cnc`

---

## What is CNC?

**Computer Numerical Control (CNC)** is automated machine tool manufacturing where computers control cutting tools, 3D milling, routing, plasma cutting, etc., using G-code instructions.

### Core Principles

- **G-code**: ISO-standard programming language for motion (G0-X10 moves to X=10)
- **CAM software**: Converts CAD designs into G-code paths (Fusion 360, Mastercam, FreeCAD)
- **3-axis vs 5-axis**: Linear movements along X/Y/Z (+Y rotation on 4th axis)

---

## Main CNC Types

### 🪚 Router / Milling Machine
- Material: Wood, plastic, aluminum, composites
- Tools: End mills (carbide bit), spindle speed 12000–24000 RPM
- Common for: Prototypes, sign-making, small parts
- [[wikilink]] Typical G-code: `G0 X50 Y20` → rapid move, `G1 Z-5 F500` → cut at 50% speed

### 🦴 Lathe / Turning Center
- Material: Metal, wood, plastics, plastics
- Action: Rotating workpiece + stationary cutting tool
- Use case: Cylinders, shafts, fittings (lathe = turning)

### 🐍 Desktop 3D CNC Router
- Budget: $200–$500 machines (GRBL-based boards like Arduino)
- Example: X-Carve, Shapeoko, OpenBuilds
- Control software: Carveco, Inventables Cloud, Estlcam

### ✨ Laser Cutting / Engraving
- Distinct from CNC (no cutting tool, uses laser beam instead of spindle). Still controlled by G-code but different physics. Often integrated as "CNC laser combo".

---

## Essential Knowledge

### 🔧 Common Issues & Solutions
- **[Tool collision](wikilink)** → Spindle hits material surface unexpectedly → Check Z-axis zeroing (G54 offset), use probe tool
- **[Overheat on spindle](wikilink)]** → Coolant spray needed, check RPM limits
- **[Wobble in cuts](wikilink)]** → Dampener pads loose, belts slipping, tool holder not tightened

### 🐍 Example G-code Snippet
```gcode
G90 G17 G54           ; absolute coordinates, XY plane, work offset #1
G0 X20 Y20            ; rapid move (no spindle on)
G38.2 Z-0.2           ; homing probe check
G4 P2000              ; dwell 2 seconds (cooldown)
S12000 M3             ; spindle ON at 12000 RPM
G1 X70 Y50 F300       ; cut at path, feed rate 30% mm/min
M5                    ; spindle OFF  
```

### 🐍 Script to generate G-code basics (Python)
See `scripts/cnc_code_gen.py` for tooling in your folder.

---

## Tags & Cross-References

[[wikilink]] tags: [[tools]], [[manufacturing]], [[python]], [[research]]  
Related notes: See [[obsidian note system]] if storing CNC logs, [[hermes-agent]] for Python automation of CAM workflows  

---

*Keep expanding this wiki as we explore CNC projects together!*
