from math import floor

from utils import get_absolute_path

def get_fuel_4_fuel(current):
    res = 0
    while current > 0:
        current = floor(current / 3) - 2
        if current <= 0:
            break
        res += current
    return res

fuel_4_modules = 0
fuel_4_fuel = 0
with open(get_absolute_path("day1.input")) as f:
    for line in f:
        if not len(line):
            break
        module_size = int(line)
        fuel_4_module = floor(module_size / 3) - 2
        fuel_4_modules += fuel_4_module
        fuel_4_fuel += get_fuel_4_fuel(fuel_4_module)

print("Fuel for modules: {}".format(fuel_4_modules))
print("Fuel for fuels: {}".format(fuel_4_fuel))
print("Total: {}".format(fuel_4_modules + fuel_4_fuel))

