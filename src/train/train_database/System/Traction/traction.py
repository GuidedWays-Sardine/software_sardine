# Librairies par défaut python
# Librairies par défaut python
import sys
import os



# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src\\")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))


class Bogie:

    axle_count = 0
    axle_power = 0
    motor_position = []
    state = []
    ignitable = []
    linked_coaches = []
    power = []
    type = None
    bogie_mass = 0

    def __init__(self):
        self.axle_count = 0
        self.axle_power = 0
        self.motor_position = None
        self.state = None
        self.ignitable = None
        self.linked_coaches = None
        self.power = None
        self.type = None
        self.bogie_mass = 0










