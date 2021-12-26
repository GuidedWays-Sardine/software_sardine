import QtQuick 2.0
import QtQuick.Controls 2.15
import "../../components"


Item {
    id: page_rb2
    objectName: "page_rb2"



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

        default_x: a_floatinput.default_x + a_floatinput.default_width - default_text_width - 2
        default_y: a_floatinput.default_y - 4 - font_size

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

        default_x: b_floatinput.default_x + b_floatinput.default_width - default_text_width - 2
        default_y: b_floatinput.default_y - 4 - font_size

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

        default_x: c_floatinput.default_x + c_floatinput.default_width - default_text_width - 2
        default_y: c_floatinput.default_y - 4 - font_size

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



    //Tous les composants reliés au paramétrage des essieux
    //integerinput pour le nombre de bogies sur le train
    INI_text {
        id: bogies_text
        objectName: "bogies_text"

        text: "Nbogies"
        font_size: 12

        default_x: bogies_floatinput.default_x + 2
        default_y: bogies_floatinput.default_y - 4 - font_size

        is_dark_grey: false
    }

    INI_integerinput{
        id: bogies_floatinput
        objectName: "bogies_floatinput"

        default_x: 54
        default_y: 141
        default_width: 80
        default_height: 24

        maximum_value: 2e4
        minimum_value: 1

        is_max_default: false
    }

    //integerinput pour connaitre le nombre d'essieux par bogies
    INI_text {
        id: axles_text
        objectName: "axles_text"

        text: "essieux/bogies"
        font_size: 12

        default_x: axles_integerinput.default_x + 2
        default_y: axles_integerinput.default_y - 4 - font_size

        is_dark_grey: false
    }

    INI_integerinput{
        id: axles_integerinput
        objectName: "axles_integerinput"

        default_x: bogies_floatinput.default_x + 120
        default_y: bogies_floatinput.default_y
        default_width: bogies_floatinput.default_width
        default_height: bogies_floatinput.default_height

        maximum_value: 10
        minimum_value: 1

        is_max_default: false
    }

    //integerinput pour connaitre le nombre d'essieux par bogies
    INI_text {
        id: motorized_axle_wheight_text
        objectName: "motorized_axle_wheight_text"

        text: "masse/essieu moteur"
        font_size: 12

        default_x: motorized_axle_wheight_floatinput.default_x + 2
        default_y: motorized_axle_wheight_floatinput.default_y - 4 - font_size

        is_dark_grey: false
    }

    INI_text {
        id: motorized_axle_wheight_unit_text
        objectName: "motorized_axle_wheight_unit_text"

        text: "t"
        font_size: 6

        default_x: motorized_axle_wheight_floatinput.default_x + motorized_axle_wheight_floatinput.default_width - default_text_width - 2
        default_y: motorized_axle_wheight_floatinput.default_y - 4 - font_size

        is_dark_grey: true
    }

    INI_floatinput{
        id: motorized_axle_wheight_floatinput
        objectName: "motorized_axle_wheight_floatinput"

        default_x: axles_integerinput.default_x + 120
        default_y: axles_integerinput.default_y
        default_width: axles_integerinput.default_width
        default_height: axles_integerinput.default_height

        maximum_value: 1e9
        minimum_value: 0.001
        decimals: 3

        is_max_default: false
    }



    //Tous les composants reliés au paramétrage de la puissance moteur
    //integerinput pour connaitre le nombre d'essieux moteurs
    INI_text {
        id: motorized_axles_text
        objectName: "motorized_axles_text"

        text: "Nessieux moteurs"
        font_size: 12

        default_x: motorized_axles_integerinput.default_x + 2
        default_y: motorized_axles_integerinput.default_y - 4 - font_size

        is_dark_grey: false
    }

    INI_integerinput{
        id: motorized_axles_integerinput
        objectName: "motorized_axles_integerinput"

        default_x: 54
        default_y: 191
        default_width: 80
        default_height: 24

        maximum_value: 2e4
        minimum_value: 0

        is_max_default: false
    }

    //floatinput pour connaitre la puissance de chaque essieux moteurs (relié à la puissance générale
    INI_text {
        id: axle_power_text
        objectName: "axle_power_text"

        text: "Pmoteur"
        font_size: 12

        default_x: axle_power_floatinput.default_x + 2
        default_y: axle_power_floatinput.default_y - 4 - font_size

        is_dark_grey: false
    }

    INI_text {
        id: axle_power_unit_text
        objectName: "axle_power_unit_text"

        text: "kW"
        font_size: 6

        default_x: axle_power_floatinput.default_x + axle_power_floatinput.default_width - default_text_width - 2
        default_y: axle_power_floatinput.default_y - 4 - font_size

        is_dark_grey: true
    }

    INI_floatinput{
        id: axle_power_floatinput
        objectName: "axle_power_floatinput"

        default_x: motorized_axles_integerinput.default_x + 120
        default_y: motorized_axles_integerinput.default_y
        default_width: motorized_axles_integerinput.default_width
        default_height: motorized_axles_integerinput.default_height

        maximum_value: 1e6
        minimum_value: 0
        decimals: 3

        is_max_default: false
    }

    //floatinput pour connaitre la puissance totale du train (relié à la puissance moteur)
    INI_text {
        id: power_text
        objectName: "apower_text"

        text: "Pmoteur"
        font_size: 12

        default_x: power_floatinput.default_x + 2
        default_y: power_floatinput.default_y - 4 - font_size

        is_dark_grey: false
    }

    INI_text {
        id: power_unit_text
        objectName: "power_unit_text"

        text: "kW"
        font_size: 6

        default_x: power_floatinput.default_x + power_floatinput.default_width - default_text_width - 2
        default_y: power_floatinput.default_y - 4 - font_size

        is_dark_grey: true
    }

    INI_floatinput{
        id: power_floatinput
        objectName: "power_floatinput"

        default_x: axle_power_floatinput.default_x + 120
        default_y: axle_power_floatinput.default_y
        default_width: axle_power_floatinput.default_width
        default_height: axle_power_floatinput.default_height

        maximum_value: 1e9
        minimum_value: 0
        decimals: 3

        is_max_default: false
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



    //Tous les composants reliés au paramétrage générale du train
    //floatinput de la masse du convoi
    INI_text {
        id: mass_text
        objectName: "mass_text"

        text: "Mconvoi"
        font_size: 12

        default_x: mass_floatinput.default_x + 2
        default_y: mass_floatinput.default_y - 4 - font_size

        is_dark_grey: false
    }

    INI_text {
        id: mass_unit_text
        objectName: "mass_unit_text"

        text: "t"
        font_size: 6

        default_x: mass_floatinput.default_x + mass_floatinput.default_width - default_text_width - 2
        default_y: mass_floatinput.default_y - 4 - font_size

        is_dark_grey: true
    }

    INI_floatinput{
        id: mass_floatinput
        objectName: "mass_floatinput"

        default_x: 54
        default_y: 91
        default_width: 80
        default_height: 24

        maximum_value: 1e9
        minimum_value: 0.001
        decimals: 3

        is_max_default: false
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
    }

    INI_text {
        id: length_unit_text
        objectName: "length_unit_text"

        text: "m"
        font_size: 6

        default_x: length_floatinput.default_x + length_floatinput.default_width - default_text_width - 2
        default_y: length_floatinput.default_y - 4 - font_size

        is_dark_grey: true
    }

    INI_floatinput{
        id: length_floatinput
        objectName: "length_floatinput"

        default_x: mass_floatinput.default_x + 120
        default_y: mass_floatinput.default_y
        default_width: mass_floatinput.default_width
        default_height: mass_floatinput.default_height

        maximum_value: 1e9
        minimum_value: 0.001
        decimals: 3

        is_max_default: false
    }


    //integerinput de la longueur
    INI_text {
        id: coaches_text
        objectName: "coaches_text"

        text: "Nbvoitures"
        font_size: 12

        default_x: coaches_integerinput.default_x + 2
        default_y: coaches_integerinput.default_y - 4 - font_size

        is_dark_grey: false
    }

    INI_integerinput{
        id: coaches_integerinput
        objectName: "coaches_integerinput"

        default_x: length_floatinput.default_x +  120
        default_y: length_floatinput.default_y
        default_width: length_floatinput.default_width
        default_height: length_floatinput.default_height

        maximum_value: 1e4
        minimum_value: 1

        is_max_default: true//false
    }



    //Nom du matériel roulant (et du fichier dans lequel il sera sauvegardé
    //stringinput du nom du matériel roulant
    INI_text {
        id: name_text
        objectName: "name_text"

        text: "Nom du train (utilisé pour le nom du fichier)"
        font_size: 12

        default_x: name_stringinput.default_x + 2
        default_y: name_stringinput.default_y - 4 - font_size

        is_dark_grey: false
    }

    INI_stringinput{
        id: name_stringinput
        objectName: "name_stringinput"

        default_x: mass_floatinput.default_x
        default_y: 30
        default_width: coaches_integerinput.default_x + coaches_integerinput.default_width - mass_floatinput.default_x
        default_height: 34

        max_text_length: 24
        placeholder_text: "A compléter!"
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