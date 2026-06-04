# music-generation Skill

## Description
Text-to-music and lyrics generation + TTS (on-device where possible). Supports songs with lyrics or instrumental.

## Inputs
- `description`: string (style/scene/lyrics)
- `type`: "song" | "instrumental" | "tts"

## Execution
Uses audio agent + external APIs (Tunee-style) or local (Supertonic ONNX).

## Core Logic
- Lyrics guide for better output
- Generate + optional voice synthesis

## Dependencies
- audio agent
- Supertonic / Tunee integration points

## Integration
Upgrades audio/ and video/ agents. Callable from JARVIS for creative tasks.

---
*Inspired by https://github.com/tuneeai/free-music-generator and https://github.com/supertone-inc/supertonic*
