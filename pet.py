import random

class Pet:
    """DIGI-P: Your digital companion"""
    
    STAGES = {
        1: "egg",
        2: "baby", 
        3: "child",
        4: "teen",
        5: "adult"
    }
    
    # Pet types with different base traits
    TYPES = {
        "crunch": {"sprite": "dino", "strength": 15, "intelligence": 8, "charisma": 10, "speed": 7},
        "byte": {"sprite": "byte", "strength": 8, "intelligence": 15, "charisma": 7, "speed": 10},
        "pixel": {"sprite": "pixel", "strength": 10, "intelligence": 10, "charisma": 15, "speed": 8},
        "glitch": {"sprite": "glitch", "strength": 7, "intelligence": 12, "charisma": 8, "speed": 15}
    }
    
    def __init__(self, name="Crunch", pet_type="crunch"):
        self.name = name
        self.pet_type = pet_type.lower()
        self.level = 1
        self.xp = 0
        self.xp_to_next = 100
        
        # Core stats (0-100)
        self.hunger = 50
        self.happiness = 50
        self.energy = 50
        
        # Set base traits from pet type
        type_data = self.TYPES.get(self.pet_type, self.TYPES["crunch"])
        self.strength = type_data["strength"]
        self.intelligence = type_data["intelligence"]
        self.charisma = type_data["charisma"]
        self.speed = type_data["speed"]
        self.sprite_base = type_data["sprite"]
        
        # Inventory and history
        self.inventory = {"food": 3, "treats": 1, "toys": 1}
        self.history = []
        
        self.age_hours = 0
        self.is_sleeping = False
        self.alive = True
        
        self._log(f"{self.name} the {self.pet_type.title()} was born!")
    
    @property
    def stage(self):
        return self.STAGES.get(self.level, "adult")
    
    def feed(self):
        """Reduce hunger, gain some XP"""
        if self.is_sleeping:
            return False, f"Zzz... {self.name} is sleeping!"
        
        if self.inventory["food"] > 0:
            self.inventory["food"] -= 1
            self.hunger = max(0, self.hunger - 30)
            self.energy = min(100, self.energy + 5)
            self._gain_xp(10)
            self._beep()
            
            messages = [
                f"Yum! {self.name} munches happily.",
                f"{self.name} devours the food!",
                "That hit the spot!"
            ]
            self._log(f"Fed {self.name}")
            return True, random.choice(messages)
        else:
            return False, "No food left! Time to forage..."
    
    def play(self):
        """Boost happiness, consume energy"""
        if self.is_sleeping:
            return False, f"Zzz... {self.name} is sleeping!"
        if self.energy < 20:
            return False, f"{self.name} is too tired to play..."
        
        self.happiness = min(100, self.happiness + 25)
        self.energy = max(0, self.energy - 15)
        self.hunger = min(100, self.hunger + 10)
        self._gain_xp(15)
        
        self.charisma += 0.5
        self.speed += 0.3
        self._beep()
        
        messages = [
            f"{self.name} runs around joyfully!",
            f"You toss a ball. {self.name} catches it!",
            f"{self.name} does a little dance!"
        ]
        self._log(f"Played with {self.name}")
        return True, random.choice(messages)
    
    def sleep(self):
        """Recover energy"""
        if self.is_sleeping:
            self.is_sleeping = False
            self.energy = min(100, self.energy + 40)
            self.hunger = min(100, self.hunger + 20)
            return True, "Crunch wakes up refreshed! ☀️"
        else:
            self.is_sleeping = True
            return True, "Crunch curls up and falls asleep... 🌙"
    
    def _gain_xp(self, amount):
        """Add XP and check for level up"""
        self.xp += amount
        if self.xp >= self.xp_to_next:
            self._level_up()
    
    def _level_up(self):
        """Level up and evolve"""
        self.level += 1
        self.xp -= self.xp_to_next
        self.xp_to_next = int(self.xp_to_next * 1.5)
        
        # Boost all stats
        self.strength += 5
        self.intelligence += 5
        self.charisma += 5
        self.speed += 5
    
    def tick(self):
        """Simulate time passing (called every game tick)"""
        if not self.alive:
            return
        
        self.age_hours += 1
        
        # Decay stats
        decay_rate = 0.5 if self.is_sleeping else 2
        self.hunger = min(100, self.hunger + decay_rate)
        self.happiness = max(0, self.happiness - decay_rate * 0.5)
        
        if self.is_sleeping:
            self.energy = min(100, self.energy + 5)
        else:
            self.energy = max(0, self.energy - 1)
        
        # Check for death
        if self.hunger >= 100 or self.happiness <= 0:
            self.alive = False
    
    def _log(self, event):
        """Add event to history"""
        self.history.append(event)
        if len(self.history) > 50:
            self.history.pop(0)
    
    def _beep(self):
        """Terminal bell for sound effect"""
        print('\a', end='')
    
    def rename(self, new_name):
        """Rename the pet"""
        old_name = self.name
        self.name = new_name
        self._log(f"{old_name} was renamed to {new_name}")
        return True, f"{old_name} is now called {new_name}!"
    
    def get_sprite(self):
        """Get ASCII art for current stage"""
        try:
            with open(f"assets/sprites/{self.sprite_base}_stage{self.level}.txt", "r") as f:
                return f.read()
        except:
            # Fallback sprites
            sprites = {
                1: "  .-.'",
                2: "  (o o)",
                3: "   _._\n  /   \\\n ( o o )",
                4: "    _._\n   /   \\\n  ( o o )\n   \\ ~ /",
                5: "    _._\n   /   \\\n  ( o o )\n   \\ ~ /\n    | |\n   /   \\"
            }
            return sprites.get(self.level, sprites[5])
    
    def to_dict(self):
        return {
            "name": self.name,
            "pet_type": self.pet_type,
            "level": self.level,
            "xp": self.xp,
            "xp_to_next": self.xp_to_next,
            "hunger": self.hunger,
            "happiness": self.happiness,
            "energy": self.energy,
            "strength": self.strength,
            "intelligence": self.intelligence,
            "charisma": self.charisma,
            "speed": self.speed,
            "inventory": self.inventory,
            "history": self.history,
            "age_hours": self.age_hours,
            "is_sleeping": self.is_sleeping,
            "alive": self.alive
        }
    
    @classmethod
    def from_dict(cls, data):
        pet = cls(data.get("name", "Crunch"), data.get("pet_type", "crunch"))
        for key, value in data.items():
            if key not in ["name", "pet_type"] and hasattr(pet, key):
                setattr(pet, key, value)
        return pet
