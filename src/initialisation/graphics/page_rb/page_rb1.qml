import QtQuick 2.0
import QtQuick.Controls 2.15
import "../../../DMI_default/ETCS_3.6.0"


DMI_page {
    id: page_rb1
    objectName: "page_rb1"


    //Checkbutton pour savoir si le pupitre léger est connecté à UE (ou à Renard)
    DMI_checkbutton {
        id: pcc_checkbutton
        objectName: "pcc_checkbutton"

        boxLenght: 20
        defaultX: 55
        defaultY: 329

        text: "Activation du PCC (Poste de Commande Centralisé) ?"

        isChecked: false
        isActivable: true
        isPositive: false
    }

    //Checkbutton pour savoir si l'utilisateur veut un retour direct des donnés (courbe de vitesses, ...)
    DMI_checkbutton {
        id: data_checkbutton
        objectName: "data_checkbutton"

        boxLenght: 20
        defaultX: 55
        defaultY: 369

        text: "Affichage en direct des données du train ?"

        isChecked: false
        isActivable: true
        isPositive: false
    }

    //Bouton registre
    DMI_text {
        id: log_text
        objectName: "log_text"

        text: "Niveau de registre"

        defaultX: log_button.defaultX + 2
        defaultY: log_button.defaultY - 2 * fontSize
    }

    DMI_button{
        id: log_button
        objectName: "log_button"
        text: "Complet"

        defaultX: 50
        defaultY: 260
        defaultHeight: 50
        defaultWidth: 111

        isActivable: true
        isPositive: false
        isVisible: true
    }

    //Combobox langue
    DMI_text {
        objectName: "language_text"
        id: language_text

        text: "Langue"

        defaultX: language_combo.defaultX + 2
        defaultY: language_combo.defaultY - 2 * fontSize

        isDarkGrey: language_combo.elementsCount <= 1
    }

    DMI_combobox{
        id: language_combo
        objectName: "language_combo"
        elements: ["Français"]

        defaultX: 223
        defaultY: 260
        defaultHeight: 50
        defaultWidth: 111

        isActivable: true
        isPositive: false
        isVisible: true
    }

    //Combobox du choix du DMI
    DMI_text {
        id: dmi_text
        objectName: "dmi_text"

        text: "Interface pupitre"

        defaultX: dmi_combo.defaultX + 2
        defaultY: dmi_combo.defaultY - 2 * fontSize

        isDarkGrey: dmi_combo.elementsCount <= 1
    }

    DMI_combobox{
        id: dmi_combo
        objectName: "dmi_combo"

        defaultX: 54
        defaultY: 169
        defaultWidth: 280
        defaultHeight: 50

        elements: ["NaN"]
        amountElementsDisplayed: 2

        isPositive: false
    }

    //Checkbutton pour savoir si le pupitre léger est connecté à UE (ou à Renard)
    DMI_checkbutton {
        id: renard_checkbutton
        objectName: "renard_checkbutton"

        boxLenght: 20
        defaultX: 55
        defaultY: 104

        text: "Connecté à Renard ?"

        isChecked: false
        isActivable: true
        isPositive: false
    }

    //Checkbutton pour savoir si Renard est connecté via la caméra (ou via un visuel direct)
    DMI_checkbutton {
        id: camera_checkbutton
        objectName: "camera_checkbutton"

        boxLenght: 20
        defaultX: 335
        defaultY: 104

        text: "Connecté par une caméra ?"

        isChecked: false
        isActivable: true
        isPositive: false
    }

    //Combobox du pupitre utilisé
    DMI_text {
        id: command_board_text
        objectName: "command_board_text"

        text: "Pupitre"

        defaultX: command_board_combo.defaultX + 2
        defaultY: command_board_combo.defaultY - 2 * fontSize

        isDarkGrey: command_board_combo.elementsCount <= 1
    }

    DMI_combobox{
        id: command_board_combo
        objectName: "command_board_combo"

        defaultX: 54
        defaultY: 39
        defaultWidth: 280
        defaultHeight: 50

        elements: ["NaN"]
        amountElementsDisplayed: 2

        isPositive: false
    }
}