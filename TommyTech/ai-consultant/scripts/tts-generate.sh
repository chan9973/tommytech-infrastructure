#!/bin/bash
# AI Voice Generation Script for Demo Video
# Author: Tommy Chan
# Purpose: Generate voice narration from demo-video-script.md

echo "# 🎙️ Generating Full Voice Narration from Demo Script..."
echo ""

SCRIPT_FILE="E:/tommy vault/tommy vault/Read & Write/ai-consultant/training/demo-video-script.md"
OUTPUT_DIR="E:/tommy vault/tommy vault/Read & Write/ai-consultant/audio/"
mkdir -p "$OUTPUT_DIR"

# Parse script sections and generate voice files
echo "1. Opening Hook (0:00-0:30)"
hermes tts --text "Imagine having powerful AI that never touches the cloud. Today I show you exactly how I set up local-only agents that keep client data 100% secure while delivering real business value for Malaysian enterprises." --output "$OUTPUT_DIR/001-opening-hook.mp3" --voice "Malaysia-English"

echo "2. Your Story (0:30-2:00)"
hermes tts --text "I'm Tommy Chan, AI Consultant based in Ipoh, Malaysia. My apprenticeship model starts at just $50 for pilot testing, scaling to $299+ for full-service deployments. All remote via TeamViewer Enterprise with GDPR/PDPA compliance built-in." --output "$OUTPUT_DIR/002-your-story.mp3" --voice "Malaysia-English"

echo "3. Environment Setup (2:00-5:00)"
hermes tts --text "Here's how I set up a local Python environment for secure AI agent deployment. Using python3.11 virtual environment, install hermes-tools, requests, and flask. For clients with C dependencies like opencv, I use conda with conda-forge channel for pre-compiled binaries." --output "$OUTPUT_DIR/003-env-setup.mp3" --voice "Malaysia-English"

echo "4. Model Pull & Backup (5:00-8:00)"
hermes tts --text "Pulling the edtorre/qwen3.5-hermes model using ollama. Size is 6.6GB quantized with Q4_K_M for efficient local inference. Critical step: backup to removable F drive immediately. This ensures data sovereignty compliance under GDPR and PDPA regulations. No cloud exfiltration - all processing stays local." --output "$OUTPUT_DIR/004-model-backup.mp3" --voice "Malaysia-English"

echo "5. Agent Orchestration Demo (8:00-11:30)"
hermes tts --text "Demonstrating ollama run edtorre/qwen3.5-hermes with agent-powered workflows. Watch how the AI researches GitHub, installs packages, writes code, runs tests, and summarizes results - all without touching external APIs. Perfect for client data security requirements." --output "$OUTPUT_DIR/005-orchestration.mp3" --voice "Malaysia-English"

echo "6. Client Workflow (11:30-14:00)"
hermes tts --text "Real client workflow: intake form captures requirements, AI agent analyzes codebase, generates solution, and presents options. Typical result: 12 hours saved per week on report automation. All processes documented in secure local vault." --output "$OUTPUT_DIR/006-client-workflow.mp3" --voice "Malaysia-English"

echo "7. Call-to-Action (14:00-15:00)"
hermes tts --text "Ready to secure your AI transformation? Book your free diagnostic call via the link below. No obligation to proceed. Let's build your local AI infrastructure together." --output "$OUTPUT_DIR/007-cta.mp3" --voice "Malaysia-English"

echo ""
echo "✅ Voice narration complete!"
echo "Total files: $(ls $OUTPUT_DIR/*.mp3 | wc -l)"
echo "Output directory: $OUTPUT_DIR"