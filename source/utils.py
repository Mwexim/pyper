import jnius

from benchmarks import measure

UPPERCASE_ABBREVIATIONS = {"AABB", "ID", "IP", "UUID"}
"""Represents all commonly used abbreviations in the Spigot framework"""

imported_classes = {}


def camel_case_possibilities(text: str, pascal_case: bool = False) -> list[str]:
    """
    Changes a kebab_case string to camelCase.
    :param text: a kebab_case string
    :param pascal_case: whether to change the string to camelCase or PascalCase
    :return: the string in camelCase
    """
    results = ["", ""]
    for part in text.split("_"):
        if not results[0] and not pascal_case:
            # The first part should always be lowercase
            results[0] += part.lower()
            results[1] += part.lower() if part.upper() not in UPPERCASE_ABBREVIATIONS else part.upper()
        else:
            results[0] += part[0].upper() + part[1:].lower()
            results[1] += part[0].upper() + part[1:].lower() if part.upper() not in UPPERCASE_ABBREVIATIONS else part.upper()

    return results if results[0] != results[1] else results[:1]


def require(java_class: str, default=None):
    """
    Imports a Java class and adds all Python magic methods to it. This allows for a more Pythonic way of using Java,
    adding all the kebab_case variants of the camelCase methods.

    When importing the same class multiple times, the same instance class will be returned, meaning all instances will
    be unique.

    Examples
    --------

    Creating a spawn point location::

        from api import world

        Location = require("org.bukkit.Location")
        spawn_point = Location(world("main"), 10, 20, 30)

    Note that one should use the provided functions in the api module to create instances of the Java classes, as these
    have enhanced functionality::

        spawn_point = location(world("main"), 10, 20, 30)

    That said, the first example still acts as a good example of how to use the require function.

    :param java_class: the Java class to import
    :param default: the default value to pick if the Java class could not be imported
    :return: the imported Java class
    """
    if java_class in imported_classes:
        return imported_classes[java_class]

    try:
        imported = jnius.autoclass(java_class, include_protected=False, include_private=False)
    except jnius.JavaException:
        imported = default

    class JavaWrapper:
        # Unary math operators
        def __neg__(self):
            pass

        def __pos__(self):
            pass

        def __abs__(self):
            if hasattr(self, "length"):
                return self.length()

        def __invert__(self):
            pass

        # Binary math operators
        def __add__(self, other):
            pass

        def __sub__(self, other):
            pass

        def __mul__(self, other):
            pass

        def __matmul__(self, other):
            pass

        def __truediv__(self, other):
            pass

        def __floordiv__(self, other):
            pass

        def __mod__(self, other):
            pass

        def __divmod__(self, other):
            pass

        def __pow__(self, other, modulo):
            pass

        def __lshift__(self, other):
            pass

        def __rshift__(self, other):
            pass

        def __and__(self, other):
            pass

        def __xor__(self, other):
            pass

        def __or__(self, other):
            pass

        # Special math functions
        def __round__(self, ndigits):
            pass

        def __trunc__(self):
            pass

        def __floor__(self):
            pass

        def __ceil__(self):
            pass

        # Boolean methods
        def __bool__(self):
            pass

        # Comparison methods
        def __lt__(self, other):
            pass

        def __le__(self, other):
            pass

        def __eq__(self, other):
            pass

        def __ne__(self, other):
            pass

        def __gt__(self, other):
            pass

        def __ge__(self, other):
            pass

        # Context methods
        def __enter__(self):
            pass

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

        # Other class methods
        def __del__(self):
            pass

        def __copy__(self):
            pass

        # Container methods
        def __contains__(self, item):
            pass

        def __delitem__(self, key):
            pass

        def __getitem__(self, item):
            pass

        def __iter__(self):
            pass

        def __len__(self):
            if hasattr(self, "size"):
                return self.size()

        def __missing__(self, key):
            pass

        def __reversed__(self):
            pass

        def __setitem__(self, key, value):
            pass

        # Attribute methods
        def __delattr__(self, item):
            pass

        @measure("getattr")
        def __getattr__(self, item):
            print("$__getattr__", item)
            # Because we are putting "get" and "is" in front of it, we need to use PascalCase
            for possibility in camel_case_possibilities(item, pascal_case=True):
                # If the attribute exists on its own, it's probably camelCase, not PascalCase
                if possibility[0].lower() + possibility[1:] in dir(self):
                    result = getattr(self, possibility[0].lower() + possibility[1:])
                elif "get" + possibility in dir(self):
                    result = getattr(self, "get" + possibility)
                elif "is" + possibility in dir(self):
                    result = getattr(self, "is" + possibility)
                else:
                    raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")

                return result() if callable(result) else result

        def __setattr__(self, key, value):
            # Because we are putting "set" in front of it, we need to use PascalCase
            for possibility in camel_case_possibilities(key, pascal_case=True):
                if "set" + possibility in dir(self):
                    return getattr(self, "set" + possibility)(value)

        # String representation methods
        def __format__(self, format_spec):
            pass

        def __hash__(self):
            return self.hashCode()

        def __repr__(self):
            return self.__str__()

        def __str__(self):
            return self.toString()

    # Loops over all explicitly defined methods in the JavaWrapper class and adds them to the imported class
    for name, method in JavaWrapper.__dict__.items():
        if name not in ("__module__", "__dict__", "__weakref__", "__doc__", "__class__"):
            setattr(imported, name, method)

    imported_classes[java_class] = imported
    return imported
