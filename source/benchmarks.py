import statistics
import time

measurements = {}


class Clock:
    def __init__(self, name: str):
        self.name = name
        self.timings = [("", time.perf_counter())]

    def tick(self, name: str):
        self.timings.append((name, time.perf_counter()))

    def close(self):
        print()
        print("Timings for", self.name)
        line = "-" * (12 + len(self.name))
        print(line)

        # Print every timing separately
        for i in range(1, len(self.timings)):
            elapsed = round(1000 * (self.timings[i][1] - self.timings[i - 1][1]), 2)
            print(f"- {self.timings[i][0]} took {elapsed}ms")

        # Print total time
        print("Total time:", round(1000 * (self.timings[-1][1] - self.timings[0][1]), 2), "ms")

        print(line)
        print()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def measure(name: str):
    """
    Add a measurement to this function, calculating and saving the time it takes to execute the function
    to an Exel file.
    :param name: the name of this function
    """
    if name not in measurements:
        measurements[name] = []

    def actual_decorator(function):
        def execute_function(*args, **kwargs):
            start = time.perf_counter()
            result = function(*args, **kwargs)
            end = time.perf_counter()
            # Scale to milliseconds
            measurements[name].append(round(1000 * (end - start), 2))
            return result

        return execute_function

    return actual_decorator


def print_measurements(detailed=False):
    """
    Print the measurements to the console.
    """
    print()
    print("Measurements")
    line = "-" * 12
    print(line)

    # Print every measurement separately
    for name, times in measurements.items():
        if len(times) == 0:
            print(f"- {name} had no measurements")
            continue
        print(f"- {name} took {round(sum(times) / len(times), 2)}ms ± {round(statistics.stdev(times), 2)} (mean ± std. dev.)")
        if detailed:
            print(f"  {' '.join(str(round(time, 2)) for time in times[:10])}" + (" ..." if len(times) > 10 else ""))

    print(line)
    print()
