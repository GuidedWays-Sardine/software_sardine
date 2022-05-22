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
    readonly property double max_length: 1e9            //m
    readonly property int max_railcars: 1e3
    readonly property int max_bogies_per_railcar: 1e1
    readonly property int max_axles_per_bogie: 1e1
    readonly property double max_axles_power: 1e6        //kW
    readonly property double a_max: 1e3                 //kN
    readonly property double b_max: 1e3                 //kN/(km/h)
    readonly property double c_max: 1e3                 //kM/(km/h)²
    readonly property int abc_decimals: 8
    //Par défaut on considèrera : 2 roues (et donc plaquettes) par essieux ; 4 disques par essieux ; 2 patins magnétiques ou de foucault par bogies
    //Pour changer ces valeurs merci de uniquement changer la valeur après le *
    property int max_pad_brakes_per_axle: 1 * 1
    property int max_disk_brakes_per_axle: 4 * 1
    property int max_magnetic_brakes_per_axle: 1 * 1       //Identique pour le freinage de foucault


    //Titres des catégories (le texte des autres composants sera traduit
    property string general_data_text: "Informations générales"
    property string dynamic_data_text: "Dynamique du train (Rav)"
    property string alimentation_data_text: "Systèmes d'alimentation"
    property string brake_data_text: "Systèmes de freinage"


    //Constantes permettant de controller la taille et la position des différents éléments de la page
    readonly property int input_width: 80
    readonly property int input_height: 24
    readonly property int checkbutton_box_length : 18
    readonly property int x_offset: 150
    readonly property int y_offset: 44



    //Nom du matériel roulant (et du fichier dans lequel il sera sauvegardé)
    //stringinput du nom du matériel roulant
    INI_stringinput{
        id: train_name_stringinput
        objectName: "train_name_stringinput"

        default_x: 54
        default_y: 40
        default_width: save_button.default_x - default_x
        default_height: page_rb2.input_height

        max_text_length: 48
        placeholder_text: "Nom du train (utilisé pour le nom du fichier)"
        title: "Nom du train"

        is_activable: true
        is_positive: true
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

        INI_text {
            id: general_data_name
            objectName: "general_data_name"

            default_x: general_data_box.default_x + 1 + (general_data_box.is_positive)
            default_y: general_data_box.default_y + 1 + (general_data_box.is_positive)

            text: page_rb2.general_data_text
            font_size: 12

            is_dark_grey: page_rb2.generated
        }


        //Informations générales du train (masse, longueur, nombre de voitures)
        //floatinput de la masse du convoi
        INI_floatinput{
            id: weight_floatinput
            objectName: "weight_floatinput"

            default_x: general_data_box.default_x + 1 + (general_data_box.is_positive)
            default_y: general_data_box.default_y + 1 + (general_data_box.is_positive) + 3 * general_data_name.font_size
            default_width: page_rb2.input_width
            default_height: page_rb2.input_height

            maximum_value: page_rb2.max_weight
            minimum_value: 0.001 * bogies_count_integerinput.value * axles_per_bogie_integerinput.value
            decimals: 3

            title: "Mconvoi"
            unit: "t"
            font_size: 12

            is_max_default: false
            is_activable: !page_rb2.generated
            is_positive: false

            onValueChanged: {
                //Commence par mettre à jour les limites de masses à l'essieu moteur
                if(motorized_axles_count_integerinput.value == 0 && motorized_axle_weight_floatinput.maximum_value > (weight_floatinput.value / (bogies_count_integerinput.value * axles_per_bogie_integerinput.value))){
                    motorized_axle_weight_floatinput.minimum_value = weight_floatinput.value / (bogies_count_integerinput.value * axles_per_bogie_integerinput.value)
                    motorized_axle_weight_floatinput.maximum_value = weight_floatinput.value / (bogies_count_integerinput.value * axles_per_bogie_integerinput.value)
                }
                else if(motorized_axles_count_integerinput.value == 0 && motorized_axle_weight_floatinput.maximum_value <= (weight_floatinput.value / (bogies_count_integerinput.value * axles_per_bogie_integerinput.value))){
                    motorized_axle_weight_floatinput.maximum_value = weight_floatinput.value / (bogies_count_integerinput.value * axles_per_bogie_integerinput.value)
                    motorized_axle_weight_floatinput.minimum_value = weight_floatinput.value / (bogies_count_integerinput.value * axles_per_bogie_integerinput.value)
                }
                else if(motorized_axles_count_integerinput.value != 0) {
                    motorized_axle_weight_floatinput.minimum_value = 0.001
                    motorized_axle_weight_floatinput.maximum_value = weight_floatinput.value / motorized_axles_count_integerinput.value
                }
            }
        }

        //floatinput de la longueur du train
        INI_floatinput{
            id: length_floatinput
            objectName: "length_floatinput"

            default_x: weight_floatinput.default_x + page_rb2.x_offset
            default_y: weight_floatinput.default_y
            default_width: weight_floatinput.default_width
            default_height: weight_floatinput.default_height

            maximum_value: page_rb2.max_length
            minimum_value: 0.001 * railcars_count_integerinput.value
            decimals: 3

            title: "Lconvoi"
            unit: "m"
            font_size: 12

            is_max_default: false
            is_activable: !page_rb2.generated
            is_positive: false
        }

        //integerinput du nombre de voitures
        INI_integerinput{
            id: railcars_count_integerinput
            objectName: "railcars_count_integerinput"

            default_x: length_floatinput.default_x +  page_rb2.x_offset
            default_y: length_floatinput.default_y
            default_width: length_floatinput.default_width
            default_height: length_floatinput.default_height

            maximum_value: page_rb2.max_railcars
            minimum_value: 1

            title : "Nvoitures"
            font_size: 12

            is_max_default: false
            is_activable: !page_rb2.generated
            is_positive: false

            //Signal appelé lorsque la valeur augmente. Permet de changer le nombre de bogie de façon sécurisée
            onValue_changed: {
                //Dans le cas où la nouvelle valeur est supérieure
                if(bogies_count_integerinput.maximum_value > page_rb2.max_bogies_per_railcar * value) {
                    bogies_count_integerinput.minimum_value = value + 1
                    bogies_count_integerinput.maximum_value = page_rb2.max_bogies_per_railcar * value
                }
                else {
                    bogies_count_integerinput.maximum_value = page_rb2.max_bogies_per_railcar * value
                    bogies_count_integerinput.minimum_value = value + 1
                }
            }
        }


        //Informations sur les bogies du train (nombre de bogies, nombre d'essieux par bogies, nombre d'essieux moteurs)
        //integerinput pour le nombre de bogies sur le train
        INI_integerinput{
            id: bogies_count_integerinput
            objectName: "bogies_count_integerinput"

            default_x: weight_floatinput.default_x
            default_y: weight_floatinput.default_y + page_rb2.y_offset
            default_width: weight_floatinput.default_width
            default_height: weight_floatinput.default_height

            maximum_value: 2
            minimum_value: 2

            title: "Nbogies"
            font_size: 12

            is_max_default: false
            is_activable: !page_rb2.generated
            is_positive: false

            onValueChanged: {
                //Commence par mettre à jour les limites de masses à l'essieu moteur
                if(motorized_axles_count_integerinput.value == 0 && motorized_axle_weight_floatinput.maximum_value > (weight_floatinput.value / (bogies_count_integerinput.value * axles_per_bogie_integerinput.value))){
                    motorized_axle_weight_floatinput.minimum_value = weight_floatinput.value / (bogies_count_integerinput.value * axles_per_bogie_integerinput.value)
                    motorized_axle_weight_floatinput.maximum_value = weight_floatinput.value / (bogies_count_integerinput.value * axles_per_bogie_integerinput.value)
                }
                else if(motorized_axles_count_integerinput.value == 0 && motorized_axle_weight_floatinput.maximum_value <= (weight_floatinput.value / (bogies_count_integerinput.value * axles_per_bogie_integerinput.value))){
                    motorized_axle_weight_floatinput.maximum_value = weight_floatinput.value / (bogies_count_integerinput.value * axles_per_bogie_integerinput.value)
                    motorized_axle_weight_floatinput.minimum_value = weight_floatinput.value / (bogies_count_integerinput.value * axles_per_bogie_integerinput.value)
                }
            }
        }

        //integerinput pour connaitre le nombre d'essieux par bogies
        INI_integerinput{
            id: axles_per_bogie_integerinput
            objectName: "axles_per_bogie_integerinput"

            default_x: length_floatinput.default_x
            default_y: bogies_count_integerinput.default_y
            default_width: length_floatinput.default_width
            default_height: bogies_count_integerinput.default_height

            maximum_value: page_rb2.max_axles_per_bogie
            minimum_value: 1

            title: "Nessieux/bogies"
            font_size: 12

            is_max_default: false
            is_activable: !page_rb2.generated
            is_positive: false

            onValueChanged: {
                //Commence par mettre à jour les limites de masses à l'essieu moteur
                if(motorized_axles_count_integerinput.value == 0 && motorized_axle_weight_floatinput.maximum_value > (weight_floatinput.value / (bogies_count_integerinput.value * axles_per_bogie_integerinput.value))){
                    motorized_axle_weight_floatinput.minimum_value = weight_floatinput.value / (bogies_count_integerinput.value * axles_per_bogie_integerinput.value)
                    motorized_axle_weight_floatinput.maximum_value = weight_floatinput.value / (bogies_count_integerinput.value * axles_per_bogie_integerinput.value)
                }
                else if(motorized_axles_count_integerinput.value == 0 && motorized_axle_weight_floatinput.maximum_value <= (weight_floatinput.value / (bogies_count_integerinput.value * axles_per_bogie_integerinput.value))){
                    motorized_axle_weight_floatinput.maximum_value = weight_floatinput.value / (bogies_count_integerinput.value * axles_per_bogie_integerinput.value)
                    motorized_axle_weight_floatinput.minimum_value = weight_floatinput.value / (bogies_count_integerinput.value * axles_per_bogie_integerinput.value)
                }
            }
        }

        //integerinput pour connaitre le nombre d'essieux moteurs
        INI_integerinput{
            id: motorized_axles_count_integerinput
            objectName: "motorized_axles_count_integerinput"


            default_x: railcars_count_integerinput.default_x
            default_y: axles_per_bogie_integerinput.default_y
            default_width: railcars_count_integerinput.default_width
            default_height: axles_per_bogie_integerinput.default_height

            maximum_value: bogies_count_integerinput.value * axles_per_bogie_integerinput.value
            minimum_value: 0

            title: "Nessieux moteurs"
            font_size: 12

            is_max_default: false
            is_activable: !page_rb2.generated
            is_positive: false

            onValue_changed: {
                //Commence par mettre à jour les limites de masses à l'essieu moteur
                if(motorized_axles_count_integerinput.value == 0 && motorized_axle_weight_floatinput.maximum_value > (weight_floatinput.value / (bogies_count_integerinput.value * axles_per_bogie_integerinput.value))){
                    motorized_axle_weight_floatinput.minimum_value = weight_floatinput.value / (bogies_count_integerinput.value * axles_per_bogie_integerinput.value)
                    motorized_axle_weight_floatinput.maximum_value = weight_floatinput.value / (bogies_count_integerinput.value * axles_per_bogie_integerinput.value)
                }
                else if(motorized_axles_count_integerinput.value == 0 && motorized_axle_weight_floatinput.maximum_value <= (weight_floatinput.value / (bogies_count_integerinput.value * axles_per_bogie_integerinput.value))){
                    motorized_axle_weight_floatinput.maximum_value = weight_floatinput.value / (bogies_count_integerinput.value * axles_per_bogie_integerinput.value)
                    motorized_axle_weight_floatinput.minimum_value = weight_floatinput.value / (bogies_count_integerinput.value * axles_per_bogie_integerinput.value)
                }
                else if(motorized_axles_count_integerinput.value != 0) {
                    motorized_axle_weight_floatinput.minimum_value = 0.001
                    motorized_axle_weight_floatinput.maximum_value = weight_floatinput.value / motorized_axles_count_integerinput.value
                }

                // Si le dernier élément mis à jour est la puissance des moteurs, mets à jour la puissance du train
                power_floatinput.is_modified = true
                axles_power_floatinput.is_modified = true
                if(axles_power_floatinput.last_changed && !power_floatinput.last_changed){
                    power_floatinput.change_value(axles_power_floatinput.value * motorized_axles_count_integerinput.value)
                }
                // Si le dernier élément mis à jour est la puissance du train, mets à jour la puissance des moteurs
                else{
                    if(motorized_axles_count_integerinput.value != 0) {
                        axles_power_floatinput.change_value(power_floatinput.value / motorized_axles_count_integerinput.value)
                    }
                    else{
                        axles_power_floatinput.change_value(0)
                    }
                }
                axles_power_floatinput.is_modified = false
                power_floatinput.is_modified = false
            }
        }


        //Informations sur les essieux motorisés (masse à l'essieu motorisé, puissance moteur, puissance train)
        //integerinput pour connaitre le nombre d'essieux par bogies
        INI_floatinput{
            id: motorized_axle_weight_floatinput
            objectName: "motorized_axle_weight_floatinput"

            default_x: bogies_count_integerinput.default_x
            default_y: bogies_count_integerinput.default_y + page_rb2.y_offset
            default_width: bogies_count_integerinput.default_width
            default_height: bogies_count_integerinput.default_height

            minimum_value: 0.001
            maximum_value: 0.001

            decimals: 3

            title: "masse/essieu moteur"
            unit: "t"
            font_size: 12

            is_max_default: true
            is_positive: false
            is_activable: motorized_axles_count_integerinput.value != 0 && !page_rb2.generated
        }

        //floatinput pour connaitre la puissance de chaque essieux moteurs (relié à la puissance générale
        INI_floatinput{
            id: axles_power_floatinput
            objectName: "axles_power_floatinput"

            //propriété permettant de se souvenir si la puissance du train ou la puissance moteur a été changée en dernier
            //Utile pour savoir quelle puissance mettre à jour lorsque le nombre d'essieux moteurs est changé
            property bool last_changed: false
            property bool is_modified: false

            default_x: axles_per_bogie_integerinput.default_x
            default_y: motorized_axle_weight_floatinput.default_y
            default_width: axles_per_bogie_integerinput.default_width
            default_height: motorized_axles_count_integerinput.default_height

            maximum_value: motorized_axles_count_integerinput.value != 0 ? page_rb2.max_axles_power : 0     //Met la valeur ax à celle indiqué sauf si le train a aucun essieu motorisé (auquel cas à 0)
            minimum_value: 0
            decimals: 3

            title: "Pmoteur"
            unit: "kW"
            font_size: 12

            is_max_default: false
            is_activable: motorized_axles_count_integerinput.value != 0 && !page_rb2.generated
            is_positive: false

            onValue_changed: {
                //Met à jour la puissance générale du train
                if(!power_floatinput.is_modified){
                    power_floatinput.is_modified = true
                    power_floatinput.change_value(axles_power_floatinput.value * motorized_axles_count_integerinput.value)
                    power_floatinput.is_modified = false

                    //Indique qu'il était le dernier à être modifié
                    axles_power_floatinput.last_changed = true
                    power_floatinput.last_changed = false
                }
            }
        }

        //floatinput pour connaitre la puissance totale du train (relié à la puissance moteur)
        INI_floatinput{
            id: power_floatinput
            objectName: "power_floatinput"

            //propriété permettant de se souvenir si la puissance du train ou la puissance moteur a été changée en dernier
            //Utile pour savoir quelle puissance mettre à jour lorsque le nombre d'essieux moteurs est changé
            property bool last_changed: true
            property bool is_modified: false

            default_x: motorized_axles_count_integerinput.default_x
            default_y: axles_power_floatinput.default_y
            default_width: motorized_axle_weight_floatinput.default_width
            default_height: axles_power_floatinput.default_height

            maximum_value: motorized_axles_count_integerinput.value != 0 ? max_axles_power * motorized_axles_count_integerinput.value : 0     //Met la valeur ax à celle indiqué sauf si le train a aucun essieu motorisé (auquel cas à 0)
            minimum_value: 0
            decimals: 3

            title: "Ptrain"
            unit: "kW"
            font_size: 12

            is_max_default: false
            is_activable: motorized_axles_count_integerinput.value != 0 && !page_rb2.generated
            is_positive: false

            onValue_changed: {
                //Met à jour la puissance par essieux du train
                if(!axles_power_floatinput.is_modified){
                    power_floatinput.is_modified = true
                    if(motorized_axles_count_integerinput.value != 0) {
                        axles_power_floatinput.change_value(power_floatinput.value / motorized_axles_count_integerinput.value)
                    }
                    else{
                        axles_power_floatinput.change_value(0)
                    }
                    power_floatinput.is_modified = false

                    //Indique qu'il était le dernier à être modifié
                    axles_power_floatinput.last_changed = false
                    power_floatinput.last_changed = true
                }
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

        INI_text {
            id: dynamic_data_name
            objectName: "dynamic_data_name"

            default_x: dynamic_data_box.default_x + 1 + (dynamic_data_box.is_positive)
            default_y: dynamic_data_box.default_y + 1 + (dynamic_data_box.is_positive)

            text: page_rb2.dynamic_data_text
            font_size: 12

            is_dark_grey: page_rb2.generated
        }


        //Tous les composants par rapport aux coefficients dynamiques (A;B;C)
        //floatinput pour le coefficient A
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

            title: "A :"
            unit: "kN"
            font_size: 12

            is_max_default: false
            is_activable: !page_rb2.generated
            is_positive: false
        }

        INI_text{
            id: v0
            objectName: "v0"

            default_x: (a_floatinput.default_x + a_floatinput.default_width + b_floatinput.default_x - default_text_width) * 0.5
            default_y: a_floatinput.default_y + (a_floatinput.default_height - font_size) * 0.5 - 4

            text: " + "
            font_size: 12

            is_dark_grey: page_rb2.generated
        }

        //floatinput pour le coefficient B
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

            title: "B :"
            unit: "kN/(km/h)"
            font_size: 12

            is_max_default: false
            is_activable: a_floatinput.is_activable
            is_positive: a_floatinput.is_positive
        }

        INI_text{
            id: v1
            objectName: "v1"

            default_x: (b_floatinput.default_x + b_floatinput.default_width + c_floatinput.default_x - default_text_width) * 0.5
            default_y: b_floatinput.default_y + (b_floatinput.default_height - font_size) * 0.5 - 4

            text: "V     +     "
            font_size: v0.font_size

            is_dark_grey: v0.is_dark_grey
        }

        //floatinput pour le coefficient C
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

            title: "C :"
            unit: "kN/(km/h)²"
            font_size: 12

            is_max_default: false
            is_activable: b_floatinput.is_activable
            is_positive: b_floatinput.is_positive
        }

        INI_text{
            id: v2
            objectName: "v2"

            default_x: c_floatinput.default_x + c_floatinput.default_width + (default_text_width) * 0.5
            default_y: c_floatinput.default_y + (c_floatinput.default_height - font_size) * 0.5 - 2

            text: "V²"
            font_size: v1.font_size

            is_dark_grey: v1.is_dark_grey
        }
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

        INI_text {
            id: alimentation_data_name
            objectName: "alimentation_data_name"

            default_x: alimentation_data_box.default_x + 1 + (alimentation_data_box.is_positive)
            default_y: alimentation_data_box.default_y + 1 + (alimentation_data_box.is_positive)

            text: page_rb2.alimentation_data_text
            font_size: 12

            is_dark_grey: motorized_axles_count_integerinput.value == 0 || page_rb2.generated
        }


        //Tous les composants permetant d'indiquer les électrifications disponibles (életrique et thermique)
        //checkbutton pour indiquer si le train a des pantographes (en mode simplifié on le considère compatible avec toutes les tensions
        INI_checkbutton{
            id: pantograph_check
            objectName: "pantograph_check"

            default_x: alimentation_data_box.default_x + 1 + (alimentation_data_box.is_positive)
            default_y: alimentation_data_box.default_y + 1 + (alimentation_data_box.is_positive) + 1.5 * alimentation_data_name.font_size
            box_length: page_rb2.checkbutton_box_length

            title: "Pantographe ?"

            is_checked: false
            is_activable: motorized_axles_count_integerinput.value != 0 && !page_rb2.generated
            is_positive: false

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

            title: "Thermique ?"

            is_checked: false
            is_activable: motorized_axles_count_integerinput.value != 0 && !page_rb2.generated
            is_positive: pantograph_check.is_positive

            // Si le nombre d'essieux moteurs repasse à 0 décoche la case
            onIs_activableChanged: {
                if(!thermic_check.is_activable){
                    thermic_check.is_checked = false
                }
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

        INI_text {
            id: brake_data_name
            objectName: "brake_data_name"

            default_x: brake_data_box.default_x + 1 + (brake_data_box.is_positive)
            default_y: brake_data_box.default_y + 1 + (brake_data_box.is_positive)

            text: page_rb2.brake_data_text
            font_size: 12

            is_dark_grey: page_rb2.generated
        }


        //Tous les composants permettant de paramétrer les freinages
        //integerinput pour connaitre le nombre de roues utilisant des plaquettes de frein
        INI_integerinput{
            id: pad_brakes_count_integerinput
            objectName: "pad_brakes_count_integerinput"

            default_x: brake_data_box.default_x + 1 + (brake_data_box.is_positive)
            default_y: brake_data_box.default_y + 1 + (brake_data_box.is_positive) + 3 * brake_data_name.font_size - 2
            default_width: page_rb2.input_width
            default_height: page_rb2.input_height

            maximum_value: page_rb2.max_pad_brakes_per_axle * bogies_count_integerinput.value * axles_per_bogie_integerinput.value
            minimum_value: 0

            title: "Nplaquettes (paires)"
            font_size: 12

            is_max_default: false
            is_activable: !page_rb2.generated
            is_positive: false
        }

        //integerinput pour connaitre le nombre de disques
            INI_integerinput{
            id: disk_brakes_count_integerinput
            objectName: "disk_brakes_count_integerinput"

            default_x: pad_brakes_count_integerinput.default_x + page_rb2.x_offset
            default_y: pad_brakes_count_integerinput.default_y
            default_width: pad_brakes_count_integerinput.default_width
            default_height: pad_brakes_count_integerinput.default_height

            maximum_value: page_rb2.max_disk_brakes_per_axle * bogies_count_integerinput.value * axles_per_bogie_integerinput.value
            minimum_value: 0

            title: "Ndisques"
            font_size: 12

            is_max_default: false
            is_activable: !page_rb2.generated
            is_positive: pad_brakes_count_integerinput.is_positive
        }

        //checkbutton pour savoir si le freinage par récupération est activé ?
        INI_checkbutton{
            id: regenerative_check
            objectName: "regenerative_check"

            default_x: disk_brakes_count_integerinput.default_x + page_rb2.x_offset
            default_y: disk_brakes_count_integerinput.default_y + (page_rb2.input_height - page_rb2.checkbutton_box_length) * 0.5
            box_length: page_rb2.checkbutton_box_length

            title: "Récupération ?"
            font_size: 12

            is_checked: false
            is_activable: pantograph_check.is_checked && !page_rb2.generated
            is_positive: false

            onIs_activableChanged: {
                if(!regenerative_check.is_activable){
                    is_checked = false
                }
            }
        }

        //integerinput pour connaitre le nombre de Patins magnétiques
        INI_integerinput{
            id: magnetic_brakes_count_integerinput
            objectName: "magnetic_brakes_count_integerinput"

            default_x: pad_brakes_count_integerinput.default_x
            default_y: pad_brakes_count_integerinput.default_y + page_rb2.y_offset - 4
            default_width: pad_brakes_count_integerinput.default_width
            default_height: pad_brakes_count_integerinput.default_height

            maximum_value: -foucault_brakes_count_integerinput.value + page_rb2.max_magnetic_brakes_per_axle * bogies_count_integerinput.value * (axles_per_bogie_integerinput.value - 1)
            minimum_value: 0

            title: "Nmagnétique (paires)"
            font_size: 12

            is_max_default: false
            is_activable: (axles_per_bogie_integerinput.value > 1) && !page_rb2.generated
            is_positive: pad_brakes_count_integerinput.is_positive
        }

        //integerinput pour connaitre le nombre de systèmes de freinage de foucault
        INI_integerinput{
            id: foucault_brakes_count_integerinput
            objectName: "foucault_brakes_count_integerinput"

            default_x: magnetic_brakes_count_integerinput.default_x + page_rb2.x_offset
            default_y: magnetic_brakes_count_integerinput.default_y
            default_width: magnetic_brakes_count_integerinput.default_width
            default_height: magnetic_brakes_count_integerinput.default_height

            maximum_value: -magnetic_brakes_count_integerinput.value + page_rb2.max_magnetic_brakes_per_axle * bogies_count_integerinput.value * (axles_per_bogie_integerinput.value - 1)
            minimum_value: 0

            title: "Nfoucault (paires)"
            font_size: 12

            is_max_default: false
            is_activable: (axles_per_bogie_integerinput.value > 1) && !page_rb2.generated
            is_positive: disk_brakes_count_integerinput.is_positive
        }

        //checkbutton pour savoir si le freinage par récupération est activé ?
        INI_checkbutton{
            id: dynamic_check
            objectName: "dynamic_check"

            default_x: foucault_brakes_count_integerinput.default_x + page_rb2.x_offset
            default_y: foucault_brakes_count_integerinput.default_y + (page_rb2.input_height - page_rb2.checkbutton_box_length) * 0.5
            box_length: regenerative_check.box_length

            title: "Rhéostatique ?"

            is_checked: false
            is_activable: motorized_axles_count_integerinput.value != 0 && !page_rb2.generated
            is_positive: false

            onIs_activableChanged: {
                if(!dynamic_check.is_activable){
                     dynamic_check.is_checked = false
                }
            }
        }
    }


    //Tous les boutons annexes (situés à droite de la page)
    //switchbutton permettant de choisir le mode de paramétrage (simple ou complexe)
    INI_switchbutton {
        id: mode_switchbutton
        objectName: "mode_switchbutton"

        default_x: 480
        default_y: train_name_stringinput.default_y
        default_width: 100
        default_height: train_name_stringinput.default_height

        elements: ["Simple", "Complexe"]

        title: "Paramétrage"
        font_size: 12

        is_activable: false         //Activé après l'initialisation de la popup de paramétrage complexe
        is_positive: false
    }

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

        is_activable: train_name_stringinput.value != ""
        is_positive: train_name_stringinput.value != ""
    }

    //Bouton de configuration freinage
    INI_button{
        id: brake_button
        objectName: "brake_button"

        default_x: save_button.default_x
        default_height: save_button.default_height
        default_y: brake_data_box.default_y
        default_width: save_button.default_width

        text: "Freinage"

        is_activable: false     //Activé après l'initialisation de la popup de paramétrage freinage
        is_positive: false
    }

    //Combobox permettant de choisir le type de missions réalisés par le matériel roulant
    INI_combobox{
        id: mission_type_combo
        objectName: "mission_type_combo"

        default_x: mode_switchbutton.default_x
        default_y: 65
        default_width: mode_switchbutton.default_width
        default_height: 50

        elements: ["Voyageurs", "Fret"]

        is_positive: true
        is_activable: !page_rb2.generated
    }
}
