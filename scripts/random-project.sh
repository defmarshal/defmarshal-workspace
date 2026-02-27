#!/usr/bin/env bash
# random-project — suggest a fun weekend project (non-web)

projects=(
  "Build a mechanical keyboard with custom keycaps (3D print or resin)"
  "Create a Raspberry Pi retro gaming console (retroarch + 8Bitdo)"
  "Write a short text adventure game in Python with puzzles"
  "Compose a chiptune track using Famistracker and convert to MP3"
  "Assemble a mini arcade cabinet (Raspberry Pi + monitor + controls)"
  "Make a smart mirror with weather, calendar, and news feeds"
  "Design and 3D print a modular desk organizer"
  "Build a plant monitoring system (moisture sensor + notifications)"
  "Fabricate a custom guitar pedal (distortion/overdrive circuit)"
  "Write a generating poetry AI using Markov chains"
  "Create an analog synth module (Eurorack format) from a kit"
  "Program a LED matrix display for anime art scrolling"
  "Make a portable Bluetooth speaker in a custom enclosure"
  "Develop a simple arcade game using PICO-8 or TIC-80"
  "Build a mechanical watch with a 3D-printed case and movement"
  "Craft a leather notebook cover with laser engraving"
  "Construct a solar-powered phone charger for hiking"
  "Design and print a cosplay prop (light-up sword, armor piece)"
  "Set up a home server cluster in a mini-ITX rack with Proxmox"
  "Write a browser plugin that translates meme captions to Shakespearean English"
  "Make a kinetic sculpture with Arduino-controlled servos"
  "Build a drone from scratch (frame, motors, flight controller)"
  "Create a stop‑motion animation film using clay figures and a phone"
  "Fabricate a custom game controller for a specific game (e.g., flight stick)"
  "Develop a tiny MMO text game with persistent world and chat"
)

count=${#projects[@]}
index=$((RANDOM % count))
echo "🎲 Random weekend project:"
echo ""
echo "  ${projects[$index]}"
echo ""
echo "Tools you might need: varies, but usually maker tools (3D printer, soldering iron, Raspberry Pi, Arduino, etc.)"
echo "Good luck and have fun!"
