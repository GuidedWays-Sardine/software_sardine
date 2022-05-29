// For testing reasons, this test file must integrate composants from the initialisation module.
// This doesn't create any issues on the rest of the simulator as it is a test module.
import QtQuick 2.15
import QtQuick.Window 2.2
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.3
import QtQml 2.15

import "../../initialisation/components"

Window {
    id: window
    width: 640
    height: 480
    visible: true

    color: "#031122"


    // Mouse area de fond permettant de récupérer le focus quand le fond est cliqué
    MouseArea {
        id: area

        anchors.fill: parent

        onClicked: {
            area.forceActiveFocus()
        }
    }

    // Signal permettant de fermer l'application lorsque la fenêtre est fermée
    signal closed()
    onVisibilityChanged: {
        if(!window.visible) {
            closed()
        }
    }


    // Floatinput pour tester : le numpad ; la désactivation du - pour les valeurs positives
    INI_floatinput {
        id: test_float
        objectName: "test_float"

        default_x: 300
        default_y: 250
        default_width: 100
        default_height: 40

        minimum_value: 0.0
        maximum_value: 101.36

        conversion_list: [["A", 1, 0], ["B", 1, -15]]
    }

    // Integerinput pour tester : le numpad ; la désactivation du . ; la désactivation du - pour les valeurs positives
    INI_integerinput {
        id: test_integer
        objectName: "test_integer"

        default_x: 300
        default_y: 350
        default_width: 100
        default_height: 40

        minimum_value: 0
        maximum_value: 80

        conversion_list: [["A", 1, 0], ["B", 1, -35]]
    }

    // Stringinput pour tester : le clavier ; la désactivation des touches claviers interdites ; le positionement du clavier
    INI_stringinput {
        id: test_string
        objectName: "test_string"

        default_x: 150
        default_y: 150
        default_width: 400
        default_height: 40
    }
}