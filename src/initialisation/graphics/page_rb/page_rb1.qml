import QtQuick 2.0
import QtQuick.Controls 2.15
import "../../../DMI_default/ETCS_3.6.0"


DMI_page {
    id: page_rb1
    objectName: "page_rb1"


    //définit le ratio entre les dimensions de base de la fenètre et les dimensions de la fenètre actuelles
    readonly property real ratio:  (parent.width >= 640 && parent.height >= 480) ? parent.width/640 * (parent.width/640 < parent.height/480) + parent.height/480 * (parent.width/640 >= parent.height/480) : 1  //parent.height et parent.width représentent la taille de la fenêtre

    //Checkbutton pour savoir si le pupitre léger est connecté à UE (ou à Renard)
    DMI_checkbutton {
        id: pcc_checkbutton
        objectName: "pcc_checkbutton"

        boxLenght: 20
        defaultX: 55
        defaultY: 329

        text: "Activation du PCC ?"

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

        text: "Affichage en direct des donnés du train ?"

        isChecked: false
        isActivable: true
        isPositive: false
    }

    //Bouton registre
    Text{
        id: log_text
        objectName: "log_text"
        text: "Registre"
        color: "#C3C3C3"
        font.pixelSize: 12 * page_rb1.ratio

        anchors.left: log_button.left
        anchors.leftMargin: (1 + 2 * log_button.isPositive) * page_rb1.ratio
        anchors.bottom: log_button.top
        anchors.bottomMargin: log_text.font.pixelSize
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
    Text{
        id: language_text
        objectName: "language_text"
        text: "Langue"
        color: "#C3C3C3"
        font.pixelSize: 12 * page_rb1.ratio

        anchors.left: language_combo.left
        anchors.leftMargin: (1 + 2 * language_combo.isPositive) * page_rb1.ratio
        anchors.bottom: language_combo.top
        anchors.bottomMargin: language_text.font.pixelSize
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
    Text{
        id: dmi_text
        objectName: "dmi_text"
        text: "Interface pupitre"
        color: "#C3C3C3"
        font.pixelSize: 12 * page_rb1.ratio

        anchors.left: dmi_combo.left
        anchors.leftMargin: (1 + 2 * dmi_combo.isPositive) * page_rb1.ratio
        anchors.bottom: dmi_combo.top
        anchors.bottomMargin: dmi_text.font.pixelSize
    }

    DMI_combobox{
        id: dmi_combo
        objectName: "dmi_combo"

        defaultX: 54
        defaultY: 169
        defaultWidth: 280
        defaultHeight: 50

        elements: ["ETCS 3.6.0"]
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
    Text{
        id: command_board_text
        objectName: "command_board_text"
        text: "Pupitre"
        color: "#C3C3C3"
        font.pixelSize: 12 * page_rb1.ratio

        anchors.left: command_board_combo.left
        anchors.leftMargin: (1 + 2 * command_board_combo.isPositive) * page_rb1.ratio
        anchors.bottom: command_board_combo.top
        anchors.bottomMargin: command_board_text.font.pixelSize
    }

    DMI_combobox{
        id: command_board_combo
        objectName: "command_board_combo"

        defaultX: 54
        defaultY: 39
        defaultWidth: 280
        defaultHeight: 50

        elements: ["Pupitre lourd"]
        amountElementsDisplayed: 2

        isPositive: false
    }
}