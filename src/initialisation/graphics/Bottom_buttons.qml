import QtQuick 2.0

import "../../DMI_default/ETCS"


Item {
    id: bottom_buttons
    objectName: "bottom_buttons"

    anchors.fill: parent



    //Bouton quitter
    DMI_button{
        id: quit
        objectName: "quit"

        default_x: 0
        default_y: 415
        default_height: 50
        default_width: 120

        text: "Quitter"

        is_activable: true
        is_positive: true
        is_visible: true
    }


    //Bouton ouvrir
    DMI_button{
        id: open
        objectName: "open"

        default_x: 280
        default_y: 415
        default_height: 50
        default_width: 120

        text: "Ouvrir"

        is_activable: true
        is_positive: true
        is_visible: true
    }

    //Bouton sauvegarder
    DMI_button{
        id: save
        objectName: "save"

        default_x: 400
        default_y: 415
        default_height: 50
        default_width: 120

        text: "Sauvegarder"

        is_activable: true
        is_positive: true
        is_visible: true
    }

    //Bouton lancer
    DMI_button{
        id: launch
        objectName: "launch"

        default_x: 520
        default_y: 415
        default_height: 50
        default_width: 120

        text: "Lancer"

        is_activable: true
        is_positive: true
        is_visible: true
    }
}