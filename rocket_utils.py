"""
    This module hold information relating to rocket engine types as well as
    functions to calculate rocket height, speed, etc
"""
import random
import csv

engines = {
    1: {
        "name": "LV-T30",
        "mass": 1.25,
        "thrust": 215.0,
        "fuel_flow": .0685,
        "isp_atm": 320.0,
        "asp_vac": 370,
    },
    2: {
        "name": "LV-909",
        "mass": .5,
        "thrust": 50.0,
        "fuel_flow": .0170,
        "isp_atm": 300.0,
        "asp_vac": 390.0,
    },
    3: {
        "name": "Poodle",
        "mass": 2.5,
        "thrust": 220.0,
        "fuel_flow": .0831,
        "isp_atm": 270.0,
        "asp_vac": 390.0,
    },
    4: {
        "name": "Mainsail",
        "mass": 6.0,
        "thrust": 1500.0,
        "fuel_flow": .5461,
        "isp_atm": 280.0,
        "asp_vac": 330.0,
    },
    5: {
        "name": "Atomic",
        "mass": 2.25,
        "thrust": 60.0,
        "fuel_flow": .0278,
        "isp_atm": 220.0,
        "asp_vac": 800.0,
    }
}


# Type is an integer which matches a rocket engine
def lookup_engine(engine_type):
    return engines[engine_type]


def random_engine():
    # Returns an engine type
    return random.randint(1, 20)
    # return random.randint(1, len(engines))


def random_fuel():
    # Measured in meters
    return random.randint(1, 20)


def rocket_height(rocket):
    pass


# Takes a 2-dimension array and puts it into a csv file
def save_csv(table, outputfile):
    with open(outputfile, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in table:
            writer.writerow(row)
