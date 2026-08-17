# 👥 Human-Robot Collaboration Guidelines

[[robotics-integration-main]] • [[robotics-software]] • [[CNC n Robotic|↩]] • [[safety-standards|↩ Safety]]

---

## 🎯 Core Principles of Safe Coexistence

### Safety First → Always
```
┌───────────────────────────────────────────┐
│     ROBOTIC SAFETY HIERARCHY               │
├───────────────────────────────────────────┤
│  1. Physical barriers (fencing)            │
│  2. Emergency stops                         │
│  3. Force limiting brakes                   │
│  4. Software monitoring (E-stops)          │
│  5. Human override authority                │
└───────────────────────────────────────────┘
```

**Key Rule**: Humans always have final say and safe exit!

---

## 📋 Zone Definitions (ISO 13849 / ISO/TS 15066)

### Safety Zones

```yaml
Zone A - Danger Zone:
  Description: Robot working envelope
  Speed limit: Full operational speed
  Human presence: Only during manual mode
  
Zone B - Caution Zone:
  Description: Robot approach path  
  Speed limit: Reduced by software
  Human presence: Monitored, slow approach OK

Zone C - Safe Zone:
  Description: Outside robot range
  Speed limit: No restriction
  Human presence: Frequent (normal work)

Zone D - Collaboration Zone:
  Description: Directly adjacent to robot
  Speed limit: ≤250mm/s (power & force limited)
```

**Implementation**: Set up light curtains marking Zone A boundary.

---

## 🤖 Cobot Design Guidelines (Collaborative Robots)

### Power & Force Limiting

| Parameter | ISO/TS 15066 Limit | Implementation Notes |
|-----------|---------------------|----------------------|
| Force impact | ≤80N (adults), ≤340J energy | Soft joints, brake disengagement |
| Velocity | ≤250mm/s | Speed monitoring required |
| Torque at tip (point force) | ≤100N | End-effector compliance |

### Design Techniques

```python
def design_cobotsafe():
    """
    Cobot design checklist:
    
    1. Compliant end-effectors
    2. Software velocity limiting
    3. Emergency stop integration
    4. Force monitoring sensors
    5. Safe stop distance calculation
    """
    
    # Calculate safe work envelope
    work_envelope = calculate_safe_zone(cobot_speed, mass)
    
    # Set speed limits per zone
    zones = {
        'A': {'speed_limit': 'manual_mode_only'},
        'B': {'speed_limit': 'reduced(0.5)'},
        'C': {'speed_limit': 'full_speed'}
    }
```

---

## 🔄 Workflow Safety Patterns

### Human-Robot Task Delegation

**Kanban Board for HRC Tasks**:

| Column | Who Does What | Safety Check |
|--------|---------------|--------------|
| 📋 Backlog | Task ideas | Feasibility review |
| 🔍 Analysis | Risk assessment | Zone mapping |
| ✅ Implement | Build safety features | Testing complete |
| 🚀 Deploy | Operate with monitors | Continuous monitoring |

### Task Handoff Protocol

```
[Human assigns task] → [Robot accepts] 
                    ↓
          [Safety briefing]
                    ↓
         [Zone verification complete]
                    ↓
          [Collaboration enabled]
                    ↓
       [Human/Robot work together]
                    ↓
         [Task completion verified]
```

---

## ⚠️ Error Handling in Collaboration

### When Robot Fails → Safe Mode Activates

```yaml
Failure Scenarios & Responses:
  
  Scenario 1: Vision loss
    Response: Stop immediately
    Escalation: Request manual inspection
  
  Scenario 2: Motion controller fault
    Response: Hold position, brake engage
    Recovery: Reboot after diagnostic
    
  Scenario 3: Force sensor anomaly
    Response: Reduce speed by 50%
    Recovery: Calibrate sensors
```

---

## 🎓 Training Requirements

### Human Operators Need Training On

| Topic | Why It Matters | Training Time |
|-------|----------------|---------------|
| Emergency stops | Quick safety response | 3 hr minimum |
| Tool change procedures | Prevent injury during swap | 1 hr |
| Zone definitions | Know safe vs dangerous areas | 2 hr |
| Robot limitations | Understand boundaries | Ongoing demo |

**Certification**: Document completion; refresh annually!

---

## 📊 Communication Methods

### Human-Robot Interaction (HRI) Design

```
┌──────────────────────────────────────┐
│      HUMAN-ROBOT COMMSCHEM           │
├──────────────────────────────────────┤
│                                      │
│   [LED lights]                       │
│   ───────────                       │
│   Green: Normal operation           │
│   Yellow: Caution/learning          │
│   Red: Stop/error                   │
│                                       │
│   [Audio cues]                      │
│   → Bleeps for alerts              │
│                                       │
│   [Tablets/LCD screens]             │
│   → Display task progress           │
└──────────────────────────────────────┘
```

---

## 🔧 Implementation Checklist

### Pre-Deployment Safety Validation

```bash
# Run this checklist before going live:

[ ] 1. All safety interlocks tested
[ ] 2. E-stop pulls verified (all locations)
[ ] 3. Light curtains calibrated at 65% occlusion
[ ] 4. Speed monitoring enabled per zone
[ ] 5. Force limits confirmed <80N
[ ] 6. Users trained & certified
[ ] 7. Emergency procedure document ready
[ ] 8. Risk assessment documented (ISO 12100)

# Command: python verify_safety_checklist.py
```

---

## 📖 Standards References

### Must-Know Safety Standards

- **ISO 10218**: Industrial robot safety  
- **ISO/TS 15066**: Collaborative robot specific  
- **ISO 13849**: Control system reliability  
- **ANSI/RIA R15.08**: US safety standard  
- **IEC 62061**: Functional safety  

---

## 🎯 Best Practices Summary

### Do's ✅
- [ ] Always enable E-stops before approaching robot  
- [ ] Keep work area clean and unobstructed  
- [ ] Use light curtains for dangerous zones  
- [ ] Document all safety modifications  
- [ ] Perform regular safety audits  

### Don'ts ❌
- [ ] Never bypass safety interlocks  
- [ ] Don't run at full speed with humans present  
- [ ] Avoid touching robot while operational except in manual mode  
- [ ] Never ignore error messages  
- [ ] Don't modify firmware without safety review  

---

## 🔗 Related Knowledge Nodes

| Node | Relevance | Link Type |
|------|-----------|----------|
| [[robotics-standards]] | Regulatory requirements | Reference |
| [[agentic-workflows]] | AI-driven supervision | Integration |
| [[humanizer]] | Make safety docs clear | Accessibility |
| [[monitoring-dashboard]] | Real-time safety monitoring | Tools |

---

## 📈 Continuous Improvement

### Safety Metrics to Track

```yaml
Metrics:
  Stop_events: 0 → Target <1/month
  Near_misses: Log all immediately  
  Training_hours_per_user: Min 4 annually
  Safety_audit_score: >95% compliance
  Incident_rate: 0 (zero goal)
```

**Review**: Monthly safety meetings; quarterly system audits.

---

## 📚 Further Reading

- ISO 10218 documents at iso.org  
- Collaborative robotics research: robocollab.com  
- Automation society webinars: automation.org  

[[robotics-history]] [[robotics-hardware]] [[robotics-software]]
[[CNC n Robotic]]

```
---
Tags: [safety hrc-cobots human-robot safety-standards training]
Status: Safety synthesis complete
Kanban: Backlog items prioritized for review phase
Last updated: Now
```
