import math

from BaseClasses import Region, Item, ItemClassification
from .Locations import grinch_locations_to_id, grinch_locations, GrinchLocation, get_location_names_per_category
from .Items import grinch_items_to_id, GrinchItem, ALL_ITEMS_TABLE, MISC_ITEMS_TABLE, get_item_names_per_category, TRAPS_TABLE
from .Regions import connect_regions
from .Rules import set_location_rules

from .Client import *
from typing import ClassVar

from worlds.AutoWorld import World
from Options import OptionError

from .Options import GrinchOptions
from .Rules import access_rules_dict


class GrinchWorld(World):
    game: ClassVar[str] = "The Grinch"
    options_dataclass = Options.GrinchOptions
    options: Options.GrinchOptions
    topology_present = True #not an open world game, very linear
    item_name_to_id: ClassVar[dict[str,int]] = grinch_items_to_id()
    location_name_to_id: ClassVar[dict[str,int]] = grinch_locations_to_id()
    required_client_version = (0, 6, 3)
    item_name_groups = get_item_names_per_category()
    location_name_groups = get_location_names_per_category()

    def __init__(self, *args, **kwargs): #Pulls __init__ function and takes control from there in BaseClasses.py
        self.origin_region_name: str = "Mount Crumpit"
        super(GrinchWorld, self).__init__(*args, **kwargs)

    def generate_early(self) -> None: #Special conditions changed before generation occurs
        if self.options.ring_link == 1 and self.options.unlimited_eggs == 1:
            raise OptionError("Cannot enable both unlimited rotten eggs and ring links. You can only enable one of " +
                f"these at a time. The following player's YAML needs to be fixed: {self.player_name}")

        # Total available weight sum of filler items.
        # If this is 0, it means no filler was provided by the user, which will cause generation errors as there will
        #   be not enough items for all defined locations. Later this can be changed to default item and this get removed.
        total_fillerweights = sum(self.options.filler_weight[filler] for filler in self.options.filler_weight.keys())
        if total_fillerweights <= 0:
            raise OptionError("Cannot begin generation as no filler options are defined. At least one filler item " +
                f"must have a weight of at least 1. The following player's YAML needs to be fixed: {self.player_name}")


    def create_regions(self): #Generates all regions for the multiworld
        for region_name in access_rules_dict.keys():
            self.multiworld.regions.append(Region(region_name, self.player, self.multiworld))
        self.multiworld.regions.append(Region("Mount Crumpit", self.player, self.multiworld))
        for location, data in grinch_locations.items():
            region = self.get_region(data.region)
            entry = GrinchLocation(self.player, location, region, data)
            if location == "MC - Sleigh Ride - Neutralizing Santa":
                entry.place_locked_item(Item("Goal", ItemClassification.progression, None, self.player))
            region.locations.append(entry)
        connect_regions(self)

    def create_item(self, item: str) -> GrinchItem: #Creates specific items on demand
        if item in ALL_ITEMS_TABLE.keys():
            return GrinchItem(item, self.player, ALL_ITEMS_TABLE[item])
        raise Exception(f"Invalid item name: {item}")

    def create_items(self): #Generates all items for the multiworld
        self_itempool: list[GrinchItem] = []
        for item, data in ALL_ITEMS_TABLE.items():
            self_itempool.append(self.create_item(item))
            if item == "Heart of Stone":
                for _ in range(3):
                    self_itempool.append(self.create_item(item))

        #Get number of current unfilled locations
        unfilled_locations: int = len(self.multiworld.get_unfilled_locations(self.player)) - len(self_itempool)
        trap_locations: int = int(math.floor(unfilled_locations * (self.options.trap_percentage / 100)))
        filler_locations = unfilled_locations - trap_locations

        # If trap_locations is 0, this will automatically get skipped
        for _ in range(trap_locations):
            self_itempool.append(self.create_item(self.random.choices(
                list(self.options.trap_weight.keys()), list(self.options.trap_weight.values()))[0]))

        # total_fillerweights = sum(self.options.filler_weight[filler] for filler in self.options.filler_weight.keys())
        for _ in range(filler_locations):
            # if total_fillerweights > 0:
                self_itempool.append(self.create_item(self.random.choices(
                    list(self.options.filler_weight.keys()), list(self.options.filler_weight.values()))[0]))
            # else:
                # self_itempool.append(self.create_item("5 Rotten Eggs"))

        self.multiworld.itempool += self_itempool


    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Goal", self.player)
        set_location_rules(self)

    def get_other_filler_item(self, other_filler: list[str]) -> str:
        return self.random.choices(other_filler)[0]

    def fill_slot_data(self):
        return {
            "give_unlimited_eggs": self.options.unlimited_eggs.value,
            "ring_link": self.options.ring_link.value,
        }

    def generate_output(self, output_directory: str) -> None:
        # print("")
        pass