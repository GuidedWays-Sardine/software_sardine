import QtQuick 2.0

import "../../DMI_default/ETCS_3.6.0"


Item {
    id: right_buttons
    objectName: "right_buttons"

    anchors.fill: parent



    //Bouton rb1
    DMI_button{
        id: rb1
        objectName: "rb1"

        default_x: 580
        default_y: 15
        default_height: 50
        default_width: 60

        is_activable: true
        is_positive: true
        is_visible: true
    }

    //Bouton rb2
    DMI_button{
        id: rb2
        objectName: "rb2"

        default_x: 580
        default_y: 65
        default_height: 50
        default_width: 60

        is_activable: true
        is_positive: true
        is_visible: true
    }

    //Bouton rb3
    DMI_button{
        id: rb3
        objectName: "rb3"

        default_x: 580
        default_y: 115
        default_height: 50
        default_width: 60

        is_activable: true
        is_positive: true
        is_visible: true
    }

    //Bouton rb4
    DMI_button{
        id: rb4
        objectName: "rb4"

        default_x: 580
        default_y: 165
        default_height: 50
        default_width: 60

        is_activable: true
        is_positive: true
        is_visible: true
    }

    //Bouton rb5
    DMI_button{
        id: rb5
        objectName: "rb5"

        default_x: 580
        default_y: 215
        default_height: 50
        default_width: 60

        is_activable: true
        is_positive: true
        is_visible: true
    }

    //Bouton rb6
    DMI_button{
        id: rb6
        objectName: "rb6"

        default_x: 580
        default_y: 265
        default_height: 50
        default_width: 60

        is_activable: true
        is_positive: true
        is_visible: true
    }

    //Bouton rb7
    DMI_button{
        id: rb7
        objectName: "rb7"

        default_x: 580
        default_y: 315
        default_height: 50
        default_width: 60

        is_activable: true
        is_positive: true
        is_visible: true
    }

    //Bouton rb8
    DMI_button{
        id: rb8
        objectName: "rb8"

        default_x: 580
        default_y: 365
        default_height: 50
        default_width: 60

        is_activable: true
        is_positive: true
        is_visible: true
    }
}
