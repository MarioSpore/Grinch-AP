from typing import NamedTuple, Optional

from BaseClasses import Item
from BaseClasses import ItemClassification as IC

class GrinchItemData(NamedTuple):
    type: str
    code: Optional[int]
    classification: IC
    update_ram_addr: Optional[list[GrinchRamData]] = None
    value: Optional[int] = None #I can either set or add either hex or unsigned values through Client.py
    binary_bit_pos: Optional[int] = None
    bit_size: int = 1


#Gadgets
GADGETS_TABLE: dict[str, GrinchItemData] = {
    "Binoculars": GrinchItemData("Gadgets", 100, IC.useful,
        [GrinchRamData(0x800102B6, value=0x40), GrinchRamData(0x800102B7, value=0x41),
        GrinchRamData(0x800102B8, value=0x44), GrinchRamData(0x800102B9, value=0x45)]),
    "Rotten Egg Launcher": GrinchItemData("Gadgets", 101, IC.progression,
        [GrinchRamData(0x800102BA, value=0x40), GrinchRamData(0x800102BB, value=0x41),
        GrinchRamData(0x800102BC, value=0x44), GrinchRamData(0x800102BD, value=0x45)]),
    "Rocket Spring": GrinchItemData("Gadgets", 102, IC.progression,
        [GrinchRamData(0x800102BE, value=0x40), GrinchRamData(0x800102BF, value=0x41),
        GrinchRamData(0x800102C0, value=0x42), GrinchRamData(0x800102C1, value=0x44),
        GrinchRamData(0x800102C2, value=0x45), GrinchRamData(0x800102C3, value=0x46),
        GrinchRamData(0x800102C4, value=0x48), GrinchRamData(0x800102C5, value=0x49),
        GrinchRamData(0x800102C6, value=0x4A)]),
    "Slime Shooter": GrinchItemData("Gadgets", 103, IC.progression,
        [GrinchRamData(0x800102C7, value=0x40), GrinchRamData(0x800102C8, value=0x41),
        GrinchRamData(0x800102C9, value=0x42), GrinchRamData(0x800102CA, value=0x44),
        GrinchRamData(0x800102CB, value=0x45), GrinchRamData(0x800102CC, value=0x46),
        GrinchRamData(0x800102CD, value=0x48), GrinchRamData(0x800102CE, value=0x49),
        GrinchRamData(0x800102CF, value=0x4A)]),
    "Octopus Climbing Device": GrinchItemData("Gadgets", 104, IC.progression,
        [GrinchRamData(0x800102D0, value=0x40), GrinchRamData(0x800102DA, value=0x41),
        GrinchRamData(0x800102DB, value=0x42), GrinchRamData(0x800102DC, value=0x44),
        GrinchRamData(0x800102DD, value=0x45), GrinchRamData(0x800102DE, value=0x46),
        GrinchRamData(0x800102DF, value=0x48), GrinchRamData(0x800102E0, value=0x49),
        GrinchRamData(0x800102E1, value=0x4A)]),
    "Marine Mobile": GrinchItemData("Gadgets", 105, IC.progression,
        [GrinchRamData(0x800102D9, value=0x40), GrinchRamData(0x800102DA, value=0x41),
        GrinchRamData(0x800102DB, value=0x42), GrinchRamData(0x800102DC, value=0x43),
        GrinchRamData(0x800102DD, value=0x43), GrinchRamData(0x800102DE, value=0x44),
        GrinchRamData(0x800102DF, value=0x44), GrinchRamData(0x800102E0, value=0x45),
        GrinchRamData(0x800102E1, value=0x46), GrinchRamData(0x800102E2, value=0x47),
        GrinchRamData(0x800102E3, value=0x48), GrinchRamData(0x800102E4, value=0x49),
        GrinchRamData(0x800102E5, value=0x4A), GrinchRamData(0x800102E6, value=0x4B),
        GrinchRamData(0x800102E7, value=0x4C), GrinchRamData(0x800102E8, value=0x4D)]),
    "Grinch Copter": GrinchItemData("Gadgets", 106, IC.progression,
        [GrinchRamData(0x800102E9, value=0x40), GrinchRamData(0x800102EA, value=0x41),
        GrinchRamData(0x800102EB, value=0x42), GrinchRamData(0x800102EC, value=0x43),
        GrinchRamData(0x800102ED, value=0x43), GrinchRamData(0x800102EE, value=0x44),
        GrinchRamData(0x800102EF, value=0x44), GrinchRamData(0x800102F0, value=0x45),
        GrinchRamData(0x800102F1, value=0x46), GrinchRamData(0x800102F2, value=0x47),
        GrinchRamData(0x800102F3, value=0x48), GrinchRamData(0x800102F4, value=0x49),
        GrinchRamData(0x800102F5, value=0x4A), GrinchRamData(0x800102F6, value=0x4B),
        GrinchRamData(0x800102F7, value=0x4C), GrinchRamData(0x800102F8, value=0x4D)])
}

#Mission Specific Items
MISSION_ITEMS_TABLE: dict[str, GrinchItemData] = {
    "Who Cloak": GrinchItemData("Mission Specific Items", 200, IC.progression,
        [GrinchRamData(0x800101F9, binary_bit_pos=1)]),
    "Painting Bucket": GrinchItemData("Mission Specific Items", 201, IC.progression,
        [GrinchRamData(0x800101F9, binary_bit_pos=2)]),
    "Scissors": GrinchItemData("Mission Specific Items", 202, IC.progression,
        [GrinchRamData(0x800101F9, binary_bit_pos=7)]),
    "Glue Bucket": GrinchItemData("Mission Specific Items", 203, IC.progression,
        [GrinchRamData(0x800101F9, binary_bit_pos=5)]),
    "Cable Car Access Card": GrinchItemData("Mission Specific Items", 204, IC.progression,
        [GrinchRamData(0x800101F9, binary_bit_pos=6)]),
    "Drill": GrinchItemData("Mission Specific Items", 205, IC.progression,
        [GrinchRamData(0x800101FA, binary_bit_pos=3)]),
    "Rope": GrinchItemData("Mission Specific Items", 206, IC.progression,
        [GrinchRamData(0x800101FA, binary_bit_pos=2)]),
    "Hook": GrinchItemData("Mission Specific Items", 207, IC.progression,
        [GrinchRamData(0x800101FA, binary_bit_pos=1)]),
    "Sculpting Tools": GrinchItemData("Mission Specific Items", 208, IC.progression,
        [GrinchRamData(0x800101F9, binary_bit_pos=3)]),
    "Hammer": GrinchItemData("Mission Specific Items", 209, IC.progression,
        [GrinchRamData(0x800101F9, binary_bit_pos=4)]),
    "Scout Clothes": GrinchItemData("Mission Specific Items", 210, IC.progression,
        [GrinchRamData(0x800101F9, binary_bit_pos=8)])
}

#Sleigh Parts
SLEIGH_PARTS_TABLE: dict[str, GrinchItemData] = {
    "Exhaust Pipes": GrinchItemData("Sleigh Parts", 300, IC.progression_skip_balancing,
        [GrinchRamData(0x800101FB, binary_bit_pos=3), GrinchRamData(0x800100AA, binary_bit_pos=6)]),
    "GPS": GrinchItemData("Sleigh Parts", 301, IC.progression_skip_balancing,
        [GrinchRamData(0x800101FB, binary_bit_pos=6), GrinchRamData(0x800100AA, binary_bit_pos=6)]),
    "Tires": GrinchItemData("Sleigh Parts", 302, IC.progression_skip_balancing,
        [GrinchRamData(0x800101FB, binary_bit_pos=5), GrinchRamData(0x800100AA, binary_bit_pos=6)]),
    "Skis": GrinchItemData("Sleigh Parts", 303, IC.progression_skip_balancing,
        [GrinchRamData(0x800101FB, binary_bit_pos=4), GrinchRamData(0x800100AA, binary_bit_pos=6)]),
    "Twin-End Tuba": GrinchItemData("Sleigh Parts", 304, IC.progression_skip_balancing,
        [GrinchRamData(0x800101FB, binary_bit_pos=7), GrinchRamData(0x800100AA, binary_bit_pos=6)])
}

#Access Keys
KEYS_TABLE: dict[str, GrinchItemData] = {
    "Whoville Vacuum Access": GrinchItemData("Vacuum Access", 400, IC.progression,
        [GrinchRamData()]),
    "Who Forest Vacuum Access": GrinchItemData("Vacuum Access", 401, IC.progression,
        [GrinchRamData(0x800100AA, binary_bit_pos=3)]),
    "Who Dump Vacuum Access": GrinchItemData("Vacuum Access", 402, IC.progression,
        [GrinchRamData(0x800100AA, binary_bit_pos=4)]),
    "Who Lake Vacuum Access": GrinchItemData("Vacuum Access", 403, IC.progression,
        [GrinchRamData(0x800100AA, binary_bit_pos=5)]),
    "Progressive Vacuum Access": GrinchItemData("Vacuum Access", 404, IC.progression,
        [GrinchRamData()]),
    "Spin N' Win Door Unlock": GrinchItemData("Supadow Door Unlocks", 405, IC.progression,
        [GrinchRamData()]),
    "Dankamania Door Unlock": GrinchItemData("Supadow Door Unlocks", 406, IC.progression,
        [GrinchRamData()]),
    "The Copter Race Contest Door Unlock": GrinchItemData("Supadow Door Unlocks", 407, IC.progression,
        [GrinchRamData()]),
    "Progressive Supadow Door Unlock": GrinchItemData("Supadow Door Unlocks", 408, IC.progression,
        [GrinchRamData()])
}

#Misc Items
MISC_ITEMS_TABLE: dict[str, GrinchItemData] = {
    "Fully Healed Grinch": GrinchItemData("Health Items", 500, IC.filler, [GrinchRamData(0x800E8FDC, value=120)]),
    "Heart of Stones": GrinchItemData("Health Items", 501, IC.useful, [GrinchRamData(0x800100ED, value=1)]),
    "5 Rotten Eggs": GrinchItemData("Rotten Egg Bundles", 502, IC.filler, [GrinchRamData(0x80010058, value=5)]),
    "10 Rotten Eggs": GrinchItemData("Rotten Egg Bundles", 503, IC.filler, [GrinchRamData(0x80010058, value=10)]),
    "20 Rotten Eggs": GrinchItemData("Rotten Egg Bundles", 504, IC.filler, [GrinchRamData(0x80010058, value=20)])
}

#Traps
TRAPS_TABLE: dict[str, GrinchItemData] = {
    "Ice Trap": GrinchItemData("Traps", 600, IC.trap, [GrinchRamData()]),
    "Bee Trap": GrinchItemData("Traps", 601, IC.trap, [GrinchRamData()]),
    "Electric Trap": GrinchItemData("Traps", 602, IC.trap, [GrinchRamData()]),
    "Tip Toe Trap": GrinchItemData("Traps", 603, IC.trap, [GrinchRamData()]),
    "Damage Trap": GrinchItemData("Traps", 604, IC.trap, [GrinchRamData(0x800E8FDC, value=20)]),
    "Depletion Trap": GrinchItemData("Traps", 605, IC.trap, [GrinchRamData(0x80010058, value=0)]),
    "Dump it to Crumpit": GrinchItemData("Traps", 606, IC.trap,
        [GrinchRamData(0x80010000, value=0x05), GrinchRamData(0x8008FB94, value=1)]),
    "Rocket Spring Trap": GrinchItemData("Traps", 607, IC.trap, [GrinchRamData()]),
    "Who sent me here?": GrinchItemData("Traps", 608, IC.trap, [GrinchRamData(0x8008FB94, value=1)])
}