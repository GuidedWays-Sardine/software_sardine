import QtQuick 2.15
import QtQuick.Controls 2.15
import "../../../components"


Item {
    id: root

    //propriétés sur la position ddu composant
    property int default_x: 0
    property int default_y: 0
    property int railcar_view_height: 180
    anchors.fill: parent

    //Propriétés sur l'état des paramètres simple
    property bool generated: false
    property int railcar_index: 0

    //Propriétés sur les valeurs maximales
    property double max_railcar_weight: 1e9   //t
    property double max_railcar_length: 1e9   //m
    property double a_max: 1e3        //kN
    property double b_max: 1e3        //kN/(km/h)
    property double c_max: 1e3        //kM/(km/h)²
    property int abc_decimals: 6
    property var positions_type: []         //Liste des différentes positions possibles
    property var missions_type: []          //Liste des différentes missions EN ANGLAIS (nécessaire pour la position
    property var missions_type_trad: []     //Liste des différentes missions EN ANGLAIS (nécessaire pour la position
    property var max_doors_list: []         //Liste du nombre de portes maximales selon la mission
    property var max_levels_list: []        //Liste du nombre de niveaux maximum selon la mission


    //signal et variables nécessaire pour mettre à jour l'icone
    readonly property string railcar_position_type: positions_type.length > 0 && position_switch.selection_index != -1 ? positions_type[position_switch.selection_index] : ""
    readonly property string railcar_mission_type: missions_type.length > 0 && mission_combo.selection_index != -1 ? missions_type[mission_combo.selection_index] : ""
    signal update_icon()

    //Fonction pour réinitialiser le module
    function clear() {
        //Décoche tous les checkbuttons
        m_full_check.is_checked = false
        m_empty_check.is_checked = false
        different_check.is_checked = false
        modify_check.is_checked = false

        //Remet la mission à la première et repasse le nombre de niveaux et de portes à 0
        position_switch.change_selection(1)
        mission_combo.change_selection(0)
        levels_integerinput.clear()
        doors_integerinput.clear()
        empty_weight_floatinput.clear()
        full_weight_floatinput.clear()
        length_floatinput.clear()

        //Remet les valeurs des différents coefficients à 0
        a_empty_floatinput.clear()
        b_empty_floatinput.clear()
        c_empty_floatinput.clear()
        a_full_floatinput.clear()
        b_full_floatinput.clear()
        c_full_floatinput.clear()
    }


    //Fonction permettant de changer les valeurs du module
    //Format : int(tdb.Mission.value), str(tdb.Position.value), [empty_weight, full_weight], length, levels, doors, [ABCempty] bool(xm_empty), [ABCfull], bool(xm_full)
    function change_values(mission_int, position_type, weight, length, levels, doors, ABCempty, xm_empty, ABCfull, xm_full) {
        //commence par les informations générales
        mission_combo.change_selection(mission_int)
        position_switch.change_selection(root.positions_type.includes(position_type) ? root.positions_type.indexOf(position_type) : 1)
        levels_integerinput.change_value(levels)
        doors_integerinput.change_value(doors)
        empty_weight_floatinput.change_value(weight[0])
        full_weight_floatinput.change_value(weight[1])
        length_floatinput.change_value(levels)

        //si les valeurs sont différentes active les checkbuttons
        if(xm_empty != xm_full || ABCempty.length != 3 || ABCfull.length != 3 || ABCempty[0] != ABCfull[0] || ABCempty[1] != ABCfull[1] || ABCempty[2] != ABCfull[2]) {
            modify_check.is_checked = true
            different_check.is_checked = true
        }
        else {
            different_check.is_checked = false
        }

        //Change les facteurs vides
        if(ABCempty.length == 3) {
            m_empty_check.is_checked = xm_empty
            a_empty_floatinput.change_value(ABCempty[0])
            b_empty_floatinput.change_value(ABCempty[1])
            c_empty_floatinput.change_value(ABCempty[2])
        }

        //Change les facteurs à charge
        if(ABCfull.length == 3) {
            m_full_check.is_checked = xm_full
            a_full_floatinput.change_value(ABCfull[0])
            b_full_floatinput.change_value(ABCfull[1])
            c_full_floatinput.change_value(ABCfull[2])
        }
    }


    //Fonction permettant de récupérer les valeurs
    function get_values() {
        //Format : [int(mission_type), int(tdb.Position), empty_weight, full_weight, length, levels, doors, [ABCempty] bool(xm_empty), [ABCfull], bool(xm_full)]
        return [mission_combo.selection_index, position_switch.selection_index,
                empty_weight_floatinput.value, full_weight_floatinput.value, length_floatinput.value,
                levels_integerinput.value, doors_integerinput.value,
                [a_empty_floatinput.value, b_empty_floatinput.value, c_empty_floatinput.value], m_empty_check.is_checked,
                [a_full_floatinput.value, b_full_floatinput.value, c_full_floatinput.value], m_full_check.is_checked]
    }



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

        maximum_value: root.max_railcar_length
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

        maximum_value: root.max_railcar_weight
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

        maximum_value: root.max_railcar_weight
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


    INI_button {
        id: general_data_box
        objectName: "general_data_box"

        default_x: 640 - default_width - 31
        default_y: dynamic_empty_data_box.default_y - root.railcar_view_height - 27
        default_height: 36
        default_width: 240

        is_visible: root.generated
        is_positive: false
        is_activable: false


        //combobox pour indiquer la mission de la voiture (à titre visuel)
        INI_combobox {
            id: mission_combo
            objectName: "mission_combo"

            default_x: general_data_box.default_x + 1
            default_y: general_data_box.default_y + 16
            default_width: 88
            default_height: 20

            elements: root.missions_type_trad
            title: "mission"
            font_size: 10

            is_positive: false
            is_activable: true
            is_visible: root.generated

            // Signal appelé lorsque la sélection du combobox change
            onSelection_changed: {
                // mets à jour la liste des images et remet l'image visible
                var index = position_switch.selection_index
                if(mission_combo.selection_index != -1 && root.missions_type.length > mission_combo.selection_index) {
                    position_switch.elements = [("INI_trainpreview/" + root.missions_type[mission_combo.selection_index] + "/full/" + (position_switch.is_activable ? "" : "dark_") + "grey_front.png"),
                                                ("INI_trainpreview/" + root.missions_type[mission_combo.selection_index] + "/full/" + (position_switch.is_activable ? "" : "dark_") + "grey_middle.png"),
                                                ("INI_trainpreview/" + root.missions_type[mission_combo.selection_index] + "/full/" + (position_switch.is_activable ? "" : "dark_") + "grey_back.png")]
                    position_switch.change_selection(index)
                }
            }

            // Signal appelé lorsque le combobox est fermée
            onCombobox_closed: {
                // Appelle le signal pour mettre à jour l'icone
                root.update_icon()
            }
        }

        //switchbutton pour indiquer le type de position de la voiture (avant, arrière, milieu)
        INI_switchbutton {
            id: position_switch
            objectName: "position_switch"

            default_x: mission_combo.default_x + mission_combo.default_width + 6
            default_y: mission_combo.default_y
            default_width: 44
            default_height: mission_combo.default_height

            elements: []
            image_mode: true
            title: "position"
            font_size: 10

            is_positive: false
            is_activable: root.railcar_index != 0
            is_visible: root.generated

            // Signal appelé lorsque l'activabilité du switchbutton change
            onIs_activableChanged: {
                // mets à jour la liste des images et remet l'image visible
                var index = position_switch.selection_index
                if(mission_combo.selection_index != -1 && root.missions_type.length > mission_combo.selection_index) {
                    position_switch.elements = [("INI_trainpreview/" + root.missions_type[mission_combo.selection_index] + "/full/" + (position_switch.is_activable ? "" : "dark_") + "grey_front.png"),
                                                ("INI_trainpreview/" + root.missions_type[mission_combo.selection_index] + "/full/" + (position_switch.is_activable ? "" : "dark_") + "grey_middle.png"),
                                                ("INI_trainpreview/" + root.missions_type[mission_combo.selection_index] + "/full/" + (position_switch.is_activable ? "" : "dark_") + "grey_back.png")]
                    position_switch.change_selection(index)
                }
            }

            // Signal appelé lorsque le switchbutton est cliqué
            onClicked: {
                root.update_icon()
            }
        }

        INI_integerinput {
            id: levels_integerinput
            objectName: "levels_integerinput"

            default_x: position_switch.default_x + position_switch.default_width + 6
            default_y: mission_combo.default_y
            default_width: 44
            default_height: mission_combo.default_height

            minimum_value: 0
            maximum_value: root.max_levels_list.length > mission_combo.selection_index && mission_combo.selection_index != -1 ? root.max_levels_list[mission_combo.selection_index] : 0
            is_max_default: false
            title: "niveaux"
            font_size: 10

            is_positive: false
            is_activable: maximum_value > 0
            is_visible: root.generated
        }

        INI_integerinput {
            id: doors_integerinput
            objectName: "doors_integerinput"

            default_x: levels_integerinput.default_x + levels_integerinput.default_width + 6
            default_y: mission_combo.default_y
            default_width: 44
            default_height: mission_combo.default_height

            minimum_value: 0
            maximum_value: root.max_doors_list.length > 0 && mission_combo.selection_index != -1 ? root.max_doors_list[mission_combo.selection_index] : 0
            is_max_default: false
            title: "portes"
            font_size: 10

            is_positive: false
            is_activable: maximum_value > 0
            is_visible: root.generated
        }
    }


    //Boite pour les coefficients de résistance à l'avancement à vide
    INI_button {
        id: dynamic_empty_data_box
        objectName: "dynamic_empty_data_box"

        default_x: root.default_x
        default_y: length_floatinput.default_y + length_floatinput.default_height
        default_width: 320
        default_height: 52

        is_visible: root.generated
        is_positive: false
        is_activable: false

        //checkbutton pour savoir si les coefficients doivent être changés
        INI_checkbutton {
            id: modify_check
            objectName: "modify_check"

            default_x: 1
            default_y: dynamic_empty_data_box.default_y + dynamic_empty_data_box.default_height - box_length - 1
            box_length: 16

            title: "coefficients à vide modifiables ?"
            font_size: 10

            //signal appelé lorsque le checkbutton est cliqué
            onValue_changed: {
                if(!is_checked) {
                    different_check.is_checked = false
                }
            }
        }

        //checkbutton pour indiquer si les coéfficients doivent être multipliés par la masse de la voiture
        INI_text {
            id: m_empty_text
            objectName: "m_empty_text"

            text: "m       (                                                                       )"
            font_size: 10

            default_x: dynamic_empty_data_box.default_x + 5
            default_y: a_empty_floatinput.default_y + (a_empty_floatinput.default_height - font_size) * 0.5 - 4

            is_dark_grey: !modify_check.is_checked || !m_empty_check.is_checked
            is_visible: root.generated
        }

        INI_text {
            id: m_empty_unit
            objectName: "m_empty_unit"

            text: "t"
            font_size: 4

            default_x: m_empty_check.default_x - default_text_width - 4
            default_y: a_empty_floatinput.default_y + (a_empty_floatinput.default_height - font_size) * 0.5 - 1

            is_dark_grey: true
            is_visible: root.generated
        }

        INI_checkbutton {
            id: m_empty_check
            objectName: "m_empty_check"

            default_x: dynamic_empty_data_box.default_x + 20
            default_y: v0_empty.default_y + 2
            box_length: a_empty_floatinput.font_size + 4

            is_dark_grey: !is_checked
            is_activable: modify_check.is_checked

            // Signal appelé lorsque le checkbutton est cliqué
            onValue_changed : {
                //dans le cas où les coefficients à charge sont identiques, change l'état de la multiplication par m
                if(!different_check.is_checked) {
                    m_full_check.is_checked = m_empty_check.is_checked
                }

                //différencie le cas où les facteurs sont multipliés par la masse ou pas
                if(is_checked) {
                    //Divise chacun des coefficients par la masse minimale
                    a_empty_floatinput.change_value(a_empty_floatinput.value / empty_weight_floatinput.value)
                    b_empty_floatinput.change_value(b_empty_floatinput.value / empty_weight_floatinput.value)
                    c_empty_floatinput.change_value(c_empty_floatinput.value / empty_weight_floatinput.value)
                }
                else {
                    //Multiplie chacun des coefficients par la masse minimale
                    a_empty_floatinput.change_value(a_empty_floatinput.value * empty_weight_floatinput.value)
                    b_empty_floatinput.change_value(b_empty_floatinput.value * empty_weight_floatinput.value)
                    c_empty_floatinput.change_value(c_empty_floatinput.value * empty_weight_floatinput.value)
                }
            }
        }


        //floatinput pour le coefficient A vide
        INI_floatinput{
            id: a_empty_floatinput
            objectName: "a_empty_floatinput"

            default_x: m_empty_check.default_x + m_empty_check.box_length + 16
            default_y: dynamic_empty_data_box.default_y + 4 + font_size
            default_width: 3 * default_height
            default_height: 16

            maximum_value: root.a_max
            minimum_value: 0
            decimals: root.abc_decimals

            title: "A(vide) :"
            unit: "kN"
            font_size: 10

            is_max_default: false
            is_activable: modify_check.is_checked
            is_positive: false
            is_visible: root.generated

            //signal appelé lorsque la valeur est changée
            onValue_changed: {
                // Si la valeur à vide et à charge sont les même, mets aussi à jour la valeur à charge
                if(!different_check.is_checked) {
                    a_full_floatinput.change_value(a_empty_floatinput.value)
                }
            }
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

            title: "B(vide) :"
            unit: "kN/(km/h)"
            font_size: 10

            is_max_default: false
            is_activable: modify_check.is_checked
            is_positive: false
            is_visible: root.generated

            //signal appelé lorsque la valeur est changée
            onValue_changed: {
                // Si la valeur à vide et à charge sont les même, mets aussi à jour la valeur à charge
                if(!different_check.is_checked) {
                    b_full_floatinput.change_value(b_empty_floatinput.value)
                }
            }
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

            title: "C(vide) :"
            unit: "kN/(km/h)²"
            font_size: 10

            is_max_default: false
            is_activable: modify_check.is_checked
            is_positive: false
            is_visible: root.generated

            //signal appelé lorsque la valeur est changée
            onValue_changed: {
                // Si la valeur à vide et à charge sont les même, mets aussi à jour la valeur à charge
                if(!different_check.is_checked) {
                    c_full_floatinput.change_value(c_empty_floatinput.value)
                }
            }
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



    //Boite pour les coefficients de résistance à l'avancement chargé
    INI_button {
        id: dynamic_full_data_box
        objectName: "dynamic_full_data_box"

        default_x: root.default_x + 320
        default_y: length_floatinput.default_y + length_floatinput.default_height
        default_width: 320
        default_height: 52
        background_color: "transparent"

        is_visible: root.generated
        is_positive: false
        is_activable: false

        //checkbutton pour savoir si les valeurs à charge sont identiques
        INI_checkbutton {
            id: different_check
            objectName: "different_check"

            default_x: dynamic_full_data_box.default_x + 1
            default_y: dynamic_full_data_box.default_y + dynamic_full_data_box.default_height - box_length - 1
            box_length: 16

            title: "coefficients à charge différents ?"
            font_size: 10

            is_visible: root.generated
            is_activable: modify_check.is_checked

            // Signal appelé lorsque le checkbutton est cliqué
            onValue_changed: {
                // Dans le cas où le checkbutton est décoché, normalise les données pleines avec les données vides
                if(!is_checked) {
                    //Normalise le checlbutton pour multiplier les coefficients par la masse
                    m_full_check.is_checked = m_empty_check.is_checked

                    //normalise les valeurs des différents coefficients
                    a_full_floatinput.change_value(a_empty_floatinput.value)
                    b_full_floatinput.change_value(b_empty_floatinput.value)
                    c_full_floatinput.change_value(c_empty_floatinput.value)
                }
            }
        }


        //checkbutton pour indiquer si les coéfficients doivent être multipliés par la masse de la voiture
        INI_text {
            id: m_full_text
            objectName: "m_full_text"

            text: "m       (                                                                       )"
            font_size: 10

            default_x: dynamic_full_data_box.default_x + 5
            default_y: a_full_floatinput.default_y + (a_full_floatinput.default_height - font_size) * 0.5 - 4

            is_dark_grey: !different_check.is_checked || !m_full_check.is_checked
            is_visible: root.generated
        }

        INI_text {
            id: m_full_unit
            objectName: "m_full_unit"

            text: "t"
            font_size: 4

            default_x: m_full_check.default_x - default_text_width - 4
            default_y: a_full_floatinput.default_y + (a_full_floatinput.default_height - font_size) * 0.5 - 1

            is_dark_grey: true
            is_visible: root.generated
        }

        INI_checkbutton {
            id: m_full_check
            objectName: "m_full_check"

            default_x: dynamic_full_data_box.default_x + 20
            default_y: v0_full.default_y + 2
            box_length: a_full_floatinput.font_size + 4

            is_dark_grey: !is_checked
            is_activable: different_check.is_checked

            // Signal appelé lorsque le checkbutton est cliqué
            onValue_changed : {
                //différencie le cas où les facteurs sont multipliés par la masse
                if(is_checked) {
                    //Divise chacun des coefficients par la masse maximale
                    a_full_floatinput.change_value(a_full_floatinput.value / full_weight_floatinput.value)
                    b_full_floatinput.change_value(b_full_floatinput.value / full_weight_floatinput.value)
                    c_full_floatinput.change_value(c_full_floatinput.value / full_weight_floatinput.value)

                    //change les limites et la valeur par défaut pour le pourcentage de masse applicable
                    percentage_floatinput.maximum_value = 100
                    percentage_floatinput.change_value(7)
                }
                else {
                    //Multiplie chacun des coefficients par la masse maximale
                    a_full_floatinput.change_value(a_full_floatinput.value * full_weight_floatinput.value)
                    b_full_floatinput.change_value(b_full_floatinput.value * full_weight_floatinput.value)
                    c_full_floatinput.change_value(c_full_floatinput.value * full_weight_floatinput.value)

                    //remet les limites de la masse applicable
                    percentage_floatinput.maximum_value = 0
                }
            }
        }


        //floatinput pour le coefficient A vide
        INI_floatinput{
            id: a_full_floatinput
            objectName: "a_full_floatinput"

            default_x: m_full_check.default_x + m_full_check.box_length + 16
            default_y: dynamic_full_data_box.default_y + 4 + font_size
            default_width: 3 * default_height
            default_height: 16

            maximum_value: root.a_max
            minimum_value: 0
            decimals: root.abc_decimals

            title: "A(plein) :"
            unit: m_full_check.is_checked ? "kN/t" : "kN"
            font_size: 10

            is_max_default: false
            is_activable: different_check.is_checked
            is_positive: false
            is_visible: root.generated
        }

        INI_text{
            id: v0_full
            objectName: "v0_full"

            text: " + "
            font_size: 10

            default_x: (a_full_floatinput.default_x + a_full_floatinput.default_width + b_full_floatinput.default_x - default_text_width) * 0.5
            default_y: a_full_floatinput.default_y + (a_full_floatinput.default_height - font_size) * 0.5 - 4

            is_dark_grey: !different_check.is_checked
            is_visible: root.generated
        }

        //floatinput pour le coefficient B vide
        INI_floatinput{
            id: b_full_floatinput
            objectName: "b_full_floatinput"

            default_x: a_full_floatinput.default_x + 80
            default_y: a_full_floatinput.default_y
            default_width: a_full_floatinput.default_width
            default_height: a_full_floatinput.default_height

            maximum_value: root.b_max
            minimum_value: 0
            decimals: root.abc_decimals

            title: "B(plein) :"
            unit: m_full_check.is_checked ? "kN/t/(km/h)" : "kN/(km/h)"
            font_size: 10

            is_max_default: false
            is_activable: different_check.is_checked
            is_positive: false
            is_visible: root.generated
        }

        INI_text{
            id: v1_full
            objectName: "v1_full"

            text: "V + "
            font_size: v0_full.font_size

            default_x: (b_full_floatinput.default_x + b_full_floatinput.default_width + c_full_floatinput.default_x - default_text_width) * 0.5
            default_y: b_full_floatinput.default_y + (b_full_floatinput.default_height - font_size) * 0.5 - 4

            is_dark_grey: !different_check.is_checked
            is_visible: root.generated
        }

        // floatinput pour le coefficient C
        INI_floatinput{
            id: c_full_floatinput
            objectName: "c_full_floatinput"

            default_x: b_full_floatinput.default_x + 80
            default_y: b_full_floatinput.default_y
            default_width: b_full_floatinput.default_width
            default_height: b_full_floatinput.default_height

            maximum_value: root.c_max
            minimum_value: 0
            decimals: root.abc_decimals

            title: "C(plein) :"
            unit: m_full_check.is_checked ? "kN/t/(km/h)²" : "kN/(km/h)²"
            font_size: 10

            is_max_default: false
            is_activable: different_check.is_checked
            is_positive: false
            is_visible: root.generated
        }

        INI_text{
            id: v2_full
            objectName: "v2_full"

            text: "V²"
            font_size: v1_full.font_size

            default_x: c_full_floatinput.default_x + c_full_floatinput.default_width + (default_text_width) * 0.5
            default_y: c_full_floatinput.default_y + (c_full_floatinput.default_height - font_size) * 0.5 - 4

            is_dark_grey: !different_check.is_checked
            is_visible: root.generated
        }

        INI_floatinput {
            id: percentage_floatinput
            objectName: "percentage_floatinput"

            default_x: dynamic_full_data_box.default_x + dynamic_full_data_box.default_width - 1 - default_width
            default_y: dynamic_full_data_box.default_y + dynamic_full_data_box.default_height - 1 - default_height

            default_width: c_full_floatinput.default_width
            default_height: c_full_floatinput.default_height

            minimum_value: 0
            maximum_value: 0
            decimals: 2

            is_positive: false
            is_activable: m_full_check.is_checked
            is_visible: root.generated
        }
    }
}