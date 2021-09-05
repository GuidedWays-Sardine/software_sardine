import QtQuick 2.0
import "../../DMI_default/ETCS_3.6.0"

Item {
    id: bottom_buttons
    objectName: "bottom_buttons"
    anchors.fill: parent

    //Bouton quitter
    DMI_button{
        id: quit
        objectName: "quit"
        text: "Quitter"

        defaultX: 0
        defaultY: 415
        defaultHeight: 50
        defaultWidth: 120

        isActivable: true
        isPositive: true
        isVisible: true
    }


    //Bouton ouvrir
    DMI_button{
        id: open
        objectName: "open"
        text: "Ouvrir"

        defaultX: 280
        defaultY: 415
        defaultHeight: 50
        defaultWidth: 120

        isActivable: true
        isPositive: true
        isVisible: true
    }

    //Bouton sauvegarder
    DMI_button{
        id: save
        objectName: "save"
        text: "Sauvegarder"

        defaultX: 400
        defaultY: 415
        defaultHeight: 50
        defaultWidth: 120

        isActivable: true
        isPositive: true
        isVisible: true
    }

    //Bouton lancer
    DMI_button{
        id: launch
        objectName: "launch"
        text: "Lancer"

        defaultX: 520
        defaultY: 415
        defaultHeight: 50
        defaultWidth: 120

        isActivable: true
        isPositive: true
        isVisible: true
    }
}