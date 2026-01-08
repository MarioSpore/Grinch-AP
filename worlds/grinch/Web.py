from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

from .GrinchOptions import *
from Options import OptionGroup

class GrinchWeb(WebWorld):
    theme = "ice"
    option_groups = [
        OptionGroup("Filler/Trap Settings", [
            FillerWeight,
            TrapPercentage,
            TrapWeight,
            RingLinkOption,
            TrapLinkOption,
        ]),
        OptionGroup("Location Settings", [
            Missionsanity,
            ExcludeEnvironments,
            Gifts,
            Supadow,
            Killsanity,
        ]),
        OptionGroup("Quality of Life", [
            UnlimitedEggs,
        ]),
        OptionGroup("Item Pool", [
            ProgressiveVacuums,
            StartingArea,
            ProgressiveGadgets,
            Gadgetrando,
            Gadgetrandolist,
            ExcludeGC,
            Moverando,
            Moverandolist
        ]),
        OptionGroup("Logic Settings", [
            AdvancedLogic,
        ]),
    ]

    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up The Grinch randomizer connected to an Archipelago Multiworld",
            "English",
            "setup_en.md",
            "setup/en",
            ["MarioSpore", "SomeJakeGuy", "Artamiss"],
        )
    ]