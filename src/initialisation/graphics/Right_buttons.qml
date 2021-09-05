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
        text: "Général"

        defaultX: 580
        defaultY: 15
        defaultHeight: 50
        defaultWidth: 60

        isActivable: true
        isPositive: true
        isVisible: true
    }

    //Bouton rb2
    DMI_button{
        id: rb2
        objectName: "rb2"
        text: "Train"

        defaultX: 580
        defaultY: 65
        defaultHeight: 50
        defaultWidth: 60

        isActivable: true
        isPositive: true
        isVisible: true
    }

    //Bouton rb3
    DMI_button{
        id: rb3
        objectName: "rb3"
        text: "Trajet"

        defaultX: 580
        defaultY: 115
        defaultHeight: 50
        defaultWidth: 60

        isActivable: true
        isPositive: true
        isVisible: true
    }

    //Bouton rb4
    DMI_button{
        id: rb4
        objectName: "rb4"
        text: "Ecrans"

        defaultX: 580
        defaultY: 165
        defaultHeight: 50
        defaultWidth: 60

        isActivable: true
        isPositive: true
        isVisible: true
    }

    //Bouton rb5
    DMI_button{
        id: rb5
        objectName: "rb5"
        text: ""

        defaultX: 580
        defaultY: 215
        defaultHeight: 50
        defaultWidth: 60

        isActivable: true
        isPositive: true
        isVisible: true
    }

    //Bouton rb6
    DMI_button{
        id: rb6
        objectName: "rb6"
        text: ""

        defaultX: 580
        defaultY: 265
        defaultHeight: 50
        defaultWidth: 60

        isActivable: true
        isPositive: true
        isVisible: true
    }

    //Bouton rb7
    DMI_button{
        id: rb7
        objectName: "rb7"
        text: ""

        defaultX: 580
        defaultY: 315
        defaultHeight: 50
        defaultWidth: 60

        isActivable: true
        isPositive: true
        isVisible: true
    }

    //Bouton rb8
    DMI_button{
        id: rb8
        objectName: "rb8"
        text: ""

        defaultX: 580
        defaultY: 365
        defaultHeight: 50
        defaultWidth: 60

        isActivable: true
        isPositive: true
        isVisible: true
    }
}
