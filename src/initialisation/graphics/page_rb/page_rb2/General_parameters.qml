import QtQuick 2.15
import QtQuick.Controls 2.15
import "../../../components"


Item {
    id: root

    //propriétés sur la position ddu composant
    property int default_x: 0
    property int default_y: 0
    anchors.fill: parent

    //Propriétés sur l'état des paramètres simple
    property bool generated: false

    //Propriétés sur les valeurs maximales
    property double max_weight: 1e9            //t
    property double max_length: 1e9            //m
    readonly property double a_max: 1e3                 //kN
    readonly property double b_max: 1e3                 //kN/(km/h)
    readonly property double c_max: 1e3                 //kM/(km/h)²
    readonly property int abc_decimals: 8

    INI_text {
        id: length_bar
        objectName: "length_bar"

        default_x: (640 - default_text_width) * 0.5
        default_y: root.default_y - font_size

        text: "├─────────────────────────────────────────────┤"
        font_size: 12

        is_dark_grey: false
        is_visible: root.generated
    }

    //floatinput de la longueur de la voiture
    INI_text {
        id: length_text
        objectName: "length_text"

        text: "Lvoiture"
        font_size: 6

        default_x: length_floatinput.default_x + 2
        default_y: length_floatinput.default_y - 10

        is_dark_grey: false
        is_visible: root.generated
    }

    INI_text {
        id: length_unit_text
        objectName: "length_unit_text"

        text: "m"
        font_size: 4

        default_x: length_floatinput.default_x + length_floatinput.default_width + 2
        default_y: length_floatinput.default_y + length_floatinput.default_height - font_size - 2

        is_dark_grey: true
        is_visible: root.generated
    }

    INI_floatinput{
        id: length_floatinput
        objectName: "length_floatinput"

        default_x: (640 - default_width) * 0.5
        default_y: root.default_y - 2
        default_width: 48
        default_height: 16

        maximum_value: root.max_length
        minimum_value: 0.001
        decimals: 3
        font_size: 10

        is_max_default: false
        is_activable: true
        is_positive: false
        is_visible: root.generated
    }

    //floatinput de la masse vide
    INI_text {
        id: empty_weight_text
        objectName: "empty_weight_text"

        text: "Mvoiture(vide)"
        font_size: 6

        default_x: empty_weight_floatinput.default_x + 2
        default_y: empty_weight_floatinput.default_y - 10

        is_dark_grey: false
        is_visible: root.generated
    }

    INI_text {
        id: empty_weight_unit_text
        objectName: "empty_weight_unit_text"

        text: "t"
        font_size: 4

        default_x: empty_weight_floatinput.default_x + empty_weight_floatinput.default_width + 2
        default_y: empty_weight_floatinput.default_y + empty_weight_floatinput.default_height - font_size - 2

        is_dark_grey: true
        is_visible: root.generated
    }

    INI_floatinput{
        id: empty_weight_floatinput
        objectName: "empty_weight_floatinput"

        default_x: (640 - default_width) * 0.5 - 80
        default_y: root.default_y - 2
        default_width: 48
        default_height: 16

        maximum_value: root.max_weight
        minimum_value: 0.001
        decimals: 3
        font_size: 10

        is_max_default: false
        is_activable: true
        is_positive: false
        is_visible: root.generated
    }

    //floatinput de la masse pleine
    INI_text {
        id: full_weight_text
        objectName: "full_weight_text"

        text: "Mvoiture(pleine)"
        font_size: 6

        default_x: full_weight_floatinput.default_x + 2
        default_y: full_weight_floatinput.default_y - 10

        is_dark_grey: false
        is_visible: root.generated
    }

    INI_text {
        id: full_weight_unit_text
        objectName: "full_weight_unit_text"

        text: "t"
        font_size: 4

        default_x: full_weight_floatinput.default_x + full_weight_floatinput.default_width + 2
        default_y: full_weight_floatinput.default_y + full_weight_floatinput.default_height - font_size - 2

        is_dark_grey: true
        is_visible: root.generated
    }

    INI_floatinput{
        id: full_weight_floatinput
        objectName: "full_weight_floatinput"

        default_x: (640 - default_width) * 0.5 + 80
        default_y: root.default_y - 2
        default_width: 48
        default_height: 16

        maximum_value: root.max_weight
        minimum_value: empty_weight_floatinput.value
        decimals: 3
        font_size: 10

        is_max_default: false
        is_activable: true
        is_positive: false
        is_visible: root.generated
    }

    //Boite pour la dynamique
    INI_button {
        id: dynamic_data_box
        objectName: "dynamic_data_box"

        default_x: root.default_x
        default_y: length_floatinput.default_y + length_floatinput.default_height
        default_width: 640
        default_height: 52

        is_visible: root.generated
        is_positive: false
        is_activable: false
    }


}