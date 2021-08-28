import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

import "page_rb5"
import "../../../DMI_default"


DMI_page{
    id: page_rb5
    objectName: "page_rb5"

    //checkbutton pour savoir si l'application doit éteindre les écrans qui ne sont pas utilisés
    DMI_checkbutton {
        id: test
        objectName: "test"

        defaultX: 15
        defaultY: 380
        boxLenght: 20
        text: "Eteindre les écrans qui ne sont pas utilisés"

        isActivable: true
        isPositive: false
        isActivated: true
    }

    //paramètres pour l'écran 1
    Screen_Parameters_Item {
        id: screen_parameter1
        objectName: "screen_parameter1"
        defaultX: 15
        defaultY: 15
    }

    //paramètres pour l'écran 2
    Screen_Parameters_Item {
        id: screen_parameter2
        objectName: "screen_parameter2"
        defaultX: 15
        defaultY: 59
    }

    //paramètres pour l'écran 3
    Screen_Parameters_Item {
        id: screen_parameter3
        objectName: "screen_parameter3"
        defaultX: 15
        defaultY: 103
    }

    //paramètres pour l'écran 4
    Screen_Parameters_Item {
        id: screen_parameter4
        objectName: "screen_parameter4"
        defaultX: 15
        defaultY: 147
    }

    //paramètres pour l'écran 5
    Screen_Parameters_Item {
        id: screen_parameter5
        objectName: "screen_parameter5"
        defaultX: 15
        defaultY: 191
    }

    //paramètres pour l'écran 6
    Screen_Parameters_Item {
        id: screen_parameter6
        objectName: "screen_parameter6"
        defaultX: 15
        defaultY: 235
    }

    //paramètres pour l'écran 7
    Screen_Parameters_Item {
        id: screen_parameter7
        objectName: "screen_parameter7"
        defaultX: 15
        defaultY: 279
    }

    //paramètres pour l'écran 8
    Screen_Parameters_Item {
        id: screen_parameter8
        objectName: "screen_parameter8"
        defaultX: 15
        defaultY: 323
    }

}