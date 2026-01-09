import math

from BaseClasses import Region, Item, Location
from .Locations import grinch_locations_to_id, grinch_locations, GrinchLocation, get_location_names_per_category, GrinchLocationData
from .Items import (grinch_items_to_id, GrinchItem, ALL_ITEMS_TABLE, MISC_ITEMS_TABLE, get_item_names_per_category,
    TRAPS_TABLE, MOVES_TABLE, USEFUL_ITEMS_TABLE)
from .Regions import connect_regions
from .Rules import set_location_rules

from .Client import *
from typing import ClassVar

from worlds.AutoWorld import World
from Options import OptionError

from .GrinchOptions import GrinchOptions
from .Rules import access_rules_dict
from .Web import GrinchWeb


class GrinchWorld(World):
    game: ClassVar[str] = "The Grinch"
    options_dataclass = GrinchOptions
    options: GrinchOptions
    topology_present = True # not an open world game, very linear, allows "Paths" in spoiler log
    item_name_to_id: ClassVar[dict[str, int]] = grinch_items_to_id()
    location_name_to_id: ClassVar[dict[str, int]] = grinch_locations_to_id()
    required_client_version = (0, 6, 5) # Unused atm, replaced by ap.json
    item_name_groups = get_item_names_per_category()
    location_name_groups = get_location_names_per_category()
    web = GrinchWeb()

    ut_can_gen_without_yaml = True  # class var that tells it to ignore the player yaml

    def __init__(self, *args, **kwargs):  # Pulls __init__ function and takes control from there in BaseClasses.py
        self.origin_region_name: str = "Mount Crumpit"
        super(GrinchWorld, self).__init__(*args, **kwargs)

    def generate_early(self) -> None:  # Special conditions changed before generation occurs
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

        total_trapweights = sum(self.options.trap_weight[trap] for trap in self.options.trap_weight.keys())
        if total_trapweights <= 0 and self.options.trap_percentage >= 1:
            raise OptionError("Cannot begin generation as no trap options are defined. At least one trap item " +
                f"must have a weight of at least 1. The following player's YAML needs to be fixed: {self.player_name}")

        if hasattr(self.multiworld, "re_gen_passthrough"):
            if self.game in self.multiworld.re_gen_passthrough:
                slot_data = self.multiworld.re_gen_passthrough[self.game]
                print(slot_data)
                self.options.unlimited_eggs.value = slot_data["give_unlimited_eggs"]
                self.options.starting_area.value = slot_data["starting_area"]
                self.options.exclude_environments.value = ["exclude_environments"]
                self.options.giftsanity.value = slot_data["giftsanity"]
                self.options.progressive_vacuums = slot_data["progressive_vacuums"]
                self.options.missionsanity = slot_data["missionsanity"]
                self.options.supadow_minigames = slot_data["supadow_minigames"]
                self.options.move_rando = slot_data["move_rando"]
                self.options.moves_to_randomize = slot_data["moves_to_randomize"]
                self.options.gadget_rando = slot_data["gadget_rando"]
                self.options.gadgets_to_randomize = slot_data["gadgets_to_randomize"]
                self.options.exclude_gc = slot_data["exclude_gc"]
                self.options.progressive_gadgets = slot_data["progressive_gadgets"]
                self.options.killsanity = slot_data["killsanity"]

    def create_regions(self):  # Generates all regions for the multiworld
        for region_name in access_rules_dict.keys():
            self.multiworld.regions.append(Region(region_name, self.player, self.multiworld))

        self.multiworld.regions.append(Region("Mount Crumpit", self.player, self.multiworld))

        for location, data in grinch_locations.items():
            region = self.get_region(data.region)

            if location == "MC - Sleigh Ride - Neutralizing Santa":
                region.add_event(location, "Goal", None, Location, Item)
                continue

            # No .value after self.options.giftsanity because UT no likey
            if "Giftsanity" in data.location_group and (not self.options.giftsanity or self.options.exclude_gc):
                continue

            # No .value after self.options.missionsanity because UT no likey
            if "Missions" in data.location_group and self.options.missionsanity in [0,2]:
                continue

            # No .value after self.options.missionsanity because UT no likey
            if "Missionsanity" in data.location_group and self.options.missionsanity in [0,1]:
                continue

            # If the region is in the list to be ignored, DON'T create the location and just continue.
            # Ex if Mount Crumpit is in the exclude env list, no locations should exist in Mount Crumpit.
            if region.name in self.options.exclude_environments.value:
                if region.name == "Mount Crumpit":
                    logger.warning(f"Player {self.player_name} has excluded Mount Crumpit, which is where a large number of Sphere 1 locations usually exist.")
                continue

            entry = GrinchLocation(self.player, location, region, data)
            region.locations.append(entry)

        connect_regions(self)

    def create_item(self, item: str) -> GrinchItem:  # Creates specific items on demand
        if item in ALL_ITEMS_TABLE.keys():
            return GrinchItem(item, self.player, ALL_ITEMS_TABLE[item])

        raise Exception(f"Invalid item name: {item}")

    def create_items(self):  # Generates all items for the multiworld
        self_itempool: list[GrinchItem] = []
        sub_area_items: dict[str, list[str]] = {
            "Who Cloak": ["Post Office"],
            "Scout Clothes": ["Mayor's Villa", "North Shore"],
            "Cable Car Access Card": ["Ski Resort"],
        }
        missionsanity_items: list[str] = [
            "Painting Bucket",
            "Drill",
        ]

        # Precollected items is stored per player. First, we must get the current player's starting inventory.
        # From here, we get an AP item list. But, we only care about the name. So we get a list of strings as a result.
        player_start_inv: list[str] = [item.name for item in self.multiworld.precollected_items[self.player]]

        for item, data in {**SLEIGH_TABLE}.items():
            # Only create the item if it doesn't already exist in the player's start inventory.
            if not item in player_start_inv:
                self_itempool.append(self.create_item(item))

        for hearts_added in USEFUL_ITEMS_TABLE:
            if hearts_added == grinch_items.useful_items.HEART_OF_STONE:
                # Get the count of already created Heart of Stone items, but capped to 4
                heart_stone_count: int = min(player_start_inv.count(grinch_items.useful_items.HEART_OF_STONE), 4)
                for _ in range(4 - heart_stone_count):
                    self_itempool.append(self.create_item(hearts_added))

        for mission_item in MISSION_ITEMS_TABLE:
            # Only create the item if it doesn't already exist in the player's start inventory.
            if mission_item in player_start_inv:
                continue

            # Checks to see if there are any locations in the Sub-area list.
            sub_area_has_no_locations: bool = False
            if mission_item in sub_area_items.keys():
                for grinch_reg in sub_area_items[mission_item]:
                    if len(self.get_region(grinch_reg).get_locations()) == 0:
                        sub_area_has_no_locations = True

            # If the item is a sub_area_item and it has 0 locations, add it to start inventory
            if sub_area_has_no_locations:
                self.multiworld.push_precollected(self.create_item(mission_item))
                player_start_inv.append(mission_item)
            # Else if the player disables missionsanity, add the item into start inventory
            # No .value after self.options.missionsanity because UT no likey
            elif self.options.missionsanity == 0:
                self.multiworld.push_precollected(self.create_item(mission_item))
                player_start_inv.append(mission_item)
            # Else, let the multiworld create the item normally.
            else:
                self_itempool.append(self.create_item(mission_item))

        # Add various moves that the user requested.
        for moves_added in MOVES_TABLE:
            # Only create the item if it doesn't already exist in the player's start inventory.
            if moves_added in player_start_inv:
                continue

            if self.options.move_rando and moves_added in self.options.moves_to_randomize:
                self_itempool.append(self.create_item(moves_added))
            else:
                self.multiworld.push_precollected(self.create_item(moves_added))
                player_start_inv.append(moves_added)

        # Adds gadgets
        for gadgets_added in GADGETS_TABLE:
            if gadgets_added == "Grinch Copter" and self.options.exclude_gc:
                continue

            # Only create the item if it doesn't already exist in the player's start inventory.
            elif gadgets_added in player_start_inv:
                continue

            if self.options.gadget_rando and gadgets_added in self.options.gadgets_to_randomize:
                self_itempool.append(self.create_item(gadgets_added))
            else:
                self.multiworld.push_precollected(self.create_item(gadgets_added))
                player_start_inv.append(gadgets_added)

        if not self.options.progressive_vacuums:
        # When the starting area is chosen, add the key to the starting inventory.
            if self.options.starting_area.value == 0:
                self.multiworld.push_precollected(self.create_item("Whoville Vacuum Tube"))
                player_start_inv.append("Whoville Vacuum Tube")
            elif self.options.starting_area.value == 1:
                self.multiworld.push_precollected(self.create_item("Who Forest Vacuum Tube"))
                player_start_inv.append("Who Forest Vacuum Tube")
            elif self.options.starting_area.value == 2:
                self.multiworld.push_precollected(self.create_item("Who Dump Vacuum Tube"))
                player_start_inv.append("Who Dump Vacuum Tube")
            elif self.options.starting_area.value == 3:
                self.multiworld.push_precollected((self.create_item("Who Lake Vacuum Tube")))
                player_start_inv.append("Who Lake Vacuum Tube")
        else:
            self.multiworld.push_precollected((self.create_item("Progressive Vacuum Tube")))
            player_start_inv.append("Progressive Vacuum Tube")

        if not self.options.progressive_vacuums:
            for vacuums_added in KEYS_TABLE.keys():
                if vacuums_added == "Progressive Vacuum Tube":
                    continue

                if vacuums_added not in player_start_inv:
                    self_itempool.append(self.create_item(vacuums_added))
        else:
            progress_vac_count: int = min(player_start_inv.count("Progressive Vacuum Tube"),4)
            for _ in range(4 - progress_vac_count):
                self_itempool.append(self.create_item("Progressive Vacuum Tube"))

        # Get number of current unfilled locations
        unfilled_locations: int = len(self.multiworld.get_unfilled_locations(self.player)) - len(self_itempool)
        trap_locations: int = int(math.floor(unfilled_locations * (self.options.trap_percentage / 100)))
        filler_locations = unfilled_locations - trap_locations

        # If trap_locations is 0, this will automatically get skipped
        for _ in range(trap_locations):
            # Keys are the individual items, values are the weights based on the option being set
            self_itempool.append(self.create_item(self.get_weighted_filler_item
                (list(self.options.trap_weight.keys()), list(self.options.trap_weight.values()))))

        # total_fillerweights = sum(self.options.filler_weight[filler] for filler in self.options.filler_weight.keys())
        for _ in range(filler_locations):
            # if total_fillerweights > 0:
                # Keys are the individual items, values are the weights based on the option being set
                self_itempool.append(self.create_item(self.get_weighted_filler_item(
                    list(self.options.filler_weight.keys()), list(self.options.filler_weight.values()))))
            # else:
                # self_itempool.append(self.create_item("5 Rotten Eggs"))

        self.multiworld.itempool += self_itempool

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Goal", self.player)
        set_location_rules(self)

    def get_weighted_filler_item(self, other_filler: list[str], weights_dict: list[int]) -> str:
        # The below does this for deterministic reasons, otherwise if you rolled the same seed, you would get different outcomes.
        local_dict: dict[str, int] = dict(sorted(dict(zip(other_filler, weights_dict)).items()))
        return self.random.choices(list(local_dict.keys()), list(local_dict.values()))[0]

    def fill_slot_data(self):
        return {
            "give_unlimited_eggs": self.options.unlimited_eggs.value,
            "ring_link": self.options.ring_link.value,
            "starting_area": self.options.starting_area.value,
            "exclude_environments": self.options.exclude_environments.value,
            "giftsanity": self.options.giftsanity.value,
            "progressive_vacuums": self.options.progressive_vacuums.value,
            "missionsanity": self.options.missionsanity.value,
            "supadow_minigames": self.options.supadow_minigames.value,
            "move_rando": self.options.move_rando.value,
            "moves_to_randomize": self.options.moves_to_randomize.value,
            "gadget_rando": self.options.gadget_rando.value,
            "gadgets_to_randomize": self.options.gadgets_to_randomize.value,
            "exclude_gc": self.options.exclude_gc.value,
            "progressive_gadgets": self.options.progressive_gadgets.value,
            "killsanity": self.options.killsanity.value,

        }

    def generate_output(self, output_directory: str) -> None:
        # print("")
        pass