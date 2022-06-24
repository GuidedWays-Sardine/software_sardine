import QtQuick 2.0
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import "../../../components"


Window{
    id: complex_popup

    //propriétés de base
    minimumWidth: 640
    minimumHeight: 480
    color: "#031122"
    title: "Outil de paramétrage complexe de train Sardine"
    //Flags permettant de laisser la fenêtre toujours au dessus et de laisser uniquement le bouton de fermeture
    flags: Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint | Qt.CustomizeWindowHint | Qt.Dialog | Qt.WindowTitleHint
    property bool generated: false


    // Différentes propriétés sur le train complet
    property var mission_list: []   // Liste contenant le type de chacune des voitures (fret, passager, ...)
    property var position_list: []  // Liste contenant la position de chacune des voitures (avant, arrière, milieu)

    // Propriétés sur les bogies
    property var front_bogie_data: []
    onFront_bogie_dataChanged: {
        if(complex_popup.front_bogie_data.length != 0) {
            front_bogie.change_values(front_bogie_data[0], front_bogie_data[1], front_bogie_data[2], front_bogie_data[3], front_bogie_data[4])
        }
        else {
            front_bogie.clear()
        }
    }
    property var middle_bogie_data: []
    onMiddle_bogie_dataChanged: {
        if(complex_popup.middle_bogie_data.length != 0) {
            middle_bogie.change_values(middle_bogie_data[0], middle_bogie_data[1], middle_bogie_data[2], middle_bogie_data[3], false)
        }
        else {
            middle_bogie.clear()
        }
    }
    property var back_bogie_data: []
    onBack_bogie_dataChanged: {
    if(complex_popup.back_bogie_data.length != 0){
            back_bogie.change_values(back_bogie_data[0], back_bogie_data[1], back_bogie_data[2], back_bogie_data[3], back_bogie_data[4])
        }
        else {
            back_bogie.clear()
        }
    }

    //Propriétés sur l'index
    property int previous_railcar_index: 0
    property int current_railcar_index: train_preview.current_index
    onCurrent_railcar_indexChanged: {
        // lorsque l'index de la voiture paramétrée est changée, appelle la fonction update et change le précédent index
        complex_popup.railcar_changed()
        complex_popup.previous_railcar_index = complex_popup.current_railcar_index
    }


    //Propriétés sur les différentes valeurs par défaut (définit lorsque la gfenêtre est générée
    property var positions_type: []         //Liste des différentes positions possibles
    property var missions_type: []          //Liste des différentes missions EN ANGLAIS (nécessaire pour la position
    property int default_axles_count: 2
    property double default_axles_power: 750.0
    property int default_pad_brakes_count: 0
    property int default_disk_brakes_count: 0
    property int default_magnetic_brake_count: 0
    property int default_foucault_brake_count: 0

    //Propriétés sur les différentes limites de paramétrabilité
    property double max_railcar_weight: 1e9   //t
    property double max_railcar_length: 1e9   //m
    property double a_max: 1e3        //kN
    property double b_max: 1e3        //kN/(km/h)
    property double c_max: 1e3        //kM/(km/h)²
    property int abc_decimals: 8
    property var max_doors_list: []         //Liste du nombre de portes maximales selon la mission
    property var max_levels_list: []        //Liste du nombre de niveaux maximum selon la mission
    property int max_bogies_per_railcar: 1e1
    onMax_bogies_per_railcarChanged: {if(max_bogies_per_railcar < 3) {max_bogies_per_railcar = 3;}} //Pour s'assure qu'il est au moins à 3
    property int max_axles_per_bogie: 1e1
    property double max_axles_power: 1e4
    property int max_pad_brakes_per_axle: 2
    property int max_disk_brakes_per_axle: 4
    property int max_magnetic_brakes_per_axle: 2       //Identique pour le freinage de foucault


    //Signal utilisé pour détecter quand le fenêtre est fermée et quitter l'application
    signal closed()
    signal railcar_changed()
    signal update()


    onVisibilityChanged: {
        if(!complex_popup.visible) {
            closed()
        }
    }



    //Bouton permettant de générer le train (et donc de commencer le paramétrage complexe)
    INI_button {
        id: generate_button
        objectName: "generate_button"

        default_x: (640 - default_width)/2
        default_y: 300
        default_width: 120
        default_height: 50

        text: "Générer"

        is_activable: true
        is_positive: true
        is_visible: !complex_popup.generated
    }

    // Série de textes permettant d'indiquer le fonctionnement de la génération du train
    INI_text {
        id: generate_l1
        objectName: "generate_l1"

        default_x: 54
        default_y: 65

        text: "Avant de générer le fichier il est important de compléter le paramétrage simple."
        font_size: 12

        is_dark_grey: false
        is_visible: !complex_popup.generated
    }

    INI_text {
        id: generate_l2
        objectName: "generate_l2"

        default_x: generate_l1.default_x
        default_y: generate_l1.default_y + 2 * font_size

        text: "Une fois le train généré, Certains paramètres seront inchangeables ou utilisés comme valeurs par défaut."
        font_size: generate_l1.font_size

        is_dark_grey: false
        is_visible: !complex_popup.generated
    }


    //Flèches permettant de naviguer dans les voitures
    INI_button {
        id: left_arrow
        objectName: "left_arrow"

        default_x: 0
        default_y: railcar_view.default_y
        default_width: 30
        default_height: railcar_view.default_height

        image_activable: "Navigation/grey_left_arrow.bmp"
        image_not_activable: "Navigation/dark_grey_left_arrow.bmp"

        is_activable: train_preview.current_index > 0
        is_positive: false
        is_visible: complex_popup.generated

        //Signal activé lorsque le bouton est cliqué et permettant d'incrémenter
        onClicked: {
            train_preview.current_index = train_preview.current_index - 1
        }
    }

    INI_railcarview {
        id: railcar_view

    default_y: general_data.default_y - default_height - 14
    current_railcar_mission: general_data.railcar_mission_type
    current_railcar_position: general_data.railcar_position_type

    current_railcar_front_bogie_axles_count: 2//back_bogie.axles_count[0]
    current_railcar_front_bogie_jacob: front_bogie.articulated
    current_railcar_middle_bogies_count: 0//middle_bogie.axles_count.length
    current_railcar_middle_bogie_axles_count: 0//middle_bogie.axles_count.length ? middle_bogie.axles_count[(middle_bogie.axles_count.length - 1) / 2] : 0
    current_railcar_back_bogie_axles_count: 2//front_bogie.axles_count[0]
    current_railcar_back_bogie_jacob: back_bogie.articulated


        is_visible: complex_popup.generated
    }

    INI_button {
        id: right_arrow
        objectName: "right_arrow"

        default_x: 640 - default_width
        default_y: railcar_view.default_y
        default_width: 30
        default_height: railcar_view.default_height

        image_activable: "Navigation/grey_right_arrow.bmp"
        image_not_activable: "Navigation/dark_grey_right_arrow.bmp"

        is_activable: train_preview.current_index < train_preview.train_length - 1
        is_positive: false
        is_visible: complex_popup.generated

        //Signal activé lorsque le bouton est cliqué et permettant d'incrémenter
        onClicked: {
            train_preview.current_index = train_preview.current_index + 1
        }
    }

    //paramètres généraux sur la voiture (masse, longueur, type, niveaux, mission, portes, paramètres dynamiques)
    General_parameters {
        id: general_data
        objectName: "general_data"

        default_x: 0
        default_y: front_bogie.default_y - 66
        railcar_view_height: railcar_view.default_height
        generated: complex_popup.generated
        railcar_index: train_preview.current_index

        max_railcar_weight: complex_popup.max_railcar_weight
        max_railcar_length: complex_popup.max_railcar_length
        a_max: complex_popup.a_max
        b_max: complex_popup.b_max
        c_max: complex_popup.c_max
        abc_decimals: complex_popup.abc_decimals

        positions_type: complex_popup.positions_type
        missions_type: complex_popup.missions_type
        missions_type_trad: complex_popup.missions_type
        max_doors_list: complex_popup.max_doors_list
        max_levels_list: complex_popup.max_levels_list

        onUpdate_icon: {
            complex_popup.mission_list[railcar_index] = railcar_mission_type
            complex_popup.position_list[railcar_index] = railcar_position_type
            train_preview.mission_listChanged()
            train_preview.position_listChanged()
        }
    }

    //Paramètres pour le bogie avant du train
    Bogie_parameters {
        id: front_bogie
        objectName: "front_bogie"

        default_x: 16
        default_y: train_preview.default_y - 104
        generated: complex_popup.generated

        position: "front"
        railcars_count: train_preview.train_length
        railcar_index: train_preview.current_index

        default_axles_count: complex_popup.default_axles_count
        default_axles_power: complex_popup.default_axles_power
        default_pad_brakes_count: complex_popup.default_pad_brakes_count
        default_disk_brakes_count: complex_popup.default_disk_brakes_count
        default_magnetic_brake_count: complex_popup.default_magnetic_brake_count
        default_foucault_brake_count: complex_popup.default_foucault_brake_count

        max_central_bogies: complex_popup.max_bogies_per_railcar - 2
        max_axles_per_bogie: complex_popup.max_axles_per_bogie
        max_axles_power: complex_popup.max_axles_power
        max_pad_brakes_per_axle: complex_popup.max_pad_brakes_per_axle
        max_disk_brakes_per_axle: complex_popup.max_disk_brakes_per_axle
        max_magnetic_brakes_per_axle: complex_popup.max_magnetic_brakes_per_axle
    }


    //Paramètres pour les différents bogies du train
    Bogie_parameters {
        id: middle_bogie
        objectName: "middle_bogie"

        default_x: (640 - 140) * 0.5
        default_y: train_preview.default_y - 104
        generated: complex_popup.generated

        position: "middle"
        railcars_count: train_preview.train_length
        railcar_index: train_preview.current_index

        default_axles_count: complex_popup.default_axles_count
        default_axles_power: complex_popup.default_axles_power
        default_pad_brakes_count: complex_popup.default_pad_brakes_count
        default_disk_brakes_count: complex_popup.default_disk_brakes_count
        default_magnetic_brake_count: complex_popup.default_magnetic_brake_count
        default_foucault_brake_count: complex_popup.default_foucault_brake_count

        max_central_bogies: complex_popup.max_bogies_per_railcar - 2
        max_axles_per_bogie: complex_popup.max_axles_per_bogie
        max_axles_power: complex_popup.max_axles_power
        max_pad_brakes_per_axle: complex_popup.max_pad_brakes_per_axle
        max_disk_brakes_per_axle: complex_popup.max_disk_brakes_per_axle
        max_magnetic_brakes_per_axle: complex_popup.max_magnetic_brakes_per_axle
    }

    //Paramètres pour les différents bogies du train
    Bogie_parameters {
        id: back_bogie
        objectName: "back_bogie"

        default_x: 640 - 140 - 16
        default_y: train_preview.default_y - 104
        generated: complex_popup.generated

        position: "back"
        railcars_count: train_preview.train_length
        railcar_index: train_preview.current_index

        default_axles_count: complex_popup.default_axles_count
        default_axles_power: complex_popup.default_axles_power
        default_pad_brakes_count: complex_popup.default_pad_brakes_count
        default_disk_brakes_count: complex_popup.default_disk_brakes_count
        default_magnetic_brake_count: complex_popup.default_magnetic_brake_count
        default_foucault_brake_count: complex_popup.default_foucault_brake_count

        max_central_bogies: complex_popup.max_bogies_per_railcar - 2
        max_axles_per_bogie: complex_popup.max_axles_per_bogie
        max_axles_power: complex_popup.max_axles_power
        max_pad_brakes_per_axle: complex_popup.max_pad_brakes_per_axle
        max_disk_brakes_per_axle: complex_popup.max_disk_brakes_per_axle
        max_magnetic_brakes_per_axle: complex_popup.max_magnetic_brakes_per_axle
    }


    // trainpreview pour montrer un apperçu des différentes voitures du train
    INI_trainpreview {
        id: train_preview
        objectName: "train_preview"

        default_x: 0
        default_y: 480 - default_height
        default_width: 640
        default_height: 32

        mission_list: complex_popup.mission_list
        position_list: complex_popup.position_list

        is_visible: complex_popup.generated
        visible_count: 10
        is_activable: true
    }
}