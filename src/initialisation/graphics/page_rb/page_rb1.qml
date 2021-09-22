import QtQuick 2.0
import QtQuick.Controls 2.15
import "../../../DMI_default/ETCS_3.6.0"


DMI_page {
    id: page_rb1
    objectName: "page_rb1"



    //Checkbutton pour savoir si l'utilisateur veut un retour direct des donnés (courbe de vitesses, ...)
    DMI_checkbutton {
        id: data_check
        objectName: "data_check"

        box_length: 20
        default_x: 55
        default_y: 369

        text: "Affichage en direct des données du train ?"

        is_checked: false
        is_activable: true
        is_positive: false
    }

    //Checkbutton pour savoir si le pupitre léger est connecté à UE (ou à Renard)
    DMI_checkbutton {
        id: pcc_check
        objectName: "pcc_check"

        box_length: 20
        default_x: 55
        default_y: 329

        text: "Activation du PCC (Poste de Commande Centralisé) ?"

        is_checked: false
        is_activable: true
        is_positive: false
    }

    //Bouton registre
    DMI_text {
        id: log_text
        objectName: "log_text"

        text: "Niveau de registre"

        default_x: log_button.default_x + 2
        default_y: log_button.default_y - 2 * font_size
    }

    DMI_button{
        id: log_button
        objectName: "log_button"
        text: "Complet"

        default_x: 55
        default_y: 260
        default_height: 50
        default_width: 111

        is_activable: true
        is_positive: false
        is_visible: true
    }

    //Combobox langue
    DMI_text {
        objectName: "language_text"
        id: language_text

        text: "Langue"

        default_x: language_combo.default_x + 2
        default_y: language_combo.default_y - 2 * font_size

        is_dark_grey: language_combo.elements_count <= 1
    }

    DMI_combobox{
        id: language_combo
        objectName: "language_combo"
        elements: ["Français"]

        default_x: 54 + 111 + 58 - 1
        default_y: 260
        default_height: 50
        default_width: 111

        is_activable: true
        is_positive: false
        is_visible: true
    }

    //Combobox du choix du DMI
    DMI_text {
        id: dmi_text
        objectName: "dmi_text"

        text: "Interface pupitre"

        default_x: dmi_combo.default_x + 2
        default_y: dmi_combo.default_y - 2 * font_size

        is_dark_grey: dmi_combo.elements_count <= 1
    }

    DMI_combobox{
        id: dmi_combo
        objectName: "dmi_combo"

        default_x: 55 - 1
        default_y: 169
        default_width: 280
        default_height: 50

        elements: ["NaN"]
        elements_displayed: 2

        is_positive: false
    }

    //Checkbutton pour savoir si le pupitre léger est connecté à UE (ou à Renard)
    DMI_checkbutton {
        id: renard_check
        objectName: "renard_check"

        box_length: 20
        default_x: 55
        default_y: 104

        text: "Connecté à Renard ?"

        is_checked: false
        is_activable: true
        is_positive: false
    }

    //Checkbutton pour savoir si Renard est connecté via la caméra (ou via un visuel direct)
    DMI_checkbutton {
        id: camera_check
        objectName: "camera_check"

        box_length: 20
        default_x: 335
        default_y: 104

        text: "Connecté par une caméra ?"

        is_checked: false
        is_activable: true
        is_positive: false
    }

    //Combobox du pupitre utilisé
    DMI_text {
        id: command_board_text
        objectName: "command_board_text"

        text: "Pupitre"

        default_x: command_board_combo.default_x + 2
        default_y: command_board_combo.default_y - 2 * font_size

        is_dark_grey: command_board_combo.elements_count <= 1
    }

    DMI_combobox{
        id: command_board_combo
        objectName: "command_board_combo"

        default_x: 55 - 1
        default_y: 39
        default_width: 280
        default_height: 50

        elements: ["NaN"]
        elements_displayed: 2

        is_positive: false
    }
}