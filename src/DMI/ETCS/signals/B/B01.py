import time


class B01:
    # variables nécessaire au bon fonctionnement de la page
    simulation = None
    section = "B"
    page_name = "B01"
    engine = None
    page = None


    # séries de tests suivant la documentation DMI (pour s'assurer que les différents modules fonctionne bien
    tests = [[400, "FS", "CSM", "NoS", 25, -1, 160, 138],
             [400, "FS", "CSM", "NoS", 25, -1, 160, 67],
             [400, "FS", "CSM", "Nos", 25, -1, 100, 67],
             [400, "FS", "TSM", "Inds", 25, 100, 150, 138],
             [400, "FS", "TSM", "IndS", 25, 100, 140, 109],
             [400, "FS", "TSM", "IndS", 30, 0, 78, 67],
             [400, "FS", "TSM", "WaS", 30, 0, 52, 67],
             [400, "FS", "TSM", "Ints", 30, 0, 39, 61],
             [400, "FS", "RSM", 'IndS', 30, 0, 14, 25],
             [400, "FS", "TSM", "IndS", 25, 0, 140, 133],
             [400, "FS", "CSM", "NoS", 25, -1, 140, 133],
             [250, "FS", "CSM", "NoS", 25, -1, 140, 133],
             [180, "FS", "CSM", "NoS", 25, -1, 140, 133],
             [140, "FS", "CSM", "NoS", 25, -1, 100, 96],
             [400, "FS", "CSM", "NoS", 25, -1, 140, 133],
             [400, "FS", "TSM", "OvS", 30, 40, 132, 143],
             [400, "FS", "CSM", "NoS", 30, 60, 140, 133],
             [400, "OS", "CSM", "noS", 30, -1, 40, 36],
             [400, "OS", "TSM", "IndS", 30, 0, 40, 36],
             [400, "SR", "TSM", "IndS", 30, 90, 117, 102],
             [400, "FS", "RSM", "IndS", 25, 0, 52, 28],
             [400, "FS", "RSM", "IndS", 25, 0, 12, 19]]

    def __init__(self, simulation, engine, folder, file):
        self.simulation = simulation
        self.section = folder
        self.page_name = file
        self.engine = engine
        self.page = engine.rootObjects()[0]

    def run(self):
        print("nothing")


    def update(self):
        for test in self.tests:
            self.page.setProperty("max_speed", test[0])
            self.page.setProperty("operating_mode", test[1])
            self.page.setProperty("speed_monitoring", test[2])
            self.page.setProperty("status_information", test[3])
            self.page.setProperty("release_speed", test[4])
            self.page.setProperty("target_speed", test[5])
            self.page.setProperty("permitted_speed", test[6])
            self.page.setProperty("speed", test[7])
            time.sleep(0.250)


