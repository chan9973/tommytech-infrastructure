# 🎬 OBS Studio Scene Template - Firefox Edition
**Author**: Tommy Chan | **Created**: 2026-08-18 | **Compliance**: GDPR/PDPA Localized Processing Only

---

## 🚨 IMPORTANT: Use This Template With Firefox Only (No Chrome)
Chrome's telemetry conflicts with local-only compliance requirements. Always open vault files via Firefox's "File → Open File" menu.

---

## 📋 Scene Setup Instructions

### Scene 1: `main-recording`
**Sources (in order - top to bottom):**
1. **Browser Source** → Firefox window → `ai-consultant/training/demo-video-script.md`
   - Position: Full window (0,0,1920,1080)
   - Crop: Remove Firefox title bar (leave ~40px for clean edge)
2. **Window Capture** → Windows Terminal (`conda activate py311`)
   - Position: Right side, 40% width (~768px)
   - Size: 1080x204 (match Firefox height minus scrollbar)
3. **$OLLAMA_FLASH_ATTENTION Overlay**
   - Text: "⚠️ GPU OPTIMIZED: OLLAMA_FLASH_ATTENTION=1"
   - Font: Consolas 14px, red color
   - Position: Top-right corner
4. **Audio Output Capture** → System default (for voice MP3 playback)

---

## 📐 Firefox Window Settings

| Setting | Value | Purpose |
|---------|-------|---------|
| **Window Size** | 1280x720 (half screen) | Fits OBS with terminal side-by-side |
| **Title Bar Height** | Crop 40px | Eliminates browser UI from recording |
| **Scroll Behavior** | Smooth scrolling | Clean camera pan through vault |
| **Performance Mode** | Basic (no animations) | Consistent frame rate in recording |

---

## 🎞️ Scene-Specific Recording Guide

### `scene-main-recording` (0:00–15:00)
Use throughout entire video:
- Switch Firefox tabs to show:
  - Vault structure (front page)
  - `demo-video-script.md` content
  - F: drive backup folder
  - Calendly booking page

### `scene-terminal-demo` (2:00–8:00)
Replace Firefox source with Terminal capture:
- Source 1: Window Capture → Terminal (showing commands)
- Source 2: Browser Source → Firefox (in background, 50% opacity)
- Shows you typing while terminal processes execute

### `scene-obsidian-vault` (0:30–2:00)
For "Your Story" section:
- Source 1: Full Firefox window → Obsidian vault homepage
- Source 2: Small text overlay: "$50 pilot → $299+ full service"
- Cursor focus on vault file structure

---

## ⚙️ Audio Configuration

**Voice File Track** (Import all 7 MP3 files):
1. `001-opening-hook.mp3` → 0:00-0:30
2. `002-your-story.mp3` → 0:30-2:00
3. `003-env-setup.mp3` → 2:00-5:00
4. `004-model-backup.mp3` → 5:00-8:00
5. `005-orchestration.mp3` → 8:00-11:30
6. `006-client-workflow.mp3` → 11:30-14:00
7. `007-cta.mp3` → 14:00-15:00

**Media Sources Order**:
```
[Voice Track 001] → [Media Track 002] → Live OBS Recording
```

---

## 🛠️ Firefox Recording Commands (Run Before Session)

```bash
# Ensure Firefox is in correct mode before recording
firefox --private-window &
sleep 2
xdotool search --name "Mozilla Firefox" windowmove 0 0
xdotool search --name "Mozilla Firefox" windowsize 1280 720
```

---

## 🎯 Scene Transition Points

| Time | Scene | Action |
|------|-------|--------|
| 0:00 | `main-recording` | Open vault in Firefox |
| 0:30 | `scene-obsidian-vault` | Show file structure |
| 2:00 | `scene-terminal-demo` | Switch to terminal |
| 5:00 | `main-recording` | Back to Firefox, F: drive |
| 8:00 | `scene-terminal-demo` | Ollama commands demo |
| 11:30 | `main-recording` | Show client workflow files |
| 14:00 | `main-recording` | Calendly booking page |

---

## 📁 File Locations

- **Scene template**: `/ai-consultant/training/obs-scenes/firefox-demo.json`
- **Voice files**: `C:/Users/tommy/AppData/Local/hermes/audio/`
- **Vault files**: `E:/tommy vault/tommy vault/Read & Write/ai-consultant/`

---

## 🔒 Security Note

All recording done locally. No cloud upload required until final export to client email.

**File saved**: `E:/tommy vault/tommy vault/Read & Write/ai-consultant/training/obs-scenes/firefox-recording-template.md`