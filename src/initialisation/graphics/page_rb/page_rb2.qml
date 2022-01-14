import QtQuick 2.0
import QtQuick.Controls 2.15
import "../../components"


Item {
    id: page_rb2
    objectName: "page_rb2"


    //Information permettant de savoir si le mode complex a été activé
    property bool generated: false


    //Constantes permettant de controller les différentes valeurs maximales de chacun des trains
    readonly property double max_weight: 1e9            //t
    readonly property double max_length: 1e9            //mf
    readonly property int max_coaches: 1e3
    readonly property int max_bogies: 2 * coaches_integerinput.value
    readonly property int max_axles_per_bogies: 1e1
    readonly property double max_motor_power: 1e6       //kW
    readonly property double max_power: max_motor_power * motorized_axles_count_integerinput.value      //NE PAS CHANGER
    readonly property double a_max: 1e3                 //kN
    readonly property double b_max: 1e3                 //kN/(km/h)
    readonly property double c_max: 1e3                 //kM/(km/h)²
    readonly property int abc_decimals: 8
    //Par défautl on considèrera : 2 roues (et donc plaquettes) par essieux ; 4 disques par essieux ; 2 patins magnétiques ou de foucault par bogies
    readonly property int max_brake_pad: 2 * bogies_count_integerinput.value * axles_per_bogies_integerinput.value * 1      //Uniquement changer la dernière constante
    readonly property int max_brake_disk:4 * bogies_count_integerinput.value * axles_per_bogies_integerinput.value * 1      //Uniquement changer la dernière constante
    readonly property int max_brake_magnetic: -foucault_brake_integerinput.value + 2 * bogies_count_integerinput.value * (axles_per_bogies_integerinput.value - 1) * 1 //Uniquement changer la dernière constante
    readonly property int max_brake_foucault: -magnetic_brake_integerinput.value + 2 * bogies_count_integerinput.value * (axles_per_bogies_integerinput.value - 1) * 1 //Uniquement changer la dernière constante


    //Constantes permettant de controller la taille et la position des différents éléments de la page
    readonly property int input_width: 80
    readonly property int input_height: 24
    readonly property int checkbutton_box_length : 18
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
        default_width: save_button.default_x - default_x
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

        is_dark_grey: page_rb2.generated
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

        is_dark_grey: page_rb2.generated
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
        default_width: page_rb2.input_width
        default_height: page_rb2.input_height

        maximum_value: page_rb2.max_weight
        minimum_value: 0.001 * bogies_count_integerinput.value * axles_per_bogies_integerinput.value
        decimals: 3

        is_max_default: false
        is_activable: !page_rb2.generated
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

        is_dark_grey: page_rb2.generated
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
        is_activable: !page_rb2.generated
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

        is_dark_grey: page_rb2.generated
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
        is_activable: !page_rb2.generated
        is_positive: false
        is_visible: true

        //Signal appelé lorsque la valeur augmente. Permet de changer le nombre de bogie de façon sécurisée
        onValue_changed: {
            //Dans le cas où la nouvelle valeur est supérieure
            if(bogies_count_integerinput.maximum_value > 2 * value) {
                bogies_count_integerinput.minimum_value = value + 1
                bogies_count_integerinput.maximum_value = 2 * value
            }
            else {
                bogies_count_integerinput.maximum_value = 2 * value
                bogies_count_integerinput.minimum_value = value + 1
            }
        }
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

        is_dark_grey: page_rb2.generated
        is_visible: true
    }

    INI_integerinput{
        id: bogies_count_integerinput
        objectName: "bogies_count_integerinput"

        default_x: weight_floatinput.default_x
        default_y: weight_floatinput.default_y + page_rb2.y_offset
        default_width: weight_floatinput.default_width
        default_height: weight_floatinput.default_height

        maximum_value: 2
        minimum_value: 2

        is_max_default: true
        is_activable: !page_rb2.generated
        is_positive: false
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

        is_dark_grey: page_rb2.generated
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
        is_activable: !page_rb2.generated
        is_positive: false
        is_visible: true
    }

    //integerinput pour connaitre le nombre d'essieux moteurs
    INI_text {
        id: motorized_axles_count_text
        objectName: "motorized_axles_count_text"

        text: "Nessieux moteurs"
        font_size: 12

        default_x: motorized_axles_count_integerinput.default_x + 2
        default_y: motorized_axles_count_integerinput.default_y - 4 - font_size

        is_dark_grey: page_rb2.generated
        is_visible: true
    }

    INI_integerinput{
        id: motorized_axles_count_integerinput
        objectName: "motorized_axles_count_integerinput"


        default_x: coaches_integerinput.default_x
        default_y: axles_per_bogies_integerinput.default_y
        default_width: coaches_integerinput.default_width
        default_height: axles_per_bogies_integerinput.default_height

        maximum_value: bogies_count_integerinput.value * axles_per_bogies_integerinput.value
        minimum_value: 0

        is_max_default: false
        is_activable: !page_rb2.generated
        is_positive: false
        is_visible: true

        onValue_changed: {
            //Commence par changer la valeur de la masse à l'essieu
            if(motorized_axles_count_integerinput.value != 0){
                motorized_axle_weight_floatinput.change_value(weight_floatinput.value / (bogies_count_integerinput.value * axles_per_bogies_integerinput.value))
            }
            else {
                motorized_axle_weight_floatinput.clear()
            }

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



    //Tous les composants reliés au paramétrage de la puissance moteur
    //integerinput pour connaitre le nombre d'essieux par bogies
    INI_text {
        id: motorized_axle_weight_text
        objectName: "motorized_axle_weight_text"

        default_x: motorized_axle_weight_floatinput.default_x + 2
        default_y: motorized_axle_weight_floatinput.default_y - 4 - font_size

        text: "masse/essieu moteur"
        font_size: 12

        is_dark_grey: motorized_axles_count_integerinput.value == 0 || page_rb2.generated
        is_visible: true
    }

    INI_text {
        id: motorized_axle_weight_unit_text
        objectName: "motorized_axle_weight_unit_text"

        default_x: motorized_axle_weight_floatinput.default_x + motorized_axle_weight_floatinput.default_width + 2
        default_y: motorized_axle_weight_floatinput.default_y + motorized_axle_weight_floatinput.default_height - 2 - font_size

        text: "t"
        font_size: 6

        is_dark_grey: true
        is_visible: true
    }

    INI_floatinput{
        id: motorized_axle_weight_floatinput
        objectName: "motorized_axle_weight_floatinput"

        default_x: bogies_count_integerinput.default_x
        default_y: bogies_count_integerinput.default_y + page_rb2.y_offset
        default_width: bogies_count_integerinput.default_width
        default_height: bogies_count_integerinput.default_height

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
        is_activable: motorized_axles_count_integerinput.value != 0 && !page_rb2.generated
        is_visible: true
    }

    //floatinput pour connaitre la puissance de chaque essieux moteurs (relié à la puissance générale
    INI_text {
        id: axle_power_text
        objectName: "axle_power_text"

        text: "Pmoteur"
        font_size: 12

        default_x: axle_power_floatinput.default_x + 2
        default_y: axle_power_floatinput.default_y - 4 - font_size

        is_dark_grey: motorized_axles_count_integerinput.value == 0 || page_rb2.generated
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
        default_y: motorized_axle_weight_floatinput.default_y
        default_width: axles_per_bogies_integerinput.default_width
        default_height: motorized_axles_count_integerinput.default_height

        maximum_value: motorized_axles_count_integerinput.value != 0 ? page_rb2.max_motor_power : 0     //Met la valeur ax à celle indiqué sauf si le train a aucun essieu motorisé (auquel cas à 0)
        minimum_value: 0
        decimals: 3

        is_max_default: false
        is_activable: motorized_axles_count_integerinput.value != 0 && !page_rb2.generated
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

        is_dark_grey: motorized_axles_count_integerinput.value == 0 || page_rb2.generated
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

        default_x: motorized_axles_count_integerinput.default_x
        default_y: axle_power_floatinput.default_y
        default_width: motorized_axle_weight_floatinput.default_width
        default_height: axle_power_floatinput.default_height

        maximum_value: motorized_axles_count_integerinput.value != 0 ? page_rb2.max_power : 0     //Met la valeur ax à celle indiqué sauf si le train a aucun essieu motorisé (auquel cas à 0)
        minimum_value: 0
        decimals: 3

        is_max_default: false
        is_activable: motorized_axles_count_integerinput.value != 0 && !page_rb2.generated
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



    //Tous les composants reliés au paramétrage des informations dynamiques (efforts résistants) du train
    INI_button {
        id: dynamic_data_box
        objectName: "dynamic_data_box"

        default_x: train_name_stringinput.default_x
        default_y: general_data_box.default_y + general_data_box.default_height
        default_width: train_name_stringinput.default_width
        default_height: 1*50 + 12

        is_activable: false
        is_positive: general_data_box.is_positive
        is_visible: true
    }

    INI_text {
        id: dynamic_data_name
        objectName: "dynamic_data_name"

        default_x: dynamic_data_box.default_x + 1 + (dynamic_data_box.is_positive)
        default_y: dynamic_data_box.default_y + 1 + (dynamic_data_box.is_positive)

        text: "Dynamique du train (Rav)"
        font_size: 12

        is_dark_grey: page_rb2.generated
        is_visible: true
    }



    //floatinput pour le coefficient A
    INI_text {
        id: a_text
        objectName: "a_text"

        text: "A"
        font_size: 12

        default_x: a_floatinput.default_x + 2
        default_y: a_floatinput.default_y - 4 - font_size

        is_dark_grey: page_rb2.generated
        is_visible: true
    }

    INI_text {
        id: a_unit_text
        objectName: "a_unit_text"

        text: "kN"
        font_size: 6

        default_x: a_floatinput.default_x + a_floatinput.default_width + 2
        default_y: a_floatinput.default_y + a_floatinput.default_height - 2 - font_size

        is_dark_grey: true
        is_visible: true
    }

    INI_floatinput{
        id: a_floatinput
        objectName: "a_floatinput"

        default_x: dynamic_data_box.default_x + 1 + (dynamic_data_box.is_positive)
        default_y: dynamic_data_box.default_y + 1 + (dynamic_data_box.is_positive) + 3 * font_size
        default_width: page_rb2.input_width
        default_height: page_rb2.input_height

        maximum_value: page_rb2.a_max
        minimum_value: 0
        decimals: page_rb2.abc_decimals

        is_max_default: false
        is_activable: !page_rb2.generated
        is_positive: false
        is_visible: true
    }

    INI_text{
        id: v0
        objectName: "v0"

        text: " + "
        font_size: 12

        default_x: (a_floatinput.default_x + a_floatinput.default_width + b_floatinput.default_x - default_text_width) * 0.5
        default_y: a_floatinput.default_y + (a_floatinput.default_height - font_size) * 0.5 - 4

        is_dark_grey: page_rb2.generated
        is_visible: true
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
        is_visible: true
    }

    INI_text {
        id: b_unit_text
        objectName: "b_unit_text"

        text: "kN/(km/h)"
        font_size: a_unit_text.font_size

        default_x: b_floatinput.default_x + b_floatinput.default_width + 2
        default_y: b_floatinput.default_y + b_floatinput.default_height - 2 - font_size

        is_dark_grey: a_unit_text.is_dark_grey
        is_visible: true
    }

    INI_floatinput{
        id: b_floatinput
        objectName: "b_floatinput"

        default_x: a_floatinput.default_x + page_rb2.x_offset
        default_y: a_floatinput.default_y
        default_width: a_floatinput.default_width
        default_height: a_floatinput.default_height

        maximum_value: page_rb2.b_max
        minimum_value: 0
        decimals: page_rb2.abc_decimals

        is_max_default: false
        is_activable: a_floatinput.is_activable
        is_positive: a_floatinput.is_positive
        is_visible: true
    }

    INI_text{
        id: v1
        objectName: "v1"

        text: "V  + "
        font_size: v0.font_size

        default_x: (b_floatinput.default_x + b_floatinput.default_width + c_floatinput.default_x - default_text_width) * 0.5
        default_y: b_floatinput.default_y + (b_floatinput.default_height - font_size) * 0.5 - 4

        is_dark_grey: v0.is_dark_grey
        is_visible: true
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
        is_visible: true
    }

    INI_text {
        id: c_unit_text
        objectName: "c_unit_text"

        text: "kN/(km/h)²"
        font_size: b_unit_text.font_size

        default_x: c_floatinput.default_x + c_floatinput.default_width + 2
        default_y: c_floatinput.default_y + c_floatinput.default_height - 2 - font_size

        is_dark_grey: b_unit_text.is_dark_grey
        is_visible: true
    }

    INI_floatinput{
        id: c_floatinput
        objectName: "c_floatinput"

        default_x: b_floatinput.default_x + page_rb2.x_offset
        default_y: b_floatinput.default_y
        default_width: b_floatinput.default_width
        default_height: b_floatinput.default_height

        maximum_value: page_rb2.c_max
        minimum_value: 0
        decimals: page_rb2.abc_decimals

        is_max_default: false
        is_activable: b_floatinput.is_activable
        is_positive: b_floatinput.is_positive
        is_visible: true
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
    INI_button {
        id: alimentation_data_box
        objectName: "alimentation_data_box"

        default_x: train_name_stringinput.default_x
        default_y: dynamic_data_box.default_y + dynamic_data_box.default_height
        default_width: train_name_stringinput.default_width
        default_height: 1*50 - 12

        is_activable: false
        is_positive: dynamic_data_box.is_positive
        is_visible: true
    }

    INI_text {
        id: alimentation_data_name
        objectName: "alimentation_data_name"

        default_x: alimentation_data_box.default_x + 1 + (alimentation_data_box.is_positive)
        default_y: alimentation_data_box.default_y + 1 + (alimentation_data_box.is_positive)

        text: "Systèmes d'alimentation"
        font_size: 12

        is_dark_grey: motorized_axles_count_integerinput.value == 0 || page_rb2.generated
        is_visible: true
    }



    //checkbutton pour indiquer si le train a des pantographes (en mode simplifié on le considère compatible avec toutes les tensions
    INI_checkbutton{
        id: pantograph_check
        objectName: "pantograph_check"

        default_x: alimentation_data_box.default_x + 1 + (alimentation_data_box.is_positive)
        default_y: alimentation_data_box.default_y + 1 + (alimentation_data_box.is_positive) + 1.5 * alimentation_data_name.font_size
        box_length: page_rb2.checkbutton_box_length

        text: "Pantographe ?"

        is_checked: false
        is_activable: motorized_axles_count_integerinput.value != 0 && !page_rb2.generated
        is_positive: true
        is_visible: true

        // Si le nombre d'essieux moteurs repasse à 0 décoche la case
        onIs_activableChanged: {
            if(!pantograph_check.is_activable){
                pantograph_check.is_checked = false
            }
        }
    }


    //checkbutton pour indiquer si le train a un système d'alimentation thermique
    INI_checkbutton{
        id: thermic_check
        objectName: "thermic_check"

        default_x: pantograph_check.default_x + 2 * page_rb2.x_offset
        default_y: pantograph_check.default_y
        box_length: pantograph_check.box_length

        text: "Thermique ?"

        is_checked: false
        is_activable: motorized_axles_count_integerinput.value != 0 && !page_rb2.generated
        is_positive: pantograph_check.is_positive
        is_visible: true

        // Si le nombre d'essieux moteurs repasse à 0 décoche la case
        onIs_activableChanged: {
            if(!thermic_check.is_activable){
                thermic_check.is_checked = false
            }
        }
    }



    //Tous les composants permettant la paramétrabilité des systèmes de freinage
    INI_button {
        id: brake_data_box
        objectName: "brake_data_box"

        default_x: train_name_stringinput.default_x
        default_y: alimentation_data_box.default_y + alimentation_data_box.default_height
        default_width: train_name_stringinput.default_width
        default_height: 2*50

        is_activable: false
        is_positive: alimentation_data_box.is_positive
        is_visible: true
    }

    INI_text {
        id: brake_data_name
        objectName: "brake_data_name"

        default_x: brake_data_box.default_x + 1 + (brake_data_box.is_positive)
        default_y: brake_data_box.default_y + 1 + (brake_data_box.is_positive)

        text: "Systèmes de freinage"
        font_size: 12

        is_dark_grey: page_rb2.generated
        is_visible: true
    }


    //integerinput pour connaitre le nombre de roues utilisant des plaquettes de frein
    INI_text {
        id: pad_brake_text
        objectName: "pad_brake_text"

        text: "Nplaquettes"
        font_size: 12

        default_x: pad_brake_integerinput.default_x + 2
        default_y: pad_brake_integerinput.default_y - 4 - font_size

        is_dark_grey: page_rb2.generated
        is_visible: true
    }

    INI_integerinput{
        id: pad_brake_integerinput
        objectName: "pad_brake_integerinput"

        default_x: brake_data_box.default_x + 1 + (brake_data_box.is_positive)
        default_y: brake_data_box.default_y + 1 + (brake_data_box.is_positive) + 3 * brake_data_name.font_size - 2
        default_width: page_rb2.input_width
        default_height: page_rb2.input_height

        maximum_value: page_rb2.max_brake_pad
        minimum_value: 0

        is_max_default: false
        is_activable: !page_rb2.generated
        is_positive: false
        is_visible: true
    }

    //integerinput pour connaitre le nombre de Patins magnétiques
    INI_text {
        id: magnetic_brake_text
        objectName: "magnetic_brake_text"

        text: "Npatins magnétiques"
        font_size: 12

        default_x: magnetic_brake_integerinput.default_x + 2
        default_y: magnetic_brake_integerinput.default_y - 4 - font_size

        is_dark_grey: (axles_per_bogies_integerinput.value <= 1) || page_rb2.generated
        is_visible: true
    }

    INI_integerinput{
        id: magnetic_brake_integerinput
        objectName: "magnetic_brake_integerinput"

        default_x: pad_brake_integerinput.default_x + page_rb2.x_offset
        default_y: pad_brake_integerinput.default_y
        default_width: pad_brake_integerinput.default_width
        default_height: pad_brake_integerinput.default_height

        maximum_value: page_rb2.max_brake_magnetic
        minimum_value: 0

        is_max_default: false
        is_activable: (axles_per_bogies_integerinput.value > 1) && !page_rb2.generated
        is_positive: pad_brake_integerinput.is_positive
        is_visible: true
    }

    //checkbutton pour savoir si le freinage par récupération est activé ?
    INI_checkbutton{
        id: regenerative_check
        objectName: "regenerative_check"

        default_x: magnetic_brake_integerinput.default_x + page_rb2.x_offset
        default_y: magnetic_brake_integerinput.default_y + (page_rb2.input_height - page_rb2.checkbutton_box_length) * 0.5
        box_length: page_rb2.checkbutton_box_length

        text: "Récupération ?"

        is_checked: false
        is_activable: pantograph_check.is_checked && !page_rb2.generated
        is_positive: true

        onIs_activableChanged: {
            if(!regenerative_check.is_activable){
                is_checked = false
            }
        }
    }

    //integerinput pour connaitre le nombre de disques
    INI_text {
        id: disk_brake_text
        objectName: "disk_brake_text"

        text: "Ndisques"
        font_size: 12

        default_x: disk_brake_integerinput.default_x + 2
        default_y: disk_brake_integerinput.default_y - 4 - font_size

        is_dark_grey: page_rb2.generated
        is_visible: true
    }

    INI_integerinput{
        id: disk_brake_integerinput
        objectName: "disk_brake_integerinput"

        default_x: pad_brake_integerinput.default_x
        default_y: pad_brake_integerinput.default_y + page_rb2.y_offset - 4
        default_width: pad_brake_integerinput.default_width
        default_height: pad_brake_integerinput.default_height

        maximum_value: page_rb2.max_brake_disk
        minimum_value: 0

        is_max_default: false
        is_activable: !page_rb2.generated
        is_positive: pad_brake_integerinput.is_positive
        is_visible: true
    }

    //integerinput pour connaitre le nombre de systèmes de freinage de foucault
    INI_text {
        id: foucault_brake_text
        objectName: "foucault_brake_text"

        text: "Nfoucault"
        font_size: 12

        default_x: foucault_brake_integerinput.default_x + 2
        default_y: foucault_brake_integerinput.default_y - 4 - font_size

        is_dark_grey: (axles_per_bogies_integerinput.value <= 1) || page_rb2.generated
        is_visible: true
    }

    INI_integerinput{
        id: foucault_brake_integerinput
        objectName: "foucault_brake_integerinput"

        default_x: disk_brake_integerinput.default_x + page_rb2.x_offset
        default_y: disk_brake_integerinput.default_y
        default_width: magnetic_brake_integerinput.default_width
        default_height: magnetic_brake_integerinput.default_height

        maximum_value: page_rb2.max_brake_foucault
        minimum_value: 0

        is_max_default: false
        is_activable: (axles_per_bogies_integerinput.value > 1) && !page_rb2.generated
        is_positive: disk_brake_integerinput.is_positive
        is_visible: true
    }

    //checkbutton pour savoir si le freinage par récupération est activé ?
    INI_checkbutton{
        id: dynamic_check
        objectName: "dynamic_check"

        default_x: foucault_brake_integerinput.default_x + page_rb2.x_offset
        default_y: foucault_brake_integerinput.default_y + (page_rb2.input_height - page_rb2.checkbutton_box_length) * 0.5
        box_length: regenerative_check.box_length

        text: "Rhéostatique ?"

        is_checked: false
        is_activable: motorized_axles_count_integerinput.value != 0 && !page_rb2.generated
        is_positive: true
        
        onIs_activableChanged: {
            if(!dynamic_check.is_activable){
                 dynamic_break.is_checked = false
            }
        }
    }



    //Bouton permettant de changer le mode de paramétrage (simple ou complexe)
    INI_text {
        id: mode_text
        objectName: "mode_text"

        text: "Paramétrage"
        font_size: 12

        default_x: mode_button.default_x + 2
        default_y: mode_button.default_y - 4 - font_size

        is_dark_grey: mode_button.is_activable
        is_visible: true
    }

    INI_button{
        id: mode_button
        objectName: "mode_button"

        default_x: 480
        default_y: train_name_stringinput.default_y
        default_width: 100
        default_height: train_name_stringinput.default_height

        text: "Simple"

        is_activable: false     //Changé lorsque logique initialisée
        is_positive: is_activable
        is_visible: true
    }



    //Combobox permettant de choisir le type de missions réalisés par le matériel roulant
    INI_combobox{
        id: mission_type_combo
        objectName: "mission_type_combo"

        default_x: mode_button.default_x
        default_y: 65
        default_width: mode_button.default_width
        default_height: 50

        elements: ["Voyageurs", "Fret"]

        is_positive: true
        is_activable: !page_rb2.generated
        is_visible: true
    }



    //Boutons permettant d'ouvrir et d'enregistrer le fichier train
    //Bouton ouvrir
    INI_button{
        id: open_button
        objectName: "open_button"

        default_x: mission_type_combo.default_x
        default_y: mission_type_combo.default_y + 2* 50
        default_width: mission_type_combo.default_width
        default_height: mission_type_combo.default_height

        text: "Ouvrir"

        is_activable: true
        is_positive: true
        is_visible: true
    }

    //Bouton sauvegarder
    INI_button{
        id: save_button
        objectName: "save_button"

        default_x: open_button.default_x
        default_y: open_button.default_y + 50
        default_width: open_button.default_width
        default_height: open_button.default_height

        text: "Sauvegarder"

        is_activable: train_name_stringinput.text != ""
        is_positive: train_name_stringinput.text != ""
        is_visible: true
    }



    //Bouton de configuration freinage
    INI_button{
        id: brake_configuration_button
        objectName: "brake_configuration_button"

        default_x: save_button.default_x
        default_height: save_button.default_height
        default_y: brake_data_box.default_y
        default_width: save_button.default_width

        text: "Freinage"

        is_activable: false
        is_positive: true
        is_visible: true
    }
}