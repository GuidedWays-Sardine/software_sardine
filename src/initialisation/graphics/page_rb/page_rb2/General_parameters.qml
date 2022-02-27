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

        text: "├────────────────────────────────────────────────────────────────┤"
        font_size: 12

        is_dark_grey: false
        is_visible: root.generated
    }

    //floatinput de la longueur de la voiture
    INI_floatinput{
        id: length_floatinput
        objectName: "length_floatinput"

        default_x: (640 - default_width) * 0.5
        default_y: root.default_y - 2
        default_width: 54
        default_height: 16

        maximum_value: root.max_length
        minimum_value: 0.001
        decimals: 3

        title: "Lvoiture"
        unit: "m"
        font_size: 10

        is_max_default: false
        is_activable: true
        is_positive: false
        is_visible: root.generated
    }

    //floatinput de la masse vide
    INI_floatinput{
        id: empty_weight_floatinput
        objectName: "empty_weight_floatinput"

        default_x: (640 - default_width) * 0.5 - 100
        default_y: root.default_y - 2
        default_width: 54
        default_height: 16

        maximum_value: root.max_weight
        minimum_value: 0.001
        decimals: 3

        title: "Mvide"
        unit: "t"
        font_size: 10

        is_max_default: false
        is_activable: true
        is_positive: false
        is_visible: root.generated
    }

    //floatinput de la masse pleine
    INI_floatinput{
        id: full_weight_floatinput
        objectName: "full_weight_floatinput"

        default_x: (640 - default_width) * 0.5 + 100
        default_y: root.default_y - 2
        default_width: 54
        default_height: 16

        maximum_value: root.max_weight
        minimum_value: empty_weight_floatinput.value
        decimals: 3

        title : "Mplein"
        unit: "t"
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

        //checkbutton pour savoir si les coefficients doivent être changés
        INI_checkbutton {
            id: modify_check
            objectName: "modify_check"

            default_x: 1
            default_y: dynamic_data_box.default_y + dynamic_data_box.default_height - box_length - 1
            box_length: 16

            title: "coefficients modifiables ?"
            font_size: 10
        }

        //floatinput pour le coefficient A vide
        INI_floatinput{
            id: a_empty_floatinput
            objectName: "a_empty_floatinput"

            default_x: dynamic_data_box.default_x + 1
            default_y: dynamic_data_box.default_y + 4 + font_size
            default_width: 3 * default_height
            default_height: 16

            maximum_value: root.a_max
            minimum_value: 0
            decimals: root.abc_decimals

            title: "A(vide)"
            unit: "kN"
            font_size: 10

            is_max_default: false
            is_activable: modify_check.is_checked
            is_positive: false
            is_visible: root.generated
        }

        INI_text{
            id: v0_empty
            objectName: "v0_empty"

            text: " + "
            font_size: 10

            default_x: (a_empty_floatinput.default_x + a_empty_floatinput.default_width + b_empty_floatinput.default_x - default_text_width) * 0.5
            default_y: a_empty_floatinput.default_y + (a_empty_floatinput.default_height - font_size) * 0.5 - 4

            is_dark_grey: !modify_check.is_checked
            is_visible: root.generated
        }

        //floatinput pour le coefficient B vide
        INI_floatinput{
            id: b_empty_floatinput
            objectName: "b_empty_floatinput"

            default_x: a_empty_floatinput.default_x + 80
            default_y: a_empty_floatinput.default_y
            default_width: a_empty_floatinput.default_width
            default_height: a_empty_floatinput.default_height

            maximum_value: root.b_max
            minimum_value: 0
            decimals: root.abc_decimals

            title: "B(vide)"
            unit: "kN/(km/h)"
            font_size: 10

            is_max_default: false
            is_activable: modify_check.is_checked
            is_positive: false
            is_visible: root.generated
        }

        INI_text{
            id: v1_empty
            objectName: "v1_empty"

            text: "V + "
            font_size: v0_empty.font_size

            default_x: (b_empty_floatinput.default_x + b_empty_floatinput.default_width + c_empty_floatinput.default_x - default_text_width) * 0.5
            default_y: b_empty_floatinput.default_y + (b_empty_floatinput.default_height - font_size) * 0.5 - 4

            is_dark_grey: !modify_check.is_checked
            is_visible: root.generated
        }

        // floatinput pour le coefficient C
        INI_floatinput{
            id: c_empty_floatinput
            objectName: "c_empty_floatinput"

            default_x: b_empty_floatinput.default_x + 80
            default_y: b_empty_floatinput.default_y
            default_width: b_empty_floatinput.default_width
            default_height: b_empty_floatinput.default_height

            maximum_value: root.c_max
            minimum_value: 0
            decimals: root.abc_decimals

            title: "C(vide)"
            unit: "kN/(km/h)²"
            font_size: 10

            is_max_default: false
            is_activable: modify_check.is_checked
            is_positive: false
            is_visible: root.generated
        }

        INI_text{
            id: v2_empty
            objectName: "v2_empty"

            text: "V²"
            font_size: v1_empty.font_size

            default_x: c_empty_floatinput.default_x + c_empty_floatinput.default_width + (default_text_width) * 0.5
            default_y: c_empty_floatinput.default_y + (c_empty_floatinput.default_height - font_size) * 0.5 - 4

            is_dark_grey: !modify_check.is_checked
            is_visible: root.generated
        }
}