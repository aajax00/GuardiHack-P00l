import math

CHALLENGE_REWARDS = {
    10:   {"xp": 5,    "fb_bonus": 0},    # rule (10 pts)
    100:  {"xp": 10,   "fb_bonus": 5},    # intro (100 pts)
    250:  {"xp": 50,   "fb_bonus": 20},   # facile (250 pts)
    300:  {"xp": 150,  "fb_bonus": 50},   # moyen (300 pts)
    500:  {"xp": 400,  "fb_bonus": 100},  # difficile (500 pts)
    800:  {"xp": 3500, "fb_bonus": 1000}, # insane (800 pts)
}

def get_challenge_rewards(points: int, is_first_blood: bool) -> int:
    rewards = CHALLENGE_REWARDS.get(points, {"xp": points, "fb_bonus": 0})
    return rewards["xp"] + (rewards["fb_bonus"] if is_first_blood else 0)

def calculate_level(xp: int) -> int:
    if xp <= 0:
        return 0
    return int(0.5 * math.sqrt(xp))

def get_grade(level: int) -> str:
    if level < 5: return "NullByte"
    if level < 15: return "initiate"
    if level < 30: return "learner"
    if level < 50: return "solver"
    if level < 75: return "expert"
    if level < 100: return "elite"
    return "Hacker"