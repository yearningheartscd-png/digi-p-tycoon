"""DIGI-P Tycoon - Terminal UI Renderer"""

def render_ui(pet):
    """Render the game UI"""
    # Clear screen (cross-platform)
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Header
    print("╔" + "═" * 48 + "╗")
    print("║" + " DIGI-P TYCOON ".center(48) + "║")
    print("╠" + "═" * 48 + "╣")
    
    # Pet info
    status = "SLEEPING" if pet.is_sleeping else "AWAKE"
    type_icon = {"crunch": "DINO", "byte": "BOT", "pixel": "GHOST", "glitch": "CAT"}.get(pet.pet_type, "PET")
    print(f"║  {pet.name:^46}  ║")
    print(f"║  Type: {type_icon:<6} | Stage: {pet.stage.upper():<8} | {status:<6}  ║")
    print("╠" + "═" * 48 + "╣")
    
    # Stats with bars
    print(f"║  Level: {pet.level:<3}    |  XP: {pet.xp}/{pet.xp_to_next:<6}     ║")
    print(f"║  Age: {pet.age_hours:<4}h   |  Alive: {'YES' if pet.alive else 'NO':<8}      ║")
    print("╠" + "─" * 48 + "╣")
    
    # Need bars
    hunger_bar = draw_bar(pet.hunger, 100, 20)
    happy_bar = draw_bar(pet.happiness, 100, 20)
    energy_bar = draw_bar(pet.energy, 100, 20)
    
    print(f"║  Hunger:    {hunger_bar} {pet.hunger:>3}%  ║")
    print(f"║  Happiness: {happy_bar} {pet.happiness:>3}%  ║")
    print(f"║  Energy:    {energy_bar} {pet.energy:>3}%  ║")
    print("╠" + "─" * 48 + "╣")
    
    # Traits
    print(f"║  STR: {pet.strength:>4.0f}  |  INT: {pet.intelligence:>4.0f}  |  CHR: {pet.charisma:>4.0f}  ║")
    print(f"║  SPD: {pet.speed:>4.0f}                                    ║")
    print("╠" + "─" * 48 + "╣")
    
    # Inventory
    inv = pet.inventory
    print(f"║  Inventory: Food:{inv['food']}  Treats:{inv['treats']}  Toys:{inv['toys']}       ║")
    print("╠" + "═" * 48 + "╣")
    
    # Sprite
    sprite = pet.get_sprite()
    sprite_lines = sprite.split('\n')
    for line in sprite_lines[:8]:  # Max 8 lines
        padded = line.center(44)
        print(f"║  {padded:^46}  ║")
    
    print("╠" + "═" * 48 + "╣")
    print("║  [F]eed  [P]lay  [S]leep  [R]ename  [H]istory  [Q]uit  ║")
    print("╚" + "═" * 48 + "╝")

def draw_bar(value, max_val, width):
    """Draw a text progress bar"""
    filled = int((value / max_val) * width)
    bar = "█" * filled + "░" * (width - filled)
    return bar

def show_message(msg):
    """Display a message below the UI"""
    print(f"\n  >> {msg}")
    input("  Press Enter to continue...")
