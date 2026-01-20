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
            ["1:" + grinch_items.keys.PROGRESSIVE_VACUUM_TUBE]
        ],),

    "Who Forest": GrinchRegionInfo(0x0B, "Mount Crumpit", True, 0x800E1C90, 0x800E1C7B, 0x800E1C54,
        region_access=[
            [grinch_items.keys.WHO_FOREST],
            ["2:" + grinch_items.keys.PROGRESSIVE_VACUUM_TUBE],
        ],),

    "Who Dump": GrinchRegionInfo(),
    "Who Lake": GrinchRegionInfo(),
    "Sleigh Room": GrinchRegionInfo(),
    "Spin N' Win": GrinchRegionInfo(),
    "Dankamania": GrinchRegionInfo(),
    "The Copter Race Contest": GrinchRegionInfo(),
    "Post Office": GrinchRegionInfo(),
    "Clock Tower": GrinchRegionInfo(),
    "Ski Resort": GrinchRegionInfo(),
    "Civic Center": GrinchRegionInfo(),
    "Minefield": GrinchRegionInfo(),
    "Power Plant": GrinchRegionInfo(),
    "Generator Building": GrinchRegionInfo(),
    "Submarine World": GrinchRegionInfo(),
    "Scout's Hut": GrinchRegionInfo(),
    "North Shore": GrinchRegionInfo(),
    "Mayor's Villa": GrinchRegionInfo(),
    "Bike Race": GrinchRegionInfo(),
    "Sleigh Ride": GrinchRegionInfo(),
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