import QtQuick 2.0
import QtQuick.Controls 2.15
import "../../components"


Item {
    id: page_rb1
    objectName: "page_rb1"



    //Checkbutton pour savoir si l'utilisateur veut un retour direct des donnés (courbe de vitesses, ...)
    INI_checkbutton {
        id: data_check
        objectName: "data_check"

        default_x: 55
        default_y: 369
        box_length: 20

        title: "Affichage en direct des données ?"

        is_checked: false
        is_activable: true
        is_positive: false


        //Signal appelé lorsque la valeur du combobox change (par un clic ou par une commande)
        onValue_changed: {
            //Si les données en direct sont activés, active le dashboard par défaut (dashboard_check)
            //Si les données en direct sont désactivés, désactive le dashboard
            dashboard_check.is_checked = is_checked
        }
    }

    //Checkbutton pour savoir si l'utilisateur veut afficher les données avec le tableau de bord (sinon en fenêtré)
    INI_checkbutton {
        id: dashboard_check
        objectName: "dashboard_check"

        default_x: 335
        default_y: 369 - 15
        box_length: 20

        title: "Tableau de bord ?"

        is_checked: false
        is_activable: data_check.is_checked
        is_positive: false
    }

    //Checkbutton pour savoir si l'utilisateur veut sauvegarder les données de simulation
    INI_checkbutton {
        id: data_save_check
        objectName: "data_save_check"

        default_x: 335
        default_y: 369 + 15
        box_length: 20

        title: "sauvegarder les données ?"

        is_checked: false
        is_activable: true
        is_positive: false
    }

    //Checkbutton pour savoir si le pupitre léger est connecté à UE (ou à Renard)
    INI_checkbutton {
        id: ccs_check
        objectName: "ccs_check"

        default_x: 55
        default_y: 329
        box_length: 20

        title: "Activation du PCC (Poste de Commande Centralisé) ?"

        is_checked: false
        is_activable: true
        is_positive: false
    }

    //switchbutton registre
    INI_switchbutton{
        id: log_switchbutton
        objectName: "log_switchbutton"

        default_x: 55
        default_y: 260
        default_width: 111
        default_height: 50

        elements: ["Complet"]
        image_mode: false
        title: "Niveau de registre"

        is_activable: true
        is_positive: false
    }

    //Combobox langue
    INI_combobox{
        id: language_combo
        objectName: "language_combo"

        default_x: 54 + 111 + 58 - 1
        default_y: 260
        default_width: 111
        default_height: 50

        elements: ["Français"]
        title: "Langue"

        is_activable: true
        is_positive: false
    }

    //Combobox du choix du dmi
    INI_combobox{
        id: dmi_combo
        objectName: "dmi_combo"

        default_x: 55 - 1
        default_y: 169
        default_width: 280
        default_height: 50

        elements: ["NaN"]
        elements_displayed: 2
        title: "Interface pupitre"

        is_positive: false
    }

    //Checkbutton pour savoir si le pupitre léger est connecté à UE (ou à Renard)
    INI_checkbutton {
        id: renard_check
        objectName: "renard_check"

        default_x: 55
        default_y: 104
        box_length: 20

        title: "Connecté à Renard ?"

        is_checked: false
        is_activable: true
        is_positive: false


        //Signal appelé lorsque la valeur du combobox change (par un clic ou par une commande)
        onValue_changed: {
            //Si le simulateur n'est pas connecté à Renard (pas coché) enlève la caméra
            if(!is_checked) {
                camera_check.is_checked = false
            }
        }
    }

    //Checkbutton pour savoir si Renard est connecté via la caméra (ou via un visuel direct)
    INI_checkbutton {
        id: camera_check
        objectName: "camera_check"

        default_x: 335
        default_y: 104
        box_length: 20

        title: "Connecté par une caméra ?"

        is_checked: false
        is_activable: renard_check.is_checked
        is_positive: false
    }

    //Combobox du pupitre utilisé
    INI_combobox{
        id: command_board_combo
        objectName: "command_board_combo"

        default_x: 55 - 1
        default_y: 39
        default_width: 280
        default_height: 50

        elements: ["NaN"]
        elements_displayed: 2
        title: "Pupitre"

        is_positive: false
        is_activable: true
    }
}
