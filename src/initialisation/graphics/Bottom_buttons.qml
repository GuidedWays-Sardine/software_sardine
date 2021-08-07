import QtQuick 2.0
import "../../DMI_default"

Item {
    id: bottom_buttons
    objectName: "bottom_buttons"
    anchors.fill: parent

    //Bouton quitter
    DMI_button{
        id: quitter
        objectName: "quitter"
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
        id: ouvrir
        objectName: "ouvrir"
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
        id: sauvegarder
        objectName: "sauvegarder"
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
        id: lancer
        objectName: "lancer"
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