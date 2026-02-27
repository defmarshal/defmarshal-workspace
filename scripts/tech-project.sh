#!/usr/bin/env bash
# tech-project — suggest a technical (non-web, non-mobile) weekend project

projects=(
  "Implement a tiny Lisp interpreter in C (under 500 LOC)"
  "Build a custom mechanical keyboard with QMK firmware"
  "Write a simple filesystem (FAT or ext2) for educational OS"
  "Create a packet sniffer in Rust using pcap and analyze protocols"
  "Make a home automation hub with Home Assistant on a Pi"
  "Develop a tiny Forth-like stack machine and run it on AVR"
  "Build a DIY CNC machine (router or laser) from scratch"
  "Write a basic LLVM pass that optimizes loops"
  "Implement a distributed key‑value store with Raft consensus"
  "Construct a vacuum‑tube radio amplifier and measure THD"
  "Build a drone flight controller from scratch (STM32 + EKF)"
  "Create a custom language that compiles to WebAssembly (non‑web use)"
  "Design a PCB for a battery‑powered sensor node (KiCad)"
  "Write a simple hypervisor using KVM or Xen (minimal VM monitor)"
  "Build a network tap with two NICs and eBPF filtering"
  "Implement a tiny TCP/IP stack (lwIP style) for an embedded board"
  "Create a FUSE filesystem that stores data in a SQLite database"
  "Build a radiation detector with a Geiger counter and data logger"
  "Develop a static analysis tool for C that finds buffer overflows"
  "Construct a Stirling engine and instrument it with sensors"
)

count=${#projects[@]}
index=$((RANDOM % count))
echo "🔧 Tech project idea:"
echo ""
echo "  ${projects[$index]}"
echo ""
echo "Focus areas: systems programming, embedded, networking, compilers, robotics, hardware, security."
echo "No web or mobile — just good old‑fashioned deep tech!"
