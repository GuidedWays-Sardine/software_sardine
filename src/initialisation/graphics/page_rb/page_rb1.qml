import QtQuick 2.0
import QtQuick.Controls 2.15
import "../../../DMI_default"


DMI_page {
    id: page_rb1
    objectName: "page_rb1"


    //définit le ratio entre les dimensions de base de la fenètre et les dimensions de la fenètre actuelles
    readonly property real ratio:  (parent.width >= 640 && parent.height >= 480) ? parent.width/640 * (parent.width/640 < parent.height/480) + parent.height/480 * (parent.width/640 >= parent.height/480) : 1  //parent.height et parent.width représentent la taille de la fenêtre



    //Checkbutton pour savoir si le pupitre léger est connecté à UE (ou à Renard)
    DMI_checkbutton {
        id: renard_checkbutton
        objectName: "renard_checkbutton"

        boxLenght: 20
        defaultX: 55
        defaultY: 80

        text: "Connecté à Renard ?"

        isChecked: false
        isActivable: true
        isPositive: false
    }

    //Checkbutton pour savoir si le pupitre léger est connecté à UE (ou à Renard)
    DMI_checkbutton {
        id: pcc_checkbutton
        objectName: "pcc_checkbutton"

        boxLenght: 20
        defaultX: 55
        defaultY: 125

        text: "activation du PCC ?"

        isChecked: false
        isActivable: true
        isPositive: false
    }

    //Combobox du pupitre utilisé (pupitre léger ou lourd)
    DMI_combobox{
        id: command_board_combo
        objectName: "command_board_combo"

        defaultX: 54
        defaultY: 15
        defaultWidth: 280
        defaultHeight: 50

        elements: ["Pupitre lourd", "Pupitre léger"]
        amountElementsDisplayed: 2

        isPositive: false
    }

    //Bouton registre
    Text{
        id: log_text
        objectName: "log_text"
        text: "registre"
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

        defaultX: 54
        defaultY: 315
        defaultHeight: 50
        defaultWidth: 111

        isActivable: true
        isPositive: false
        isVisible: true
    }

    //Bouton langue
    Text{
        id: language_text
        objectName: "language_text"
        text: "langue"
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

        defaultX: 54 + 111 + 58
        defaultY: 315
        defaultHeight: 50
        defaultWidth: 111

        isActivable: true
        isPositive: false
        isVisible: true
    }
}