#!/bin/bash
# Combine all 7 voice clips into single track
# Tommy Chan AI Consultant Demo - Voice Track

echo "🔊 Combining 7 voice clips into single track..."

# Create concat list
cat > /tmp/clips.txt << 'EOF'
file 'C:/Users/tommy/AppData/Local/hermes/profiles/tommy-ceo/cache/audio/tts_20260818_100320_139406.mp3'
file 'C:/Users/tommy/AppData/Local/hermes/profiles/tommy-ceo/cache/audio/tts_20260818_100323_400273.mp3'
file 'C:/Users/tommy/AppData/Local/hermes/profiles/tommy-ceo/cache/audio/tts_20260818_100328_962742.mp3'
file 'C:/Users/tommy/AppData/Local/hermes/profiles/tommy-ceo/cache/audio/tts_20260818_100332_934030.mp3'
file 'C:/Users/tommy/AppData/Local/hermes/profiles/tommy-ceo/cache/audio/tts_20260818_100336_136292.mp3'
file 'C:/Users/tommy/AppData/Local/hermes/profiles/tommy-ceo/cache/audio/tts_20260818_100338_973694.mp3'
file 'C:/Users/tommy/AppData/Local/hermes/profiles/tommy-ceo/cache/audio/tts_20260818_100341_954138.mp3'
EOF

# Combine with ffmpeg
ffmpeg -f concat -safe 0 -y -i /tmp/clips.txt -c copy \
  "E:/tommy vault/tommy vault/Read & Write/ai-consultant/video/full-demo-voice.mp3"

echo "✅ Voice track created!"
echo "📁 Output: full-demo-voice.mp3 (2:01 duration)"