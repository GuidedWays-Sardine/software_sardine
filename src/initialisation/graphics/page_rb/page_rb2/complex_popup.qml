import QtQuick 2.0
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import "../../../components"


Window{
    id: complex_popup

    //propriétés de base
    minimumWidth: 640
    minimumHeight: 480
    visible: false
    color: "#031122"
    title: "Outil de paramétrage complexe de train Sardine"

    // Différentes propriétés sur le train complet
    property var type_list: []      // Liste contenant le type de chacune des voitures (fret, passager, ...)
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

    //Propriétés sur les différentes valeurs par défaut (définit lorsque la gfenêtre est générée
    property int default_axle_count: 2
    property double default_axle_power: 750.0
    property int default_pad_brake_count: 0
    property int default_disk_brake_count: 0
    property int default_magnetic_brake_count: 0
    property int default_foucault_brake_count: 0

    //Propriétés sur les différentes limites de paramétrabilité
    property int max_bogies_per_coaches: 1e1
    onMax_bogies_per_coachesChanged: {if(max_bogies_per_coaches) {max_bogies_per_coaches = 3;}} //Pour s'assure qu'il est au moins à 3
    property int max_axles_per_bogies: 1e1
    property double max_axle_power: 1e4
    property int max_pad_per_axle: 2
    property int max_disk_per_axle: 4
    property int max_magnetic_between_axle: 2       //Identique pour le freinage de foucault



    // Propriété permettant de savoir si la fenêtre a été générée
    property bool generated: false

    //Signal utilisé pour détecter quand le fenêtre est fermée et quitter l'application
    signal closed()

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
        font_size: general_l1.font_size

        is_dark_grey: false
        is_visible: !complex_popup.generated
    }




    //paramètres généraux sur la voiture (masse, longueur, type, niveaux, mission, portes, paramètres dynamiques)
    General_parameters {
        id: general_data
        objectName: "general_data"

        default_x: 0
        default_y: front_bogie.default_y - 66

        generated: complex_popup.generated
    }

    //Paramètres pour le bogie avant du train
    Bogie_parameters {
        id: front_bogie
        objectName: "front_bogie"

        default_x: 16
        default_y: train_preview.default_y - 104
        generated: complex_popup.generated

        position: "front"

        default_axle_count: complex_popup.default_axle_count
        default_axle_power: complex_popup.default_axle_power
        default_pad_brake_count: complex_popup.default_pad_brake_count
        default_disk_brake_count: complex_popup.default_disk_brake_count
        default_magnetic_brake_count: complex_popup.default_magnetic_brake_count
        default_foucault_brake_count: complex_popup.default_foucault_brake_count

        max_central_bogies: complex_popup.max_bogies_per_coaches - 2
        max_axles_per_bogies: complex_popup.max_axles_per_bogies
        max_axle_power: complex_popup.max_axle_power
        max_pad_per_axle: complex_popup.max_pad_per_axle
        max_disk_per_axle: complex_popup.max_disk_per_axle
        max_magnetic_between_axle: complex_popup.max_magnetic_between_axle
    }


    //Paramètres pour les différents bogies du train
    Bogie_parameters {
        id: middle_bogie
        objectName: "middle_bogie"

        default_x: (640 - 120) * 0.5
        default_y: train_preview.default_y - 104
        generated: complex_popup.generated

        position: "middle"

        default_axle_count: complex_popup.default_axle_count
        default_axle_power: complex_popup.default_axle_power
        default_pad_brake_count: complex_popup.default_pad_brake_count
        default_disk_brake_count: complex_popup.default_disk_brake_count
        default_magnetic_brake_count: complex_popup.default_magnetic_brake_count
        default_foucault_brake_count: complex_popup.default_foucault_brake_count

        max_central_bogies: complex_popup.max_bogies_per_coaches - 2
        max_axles_per_bogies: complex_popup.max_axles_per_bogies
        max_axle_power: complex_popup.max_axle_power
        max_pad_per_axle: complex_popup.max_pad_per_axle
        max_disk_per_axle: complex_popup.max_disk_per_axle
        max_magnetic_between_axle: complex_popup.max_magnetic_between_axle
    }

    //Paramètres pour les différents bogies du train
    Bogie_parameters {
        id: back_bogie
        objectName: "back_bogie"

        default_x: 640 - 120 - 16
        default_y: train_preview.default_y - 104
        generated: complex_popup.generated

        position: "front"

        default_axle_count: complex_popup.default_axle_count
        default_axle_power: complex_popup.default_axle_power
        default_pad_brake_count: complex_popup.default_pad_brake_count
        default_disk_brake_count: complex_popup.default_disk_brake_count
        default_magnetic_brake_count: complex_popup.default_magnetic_brake_count
        default_foucault_brake_count: complex_popup.default_foucault_brake_count

        max_central_bogies: complex_popup.max_bogies_per_coaches - 2
        max_axles_per_bogies: complex_popup.max_axles_per_bogies
        max_axle_power: complex_popup.max_axle_power
        max_pad_per_axle: complex_popup.max_pad_per_axle
        max_disk_per_axle: complex_popup.max_disk_per_axle
        max_magnetic_between_axle: complex_popup.max_magnetic_between_axle
    }


    // trainpreview pour montrer un apperçu des différentes voitures du train
    INI_trainpreview {
        id: train_preview
        objectName: "train_preview"

        default_x: 0
        default_y: 480 - default_height
        default_width: 640
        default_height: 32

        type_list: complex_popup.type_list
        position_list: complex_popup.position_list

        is_visible: complex_popup.generated
        visible_count: 10
        is_activable: true
    }
}