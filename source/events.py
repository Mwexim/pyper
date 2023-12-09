from inspect import signature

events = []


def subscribe(priority="MONITOR", ignore_cancelled=False):
    def actual_decorator(function):
        sign = signature(function)

        def execute_event(event):
            kwargs = {"event": event}
            for parameter in sign.parameters.values():
                if parameter.name != "event":
                    kwargs[parameter.name] = getattr(event, parameter.name)
            function(**kwargs)

        execute_event.__event__ = True
        execute_event.__event_type__ = sign.parameters["event"].annotation

        events.append((execute_event.__event_type__, execute_event))
        return execute_event

    return actual_decorator


def call_event(event):
    for option in events:
        if isinstance(event, option[0]):
            option[1](event)


# ************
# Testing zone
# ************

# class Event:
#     pass
#
#
# class PlayerEvent(Event):
#     def __init__(self, player):
#         self.player = player
#
#
# class PlayerEggThrowEvent(PlayerEvent):
#     def __init__(self, player, egg, hatching, num_hatches, hatching_type):
#         super().__init__(player)
#         self.egg = egg
#         self.hatching = hatching
#         self.num_hatches = num_hatches
#         self.hatching_type = hatching_type
#
#
# class BlockBreakEvent(Event):
#     def __init__(self, block, player):
#         self.block = block
#         self.player = player
#
#
# @subscribe()
# def join(event: PlayerEvent, player):
#     print(f"Hello {event.player}")
#     print(f"Or just, hello {player}")
#
#
# @subscribe()
# def egg_throw(event: PlayerEggThrowEvent, player):
#     print(f"A special egg will be hatched, {player}")
#     # Note that if we want to change event values, we can't use the parameters added
#     # in the function signature, because Python will not reference to the original attribute
#     event.hatching = True
#     event.hatching_type = "zombie"
#     event.num_hatches = 5
#     print(f"{event.num_hatches} {event.hatching_type}s will spawn!")
#
#
# call_event(PlayerEvent("Mwexim"))
# call_event(PlayerEggThrowEvent("HoningPony", None, False, 1, "chicken"))
