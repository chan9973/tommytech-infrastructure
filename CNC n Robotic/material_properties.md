# 📦 Material Properties for CNC Cutting

**Last updated:** 2026-08-17  
**[[wikilink]]**: Open in Obsidian and use [[←backlinks]] or search for `material`

---

## Why Material Properties Matter

Different materials require different:
- **Spindle RPM** (cutting speed = surface speed formula: SFM × 3.14 / tool diameter)
- **Feed Rate** (mm/min = RPM × tooth count × chip load)
- **Tool Type** (HSS vs coated carbide, end mill vs ball nose)
- **Coolant vs Air** (metal needs coolant; wood/plastic uses air exhaust)

---

## Common Materials Reference Table

### 🪵 Wood & Composites

| Material | Hardness | Typical RPM | Coolant | Notes |
|----------|----------|-------------|---------|--------|
| **Baltic Birch plywood** | Medium | 12000–18000 | Air | Edge banding may burn; use climb mill to tear less |
| **MDF** | Soft (dense) | 15000–24000 | Air/Compressed air (helps fine finish) | Dust extraction required; no coolant! |
| **Hard Maple/Oak** | Hard | 12000–16000 | Air | Pre-drill holes >7mm diameter |
| **PVC Plastic** | Medium-soft | 8000–12000 | Air | Avoid high heat (melts); use slow feed |
| **Acrylic/Plexiglass** | Soft | 8000–12000 | Air (light mist) | Slow cut to avoid cracking; edge polish needed |
| **Delrin (POM)** | Medium | 12000–18000 | Air/Compressed air | Self-lubricating plastic; runs cool |

**⚠️ Important:** Always vacuum/extract sawdust; inhalation harmful over time.

---

### ⭐ Metals (Machining)

| Material | Hardness | Typical RPM | Feed Rate (mm/min) | Tool Coating Needed? |
|----------|----------|-------------|---------------------|----------------------|
| **Aluminum 6061** | Soft/Medium | 8000–16000 | 500–2500 | Aluminum-specific coating (NiP, TiCN) |
| ** Brass C360** | Medium-Hard | 10000–16000 | 400–2000 | No special coating; good free-machining |
| **Steel 1018** | Hard | 3000–6000 | 200–1000 | Carbide with HSS or carbide (depending on budget) |
| **Stainless (304)** | Very Hard | 2500–5000 | 200–800 | Titanium nitride coating; slow, steady feed |
| Inconel (superalloy) | Extreme | 1500–3000 | 100–400 | Carbide only; very careful setup |

**⚠️ Metal Cutting Safety:**
- **Coolant essential** for heat management
- **Long chips**: Use peck drilling (G74/G83) to break chips regularly
- **Run-out**: Check tool holder runout (<0.02 mm preferred, <0.05 max)

---

### 🔮 Engineering Plastics

| Material | Properties | [[wikilink]] Tips |
|----------|------------|--------------------|
| **ABS** | Durable, heat-resistant (3D printed parts commonly) | Pre-heat bed if 3D+mill combo; can be glued after cutting |
| **PEEK** | High-temp, expensive | Requires CNC machine with good rigidity |
| **PTFE (Teflon)** | Very slippery, low friction | Stick to air cut; very soft material that grabs tool easily |

---

### ☕ Other Materials

| Material | Notes | [[wikilink]] Precautions |
|----------|-------|--------------------------|
| **Foam** | Very soft, easy cuts | Use sharp tool or bit for smooth edges; no coolant needed |
| **Carbon fiber** | Strong, expensive (CFRP composite) | **Respiratory toxicity!** Must use proper mask + extractor. Tool life limited by abrasive fibers. |
| **Glass-filled Nylon** | High strength | Slow cut speed to avoid melting/cracking at edges |

---

## Tool Selection Guide

### 🔪 End Mill Types

| Type | Description | Best for Material |
|------|-------------|-------------------|
| **Solid Carbide Ball Nose** | Rounded tip, smooth contours | 3D profiling on soft materials, wood, plastics |
| **Flute Spiral (2-flute)** | Good chip evacuation | Wood, softer aluminum (plenty of airflow) |
| **Solid Carbide Square Flute** | Rigid, precise corners | Hard metals, fine detail in steel/aluminum |
| **Aluminum Specific** | Coating, 4-flutes | Aluminum: fine finish, less heat buildup |

### ♿ Tool Size Guidelines

- **<6mm (1/4")**: Fine detail, tight tolerances (<0.05 mm)
- **8–12mm**: General-purpose stock milling, pocketing
- **>25mm**: Rough removal on soft materials only; rigid machines only

---

## Coolant vs Air

| Use Case | Method | [[wikilink]] Notes |
|----------|--------|----------------------|
| **Wood** | Compressed air/airblast | Clean chips; protect eyes from sawdust splash |
| **Aluminum (anodizable)** | Wet coolant or oil mist | Prevents "white rust" if using anodizing later |
| **Stainless steel** | Flood oil-based coolant | Essential for longevity of tool and workpiece |
| **Inconel/superalloys** | Heavy-duty flood cooling | High-heat, long-running cuts need constant coolant flow |

---

## Quick Lookup Script

```python
# scripts/material_lookup.py (draft)
from pathlib import Path
import yaml

MATERIAL_DB = {
    "aluminum-6061": {"rpm": 8000, "feed": 1500},
    "wood-baltic-birch": {"rpm": 14000, "feed": 2000},
    "steel-1018": {"rpm": 4000, "feed": 600},
}

def lookup_material(name: str):
    data = MATERIAL_DB.get(name.lower())
    return f"{name}: RPM={data['rpm']}, Feed={data['feed']} mm/min" if data else f"Not found in DB yet."
```

*See `scripts/material_lookup.py` for full implementation.*

---

## Tags & Cross-References

**Tags**: [[materials]], [[manufacturing]], [[cnc]]  
**Related notes**: [[cam_workflow]] (CAM params), [[tooling]] (bits, holders)

---

*Add new materials as you work with them!*
