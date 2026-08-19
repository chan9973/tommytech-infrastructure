# AI Video Generation Workflows

## Overview
AI video generation workflows transform voice tracks into professional presentations without manual recording. Users often prefer web-based tools (CapCut, Runway) over local GPU setups.

## User Preference Signals Detected
- **Style**: Want quick, ready-to-copy prompts (not verbose explanations)
- **Tool preference**: CapCut AI over local ComfyUI/SWD workflows
- **Accuracy**: "use my locate hardware" → typo correction opportunity for clearer typing

## CapCut AI Video Workflow

### Step 1: Prepare Voice Track
- Combine multiple clips into single MP3 (2:01 mins typical)
- Upload to CapCut AI platform

### Step 2: Structured Prompt Format
Use numbered scene breakdown for best results:

```
Scene 1 (0:00-0:30): Opening hook about local AI security
Scene 2 (0:30-2:00): Personal story/credentials  
Scene 3 (2:00-5:00): Technical setup demonstration
Scene 4 (5:00-8:00): Security/backup process
Scene 5 (8:00-11:30): Agent demo showcase
Scene 6 (11:30-14:00): Client results/case study
Scene 7 (14:00-15:00): Call-to-action
```

### Step 3: Proven Personas

| Persona | Prompt Example |
|---------|----------------|
| Malaysian Consultant | "Malaysian Asian male business consultant in corporate office" |
| Tech Professional | "Professional IT consultant demonstrating AI tools" |
| Academic Educator | "University lecturer presenting technical concepts" |

### Step 4: Visual Keywords to Include
- "Python terminal showing venv activation"
- "File Explorer displaying F drive backup"
- "Ollama interface with local model"
- "GDPR/PDPA compliance badge"
- "Clean corporate office background"
- "1080p quality, realistic human presenter"

## Common Failure Patterns

| Issue | Fix |
|-------|-----|
| Single static scene | Break prompt into numbered scenes |
| No persona | Specify ethnicity/profession explicitly |
| Missing technical details | Include CLI commands verbatim |
| Poor compliance mention | Explicitly state GDPR/PDPA badges |

## Platform Comparison

| Platform | Free Credits | Quality | Local GPU Required |
|----------|--------------|---------|-------------------|
| CapCut AI | Yes | Good | No |
| Runway Gen-4 | 200 credits | Excellent | No |
| Pika Labs | 30 actions/day | Artistic | No |
| ComfyUI | N/A | Best | Yes (12GB+ VRAM) |

## Template Prompts
See [templates/ai-video-prompts.md](templates/ai-video-prompts.md) for ready-to-use prompts optimized for CapCut AI.