# Whack-A-Mole with Raspberry Pi!

A mini hardware game built with a Raspberry Pi, LEDs, and push-buttons.  
Random LEDs light up, and the player must hit the correct button before time runs out.  
Scores are tracked and displayed on a 16x2 I²C LCD in real time. Each round lasts 30 seconds.

---

## Features
- Four LEDs (Red, Yellow, Green, Blue) paired with matching buttons  
- Random LED selection for each round  
- Score increments when the correct button is pressed while LED is lit  
- Round timer with countdown displayed on LCD  
- Real-time feedback (*“Nice!”*, *“Too slow!”*, final score)  

---

## Hardware Used
- Raspberry Pi (tested with Pi 3/4)  
- 4x LEDs (Red, Yellow, Green, Blue)  
- 4x Push-buttons with pull-up configuration  
- 16x2 I²C LCD display (PCF8574 backpack)  
- Breadboard + jumper wires + resistors  

---

## Dependencies
- `RPi.GPIO` (for GPIO control)  
- `smbus` (for I²C LCD communication)  
- `time`, `random` (Python standard libraries)  

Install GPIO and I²C support (if not already installed):  
```bash
sudo apt-get update
sudo apt-get install python3-rpi.gpio python3-smbus
