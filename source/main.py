# Configure classpath

import jnius_config

jnius_config.set_classpath("..",
                           r"/Users/maxim/Documents/Programming/Python/pyper/libraries/spigot-api-1.20.2.jar",
                           r"/Users/maxim/Documents/Programming/Python/pyper/libraries/guava-32.1.3-jre.jar")

from utils import require

from benchmarks import Clock, print_measurements


def main():
    # Testing some stuff
    with Clock("Python attribute tests") as clock:
        class BigAttributeClass:
            pass

        for i in range(2000):
            setattr(BigAttributeClass, f"someAttribute{i}", i)

        WrappedBigAttributeClass = require("BigAttributeClass", BigAttributeClass)

        clock.tick("created class")

        obj = WrappedBigAttributeClass()
        clock.tick("created object")

        print(obj.some_attribute1000)
        clock.tick("queried attribute")

        print(obj.some_attribute1000)
        clock.tick("queried attribute again")

        """
        This test learns us that Python attribute lookup is relatively slow for larger objects, but when you do it
        again, it's much faster. This is because Python caches the attribute lookup, so it doesn't have to do it again.
        """

    with Clock("location tests") as clock:
        Location = require("org.bukkit.Location")
        clock.tick("imported location")

        loc = Location(None, 20, -103.43, 1, 40, 65)
        print(loc)
        clock.tick("created location")

        other = Location(None, -3, 4, 2, 0, 0)
        print(other)
        clock.tick("created other location")

        print(loc.y)
        clock.tick("queried y")

        print(loc.block_y)
        clock.tick("queried Python block y")

        print(loc.block_y)
        clock.tick("queried Python block y again")

        print(other.block_y)
        clock.tick("queried Python block y on other location")

        print(other.blockY)
        clock.tick("queried Java block y field on other location")

        print(other.getBlockY())
        clock.tick("queried Java block y method on other location")

        print(abs(loc))
        clock.tick("queried Python abs")

        print(loc.length())
        clock.tick("queried Java length")

        print(loc.yaw)
        clock.tick("queried yaw")

        loc.yaw += 60
        clock.tick("added 60 to yaw")

        """
        This test learns us that Java classes need to warm-up before they can be used efficiently. When we call the
        same method twice, even if they are different instances, the second call is much faster.
        It seems that other methods, like length(), don't have this problem, or they get warmed up because of the other
        method calls.
        """

    with Clock("material tests") as clock:
        Material = require("org.bukkit.Material")
        clock.tick("imported material")

        Material = require("org.bukkit.Material")
        clock.tick("imported material again")

        oak_wood = Material.OAK_WOOD
        clock.tick("queried oak wood normal way")

        white_dye = Material.WHITE_DYE
        clock.tick("queried white dye normal way")

        print(oak_wood.solid)
        clock.tick("checked if oak wood is solid")

        print(oak_wood.solid)
        clock.tick("checked if oak wood is solid again")

        print(oak_wood.isSolid())
        clock.tick("checked if oak wood is solid again but with method")

        print(white_dye.solid)
        clock.tick("checked if white dye is solid")

        print(oak_wood.getEquipmentSlot())
        clock.tick("queried oak wood equipment slot with Java method")

        # TODO fix Pythonic attributes for Java enums, because they reference the pure Java instance, not the wrapper
        # print(oak_wood.equipment_slot)
        # clock.tick("queried oak wood equipment slot with Python method")

        """
        This test shows the same problem as with the location tests, but in a larger scale, because Material has more
        than 2000 attributes. This is a problem, but not a huge one. In development, this will make the first
        iterations of your code slower, but after that, we reach sufficient performance.
        We still can make adjustments to keep everything under 1ms, which will be our goal throughout the project.
        """
        # TODO for highly-used classes, import them automatically on startup, so they are warmed up

    # print_measurements(detailed=True)


if __name__ == "__main__":
    main()
