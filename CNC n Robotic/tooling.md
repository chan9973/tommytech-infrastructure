# 🔧 Tooling Reference: CNC Bits, Holders, Accessories

**Last updated:** 2026-08-17  
[[wikilink]] to this note: Open in Obsidian and use [[←backlinks]] or search for `tooling`

---

## Essential Tool Categories

```
┌──────────────────────┐
│   Cutting Tools      │ ← Bits, Inserts
│   (End mills,       │
│    drill bits)       │
└──────────────────────┘
              ↓
┌──────────────────────┐
│   Holders            │ ← Collets, tool holders
│   (ER collets,       │
│    taper shanks)     │
└──────────────────────┘
              ↓
┌──────────────────────┐
│   Spindles           │ ← Air, water-cooled motors  
│   (spindle motor)    │
└──────────────────────┘
              ↓
┌──────────────────────┐
│   Machine Basics     │ ← Rails, belts, gantry
│   (linear guides,    │
│    stepper motors)   │
└──────────────────────┘
```

---

## Cutting Tools (End Mills, Drills)

### 🔹 Solid Carbide vs High-Speed Steel (HSS)

| Attribute | Solid Carbide | HSS (High-Speed Steel) |
|-----------|---------------|------------------------|
| **Hardness** | 18×+ harder than HSS | Softer, prone to chip damage |
| **Cost** |$$$$$ ($30–$250/bit for small sizes) | $ (less $2–$15 but dulls faster) |
| **Lifespan** | Thousands of cuts until edge wear | Tens of cuts before replacement |
| **Use Case** | Production runs, fine finish | Hobby projects, occasional cuts |

### 🔹 Drill Bits vs End Mills

| Type | What It Does | When to Use |
|------|--------------|-------------|
| **Up-cut spiral (reverse flute)** | Pulls chips upward toward spindle | Good for deep holes; but can blow chips out into air/exhaust |
| **Down-cut spiral (forward)** | Pushes chips downward, good chip evacuation | Clean finish surfaces; avoid chip clogging |
| **Compression drill** | Dual-direction for balanced exit | Hard steel/aluminum where exit quality matters |

### 🔹 Carbide End Mill Sizes & Costs

| Size (mm) | Approx. USD | Typical Use |
|-----------|-------------|--------------|
| 1/64 – 3/32″ (≈1–1.5mm) | $30–$80 | Fine detail, engraving tight lines |
| 1/16″ (1.5mm) | $15–$40 | Edge detailing, pocketing small areas |
| 1/8″ (3mm) | $10–$25 | General milling, medium pockets |
| 1/4″ (6mm) | $8–$18 | Stock removal, rapid roughing |
| 1/2″ (12.7mm) | $40–$80 | Large pocketing, 3D profiling |

**💡 Tip**: Always buy extra bits! Dull tools = torn edges and heat buildup.

---

## Tool Holders & Collets

### 🔹 ER Collet Systems

| Type | Diameter Range | Rigidity | Cost | [[wikilink]] Notes |
|------|----------------|----------|-------|--------------------|
| **ER-11** | 0.6–3mm (small end mills) | Medium | $5–$20 | Good for tiny bits; low-torque machines only |
| **ER-32** | 3–14mm (mid-size) | High | $8–$30 | Most common, 2/4/3-jaw collets available |
| **R8/Taper** | Machine-specific | Excellent | $$$+10–$50 | Standard for CNC mills, R8, CAT40 |

### 🔹 Keyless vs Indexed Collets

- **Keyless**: Quick release without wrench; expensive but fast
- **Indexed**: Wrench required; cheaper (~$30) and rigid after tightening

**⚠️ Collet Maintenance:**
- Clean collets regularly (oil + grit damages precision)
- Don’t over-tighten >40–50 lb-ft torque (check tool holder)
- Store in dry place; humidity causes ER collet corrosion

### 🔹 HSK Holders (High-Speed Tooling)

| Spec | Advantage | [[wikilink]] Use Case |
|------|-----------|----------------------|
| 3D coupling (not just 2D faces) | High RPM, low vibration | CNC routers <30k RPM; not standard yet |
| Balanced weight distribution | Less heat on cutter | Aerospace-grade, but $$$+$$$ |

---

## Spindle Types & Cooling

### 🔹 Air-Cooled vs Water-Cooled

| Type | Power | Noise | Heat Dissipation [[wikilink]] Notes |
|------|-------|-------|-------------------------------------|
| **Air-cooled** | 2kW–5kW | Louder (~60 dB) | Fine for light CNC (under 1/2 HP equivalent); not good for 24/7 use |
| **Water-cooled** | 6kW–10kW | Quieter (~45 dB) | Large shops; better for long running hours, high-load metal machining |

### 🔹 Spindle Speed Ranges

| Machine Type | RPM Range | Typical Use |
|--------------|-----------|-------------|
| **Desktop CNC** (GRBL, shapeoko style) | 3000–24000 | Hobby milling, prototyping, light aluminum cutting |
| **Industrial mill** | 1200–6000 | Heavy metal machining; lower speed for torque and rigidity |

**⚠️ Important**: Never exceed rated spindle RPM; check motor thermal limits!

---

## Machine Basics & Maintenance

### 🔹 Linear Motion Parts

| Component | Purpose [[wikilink]] Notes |
|-----------|-----------------------------|
| **Belt drive (GT2/3mm pitch)** | Common for desktop CNC, smooth motion at low cost; tension belts every few months |
| **Ball screws** | Precision linear motion (lead screws with steel balls) | High-speed machining may cause vibration if not pre-loaded |
| **Linear rails (LM guides)** | Heavy-duty, smooth X/Y/Z travel | Industrial workpieces >1–2 tons |
| **DRO (Digital Readout)** | Electronic readout; precise to 0.001 mm | Optional luxury feature; manual DRO is cheaper |

### 🔹 Stepper Motortypes

| Motor Type | Torque Profile [[wikilink]] Notes |
|------------|-----------------------------------|
| **NEMA23 / NEMA17** | Standard for DIY CNC; 20–50 oz-ft torque, common |
| **HiCo (high torque)** | More motor current draw, better force at stall point |
| **Servo motors** | Closed-loop feedback, very accurate positioning | Expensive, used on industrial machines |

---

## Essential Consumables

### 🔹 Coolant vs Airblast Compressed Air Systems

| Use Case | System Type [[wikilink]] Recommendations |
|----------|-------------------------------------------|
| **Wood cutting** | Airblast (no coolant) + vacuum extractor. Clean, no oily mist in air. |
| **Aluminum machining** | Wet coolant spray. Add oil-based emulsion concentrate (5–10% solution). |
| **Stainless steel** | Flood oil + coolant; heavy-duty chip conveyor recommended for debris. |

### 🔹 Coolant Types & Mixing Ratios

| Concentrate Brand | Typical Mix Ratio | Cooling Properties [[wikilink]] Notes |
|-------------------|-------------------|--------------------------------------|
| **Tapwater / tap water** | 1:19 (5% concentrate) | Basic, no rust inhibiting; not recommended for metal parts |
| **Dedicated coolant oil** | 1:9 (10% solution) | Good heat dissipation, anti-rust, corrosion inhibitors |
| **Water-soluble lubricant** | 1:4 (20–30%) | Maximum cooling; use with caution on sensitive materials |

---

## Tags & Cross-References

**Tags**: [[tools]], [[manufacturing]], [[cnc]]  
**Related notes**: [[cnc]] (G-code basics), [[cam_workflow]] (CAM toolpath settings)

---

*Keep adding new tools you try, costs you encounter, failures you avoid!*
