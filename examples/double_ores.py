from source.events import subscribe, BlockBreakEvent
from random import random

from archive.objects.item import item


@subscribe()
def block_break(event: BlockBreakEvent, block, player):
    # When breaking any ore, has a 10% chance to drop an extra one!
    if "ore" in block.type.name.lower() and player.has_permission("ores.double") and random() < 0.1:
        block.world.drop_item(block.location, item(block=block))
