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

        default_x: 0
        default_y: 415
        default_height: 50
        default_width: 120

        is_activable: true
        is_positive: true
        is_visible: true
    }


    //Bouton ouvrir
    DMI_button{
        id: open
        objectName: "open"
        text: "Ouvrir"

        default_x: 280
        default_y: 415
        default_height: 50
        default_width: 120

        is_activable: true
        is_positive: true
        is_visible: true
    }

    //Bouton sauvegarder
    DMI_button{
        id: save
        objectName: "save"
        text: "Sauvegarder"

        default_x: 400
        default_y: 415
        default_height: 50
        default_width: 120

        is_activable: true
        is_positive: true
        is_visible: true
    }

    //Bouton lancer
    DMI_button{
        id: launch
        objectName: "launch"
        text: "Lancer"

        default_x: 520
        default_y: 415
        default_height: 50
        default_width: 120

        is_activable: true
        is_positive: true
        is_visible: true
    }
}