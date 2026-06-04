# image-generation Skill

## Description
GPT-style image generation and editing with prompt gallery, packaged as agent skill (inspired by GPT-Image2-Skill).

## Inputs
- `prompt`: string or reference to gallery item
- `mode`: "generate" | "edit" | "variation"
- `style`: optional

## Execution
Calls Designer agent or dedicated image tool. Supports safe agent execution (no arbitrary file writes outside sandbox).

## Core Logic
- Reference prompt gallery first
- Generate via OpenAI or local fallback
- Return image paths + metadata

## Prompts / Reasoning Cues
Use gallery examples for better results.

## Examples
See docs/ in this folder for prompt gallery.

## Dependencies
- tools (image gen)
- designer agent

## Integration
Added to Designer agent and JARVIS for visual tasks.

---
*Inspired by https://github.com/wuyoscar/GPT-Image2-Skill*
