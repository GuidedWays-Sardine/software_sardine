import logging


from PyQt5.QtWidgets import QDesktopWidget

import DMI.ETCS.driver_machine_interface as DMI



class Simulation:
    """Classe utile à l'initialisation et au lancement de la simulation"""
    running = True

    central_dmi = None

    def __init__(self, data):

        self.central_dmi = DMI.DriverMachineInterface(data)
