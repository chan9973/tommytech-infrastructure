# 🔧 Fusion 360 CAM Workflow — Complete Guide

**Created:** 2026-08-17  
**[[wikilink]]**: Open in Obsidian and use [[←backlinks]] or search for `fusion360`

---

## Overview: Fusion 360 CAD → CAM Integration

Fusion 360 is a **cloud-native PLM + CAD/CAM+CFD** platform that lets you design parts, then generate G-code in the same app. Free tier available; paid plans for professional teams (≈$50/mo per user).

### Workflow Summary

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────────┐
│ 1. Create CAD   │ →   │ 2. Select CAM tools  │ →   │ 3. Generate G-code  │
│    (solid model) │     │    & toolpaths       │     │    (.nc file)       │
└─────────────────┘     └──────────────────────┘     └─────────────────────┘
                                    ↓
                            ⬇️ 4. Simulate → 5. Machine
```

---

## Step 1: Creating the Part Design

### 📐 Design Fundamentals

| Concept | Fusion 360 Feature | [[wikilink]] Notes |
|---------|-------------------|---------------------|
| **Sketch** | Start with rectangular, circle, custom paths | Use constraints (horizontal/vertical/horizontal) to avoid misalignment |
| **Solidify** | Extrude, Revolve → 3D solid | Add fillets/radius before extruding for cleaner edges |
| **Holes** | HOLE command with thread or simple hole | Specify depth (% of part thickness) for countersinks |
| **Features** | Chamfer, Fillet, Shell | Fillets improve tool entry/exit smoothness (G-code quality) |

### 💡 Fusion 360 CAD Tips

| Tip | Benefit | [[wikilink]] How to Apply |
|-----|---------|---------------------------|
| **Use datum planes** | Organize features on specific faces | Right-click → Create Datum Plane → Pick face |
| **Section views** | Verify internal geometry | Insert section plane before extrude |
| **Design history browser** | Undo any step by reversing | Edit sketch → reverse feature (e.g., "Remove Extrusion #3") |

---

## Step 2: CAM Setup

### 🎛️ CAM Workspace Tabs

Fusion 360 organizes CAM operations into tabs:

- **Rough Operations**: High-material removal, fast feeds
- **Finish Operations**: Fine-passes for surface quality
- **Drilling**: Straight holes (G74/G83 peck, G81 simple), countersink, spotface
- **Milling Contours**: 2D profiles, pockets, adaptive routing
- **3D Milling**: Adaptive milling, variable-depth carving
- **Lathing**: Convert model to cylindrical part geometry

### ⚙️ Machine Setup (First Time Only)

1. **CAM Tab** → "Machine Setup"
2. **New machine**: Select your CNC type
   - Desktop: "GRBL 0909", "Mach3/Mach4", or "LinuxCNC"
   - Industrial: Fanuc, Haas, Mitsubishi, etc.

**Machine Parameters**:

| Parameter | [[wikilink]] Fusion 360 Field | Typical Values |
|-----------|-------------------------------|----------------|
| **Max spindle speed (RPM)** | `Machine → Advanced → Max Spindle Speed` | 12000 (desktop router) to 6000 (metal mill) |
| **Min step size** | `Step Over → Min Step Over` | 0.001 mm (precision), 0.05 mm (coarse) |
| **Units**: Inch/Metric | Select in CAM setup | Metric is standard for CNC; inch for US shops |

---

## Step 3: Tooling Setup

### 🛠️ Define End Mills (Tool Library)

**Before generating toolpaths**:

1. **CAM Tab** → "Tools Browser"
2. **Define End Mill**: Click "Define" + "End Mill"
   - Diameter: e.g., 0.0625″ (1.5/1.6mm), 0.125″ (3mm)
   - Flutes: 2-flute (wood/rust), 4-flute (aluminum fine finish)
   - Shank type: End mill, ball nose, V-bit

**Tool Parameters**:

| Parameter | Why It Matters | [[wikilink]] Recommended |
|-----------|----------------|--------------------------|
| **Step over %** | Tool width × stepover = cut width | Roughing: 30–40%; Finishing: 5–10% |
| **Plunge feed** | First Z-axis pass speed | Start slow (e.g., 200–400 mm/min); avoid >70% of surface feed |
| **Clamping type** | ER-32, HSK, etc. | Match your machine; Fusion uses standard R8/Taper |

### 🛠️ Toolpaths Browser

**Toolpath Types**:

- **Pocket**: Clears flat area with parallel or spiral cut
- **Contour**: Single-pass outline (clean finish)
- **Adaptive Routing**: High efficiency for large 3D surfaces; follows curvature
- **Raster Mill**: Like paper printer, slow but smooth on soft materials

---

## Step 4: Generating G-code

### ⚙️ Common Settings by Material

**Wood Cutting** (Baltic Birch, MDF):

| Setting | [[wikilink]] Fusion Value | [[wikilink]] Notes |
|---------|--------------------------|--------------------|
| **Step Over** | 30–40% of tool diameter | Faster material removal; smooth on climb mill |
| **Z-step ( plunge depth)** | 0.1–0.2 mm per pass | Avoid >0.5mm or tool will break |
| **Feed Rate** | 2000–3000 mm/min | Adjust for bit size and hardness material |

**Metal Cutting** (Aluminum 6061):

| Setting | Fusion Value | [[wikilink]] Notes |
|---------|---------------|--------------------|
| **Step Over** | 5–10% for finish pass | Harder material; use sharper coating |
| **Plunge Feed** | 100–300 mm/min | Heat management crucial; too fast = melt risk |
| **Coolant on?** | Enable in setup window | Aluminum: oil mist; stainless: flood coolant |

---

## Step 5: Simulation (Before Cutting!)

**🚨 Critical Safety Step**:

1. Click **"Show simulation"** button in toolpath preview pane
2. Inspect for:
   - Collision between tool and machine gantry
   - Over-travel beyond X/Y/Z limits
   - First cut matches material thickness

**Simulation Options**:

| Option | Use Case | [[wikilink]] Notes |
|--------|----------|--------------------|
| **Fast (light)** | Check for collisions, rapid moves | Skips feed rates, shows only geometry |
| **Detailed** | Verify Z-axis depth progression | Shows full feed rates + coolant activation |
| **Animation duration** | Preview full cut or first 60 seconds | Long cuts: preview only first minute to save time |

---

## Step 6: Post-Processors

Fusion 360 generates G-code with post-processors specific to your machine controller:

| Controller Type | Extension | [[wikilink]] Common Machines |
|-----------------|-----------|------------------------------|
| **GRBL-based** | `.nc` or `.eng` | Shapeoko, xCarve, CNCRouter (OpenBuilds) |
| **Mach3/Mach4** | `.ngc` | Mach3 post-processor (.nc equivalent) |
| **LinuxCNC** | `.gcode` | Debian-based with GRBL+Linux overlay |
| **Fanuc/Haas** | `.fanuc`, `.cnctools` | Industrial metal milling machines |

### Export Steps

1. File → Make G-code → Select toolpath (or all)
2. Choose post-processor: e.g., "GRBL 0909" for Shapeoko-like machine
3. Save as `.nc` or machine-specific format

---

## Automation with Hermes + Python

Fusion 360 has **limited scripting** (Grasshopper plugin, API calls for commercial). For workflow automation:

### 💡 Script to batch-export toolpaths

```python
# scripts/fusion360_batch_export.py (draft concept)
import json
from pathlib import Path

VARS = {
    "FUSION_API_URL": "https://apis.fusion360.design",
    "POST_PROCESSOR_GRBL": "GRBL_0909.nc",
}

def export_toolpath(project_id: str, toolpath_name: str) -> None:
    """Export Fusion 360 toolpath to local G-code."""
    # Note: Requires Fusion Cloud OAuth and Fusion API access
    # This is more for advanced integration with commercial license
    pass
```

**[[wikilink]]**: For hobbyists, manual export via File → Make G-code is sufficient. Automation scripts focus on **post-export workflow tracking**.

---

## Integration with Obsidian Wiki

### 📝 Note Structure Template

When you finish a Fusion 360 project, save to wiki:

```markdown
# Project Log — [Project Name] 2025-08-17

**CAD Part**: `parts/my-gear/final_design.step`  
**Toolpath generated**: `toolpaths/gear_v3.nc`  
**Machine**: Shapeoko (GRBL board, air-cooled 2.4kW spindle)  
**G-code export**: Fusion 360 GRBL_0909  

### Material
- Baltic Birch plywood (1/8″ or 3.175mm)

### Toolpaths Used
1. **Profile cut**: Outer contour (3×300 mm feed, 12k RPM)
2. **Pocket**: Inner holes (G-code depth step 0.2mm each pass)

### Notes
- [[wikilink]]: G-code shows toolpath collision near bottom-left corner  
- First pass chewed into edge → adjust stepover to 25%  

---

*Link related notes using wikilinks `[[part]], [[toolpaths]]` for easy lookup.*
```

### 📂 Obsidian Folder Structure Suggestion

Create these folders at root of vault:

- `/fusion360/`
  - `/projects/my-first-gear/`
  - `/toolpaths/my-first-cut.nc`
- `/cad/designs/`
- `/gcode-exports/`

---

## Resources & Documentation

| Resource | URL / Link | [[wikilink]] Notes |
|----------|------------|--------------------|
| **Fusion 360 CAD/CAM Docs** | https://fusion360.autodesk.com | Official tutorials; search by material type |
| **Toolpath Strategies (adaptive)** | [Autodesk Adaptive Milling Guide](https://fusion360.autodesk.com/docs/cam/operations) | Great for 3D carving work |
| **G-code post-processor list** | Fusion → CAM → Machine setup → Post-processors | Match GRBL version to machine controller |

---

## Tags & Cross-References

**tags**: `[[fusion360]]`, `[[cad]]`, `[[cam]]`, `[[software]]`  
**Related notes**: 
- [`cnc.md`](memories/cnc.md) (G-code commands, troubleshooting)
- [`cam_workflow.md`](memories/cam_workflow.md) (CAM workflow comparison, safety checklist)
- [`material_properties.md`](memories/material_properties.md) (cutting parameters for wood/metal/table)

---

*Continue expanding this note as you try new toolpaths or run into edge cases!*
