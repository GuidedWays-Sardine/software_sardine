import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

import "page_rb5"
import "../../../DMI_default/ETCS"


DMI_page{
    id: page_rb5
    objectName: "page_rb5"

    //Propriété pour avoir la liste des écrans et leurs dimensions
    property var screen_list: ["Aucun"]
    property var screen_size: []

    //propriétés sur le nom, les dimensions minimales de chaque écran
    property var screen_names: []
    property var screen_activable: []
    property var minimum_wh: []

    //propriété pour les informations lors de l'initialisation d'une nouvelle série de paramètres écrans
    property var initial_settings: []
    property string fullscreen_text: "Plein écran ?"


    //fonction permettant de récupérer les différentes valeurs des pages
    function get_values() {
        var values = []
        if(screen1.screen_name != "") {
             values.push([screen1.screen_name,
                          [screen1.selected_screen,
                           screen1.is_fullscreen,
                           [screen1.input_x, screen1.input_y],
                           [screen1.input_width, screen1.input_height]]])
        }
        if(screen2.screen_name != "") {
             values.push([screen2.screen_name,
                          [screen2.selected_screen,
                           screen2.is_fullscreen,
                           [screen2.input_x, screen2.input_y],
                           [screen2.input_width, screen2.input_height]]])
        }
        if(screen3.screen_name != "") {
             values.push([screen3.screen_name,
                          [screen3.selected_screen,
                           screen3.is_fullscreen,
                           [screen3.input_x, screen3.input_y],
                           [screen3.input_width, screen3.input_height]]])
        }
        if(screen4.screen_name != "") {
             values.push([screen4.screen_name,
                          [screen4.selected_screen,
                           screen4.is_fullscreen,
                           [screen4.input_x, screen4.input_y],
                           [screen4.input_width, screen4.input_height]]])
        }
        return values
    }



    //Flèche de droite pour naviguer à gauche sur les catégories d'écrans
    DMI_button {
        id: left_category_button
        objectName: "left_category_button"

        default_x: 54
        default_y: 15
        default_width: 46
        default_height: 40

        image_activable: "Navigation/NA_18.bmp"
        image_not_activable: "Navigation/NA_19.bmp"

        is_activable: false
        is_positive: true
    }

    //Encadré permettant d'afficher le nom de la catégorie d'écrans
    DMI_button {
        id: category_title
        objectName: "category_title"

        default_x: 54 + 46
        default_y: 15
        default_width: 380
        default_height: 40

        text: "NaN"

        is_activable: false
        is_positive: true
        is_dark_grey: true
    }

    //Flèche de droite pour naviguer à droite sur les catégories d'écran
    DMI_button {
        id: right_category_button
        objectName: "right_category_button"

        default_x: 380 + 54 + 46
        default_y: 15
        default_width: 46
        default_height: 40

        image_activable: "Navigation/NA_17.bmp"
        image_not_activable: "Navigation/NA_18.2.bmp"

        is_activable: false
        is_positive: true
    }

    Screen_Parameters_Item {
        id: screen4
        index: 4

        screen_list: page_rb5.screen_list
        screen_size: page_rb5.screen_size

        screen_name: screen_names.length >= index ? screen_names[index - 1].toString() : ""
        initial_settings: page_rb5.initial_settings.length >= index ? page_rb5.initial_settings[index - 1] : []
        minimum_width: page_rb5.screen_names.length >= index && page_rb5.minimum_wh.length >= index && page_rb5.minimum_wh[index - 1].length >= 2 ? page_rb5.minimum_wh[index - 1][0] : 0
        minimum_height: page_rb5.screen_names.length >= index && page_rb5.minimum_wh.length >= index && page_rb5.minimum_wh[index - 1].length >= 2 ? page_rb5.minimum_wh[index - 1][1] : 0
        fullscreen_text: page_rb5.fullscreen_text

        is_activable: page_rb5.screen_activable.length >= index && page_rb5.screen_name != "" ? page_rb5.screen_activable[index - 1] : false
    }

    Screen_Parameters_Item {
        id: screen3
        index: 3

        screen_list: page_rb5.screen_list
        screen_size: page_rb5.screen_size

        screen_name: screen_names.length >= index ? screen_names[index - 1].toString() : ""
        initial_settings: page_rb5.initial_settings.length >= index ? page_rb5.initial_settings[index - 1] : []
        minimum_width: page_rb5.screen_names.length >= index && page_rb5.minimum_wh.length >= index && page_rb5.minimum_wh[index - 1].length >= 2 ? page_rb5.minimum_wh[index - 1][0] : 0
        minimum_height: page_rb5.screen_names.length >= index && page_rb5.minimum_wh.length >= index && page_rb5.minimum_wh[index - 1].length >= 2 ? page_rb5.minimum_wh[index - 1][1] : 0
        fullscreen_text: page_rb5.fullscreen_text

        is_activable: page_rb5.screen_activable.length >= index ? page_rb5.screen_activable[index - 1] : false
    }

    Screen_Parameters_Item {
        id: screen2
        index: 2

        screen_list: page_rb5.screen_list
        screen_size: page_rb5.screen_size

        screen_name: page_rb5.screen_names.length >= index ? page_rb5.screen_names[index - 1].toString() : ""
        initial_settings: page_rb5.initial_settings.length >= index ? page_rb5.initial_settings[index - 1] : []
        minimum_width: page_rb5.screen_names.length >= index && page_rb5.minimum_wh.length >= index && page_rb5.minimum_wh[index - 1].length >= 2 ? page_rb5.minimum_wh[index - 1][0] : 0
        minimum_height: page_rb5.screen_names.length >= index && page_rb5.minimum_wh.length >= index && page_rb5.minimum_wh[index - 1].length >= 2 ? page_rb5.minimum_wh[index - 1][1] : 0
        fullscreen_text: page_rb5.fullscreen_text

        is_activable: page_rb5.screen_activable.length >= index && page_rb5.screen_name != "" ? page_rb5.screen_activable[index - 1] : false
    }

    Screen_Parameters_Item {
        id: screen1
        index: 1

        screen_list: page_rb5.screen_list
        screen_size: page_rb5.screen_size

        screen_name: page_rb5.screen_names.length >= index ? page_rb5.screen_names[index - 1].toString() : ""
        initial_settings: page_rb5.initial_settings.length >= index ? page_rb5.initial_settings[index - 1] : []
        minimum_width: page_rb5.screen_names.length >= index && page_rb5.minimum_wh.length >= index && page_rb5.minimum_wh[index - 1].length >= 2 ? page_rb5.minimum_wh[index - 1][0] : 0
        minimum_height: page_rb5.screen_names.length >= index && page_rb5.minimum_wh.length >= index && page_rb5.minimum_wh[index - 1].length >= 2 ? page_rb5.minimum_wh[index - 1][1] : 0
        fullscreen_text: page_rb5.fullscreen_text

        is_activable: page_rb5.screen_activable.length >= index && page_rb5.screen_name != "" ? page_rb5.screen_activable[index - 1] : false
    }

    //checkbutton pour savoir si l'application doit éteindre les écrans qui ne sont pas utilisés
    DMI_checkbutton {
        id: black_screens_check
        objectName: "black_screens_check"

        default_x: 15
        default_y: 379
        box_length: 20
        text: "Eteindre les écrans qui ne sont pas utilisés ?"

        is_activable: true
        is_positive: false
        is_checked: true
    }

    //Flèche de droite pour naviguer sur la liste des écrans d'une même catégorie
    DMI_button {
        id: left_screen_button
        objectName: "left_screen_button"

        default_x: 54 + 46 + 380 - 46
        default_y: 400 - 41
        default_width: 46
        default_height: 40

        image_activable: "Navigation/NA_18.bmp"
        image_not_activable: "Navigation/NA_19.bmp"

        is_activable: false
        is_positive: true
        is_visible: false
    }

    //Flèche de droite pour naviguer sur la liste des écrans d'une même catégorie
    DMI_button {
        id: right_screen_button
        objectName: "right_screen_button"

        default_x: 54 + 46 + 380
        default_y: 400 - 41
        default_width: 46
        default_height: 40

        image_activable: "Navigation/NA_17.bmp"
        image_not_activable: "Navigation/NA_18.2.bmp"

        is_activable: false
        is_positive: true
        is_visible: false
    }
}