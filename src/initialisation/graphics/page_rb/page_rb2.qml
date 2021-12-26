import QtQuick 2.0
import QtQuick.Controls 2.15
import "../../components"


Item {
    id: page_rb2
    objectName: "page_rb2"



    //Constantes permettant de controller les différentes valeurs maximales de chacun des trains
    readonly property double max_weight: 1e9            //t
    readonly property double max_length: 1e9            //mf
    readonly property int max_coaches: 1e3
    readonly property int max_bogies: 1e3
    readonly property int max_axles_per_bogies: 1e1
    readonly property double max_motor_power: 1e6       //kW
    readonly property double max_power: max_motor_power * motorized_axles_count_integerinput.value      //NE PAS CHANGER


    //Constantes permettant de controller la taille et la position des différents éléments de la page
    readonly property int input_height: 80
    readonly property int input_width: 24
    readonly property int x_offset: 140
    readonly property int y_offset: 44



    //Nom du matériel roulant (et du fichier dans lequel il sera sauvegardé)
    //stringinput du nom du matériel roulant
    INI_text {
        id: train_name_text
        objectName: "train_name_text"

        default_x: train_name_stringinput.default_x + 2
        default_y: train_name_stringinput.default_y - 2 * font_size

        text: "Configuration du train"
        font_size: 12

        is_dark_grey: false
        is_visible: true
    }

    INI_stringinput{
        id: train_name_stringinput
        objectName: "train_name_stringinput"

        default_x: 54
        default_y: 38
        default_width: save.default_x - default_x
        default_height: 26

        max_text_length: 48
        placeholder_text: "Nom du train (utilisé pour le nom du fichier)"
        is_activable: true
        is_positive: true
        is_visible: true
    }



    //Tous les composants reliés au paramétrage des informations générales du train
    INI_button {
        id: general_data_box
        objectName: "general_data_box"

        default_x: train_name_stringinput.default_x
        default_y: train_name_stringinput.default_y + train_name_stringinput.default_height
        default_width: train_name_stringinput.default_width
        default_height: 3*50

        is_activable: false
        is_positive: false
        is_visible: true
    }

    INI_text {
        id: general_data_name
        objectName: "general_data_name"

        default_x: general_data_box.default_x + 1 + (general_data_box.is_positive)
        default_y: general_data_box.default_y + 1 + (general_data_box.is_positive)

        text: "Informations générales"
        font_size: 12

        is_dark_grey: false
        is_visible: true
    }



    //Tous les composants reliés au paramétrage générale du train
    //floatinput de la masse du convoi
    INI_text {
        id: weight_text
        objectName: "weight_text"

        text: "Mconvoi"
        font_size: 12

        default_x: weight_floatinput.default_x + 2
        default_y: weight_floatinput.default_y - 4 - font_size

        is_dark_grey: false
        is_visible: true
    }

    INI_text {
        id: weight_unit_text
        objectName: "weight_unit_text"

        text: "t"
        font_size: 6

        default_x: weight_floatinput.default_x + weight_floatinput.default_width + 2
        default_y: weight_floatinput.default_y + weight_floatinput.default_height - 2 - font_size

        is_dark_grey: true
        is_visible: true
    }

    INI_floatinput{
        id: weight_floatinput
        objectName: "weight_floatinput"

        default_x: general_data_box.default_x + 1 + (general_data_box.is_positive)
        default_y: general_data_box.default_y + 1 + (general_data_box.is_positive) + 3 * general_data_name.font_size
        default_width: page_rb2.input_height
        default_height: page_rb2.input_width

        maximum_value: page_rb2.max_weight
        minimum_value: 0.001 * bogies_count_integerinput.value * axles_per_bogies_integerinput.value
        decimals: 3

        is_max_default: false
        is_activable: true
        is_positive: false
        is_visible: true
    }


    //integerinput de la longueur
    INI_text {
        id: length_text
        objectName: "length_text"

        text: "Lconvoi"
        font_size: 12

        default_x: length_floatinput.default_x + 2
        default_y: length_floatinput.default_y - 4 - font_size

        is_dark_grey: false
        is_visible: true
    }

    INI_text {
        id: length_unit_text
        objectName: "length_unit_text"

        text: "m"
        font_size: 6

        default_x: length_floatinput.default_x + length_floatinput.default_width + 2
        default_y: length_floatinput.default_y + length_floatinput.default_height - 2 - font_size

        is_dark_grey: true
        is_visible: true
    }

    INI_floatinput{
        id: length_floatinput
        objectName: "length_floatinput"

        default_x: weight_floatinput.default_x + page_rb2.x_offset
        default_y: weight_floatinput.default_y
        default_width: weight_floatinput.default_width
        default_height: weight_floatinput.default_height

        maximum_value: page_rb2.max_length
        minimum_value: 0.001 * coaches_integerinput.value
        decimals: 3

        is_max_default: false
        is_activable: true
        is_positive: false
        is_visible: true
    }


    //integerinput de la longueur
    INI_text {
        id: coaches_text
        objectName: "coaches_text"

        text: "Nvoitures"
        font_size: 12

        default_x: coaches_integerinput.default_x + 2
        default_y: coaches_integerinput.default_y - 4 - font_size

        is_dark_grey: false
        is_visible: true
    }

    INI_integerinput{
        id: coaches_integerinput
        objectName: "coaches_integerinput"

        default_x: length_floatinput.default_x +  page_rb2.x_offset
        default_y: length_floatinput.default_y
        default_width: length_floatinput.default_width
        default_height: length_floatinput.default_height

        maximum_value: page_rb2.max_coaches
        minimum_value: 1

        is_max_default: false
        is_activable: true
        is_positive: false
        is_visible: true
    }



    //Tous les composants reliés au paramétrage des essieux
    //integerinput pour le nombre de bogies sur le train
    INI_text {
        id: bogies_count_text
        objectName: "bogies_count_text"

        default_x: bogies_count_integerinput.default_x + 2
        default_y: bogies_count_integerinput.default_y - 4 - font_size

        text: "Nbogies"
        font_size: 12

        is_dark_grey: false
        is_visible: true
    }

    INI_integerinput{
        id: bogies_count_integerinput
        objectName: "bogies_count_integerinput"

        default_x: weight_floatinput.default_x
        default_y: weight_floatinput.default_y + page_rb2.y_offset
        default_width: weight_floatinput.default_width
        default_height: weight_floatinput.default_height

        maximum_value: page_rb2.max_bogies
        minimum_value: 1

        is_max_default: false
        is_positive: false
        is_activable: true
        is_visible: true
    }

    //integerinput pour connaitre le nombre d'essieux par bogies
    INI_text {
        id: axles_per_bogies_text
        objectName: "axles_per_bogies_text"

        default_x: axles_per_bogies_integerinput.default_x + 2
        default_y: axles_per_bogies_integerinput.default_y - 4 - font_size

        text: "Nessieux/bogies"
        font_size: 12

        is_dark_grey: false
        is_visible: true
    }

    INI_integerinput{
        id: axles_per_bogies_integerinput
        objectName: "axles_per_bogies_integerinput"

        default_x: length_floatinput.default_x
        default_y: bogies_count_integerinput.default_y
        default_width: length_floatinput.default_width
        default_height: bogies_count_integerinput.default_height

        maximum_value: page_rb2.max_axles_per_bogies
        minimum_value: 1

        is_max_default: false
        is_positive: false
        is_activable: true
        is_visible: true
    }

    //integerinput pour connaitre le nombre d'essieux par bogies
    INI_text {
        id: motorized_axle_weight_text
        objectName: "motorized_axle_weight_text"

        default_x: motorized_axle_weight_floatinput.default_x + 2
        default_y: motorized_axle_weight_floatinput.default_y - 4 - font_size

        text: "masse/essieu moteur"
        font_size: 12

        is_dark_grey: false
        is_visible: true
    }

    INI_text {
        id: motorized_axle_weight_unit_text
        objectName: "motorized_axle_weight_unit_text"

        default_x: motorized_axle_weight_floatinput.default_x + motorized_axle_weight_floatinput.default_width + 2
        default_y: motorized_axle_weight_floatinput.default_y + motorized_axle_weight_floatinput.default_height - 2 - font_size

        text: "t"
        font_size: 6

        is_dark_grey: motorized_axles_count_integerinput.value == 0
        is_visible: true
    }

    INI_floatinput{
        id: motorized_axle_weight_floatinput
        objectName: "motorized_axle_weight_floatinput"

        default_x: coaches_integerinput.default_x
        default_y: axles_per_bogies_integerinput.default_y
        default_width: coaches_integerinput.default_width
        default_height: axles_per_bogies_integerinput.default_height

        maximum_value: motorized_axles_count_integerinput.value != 0
                       ? // Cas où le nombre d'essieux motorisés est différent de 0 (propose de telle sorte à ce que la masse totale sur les essieux moteur ne dépasse pas celle du train)
                         weight_floatinput.value / motorized_axles_count_integerinput.value
                       : // Sinon affiche la taille moyenne à l'essieu
                       weight_floatinput.value / (bogies_count_integerinput.value * axles_per_bogies_integerinput.value)
        minimum_value: motorized_axles_count_integerinput.value != 0
                       ? // Cas où le nombre d'essieux motorisés est différent de 0 (propose à l'utilisateur de rentrer une valeur)
                         0.001
                       : // Sinon affiche la taille moyenne à l'essieu
                       weight_floatinput.value / (bogies_count_integerinput.value * axles_per_bogies_integerinput.value)
        decimals: 3

        is_max_default: false
        is_positive: false
        is_activable: motorized_axles_count_integerinput.value != 0
        is_visible: true
    }



    //Tous les composants reliés au paramétrage de la puissance moteur
    //integerinput pour connaitre le nombre d'essieux moteurs
    INI_text {
        id: motorized_axles_count_text
        objectName: "motorized_axles_count_text"

        text: "Nessieux moteurs"
        font_size: 12

        default_x: motorized_axles_count_integerinput.default_x + 2
        default_y: motorized_axles_count_integerinput.default_y - 4 - font_size

        is_dark_grey: false
        is_visible: true
    }

    INI_integerinput{
        id: motorized_axles_count_integerinput
        objectName: "motorized_axles_count_integerinput"

        default_x: bogies_count_integerinput.default_x
        default_y: bogies_count_integerinput.default_y + page_rb2.y_offset
        default_width: bogies_count_integerinput.default_width
        default_height: bogies_count_integerinput.default_height

        maximum_value: bogies_count_integerinput.value * axles_per_bogies_integerinput.value
        minimum_value: 0

        is_max_default: false
        is_activable: true
        is_positive: false
        is_visible: true

        onValue_changed: {
            // Si le dernier élément mis à jour est la puissance des moteurs, mets à jour la puissance du train
            power_floatinput.is_modified = true
            axle_power_floatinput.is_modified = true
            if(axle_power_floatinput.last_changed && !power_floatinput.last_changed){
                power_floatinput.change_value(axle_power_floatinput.value * motorized_axles_count_integerinput.value)
            }
            // Si le dernier élément mis à jour est la puissance du train, mets à jour la puissance des moteurs
            else{
                if(motorized_axles_count_integerinput.value != 0) {
                    axle_power_floatinput.change_value(power_floatinput.value / motorized_axles_count_integerinput.value)
                }
                else{
                    axle_power_floatinput.change_value(0)
                }
            }
            axle_power_floatinput.is_modified = false
            power_floatinput.is_modified = false
        }
    }

    //floatinput pour connaitre la puissance de chaque essieux moteurs (relié à la puissance générale
    INI_text {
        id: axle_power_text
        objectName: "axle_power_text"

        text: "Pmoteur"
        font_size: 12

        default_x: axle_power_floatinput.default_x + 2
        default_y: axle_power_floatinput.default_y - 4 - font_size

        is_dark_grey: motorized_axles_count_integerinput.value == 0
        is_visible: true
    }

    INI_text {
        id: axle_power_unit_text
        objectName: "axle_power_unit_text"

        text: "kW"
        font_size: 6

        default_x: axle_power_floatinput.default_x + axle_power_floatinput.default_width + 2
        default_y: axle_power_floatinput.default_y + axle_power_floatinput.default_height - 2 - font_size

        is_dark_grey: true
        is_visible: true
    }

    INI_floatinput{
        id: axle_power_floatinput
        objectName: "axle_power_floatinput"

        //propriété permettant de se souvenir si la puissance du train ou la puissance moteur a été changée en dernier
        //Utile pour savoir quelle puissance mettre à jour lorsque le nombre d'essieux moteurs est changé
        property bool last_changed: false
        property bool is_modified: false

        default_x: axles_per_bogies_integerinput.default_x
        default_y: motorized_axles_count_integerinput.default_y
        default_width: axles_per_bogies_integerinput.default_width
        default_height: motorized_axles_count_integerinput.default_height

        maximum_value: motorized_axles_count_integerinput.value != 0 ? page_rb2.max_motor_power : 0     //Met la valeur ax à celle indiqué sauf si le train a aucun essieu motorisé (auquel cas à 0)
        minimum_value: 0
        decimals: 3

        is_max_default: false
        is_activable: motorized_axles_count_integerinput.value != 0
        is_positive: false
        is_visible: true

        onValue_changed: {
            //Met à jour la puissance générale du train
            if(!power_floatinput.is_modified){
                power_floatinput.is_modified = true
                power_floatinput.change_value(axle_power_floatinput.value * motorized_axles_count_integerinput.value)
                power_floatinput.is_modified = false

                //Indique qu'il était le dernier à être modifié
                axle_power_floatinput.last_changed = true
                power_floatinput.last_changed = false
            }
        }
    }

    //floatinput pour connaitre la puissance totale du train (relié à la puissance moteur)
    INI_text {
        id: power_text
        objectName: "power_text"

        text: "Ptrain"
        font_size: 12

        default_x: power_floatinput.default_x + 2
        default_y: power_floatinput.default_y - 4 - font_size

        is_dark_grey: motorized_axles_count_integerinput.value == 0
        is_visible: true
    }

    INI_text {
        id: power_unit_text
        objectName: "power_unit_text"

        text: "kW"
        font_size: 6

        default_x: power_floatinput.default_x + power_floatinput.default_width + 2
        default_y: power_floatinput.default_y + power_floatinput.default_height - 2 - font_size

        is_dark_grey: true
        is_visible: true
    }

    INI_floatinput{
        id: power_floatinput
        objectName: "power_floatinput"

        //propriété permettant de se souvenir si la puissance du train ou la puissance moteur a été changée en dernier
        //Utile pour savoir quelle puissance mettre à jour lorsque le nombre d'essieux moteurs est changé
        property bool last_changed: true
        property bool is_modified: false

        default_x: motorized_axle_weight_floatinput.default_x
        default_y: axle_power_floatinput.default_y
        default_width: motorized_axle_weight_floatinput.default_width
        default_height: axle_power_floatinput.default_height

        maximum_value: motorized_axles_count_integerinput.value != 0 ? page_rb2.max_power : 0     //Met la valeur ax à celle indiqué sauf si le train a aucun essieu motorisé (auquel cas à 0)
        minimum_value: 0
        decimals: 3

        is_max_default: false
        is_activable: motorized_axles_count_integerinput.value != 0
        is_positive: false
        is_visible: true

        onValue_changed: {
            //Met à jour la puissance par essieux du train
            if(!axle_power_floatinput.is_modified){
                power_floatinput.is_modified = true
                if(motorized_axles_count_integerinput.value != 0) {
                    axle_power_floatinput.change_value(power_floatinput.value / motorized_axles_count_integerinput.value)
                }
                else{
                    axle_power_floatinput.change_value(0)
                }
                power_floatinput.is_modified = false

                //Indique qu'il était le dernier à être modifié
                axle_power_floatinput.last_changed = false
                power_floatinput.last_changed = true
            }
        }
    }



    //Tous les composants reliés au paramétrage de la dynamique du train
    //floatinput pour le coefficient A
    INI_text {
        id: a_text
        objectName: "a_text"

        text: "A"
        font_size: 12

        default_x: a_floatinput.default_x + 2
        default_y: a_floatinput.default_y - 4 - font_size

        is_dark_grey: false
    }

    INI_text {
        id: a_unit_text
        objectName: "a_unit_text"

        text: "kN"
        font_size: 6

        default_x: a_floatinput.default_x + a_floatinput.default_width + 2
        default_y: a_floatinput.default_y + a_floatinput.default_height - 2 - font_size

        is_dark_grey: true
    }

    INI_floatinput{
        id: a_floatinput
        objectName: "a_floatinput"

        default_x: 54
        default_y: 271
        default_width: 66
        default_height: 24

        maximum_value: Infinity
        minimum_value: 0
        decimals: 8

        is_max_default: false
    }

    INI_text{
        id: v0
        objectName: "v0"

        text: " + "
        font_size: 12

        default_x: (a_floatinput.default_x + a_floatinput.default_width + b_floatinput.default_x - default_text_width) * 0.5
        default_y: a_floatinput.default_y + (a_floatinput.default_height - font_size) * 0.5 - 2

        is_dark_grey: false
    }


    //floatinput pour le coefficient B
    INI_text {
        id: b_text
        objectName: "b_text"

        text: "B"
        font_size: a_text.font_size

        default_x: b_floatinput.default_x + 2
        default_y: b_floatinput.default_y - 4 - font_size

        is_dark_grey: a_text.is_dark_grey
    }

    INI_text {
        id: b_unit_text
        objectName: "b_unit_text"

        text: "kN/(km/h)"
        font_size: a_unit_text.font_size

        default_x: b_floatinput.default_x + b_floatinput.default_width + 2
        default_y: b_floatinput.default_y + b_floatinput.default_height - 2 - font_size

        is_dark_grey: a_unit_text.is_dark_grey
    }

    INI_floatinput{
        id: b_floatinput
        objectName: "b_floatinput"

        default_x: a_floatinput.default_x + 100
        default_y: a_floatinput.default_y
        default_width: a_floatinput.default_width
        default_height: a_floatinput.default_height

        maximum_value: Infinity
        minimum_value: 0
        decimals: 8

        is_max_default: false
    }

    INI_text{
        id: v1
        objectName: "v1"

        text: "V + "
        font_size: v0.font_size

        default_x: (b_floatinput.default_x + b_floatinput.default_width + c_floatinput.default_x - default_text_width) * 0.5
        default_y: b_floatinput.default_y + (b_floatinput.default_height - font_size) * 0.5 - 2

        is_dark_grey: v0.is_dark_grey
    }


    //floatinput pour le coefficient C
    INI_text {
        id: c_text
        objectName: "c_text"

        text: "C"
        font_size: b_text.font_size

        default_x: c_floatinput.default_x + 2
        default_y: c_floatinput.default_y - 4 - font_size

        is_dark_grey: b_text.is_dark_grey
    }

    INI_text {
        id: c_unit_text
        objectName: "c_unit_text"

        text: "kN/(km/h)²"
        font_size: b_unit_text.font_size

        default_x: c_floatinput.default_x + c_floatinput.default_width + 2
        default_y: c_floatinput.default_y + c_floatinput.default_height - 2 - font_size

        is_dark_grey: b_unit_text.is_dark_grey
    }

    INI_floatinput{
        id: c_floatinput
        objectName: "c_floatinput"

        default_x: b_floatinput.default_x + 100
        default_y: b_floatinput.default_y
        default_width: b_floatinput.default_width
        default_height: b_floatinput.default_height

        maximum_value: 100
        minimum_value: 0
        decimals: 8

        is_max_default: true//false
    }

    INI_text{
        id: v2
        objectName: "v2"

        text: "V²"
        font_size: v1.font_size

        default_x: c_floatinput.default_x + c_floatinput.default_width + (default_text_width) * 0.5
        default_y: c_floatinput.default_y + (c_floatinput.default_height - font_size) * 0.5 - 2

        is_dark_grey: v1.is_dark_grey
    }







    //Tous les composants reliés au paramétrage des systèmes d'alimentation
    //checkbutton pour indiquer si le train a des pantographes (en mode simplifié on le considère compatible avec toutes les tensions
    INI_checkbutton{
        id: pantograph_checkbutton
        objectName: pantograph_checkbutton

        default_x: 54
        default_y: 226
        box_length: 20

        text: "pantographe ?"

        is_checked: false
        is_activable: true
        is_positive: true
    }

    INI_checkbutton{
        id: thermic_checkbutton
        objectName: thermic_checkbutton

        default_x: pantograph_checkbutton.default_x + 240
        default_y: pantograph_checkbutton.default_y
        box_length: pantograph_checkbutton.box_length

        text: "thermique ?"

        is_checked: false
        is_activable: true
        is_positive: true
    }



    //Tous les composants permettant la paramétrabilité des systèmes de freinage
    //integerinput pour connaitre le nombre de roues utilisant des plaquettes de frein
    INI_text {
        id: wheel_brake_text
        objectName: "wheel_brake_text"

        text: "Nplaquettes"
        font_size: 12

        default_x: wheel_brake_integerinput.default_x + 2
        default_y: wheel_brake_integerinput.default_y - 4 - font_size

        is_dark_grey: false
    }

    INI_integerinput{
        id: wheel_brake_integerinput
        objectName: "wheel_brake_integerinput"

        default_x: 54
        default_y: 321
        default_width: 80
        default_height: 24

        maximum_value: 4e4
        minimum_value: 0

        is_max_default: false
    }

    //integerinput pour connaitre le nombre de Patins magnétiques
    INI_text {
        id: magnetic_brake_text
        objectName: "magnetic_brake_text"

        text: "Npatins magnétiques"
        font_size: 12

        default_x: magnetic_brake_integerinput.default_x + 2
        default_y: magnetic_brake_integerinput.default_y - 4 - font_size

        is_dark_grey: false
    }

    INI_integerinput{
        id: magnetic_brake_integerinput
        objectName: "magnetic_brake_integerinput"

        default_x: wheel_brake_integerinput.default_x + 120
        default_y: wheel_brake_integerinput.default_y
        default_width: wheel_brake_integerinput.default_width
        default_height: wheel_brake_integerinput.default_height

        maximum_value: 4e4
        minimum_value: 0

        is_max_default: false
    }

    //checkbutton pour savoir si le freinage par récupération est activé ?
    INI_checkbutton{
        id: regenerative_checkbutton
        objectName: "regenerative_checkbutton"

        default_x: magnetic_brake_integerinput.default_x + 120
        default_y: magnetic_brake_integerinput.default_y
        box_length: magnetic_brake_integerinput.default_height

        text: "récupération ?"

        is_checked: true
        is_activable: true
        is_positive: true
    }

    //integerinput pour connaitre le nombre de disques
    INI_text {
        id: dic_brake_text
        objectName: "disc_brake_text"

        text: "Ndisques"
        font_size: 12

        default_x: disc_brake_integerinput.default_x + 2
        default_y: disc_brake_integerinput.default_y - 4 - font_size

        is_dark_grey: false
    }

    INI_integerinput{
        id: disc_brake_integerinput
        objectName: "disc_brake_integerinput"

        default_x: wheel_brake_integerinput.default_x
        default_y: wheel_brake_integerinput.default_y + 50
        default_width: wheel_brake_integerinput.default_width
        default_height: wheel_brake_integerinput.default_height

        maximum_value: 4e4
        minimum_value: 0

        is_max_default: false
    }

    //integerinput pour connaitre le nombre de systèmes de freinage de fouccault
    INI_text {
        id: fouccault_brake_text
        objectName: "fouccault_brake_text"

        text: "Nfouccault"
        font_size: 12

        default_x: fouccault_brake_integerinput.default_x + 2
        default_y: fouccault_brake_integerinput.default_y - 4 - font_size

        is_dark_grey: false
    }

    INI_integerinput{
        id: fouccault_brake_integerinput
        objectName: "fouccault_brake_integerinput"

        default_x: magnetic_brake_integerinput.default_x
        default_y: magnetic_brake_integerinput.default_y + 50
        default_width: magnetic_brake_integerinput.default_width
        default_height: magnetic_brake_integerinput.default_height

        maximum_value: 4e4
        minimum_value: 0

        is_max_default: false
    }

    //checkbutton pour savoir si le freinage par récupération est activé ?
    INI_checkbutton{
        id: dynamic_checkbutton
        objectName: "dynamic_checkbutton"

        default_x: regenerative_checkbutton.default_x
        default_y: regenerative_checkbutton.default_y + 50
        box_length: regenerative_checkbutton.box_length

        text: "rhéostatique ?"

        is_checked: true
        is_activable: true
        is_positive: true
    }



    //Boutons permettant d'ouvrir, d'enregistrer et de passer en mode complexe
    //Bouton ouvrir
    INI_button{
        id: open
        objectName: "open"

        default_x: 480
        default_y: 15
        default_height: 50
        default_width: 100

        text: "Ouvrir"

        is_activable: true
        is_positive: true
        is_visible: true
    }

    //Bouton sauvegarder
    INI_button{
        id: save
        objectName: "save"

        default_x: 480
        default_y: 65
        default_height: 50
        default_width: 100

        text: "Sauvegarder"

        is_activable: name_stringinput.text != ""
        is_positive: name_stringinput.text != ""
        is_visible: true
    }

    //Bouton mode de paramétrage
    INI_text {
        id: mode_text
        objectName: "mode_text"

        text: "paramétrage"
        font_size: 12

        default_x: mode.default_x + 2
        default_y: mode.default_y - 4 - font_size

        is_dark_grey: false
    }

    INI_button{
        id: mode
        objectName: "mode"

        default_x: 480
        default_y: 135
        default_height: 30
        default_width: 100

        text: "Simple"

        is_activable: name_stringinput.text != ""
        is_positive: name_stringinput.text != ""
        is_visible: true
    }

    //Bouton de configuration freinage
    INI_button{
        id: brake_configuration
        objectName: "brake_configuration"

        default_x: 480
        default_y: 316
        default_height: 50
        default_width: 100

        text: "Configuration\nfreinage"

        is_activable: true
        is_positive: true
        is_visible: true
    }
}