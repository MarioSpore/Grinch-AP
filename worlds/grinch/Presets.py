from typing import Any, Dict

import Options as APOptions
from . import GrinchOptions

vanilla = {
    GrinchOptions.progressive_vacuums: "true",
    GrinchOptions.starting_area: "whoville",
    GrinchOptions.missionsanity: "completion",
    # GrinchOptions.filler_weight: "0",
    GrinchOptions.randomize_mission_items: "false",
    GrinchOptions.randomize_sleigh_parts: "false",
    GrinchOptions.gadget_rando: "true",
    GrinchOptions.move_rando: "false",
    GrinchOptions.teleport_multibind: "false",
    GrinchOptions.unlimited_eggs: "false",
    GrinchOptions.music_rando: "false",
}
beginner_friendly = {
    GrinchOptions.progressive_vacuums: "true",
    GrinchOptions.gadget_rando: "false",
    GrinchOptions.move_rando: "false",
    GrinchOptions.starting_area: "whoville",
    GrinchOptions.teleport_multibind: "true",
    GrinchOptions.randomize_mission_items: "false",
    GrinchOptions.randomize_sleigh_parts: "false",
    GrinchOptions.missionsanity: "none",
    GrinchOptions.exclude_environments: ["Post Office", "Clock Tower", "City Hall", "Ski Resort",
    "Civic Center", "Minefield", "Power Plant", "Generator Building",
    "Scout's Hut", "North Shore", "Mayor's Villa", "Submarine World"],
}
dev_settings = {
    GrinchOptions.missionsanity: "both",
    GrinchOptions.music_rando: "true",
    GrinchOptions.reduced_cutscenes: "true"
}
allsanity = {
    GrinchOptions.exclude_environments: [],
    GrinchOptions.giftsanity: "true",
    GrinchOptions.supadow_minigames: 3,
    GrinchOptions.misc_checks: "true",
    GrinchOptions.move_rando: "true",
    GrinchOptions.gadget_rando: "true",
    GrinchOptions.randomize_mission_items: "true",
    GrinchOptions.randomize_sleigh_parts: "true",
    GrinchOptions.missionsanity: "both",
    GrinchOptions.exclude_gc: "false",
}
minsanity = {
    GrinchOptions.missionsanity: "none",
    GrinchOptions.exclude_environments: ["Post Office", "Clock Tower", "City Hall", "Ski Resort",
    "Civic Center", "Minefield", "Power Plant", "Generator Building",
    "Scout's Hut", "North Shore", "Mayor's Villa", "Submarine World"],
    GrinchOptions.gadget_rando: "false",
    GrinchOptions.move_rando: "false",
    GrinchOptions.misc_checks: "false",
    GrinchOptions.randomize_mission_items: "false",
    GrinchOptions.randomize_sleigh_parts: "false",
}
sync_viable = {
    "progression_balancing": 60,
    GrinchOptions.giftsanity: "false",
    GrinchOptions.reduced_cutscenes: "true",
    GrinchOptions.teleport_multibind: "true",
    GrinchOptions.missionsanity: "completion",
    GrinchOptions.unlimited_eggs: "true",
    GrinchOptions.exclude_gc: "false",
}
async_viable = {
    "progression_balancing": "disabled",
    GrinchOptions.missionsanity: "full",
    GrinchOptions.misc_checks: "true",
}
grinch_options_presets: Dict[str, Dict] = {
    "Beginner Friendly": beginner_friendly,
    "Developer Settings": dev_settings,
    "Pure Vanilla": vanilla,
    "Allsanity": allsanity,
    "Minsanity": minsanity,
    "Sync Viable": sync_viable,
    "Async Viable": async_viable,
}