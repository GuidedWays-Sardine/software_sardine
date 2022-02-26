# Librairies par défaut python
import sys
import os

# Librairies SARDINE
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
sys.path.append(os.path.dirname(PROJECT_DIR))

import src.misc.log.log as log
import src.misc.settings_dictionary.settings as sd
import src.train.train_database.database as tdb
import src.train.train_database.Systems.frame.frame as frame
import src.train.train_database.Systems.electric.electric as electric
import src.train.train_database.Systems.traction.traction as traction
import src.train.train_database.Systems.braking.braking as braking



class Systems:
    """Classe permettant le fonctionnemetn des différents systèmes du train"""
    # Liste de tous les systèmes nécessaires au fonctionnement du train
    # Les systèmes sont initialisés plus bas pour éviter une copie (due à la mutabilité des classes et listes)
    frame = None
    electric = None
    traction = None
    braking = None

    def __init__(self, train_data):
        """Fonction permettant d'initialiser les systèmes du train, que ce soit en paramétrage simple ou complexe

        Parameters
        ----------
        train_data: `sd.SettingsDictionary`
            Tous les paramètres du train
        """
        # Commence par initialiser les différents systèmes en tant que liste
        # Les liste étant mutable, il est nécessaire de les créer à l'initialisation au risque
        # Feature: ajouter l'initialisation des futurs systèmes ici
        self.traction = traction.Traction()
        self.frame = frame.Frame()
        self.electric = electric.Electric()
        self.braking = braking.Braking(train_data)

        # Si le train a été paramétré de façon complexe, récupère les données sinon génère un train complex
        if train_data.get_value("mode", "Mode.SIMPLE").lower() == 'mode.complex':
            self.read_train(train_data)
        else:
            self.generate(train_data)

    def read_train(self, train_data):
        """Fonction permettant d'initialiser les systèmes grâce aux paramètres complexes

        Parameters
        ----------
        train_data: `sd.SettingsDictionary`
            Tous les paramètres du train
        """
        # Si le mauvais type d'initialisation a été appelé, appelle la fonction de génération de train
        if train_data.get_value("mode", "Mode.SIMPLE").lower() != 'mode.complex':
            self.generate(train_data)
            return

        # Commence par les voitures
        index = 0
        try:
            while f"railcar{index}.mission_type" in train_data:
                self.frame.add_railcar((tdb.MissionType[train_data[f"railcar{index}.mission_type"][12:]],
                                        tdb.Position[train_data[f"railcar{index}.position_type"][9:]],
                                        train_data[f"railcar{index}.position_type"],
                                        train_data[f"railcar{index}.levels"], train_data[f"railcar{index}.doors"],
                                        train_data[f"railcar{index}.Mtare"], train_data[f"railcar{index}.Mfull"],
                                        train_data[f"railcar{index}.length"],
                                        [train_data[f"railcar{index}.{leter}empty"] for leter in ["A", "B", "C"]],
                                        train_data[f"railcar{index}.multiply_mass_empty"],
                                        [train_data[f"railcar{index}.{leter}full"] for leter in ["A", "B", "C"]],
                                        train_data[f"railcar{index}.multiply_mass_full"]))
                index += 1
        except KeyError as error:
            log.warning(f"Impossible de charger la voiture {index}. Les paramètres de celle-ci sont incomplets",
                        exception=error)

        # Continue avec les bogies et leurs systèmes de freinage
        index = 0
        try:
            while f"bogie{index}.linked_railcars" in train_data:
                self.traction.add_bogie((None if train_data[f"bogie{index}.position_type"] is None else tdb.Position.MIDDLE#tdb.Position[train_data[f"bogie{index}.position_type"][9:]]
                                         ,
                                         train_data[f"bogie{index}.linked_railcars"],
                                         train_data[f"bogie{index}.axles_count"],
                                         None, train_data[f"bogie{index}.axles_power"]))

                # Récupère les paramètres de chacun des systèmes de freinages et ajoute le nombre de systèmes nécessaire
                brakes_parameters = [None if not train_data[f"bogie{index}.pad.count"] else
                                     (),  # TODO récupérer tous les paramètres du freinage par plaquette
                                     None if not train_data[f"bogie{index}.disk.count"] else
                                     (),  # TODO récupérer tous les paramètres du freinage par disque
                                     None if not train_data[f"bogie{index}.magnetic.count"] else
                                     (),  # TODO récupérer tous les paramètres du freinage par patins magnétiques
                                     None if not train_data[f"bogie{index}.foucault.count"] else
                                     (),  # TODO récupérer tous les paramètres du freinage par courant de foucault,
                                    ]
                self.braking.modify_brakes_count(self.traction.bogies[-1],
                                                 [train_data[f"bogie{index}.{brake}.count"] for brake in ["pad", "disk", "magnetic", "foucault"]],
                                                 brakes_parameters)
                index += 1
        except KeyError as error:
            log.warning(f"Impossible de charger le bogie {index}. Les paramètres de celle-ci sont incomplets",
                        exception=error)

        # TODO : ajouter la lecture des autres systèmes (électriques, freinage...)

    def generate(self, train_data):
        """Fonction permettant d'initialiser les systèmes d'un train grâce aux paramètres simples
        Certaines conditions seront prises en comptes :
        - Les bogies classiques seront mis de préférence à l'avant et à l'arrière du train
        - Les bogies articulés seront mis de préférence en milieu de train
        - Le train sera considéré comme une unité simple (qui pourra être coupée lors de la simulation si besoins)
        - Les essieux moteurs seront mis de préférence à l'avant et à l'arrière du train
        - Les systèmes de freinages semelles et disques seront mis de préférence au centre du train
        - Les systèmes de freinage magnétiques seront mis de préférence à l'avant du train
        - Les systèmes de freinages de foucault seront mis de préférence à l'arrière du train

        Parameters
        ----------
        train_data: `sd.SettingsDictionary`
            Tous les paramètres du train

        Raises
        ------
        KeyError
            Soulevé dans le cas où un paramètre nécessaire manque au dictionnaire de paramètres train
        """
        # Chaque ligne sera détaillée car les conversions entre les données paramétrées et celles du train généré
        # diffèrent énormément. De nombreuses conversions sont nécessaires

        # Récupère le nombre moyen d'essieux (pour savoir si des essieux articulés devront être placés)
        # average_bogies_count < 2  -> rame articulée      -> bogies jacobiens       -> aucun bogie central
        # average_bogies_count = 2  -> rame non articulée  -> aucun bogie jacobiens  -> aucun bogie central
        # average_bogies_count > 2  -> rame non articulée  -> aucun bogie jacobiens  -> bogies centraux
        average_bogies_count = train_data["bogies_count"] / train_data["railcars_count"]

        # Récupère le nombre moyen de chacun des systèmes de freinages, ainsi que du supplément de ces systèmes
        # Les systèmes de freinages supplémentaires seront mis vers le centre du train (à l'inverse des systèmes motorisés)
        average_brakes = [int(train_data[f"{b_s}_brakes_count"] / train_data["bogies_count"]) for b_s in ["pad", "disk", "magnetic", "foucault"]]
        bonus_brakes = [train_data[f"{b_s}_brakes_count"] - (average_brakes[i] * train_data["bogies_count"]) for i, b_s in enumerate(["pad", "disk", "magnetic", "foucault"])]

        # Récupère les paramètres nécessaires pour chacun des systèmes de freinage
        # Ces informations proviennent de la popup de freinage et sont enregistrés dans train_data
        brakes_parameters = [None,
                             None,
                             None,
                             None]  # TODO : Trouver la liste des paramètres à récupérer dans train_data

        # Récupère le nombre de bogies supplémentaires à rajouter à l'avant et à l'arrière (extérieurs priorisé)
        # Si impaire (rame assymétrique), le bogie supplémentaire sera mis à l'avant du train (d'où le +1)
        # average_bogies_count < 2   -> nombre de rames non articulés de chaque côté
        # average_bogies_count > 2   -> nombre de rames avec un bogie central supplémentaire
        if average_bogies_count <= 2:
            front_bonus_bogies = int(((train_data["bogies_count"] - (train_data["railcars_count"] + 1)) + 1) / 2.0)
            back_bonus_bogies = int((train_data["bogies_count"] - (train_data["railcars_count"] + 1)) / 2.0)
        else:
            front_bonus_bogies = int((train_data["bogies_count"] - int(average_bogies_count) * train_data["railcars_count"] + 1) / 2.0)
            back_bonus_bogies = int((train_data["bogies_count"] - int(average_bogies_count) * train_data["railcars_count"]) / 2.0)

        # Vérifie que le train n'a pas un taux de motorisation > à 100% (minimum entre essieux moteurs et essieux)
        motorized_count = min(train_data["motorized_axles_count"], train_data["bogies_count"] * train_data["axles_per_bogie"])

        # Récupère le nombre d'essieux moteurs à mettre de chaque à l'avant et à l'arrière (extérieurs priorisés)
        # Si impaire (rame assymétrique), l'essieu moteur supplémentaire sera mis à l'avant du trai (d'où le +1)
        front_motorized_axles = int((motorized_count + 1) / 2.0)
        back_motorized_axles = int(motorized_count / 2.0)

        # Récupère la masse des essieux moteurs et des essieux porteurs
        # Attention! cette masse ne sera pas précisément respectée si la structure générée ne le permet pas physiquement
        # Si un bogie d'essieux moteurs se trouvent entre deux voitures non entièrement motorisés
        # Si une voiture non articulé n'a pas tous ces essieux moteurs
        motorized_axle_weight = train_data["motorized_axle_weight"]
        carrying_axle_weight = (train_data["weight"] - motorized_axle_weight * train_data["motorized_axles_count"]) / \
                               (train_data["bogies_count"] * train_data["axles_per_bogie"] - train_data["motorized_axles_count"])

        # Initialise les variables permettant de garder en mémoire le nombre d'essieux déjà initialisés
        previous_bogies_count = 0
        next_bogies_count = train_data["bogies_count"]

        # stocke dans une varible temporaire la mission générale du train (pour simplifier sa lecture
        general_mission = tdb.MissionType[str(train_data.get_value("mission", "MissionType.PASSENGER"))[12:]]

        # Passe par chacune des voitures du train
        for car_index in range(train_data["railcars_count"]):
            # Commence par déterminer si l'essieu précédent et l'essieu suivant sont articulés
            previous_articulated = car_index > 0 and any(self.traction.get_bogies(car_index, tdb.Position.FRONT))
            next_articulated = average_bogies_count < 2 and (front_bonus_bogies <= car_index < train_data["railcars_count"] - back_bonus_bogies - 1)

            # Détermine le nombre d'essieux centraux à ajoutés (valable que si average_bogies_count > 2)
            middle_bogies_count = (int(average_bogies_count - 2) + (front_bonus_bogies > car_index or car_index > (train_data["railcars_count"] - back_bonus_bogies - 1))
                                    if average_bogies_count > 2 else 0)

            # Compte le nombre de bogies à rajouter (ne compte pas le bogie articulé précédent mais compte le suivant)
            new_bogies_count = ((not previous_articulated) + middle_bogies_count + 1)
            next_bogies_count -= new_bogies_count

            # Récupère le nombre d'essieux motorisés qui seront rajoutés. Le nombre d'essieux moteurs dépendra de :
            # S'il y a moins d'essieux avant (previous_axles_count) que d'essieux avant moteurs (front_motorized_axles)
            # S'il y a moins d'essieux après (next_axles_count) que d'essieux arrières moteurs (back_motorized_axles)
            new_motorized_count = 0
            if (previous_bogies_count * train_data["axles_per_bogie"]) < front_motorized_axles:
                new_motorized_count += min(front_motorized_axles - previous_bogies_count  * train_data["axles_per_bogie"],
                                           new_bogies_count * train_data["axles_per_bogie"])
            if (next_bogies_count * train_data["axles_per_bogie"]) < back_motorized_axles:
                new_motorized_count += min(back_motorized_axles - next_bogies_count * train_data["axles_per_bogie"],
                                           new_bogies_count * train_data["axles_per_bogie"] - new_motorized_count)

            # Récupère le nombre d'essieux à rajouter sur les diffrents bogies du train
            # 0 s'il est articulé (d'où le not previous articulated)
            front_axles_motorized_count = min(new_motorized_count, train_data["axles_per_bogie"] * (not previous_articulated))
            # Motorisation prioritaire sur les essieux avant et arrière
            back_axles_motorized_count = min(new_motorized_count - front_axles_motorized_count, train_data["axles_per_bogie"])
            # Génère une liste avec les bogies centraux
            # min pour éviter d'avoir plus d'essieux moteurs que d'essieux(axles_per_bogie si trop d'essieu à motoriser)
            # max pour éviter d'aviur un nombre d'essieux moteurs négatifs(0 si min retourne une valeur négative)
            remain_motorized = new_motorized_count - front_axles_motorized_count - back_axles_motorized_count
            middle_axles_motorized_count = [max(min(remain_motorized - c_m_c * train_data["axles_per_bogie"], train_data["axles_per_bogie"]), 0)
                                             for c_m_c in range(middle_bogies_count)]

            # Maintenant s'occupe de calculer la masse de la voiture (bogie avant -> bogies centraux -> bogie arrière)
            # Commence par le bogie avant et distingue deux cas s'il est articulé ou non
            if previous_articulated:
                # Récupère le bogie précédent, récupère sa masse et le divise par 2 car bogie articulé
                previous_bogie = self.traction.get_bogies(car_index - 1, tdb.Position.BACK)[0]
                railcar_weight = (previous_bogie.get_motorized_axles_count() * motorized_axle_weight +
                                  (train_data["axles_per_bogie"] - previous_bogie.get_motorized_axles_count()) * carrying_axle_weight) / 2
            else:
                # Sinon calcule simplement la masse du bogie (pas de division par 2 car bogie non articulé)
                railcar_weight = (front_axles_motorized_count * motorized_axle_weight +
                                  (train_data["axles_per_bogie"] - front_axles_motorized_count) * carrying_axle_weight)
            # Continue par les bogies centraux
            for c_m_a_c in middle_axles_motorized_count:
                # Pour chacun des bogies, rajoute la masse sur chacuns des essieux
                railcar_weight += (c_m_a_c * motorized_axle_weight +
                                   (train_data["axles_per_bogie"] - c_m_a_c) * carrying_axle_weight)
            # Fini par l'essieu arrière
            # Divise par 2 si l'essieu est articulé (1 + (1 si bogie articulé))
            railcar_weight += ((back_axles_motorized_count * motorized_axle_weight +
                                (train_data["axles_per_bogie"] - back_axles_motorized_count) * carrying_axle_weight) /
                               (1 + next_articulated))

            # Initialise pour chacun des bogies le nombre de systèmes de freinages à ajouter. Rappel :
            # - Les systèmes de freinages semelles et disques seront mis de préférence au centre du train
            # - Les systèmes de freinage magnétiques seront mis au maximum à l'avant du train
            # - Les systèmes de freinages de foucault seront mis au maximum à l'arrière du train
            front_brakes_count = ([0, 0, 0, 0]
                                  if previous_articulated else
                                  [average_brakes[0] + (int((train_data["bogies_count"] - bonus_brakes[0])/2) <=
                                                        previous_bogies_count <
                                                        int(train_data["bogies_count"] - (train_data["bogies_count"] - bonus_brakes[0])/2)),
                                   average_brakes[1] + (int((train_data["bogies_count"] - bonus_brakes[1]) / 2) <=
                                                        previous_bogies_count <
                                                        int(train_data["bogies_count"] - (train_data["bogies_count"] - bonus_brakes[1]) / 2)),
                                   average_brakes[2] + (bonus_brakes[2] > previous_bogies_count),
                                   average_brakes[3] + (train_data["bogies_count"] - (bonus_brakes[3]) <= previous_bogies_count)])

            middle_brakes_count = []
            for c_b in range(middle_bogies_count):
                middle_brakes_count.append([average_brakes[0] + (int((train_data["bogies_count"] - bonus_brakes[0])/2) <=
                                                                 (previous_bogies_count + (not previous_articulated) + c_b) <
                                                                 int(train_data["bogies_count"] - (train_data["bogies_count"] - bonus_brakes[0])/2)),
                                            average_brakes[1] + (int((train_data["bogies_count"] - bonus_brakes[1]) / 2) <=
                                                                 (previous_bogies_count + (not previous_articulated) + c_b) <
                                                                 int(train_data["bogies_count"] - (train_data["bogies_count"] - bonus_brakes[1]) / 2)),
                                            average_brakes[2] + (bonus_brakes[2] > (previous_bogies_count + (not previous_articulated) + c_b)),
                                            average_brakes[3] + (train_data["bogies_count"] - (bonus_brakes[3]) <= (previous_bogies_count + (not previous_articulated) + c_b))])

            back_brakes_count = ([average_brakes[0] + (int((train_data["bogies_count"] - bonus_brakes[0])/2) <=
                                                       (previous_bogies_count + (not previous_articulated) + middle_bogies_count) <
                                                       int(train_data["bogies_count"] - (train_data["bogies_count"] - bonus_brakes[0])/2)),
                                  average_brakes[1] + (int((train_data["bogies_count"] - bonus_brakes[1]) / 2) <=
                                                       (previous_bogies_count + (not previous_articulated) + middle_bogies_count) <
                                                       int(train_data["bogies_count"] - (train_data["bogies_count"] - bonus_brakes[1]) / 2)),
                                  average_brakes[2] + (bonus_brakes[2] > (previous_bogies_count + (not previous_articulated) + middle_bogies_count)),
                                  average_brakes[3] + (train_data["bogies_count"] - (bonus_brakes[3]) <= (previous_bogies_count + (not previous_articulated) + middle_bogies_count))])

            # Incrémente le nombre d'essieux déjà paramétrés par les nouveaux essieux
            previous_bogies_count += new_bogies_count

            # Ajoute les différents bogies maintenant que toutes les valeurs nécessaires ont été calculées
            # si le bogie avant n'est pas articulé (auquel cas il a été ajouté) le rajoute et ses systèmes de freinage
            if not previous_articulated:
                self.traction.add_bogie(traction.Bogie(position_type=tdb.Position.FRONT,
                                                       linked_railcars=car_index,
                                                       axles_count=train_data["axles_per_bogie"],
                                                       motorized_axles=front_axles_motorized_count,
                                                       axles_power=train_data["axles_power"]))
                self.braking.modify_brakes_count(self.traction.bogies[-1], front_brakes_count, brakes_parameters)

            # Ajoute les bogies centraux et leurs systèmes de freinages
            for c_b in range(middle_bogies_count):
                self.traction.add_bogie(traction.Bogie(position_type=tdb.Position.MIDDLE,
                                                       linked_railcars=car_index,
                                                       axles_count=train_data["axles_per_bogie"],
                                                       motorized_axles=middle_axles_motorized_count[c_b],
                                                       axles_power=train_data["axles_power"]))
                self.braking.modify_brakes_count(self.traction.bogies[-1], middle_brakes_count[c_b], brakes_parameters)

            # Ajoute le bogie arrière et ses systèmes de freinages
            self.traction.add_bogie(traction.Bogie(position_type=tdb.Position.BACK if not next_articulated else None,
                                                   linked_railcars=[car_index, car_index + 1] if next_articulated else car_index,
                                                   axles_count=train_data["axles_per_bogie"],
                                                   motorized_axles=back_axles_motorized_count,
                                                   axles_power=train_data["axles_power"]))
            self.braking.modify_brakes_count(self.traction.bogies[-1], back_brakes_count, brakes_parameters)

            # Ajoute la voiture paramétré ainsi que tous ses paramètres
            self.frame.add_railcar(frame.Railcar(mission_type=general_mission,
                                                 position_type=(tdb.Position.FRONT if car_index == 0 else
                                                                tdb.Position.BACK if car_index == (train_data["railcars_count"] - 1)
                                                                else tdb.Position.MIDDLE),
                                                 position_index=car_index,
                                                 levels=1 if general_mission != tdb.MissionType.FREIGHT else 0,
                                                 doors=2 if general_mission != tdb.MissionType.FREIGHT else 0,
                                                 Mtare=railcar_weight,
                                                 Mfull=railcar_weight,
                                                 length=train_data["length"] / train_data["railcars_count"],
                                                 ABCempty=[train_data["a"], train_data["b"], train_data["c"]],
                                                 multiply_mass_empty=False,
                                                 ABCfull=[train_data["a"], train_data["b"], train_data["c"]],
                                                 multiply_mass_full=False))

        # Appelle la fonction d'initialisation des systèmes électriques
        # TODO : initialiser le système électriques (pantographes etc...) et le pupitre

    def get_values(self):
        """Fonction permettant de récupérer tous les paramètres des systèmes du train.

        Returns: `sd.SettingsDictionary`
            Paramètres de tous les sous-systèmes du train
        """
        parameters = sd.SettingsDictionary()

        parameters.update(self.frame.get_values())
        parameters.update(self.traction.get_values(self.braking))   # S'occupe des systèmes de traction et de freinage

        return parameters
