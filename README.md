<div align="center">

# 🎛️ Bass/Lead Techno Generator

**Hardware-based generative MIDI sequencer for external synthesizers**

[![Status](https://img.shields.io/badge/Status-In_Development-orange.svg)]()
[![Language](https://img.shields.io/badge/Language-C-blue.svg)]()
[![Framework](https://img.shields.io/badge/Framework-ESP--IDF-red.svg)]()
[![Platform](https://img.shields.io/badge/Platform-ESP32--S3-green.svg)]()

*A compact, standalone hardware tool designed to generate inspiring bass and lead sequences for electronic music producers.*

</div>

---

## 👨‍💻 About the Author
Hi, I'm **Ilya** — Im electronics engineer based in Saint Petersburg, Russia. 

I have over 8 years of experience in the electronics manufacturing industry, specializing in hardware debugging, testing, assambly and development of measuring equipment. Alongside my professional engineering background, I am a hardware DAWless musician and an active member of the local electronic music community. 

This project is a synergy of my professional experience in electronics and my passion for electronic music.

📫 **Contacts:** maybe later :)

---

## 🎵 Project Overview
The **Bass/Lead Techno Generator** is a standalone, generative MIDI sequencer. It acts as an external musical equipment that generates ready-to-use bass and lead sequences, sending them via MIDI to any external synthesizer, groovebox and sampler.

### Why this project?
As a DAWless musician, I understand how sometimes there is a lack of inspiration or a small musical idea to kickstart a new track.

The goal is this project is to create a compact, useful and afoordable device designed to inspire and help overcome creative blocks.

### Core Features
*   **Markov Chain Generation:** The core generation logic is built on Markov chains. It utilizes an analysis of bass and lead patterns across various Techno subgenres — from classic Detroit to Industrial — to create stylistically accurate sequences.
*   **Key & Mode Selection:** Choose any key and select from popular modes used in the Techno genre.
*   **Real-time Step Edit:** The generated sequence can be modified on the fly. Any step can be substituted, allowing the device to be used as a standard external sequencer.
*   **Intuitive UI:** A color TFT screen displays a clear visual grid of the pattern. 
*   **Tactile Control:** Rotary encoder for step navigation and note editing; tactile buttons for mode, key, and note switching.

---

## 🛠 Hardware & Software Stack

### Hardware Specifications
*   **Microcontroller:** ESP32-S3 (16MB Flash, 8MB PSRAM)
*   **Display:** ST7735 (SPI TFT)
*   **Controls:** Rotary Encoder (EC11), Tactile Push Buttons
*   **MIDI I/O:** MIDI over TRS (3.5mm Jack, Type A) for compact form factor
*   **Development:** Custom PCB design (KiCad) and 3D enclosure (SolidWorks)

### Software Architecture
*   **Firmware:** C, ESP-IDF
*   **Prototyping & Algorithm Design:** Python (Prototype and a working Telegram Bot for pattern generation, [link](https://t.me/TechgenBot))
*   **Testing:** Unity (Host and target unit testing for C), Pytest & pytest-embedded (Hardware integration testing)

---

## 📂 Repository Structure
*(Will be updated as the project evolves)*
```text
├── firmware/       # ESP-IDF C project (main logic, MIDI, UI)
├── tests/          # Host unit tests (Unity) and integration tests (pytest)
├── hardware/       # KiCad schematics, PCB layout, BOM
├── python_proto/   # Python algorithms and Telegram bot prototype
├── docs/           # Datasheets, diagrams, Altium docs
└── README.md       # You are here