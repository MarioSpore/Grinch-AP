from typing import TYPE_CHECKING, NamedTuple, Optional

from BaseClasses import Region, MultiWorld, Entrance
from .Rules import interpret_rule
from .Items import grinch_items

from ..generic.Rules import add_rule

if TYPE_CHECKING:
    from . import GrinchWorld

mainareas_list = [
    "Mount Crumpit"
    "Whoville",
    "Who Forest",
    "Who Dump",
    "Who Lake",
]

subareas_list = [
    "Post Office",
    "City Hall",
    "Clock Tower",
    "Ski Resort",
    "Civic Center",
    "Minefield",
    "Power Plant",
    "Generator Building",
    "Submarine World",
    "Scout's Hut",
    "North Shore",
    "Mayor's Villa",
    "Sleigh Room",
    "Sleigh Ride",
]

supadow_list = [
    "Spin N' Win Supadow",
    "Dankamania Supadow",
    "The Copter Race Contest Supadow",
    "Bike Race",
]

class GrinchRegionInfo(NamedTuple):
    map_id: int
    parent_region: str
    allow_deathlink: bool = False
    health_addr: Optional[int] = None
    death_trigger_addr: Optional[int] = None
    map_table_addr: Optional[int] = None
    region_access: Optional[list[list[str]]] = None
    advanced_region_access: Optional[list[list[str]]] = None

class GrinchRegion(Region):
    region_data: GrinchRegionInfo

    def __init__(self, region_name: str, region_data: GrinchRegionInfo, player: int, multiworld: MultiWorld):
        super().__init__(region_name, player, multiworld)
        self.region_data = region_data

ALL_REGIONS_INFO: dict[str, GrinchRegionInfo] = {
    "Mount Crumpit": GrinchRegionInfo(0x05, "", False, 0x800FAAF0, 0x800FAADB, 0x800FAAB4),

    "Whoville": GrinchRegionInfo(0x07, "Mount Crumpit", True, 0x800E8FDC, 0x800E8FC7, 0x800E8FA0,
        region_access=[
            [grinch_items.keys.WHOVILLE],
            ["1:" + grinch_items.keys.PROGRESSIVE_VACUUM_TUBE],
        ],),

    "Who Forest": GrinchRegionInfo(0x0B, "Mount Crumpit", True, 0x800E1C90, 0x800E1C7B, 0x800E1C54,
        region_access=[
            [grinch_items.keys.WHO_FOREST],
            ["2:" + grinch_items.keys.PROGRESSIVE_VACUUM_TUBE],
        ],),

    "Who Dump": GrinchRegionInfo(0x0E, "Mount Crumpit", True, 0x800DFF60, 0x800DFF4B, 0x800DFF24,
        region_access=[
            [grinch_items.keys.WHO_DUMP],
            ["3:" + grinch_items.keys.PROGRESSIVE_VACUUM_TUBE],
        ],),

    "Who Lake": GrinchRegionInfo(0x12, "Mount Crumpit", True, 0x800DD1A8, 0x800DD193, 0x800DD16C,
        region_access=[
            [grinch_items.keys.WHO_LAKE],
            ["4:" + grinch_items.keys.PROGRESSIVE_VACUUM_TUBE],
        ],),

    "Sleigh Room": GrinchRegionInfo(0x05, "Mount Crumpit", False, 0x800FAAF0, 0x800FAADB, 0x800FAAB4,
        region_access=[
            [grinch_items.keys.SLEIGH_ROOM_KEY],
        ],),

    "Spin N' Win": GrinchRegionInfo(0x1A, "Mount Crumpit", False),
    "Dankamania": GrinchRegionInfo(0x1B, "Mount Crumpit", False),
    "The Copter Race Contest": GrinchRegionInfo(0X1C, "Mount Crumpit", False),
    "Post Office": GrinchRegionInfo(0x0A, "Whoville", False, 0x800DFBA0, 0x800DFB8B, 0x800DFB64,
        region_access=[
            [grinch_items.level_items.WV_WHO_CLOAK],
        ],),

    "City Hall": GrinchRegionInfo(0x08, "Whoville", True, 0x800E70CC, 0x800E70B7, 0x800E7090,
        region_access=[
            [grinch_items.gadgets.ROTTEN_EGG_LAUNCHER],
        ],),

    "Clock Tower": GrinchRegionInfo(0x09, "Whoville", False, 0x800E7124, 0x800E710F, 0x800E70E8,
        region_access=[
            [grinch_items.moves.SNEAK],
            [grinch_items.gadgets.SLIME_SHOOTER],
        ],),

    "Ski Resort": GrinchRegionInfo(0x0C, "Who Forest", True, 0x800E98FC, 0x800E98E7, 0x800E98C0,
        region_access=[
            [grinch_items.level_items.WF_CABLE_CAR_ACCESS_CARD],
        ],),

    "Civic Center": GrinchRegionInfo(0x0D, "Who Forest", True, 0x800DDEDC, 0x800DDEC7, 0x800DDEA0,
        region_access=[
            [grinch_items.gadgets.GRINCH_COPTER],
            [grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE],
        ],),

    "Minefield": GrinchRegionInfo(0x11, "Who Dump", True, 0x800E8800, 0x800E87EB, 0x800E87C4,
        region_access=[
            [grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE],
            [grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE],
        ],),

    "Power Plant": GrinchRegionInfo(0x10, "Who Dump", True, 0x800E8898, 0x800E8883, 0x800E885C,
        region_access=[
            [grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE],
            [grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE],
            [grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE],
        ],),

    "Generator Building": GrinchRegionInfo(0x0F, "Power Plant", True, 0x800E0F10, 0x800E0EFB, 0x800E0ED4,
        region_access=[
            [grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER],
            [grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
             grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
             grinch_items.gadgets.ROCKET_SPRING,
             grinch_items.moves.MAX,
             grinch_items.moves.BAD_BREATH],
        ],),

    "Submarine World": GrinchRegionInfo(0x17, "Who Lake", True, 0x800E03A4, 0X800E038F, 0x800E0368,
        region_access=[
            [grinch_items.gadgets.MARINE_MOBILE],
        ],),

    "Scout's Hut": GrinchRegionInfo(0x16, "Who Lake", True, 0x800D5E38, 0x800D5E25, 0x800D5DFC,
        region_access=[
            [grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.SNEAK],
            [grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SNEAK],
        ],),

    "North Shore": GrinchRegionInfo(0x14, "Who Lake", True, 0x800DD478, 0x800DD463, 0x800DD43C,
        region_access=[
            [grinch_items.level_items.WL_SCOUT_CLOTHES,
            grinch_items.moves.SNEAK],
        ],),
    "Mayor's Villa": GrinchRegionInfo(0x16, "North Shore", True, 0x800FA804, 0x800FA7EF, 0x800FA7C8,
        region_access=[
            [grinch_items.level_items.WL_SCOUT_CLOTHES],
        ],),
    "Bike Race": GrinchRegionInfo(0x18, "Sleigh Room", False),
    "Sleigh Ride": GrinchRegionInfo(0x19, "Sleigh Room", False, 0x800E4FBC, 0x800E4FC0, None,
        region_access=[
            [grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
             grinch_items.keys.WHOVILLE,
             grinch_items.keys.WHO_FOREST,
             grinch_items.keys.WHO_DUMP,
             grinch_items.keys.WHO_LAKE,
             grinch_items.gadgets.ROCKET_SPRING,
             grinch_items.gadgets.MARINE_MOBILE,
             grinch_items.moves.MAX,
             grinch_items.moves.SEIZE,
             grinch_items.moves.PANCAKE],
             [grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
             "4:" + grinch_items.keys.PROGRESSIVE_VACUUM_TUBE,
             grinch_items.gadgets.ROCKET_SPRING,
             grinch_items.gadgets.MARINE_MOBILE,
             grinch_items.moves.MAX,
             grinch_items.moves.SEIZE,
             grinch_items.moves.PANCAKE],
        ],),
}

def create_regions(world: "GrinchWorld"):
    for area in [*mainareas_list, *subareas_list, *supadow_list]:
        # Each area in mainarea, subarea, and supadow create a region for the given player
        world.multiworld.regions.append(Region(area, world.player, world.multiworld))


# TODO Optimize this function
def grinchconnect(
    world: "GrinchWorld",
    current_region_name: str,
    connected_region_name: str,
    access_rules: list[list[str]]
):
    current_region = world.get_region(current_region_name)
    connected_region = world.get_region(connected_region_name)
    rule_list = interpret_rule(access_rules, world.player)
    # Goes from current to connected
    curr_entr: Entrance = current_region.connect(connected_region)
    # Goes from connected to current
    connect_entr: Entrance = connected_region.connect(current_region)

    for access_rule in rule_list:
        if rule_list.index(access_rule) == 0:
            add_rule(curr_entr, access_rule)

        else:
            add_rule(curr_entr, access_rule, combine="or")


        if rule_list.index(access_rule) == 0:
            add_rule(connect_entr, access_rule)

        else:
            add_rule(connect_entr, access_rule, combine="or")


# What regions are connected to each other
def connect_regions(world: "GrinchWorld", multiworld: MultiWorld):
    for grinch_region, grinch_data in ALL_REGIONS_INFO.items():
        multiworld.regions.append(GrinchRegion(grinch_region, grinch_data, world.player, multiworld))

        if grinch_region == "Mount Crumpit":
            continue
        grinchconnect(world, grinch_region, grinch_data.parent_region)