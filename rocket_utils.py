"""
    This module hold information relating to rocket engine types as well as
    functions to calculate rocket height, speed, etc
"""
import random
import csv
from math import log

GRAVITY = 9.81

# weight: [full, empty]
fuel_tank = [1.125, .125]
FULL = 0
DRY = 1

engines = {
    1: {
        "name": "LV-T30",
        "mass": 1.25,
        "thrust": 215.0,
        "fuel_flow": .0685,
        "isp_atm": 320.0,
        "isp_vac": 370,
    },
    2: {
        "name": "LV-909",
        "mass": .5,
        "thrust": 50.0,
        "fuel_flow": .0170,
        "isp_atm": 300.0,
        "isp_vac": 390.0,
    },
    3: {
        "name": "Poodle",
        "mass": 2.5,
        "thrust": 220.0,
        "fuel_flow": .0831,
        "isp_atm": 270.0,
        "isp_vac": 390.0,
    },
    4: {
        "name": "Mainsail",
        "mass": 6.0,
        "thrust": 1500.0,
        "fuel_flow": .5461,
        "isp_atm": 280.0,
        "isp_vac": 330.0,
    },
    5: {
        "name": "Atomic",
        "mass": 2.25,
        "thrust": 60.0,
        "fuel_flow": .0278,
        "isp_atm": 220.0,
        "isp_vac": 800.0,
    }
}


# Type is an integer which matches a rocket engine
def lookup_engine(engine_type):
    return engines[engine_type]


def random_engine():
    # Returns an engine type
    # return random.randint(1, 20)
    return random.randint(1, len(engines)-1)


def random_fuel():
    # Measured in meters
    return random.randint(1, 2000)


def rocket_height(rocket):
    pass


# Takes a 2-dimension array and puts it into a csv file
def save_csv(table, outputfile):
    with open(outputfile, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in table:
            writer.writerow(row)


def calc_total_deltav(rocket):
    #  dv = 9.81 * isp * ln(total_mass/dry_mass)

    # Holds dv for each stage. Stage 0 is the bottom stage
    stage_dv = []
    # e.g. 3 stages: from 0 to 2
    for stage in range(0, len(rocket) / 2):
        deltav = calc_stage_deltav(rocket, stage)
        stage_dv.append(deltav)
        # print("Stage: {}, delta v: {}".format(stage, deltav))
    return sum(stage_dv)


def calc_stage_deltav(rocket, stage):
    #  dv = 9.81 * isp * ln(total_mass/dry_mass)
    rocket_type = rocket[stage * 2]
    fuel_size = rocket[stage * 2 + 1]
    isp = lookup_engine(rocket_type)['isp_vac']
    full_mass = 0

    full_mass = remaining_mass(rocket, stage)

    dry_mass = full_mass - (fuel_size * (fuel_tank[FULL] - fuel_tank[DRY]))

    return GRAVITY * isp * log(full_mass/dry_mass)


# Full mass of this stage plus mass of stages above it
def remaining_mass(rocket, stage):
    mass = 0
    for stage_index in range(stage, len(rocket) / 2):
        rocket_type = rocket[stage_index * 2]
        fuel_size = rocket[stage_index * 2 + 1]
        engine_mass = lookup_engine(rocket_type)['mass']
        mass += engine_mass + (fuel_size * fuel_tank[FULL])

    return mass
