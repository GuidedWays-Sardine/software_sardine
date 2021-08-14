import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

import "page_rb5"
import "../../../DMI_default"

Pane {
    id: page_rb5
    objectName: "page_rb5"
    anchors.fill: parent

    //définit les bordures à 0
    topPadding: 0
    rightPadding: 0
    bottomPadding: 0
    leftPadding: 0


    background: Rectangle {
        color: "transparent"
    }

    //checkbutton pour savoir si l'application doit éteindre les écrans qui ne sont pas utilisés
    DMI_checkbutton {
        defaultX: 15
        defaultY: 380
        box_lenght: 20
        text: "Eteindre les écrans qui ne sont pas utilisés"

        isActivable: true
        isPositive: false
        isActivated: true
    }

    //paramètres pour l'écran 1
    Screen_Parameters_Item {
        defaultX: 15
        defaultY: 15
    }

    //paramètres pour l'écran 2
    Screen_Parameters_Item {
        defaultX: 15
        defaultY: 59
    }

    //paramètres pour l'écran 3
    Screen_Parameters_Item {
        defaultX: 15
        defaultY: 103
    }

    //paramètres pour l'écran 4
    Screen_Parameters_Item {
        defaultX: 15
        defaultY: 147
    }

    //paramètres pour l'écran 5
    Screen_Parameters_Item {
        defaultX: 15
        defaultY: 191
    }

    //paramètres pour l'écran 6
    Screen_Parameters_Item {
        defaultX: 15
        defaultY: 235
    }

    //paramètres pour l'écran 7
    Screen_Parameters_Item {
        defaultX: 15
        defaultY: 279
    }

    //paramètres pour l'écran 8
    Screen_Parameters_Item {
        defaultX: 15
        defaultY: 323
    }

}