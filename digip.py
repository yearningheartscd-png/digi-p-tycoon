#!/usr/bin/env python3
"""DIGI-P Tycoon v0.1 - Terminal Pet Simulation

Quick start:
    python digip.py
    python digip.py --load  (load saved pet)
"""

import json
import sys
import os
from pathlib import Path

from pet import Pet
from render import render_ui, show_message

SAVE_DIR = Path("data/pets")
SAVE_FILE = SAVE_DIR / "crunch.json"

def save_pet(pet):
    """Save pet to JSON"""
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    with open(SAVE_FILE, 'w') as f:
        json.dump(pet.to_dict(), f, indent=2)

def load_pet():
    """Load pet from JSON"""
    if SAVE_FILE.exists():
        with open(SAVE_FILE, 'r') as f:
            return Pet.from_dict(json.load(f))
    return None

def choose_pet():
    """Let player choose a pet type"""
    print("\n" + "=" * 50)
    print("       CHOOSE YOUR DIGI-P")
    print("=" * 50)
    print("\n  1. CRUNCH - Strong, tough, reliable")
    print("  2. BYTE   - Smart, clever, strategic")  
    print("  3. PIXEL  - Charming, social, lovable")
    print("  4. GLITCH - Fast, agile, unpredictable")
    print("\n" + "=" * 50)
    
    choice = input("\n  Pick (1-4): ").strip()
    types = {"1": "crunch", "2": "byte", "3": "pixel", "4": "glitch"}
    
    pet_type = types.get(choice, "crunch")
    name = input(f"  Name your {pet_type.title()}: ").strip() or pet_type.title()
    
    return Pet(name, pet_type)

def main():
    # Auto-load if save exists, otherwise start fresh
    pet = load_pet()
    if not pet:
        print("No saved pet found. Starting fresh...")
        pet = choose_pet()
        print(f"\n  Welcome, {pet.name}! Take good care of them!")
        input("  Press Enter to start...")
    else:
        print(f"Welcome back! {pet.name} missed you!")
    
    running = True
    tick_counter = 0
    
    while running and pet.alive:
        render_ui(pet)
        
        # Auto-tick every 5 actions
        tick_counter += 1
        if tick_counter >= 5:
            pet.tick()
            tick_counter = 0
        
        # Get input
        try:
            choice = input("\n  What next? ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n\nSaving and exiting...")
            save_pet(pet)
            break
        
        if choice == 'f':
            success, msg = pet.feed()
            show_message(msg)
        elif choice == 'p':
            success, msg = pet.play()
            show_message(msg)
        elif choice == 's':
            success, msg = pet.sleep()
            show_message(msg)
        elif choice == 'r':
            new_name = input(f"  New name for {pet.name}: ").strip()
            if new_name:
                success, msg = pet.rename(new_name)
                show_message(msg)
        elif choice == 'h':
            print("\n  --- Recent History ---")
            for event in pet.history[-10:]:
                print(f"    {event}")
            input("\n  Press Enter to continue...")
        elif choice == 'q':
            save_pet(pet)
            print("Game saved! Goodbye!")
            running = False
        else:
            show_message("Huh? Try F, P, S, R, H, or Q")
    
    if not pet.alive:
        render_ui(pet)
        print("\n" + "=" * 50)
        print("  ☠️  OH NO! Your DIGI-P has passed away...")
        print("=" * 50)
        print("\n  (Delete save file to start fresh)")

if __name__ == "__main__":
    main()
