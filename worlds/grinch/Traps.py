import random

from .Regions import ALL_REGIONS_INFO

bonk_trap: dict[int, list[int]] = {
  ALL_REGIONS_INFO["Mount Crumpit"].map_id: [0x80, 0x81],
}
banana_trap: dict[int, list[int]] = {
    ALL_REGIONS_INFO["Mount Crumpit"].map_id: [0xAC],
}
electrocution_trap: dict[int, list[int]] = {
    ALL_REGIONS_INFO["Who Dump"].map_id: [0x01A3, 0x01A4]
}
damage_trap: dict[int, list[int]] = {
  ALL_REGIONS_INFO["Mount Crumpit"].map_id: [0x80, 0x81],
}

# Converts traps received from trap link into one of the above list
BEE_TRAP_EQUIV = ["Army Trap", "Buyon Trap", "Ghost", "Gooey Bag", "OmoTrap", "Police Trap"]
ICE_TRAP_EQUIV = ["Chaos Control Trap", "Freeze Trap", "Frozen Trap", "Honey Trap", "Paralyze Trap", "Stun Trap", "Bubble Trap"]
DAMAGE_TRAP_EQUIV = ["Banana Trap", "Bomb", "Bonk Trap", "Fire Trap", "Laughter Trap", "Nut Trap", "Push Trap",
"Squash Trap", "Thwimp Trap", "TNT Barrel Trap", "Meteor Trap", "Double Damage", "Spike Ball Trap"]
BONK_TRAP_EQUIV = [""]
# SPRING_TRAP_EQUIV = ["Eject Ability", "Hiccup Trap", "Jump Trap", "Jumping Jacks Trap", "Whoops! Trap"]
HOME_TRAP_EQUIV = ["Blue Balls Curse", "Instant Death Trap", "Get Out Trap"]
# SLOWNESS_TRAP_EQUIV = ["Iron Boots Trap", "Slow Trap", "Sticky Floor Trap"]
# CUTSCENE_TRAP_EQUIV = ["Phone Trap"]
ELEC_TRAP_EQUIV = []
DEPL_TRAP_EQUIV = ["Dry Trap"]

def convert_trap(map_id: int, trap_name: str) -> int | None:
    if trap_name in BONK_TRAP_EQUIV and map_id in bonk_trap:
        return random.choice(bonk_trap[map_id])
    elif trap_name in ELEC_TRAP_EQUIV and map_id in electrocution_trap:
        return  random.choice(electrocution_trap[map_id])



    elif trap_name in DAMAGE_TRAP_EQUIV and map_id in damage_trap:
        return random.choice(damage_trap[map_id])
    else:
        return None