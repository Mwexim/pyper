# Configure classpath
import time

import jnius_config

jnius_config.set_classpath("..",
                           r"/Users/maxim/Documents/Programming/Python/pyper/libraries/spigot-api-1.20.2.jar",
                           r"/Users/maxim/Documents/Programming/Python/pyper/libraries/guava-32.1.3-jre.jar")
from utils import require

from jnius import autoclass


def main():
    # Testing some stuff
    System = autoclass("java.lang.System")
    System.out.println("Hello world")
    #
    # JBukkit = autoclass("org.bukkit.Bukkit")
    # print(JBukkit)

    # from objects.location import Location, location, world
    # print(Location)
    # first = location(world("Test"), 10, 20.4, 30)
    # second = location(world("Test"), 20.12345, 100, -102, 135, -45)
    # print(first, str(first))
    # print(first.y, first.block_y)
    # print(abs(first), abs(first) ** 2, first.lengthSquared())

    # print(second.yaw)
    # second.yaw += 60
    # print(second.getYaw())

    Location = require("org.bukkit.Location")
    print(Location(None, 20, -103.43, 1, 40, 65))

    results = []
    results.append(time.perf_counter())

    Material = require("org.bukkit.Material")

    results.append(time.perf_counter())

    Material = require("org.bukkit.Material")

    results.append(time.perf_counter())

    oak_wood = Material.OAK_WOOD

    results.append(time.perf_counter())

    print(oak_wood)

    results.append(time.perf_counter())

    print(oak_wood.solid)

    results.append(time.perf_counter())

    for i in range(len(results) - 1):
        print("Main timings:", results[i + 1] - results[i])


if __name__ == "__main__":
    main()
