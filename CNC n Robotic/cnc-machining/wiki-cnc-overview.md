# Computer Numerical Control (CNC) Overview

> [!SUMMARY] CNC Machining - High-level introduction to automated machine tools controlled by computer programs. [[Computer-numerical-control/Wikipedia]]

## What is CNC?

**Computer Numerical Control (CNC)** refers to the automated control of machine tools through computer-based programming systems. Unlike traditional manual machining tools operated directly by human hands, CNC machines interpret digital instructions (typically G-code and M-code) to execute precise manufacturing operations.

---

## History & Evolution

### Early Development
- **1940s-1950s**: Numerical control (NC) pioneered with punched card input systems
- **1970s**: Introduction of computerized control systems, replacing pure mechanical programming
- **1980s-present**: CAM (Computer-Aided Manufacturing) software integration, multi-axis capabilities

### Key Milestones
1. Punched card programming → Early automation
2. Computer-integrated manufacturing (CIM)
3. Modern CNC withCAD/CAM software integration and IoT connectivity

---

## Core Components

### 1. Control System
```
┌─────────────────────────────────────────┐
│         G-Code & M-Code                 │
│  ┌───────────────────────────────────┐  │
│  │          Controller               │  │
│  │  ├── Motors & Stepper Drivers     │  │
│  │  ├── Servo Systems                │  │
│  │  ├── Coordinate System (XYZ)      │  │
│  │  └─────────────────────────────────┘  │
│  └───────────────────────────────────────┘
└─────────────────────────────────────────┘
```

### 2. Programming Languages

**G-Codes (Geometric)**: Control motion along X, Y, Z axes (e.g., `G01` → linear move, `G02` → clockwise arc)

**M-Codes (Miscellaneous)**: Auxiliary functions (e.g., `M03` → spindle on, `M05` → spindle off, `M30` → program end)

### 3. Software Stack
```
┌───────────────┐
│   CAM Software │ ← CAD/CAM integration
└───────────────┘
           ↓
┌───────────────┐
│   Controller  │ ← Machine interface
└───────────────┘
           ↓
┌───────────────┐  
│   Motors &    │ ← Physical execution
│   Actuators   │
└───────────────┘
```

---

## Applications

### Material Types

- **Woodworking**: CNC routers (visible in article's machine cutting wood example)
- **Metal Machining**: Milling centers, lathes with coolant systems
- **Composite Materials**: PCB fabrication, carbon fiber structures
- **Plastics/PVC**: Extrusion profiles, injection molding parts

### Industrial Use Cases

1. **Automotive manufacturing** ← Engine components, body parts
2. **Aerospace** ← Precision turbine blades, structural elements  
3. **Medical devices** ← Surgical tools, prosthetics
4. **Consumer goods** ← Prototyping and high-volume production
5. **3D printing / Additive manufacturing** ← CNC-based 3-axis printing

---

## Types of CNC Machines

| Machine Type | Main Axis | Typical Use | Common G-Codes |
|-------------|-----------|-------------|----------------|
| **3-Axis Mill** | X, Y, Z | 2D/3D milling | G00–G09 |
| **4-Axis Mill/Turn** | X, Y, Z, A/B | Rotational features | G00–G10 |
| **5-Axis Machine** | X, Y, Z, A, B/C | Complex surfaces | G00–G26 |
| **Router** | X, Y, Z | Large sheet materials | G00–G18 |
| **Lathe** | Z, X, C | Rotational parts | G00–G09 |

---

## Safety Features

- **Emergency stop buttons**
- **Safety guards and light curtains**
- **Interlock systems**
- **Coolant monitoring systems** (as shown in article images)
- **Tool breakage detection**

---

## References

### External Resources
1. [Wikipedia: Computer Numerical Control](https://en.wikipedia.org/wiki/Computer_numerical_control) ← Source article
2. ISO 14647 Standards for NC programming
3. GNC (G-Code Nation): Online G-code simulator

### Related Notes
- [[G-code-programming]]
- [[CAD-CAM-workflow]]
- [[Robotics-integration]]
- [[Precision-manufacturing]]

---

## See Also
<!-- Wikilinks for related topics -->
[[Computer-numerical-control/Wikipedia]]

---

*Created from [[https://en.wikipedia.org/wiki/Computer_numerical_control]] via browser automation, August 2026*
