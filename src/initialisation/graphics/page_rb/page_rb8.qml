import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

import "page_rb8"
import "../../components"


Item {
    id: page_rb8
    objectName: "page_rb8"

    //Propriété pour avoir la dimension des écrans (la liste sera mise à jour automatiquement)
    property var screens_size: []

    //propriétés sur le nom, les dimensions minimales de chaque écran
    property var windows_name: []
    property var windows_activable: []
    property var minimum_wh: []
    property var initial_settings: []

    //Propriétés sur les textes à traduire
    property string none_text: "Aucun"
    property string fullscreen_text: "Plein écran ?"
    property string window_index_text: "Index écran :"
    property string immersion_text: "Eteindre les écrans qui ne sont pas utilisés ?"


    //fonction permettant de récupérer les différentes valeurs des pages
    function get_values() {
        var values = []
        
        for(let i = 0; i < Math.min(windows_name.length , 4); i++) {
            //Récupère le composant de paramètre à l'index actuel (entre 0 et 4)
            var window = windows.itemAt(i)
            
            //Récupère tous les paramètres et les rajoutes méthodiquement à la liste de paramètres
            //Format : [window_name, [window_index, fullscreen_on_check, [x, y], [width, height]]]
            values.push([window.window_name,
                         [window.selected_window,
                          window.is_fullscreen,
                          [window.input_x, window.input_y],
                          [window.input_height, window.input_width]]])
        }
        return values
    }

    //Flèche de droite pour naviguer à gauche sur les catégories d'écrans
    INI_button {
        id: left_category_button
        objectName: "left_category_button"

        default_x: 54 + 64
        default_y: 15
        default_width: 46
        default_height: 40

        image_activable: "Navigation/grey_left_arrow.bmp"
        image_not_activable: "Navigation/dark_grey_left_arrow.bmp"

        is_activable: false
        is_positive: true
    }

    //Encadré permettant d'afficher le nom de la catégorie d'écrans
    INI_button {
        id: category_title
        objectName: "category_title"

        default_x: 54 + 46 + 64
        default_y: 15
        default_width: 380 - 2 * 64
        default_height: 40

        text: "NaN"

        is_activable: false
        is_positive: true
        is_dark_grey: initial_settings.length > 0
    }

    //Flèche de droite pour naviguer à droite sur les catégories d'écran
    INI_button {
        id: right_category_button
        objectName: "right_category_button"

        default_x: 380 + 54 + 46 - 64
        default_y: 15
        default_width: 46
        default_height: 40

        image_activable: "Navigation/grey_right_arrow.bmp"
        image_not_activable: "Navigation/dark_grey_right_arrow.bmp"

        is_activable: false
        is_positive: true
    }

    Repeater {
        id: windows
        
        model : page_rb8.windows_name.length
        
        Window_parameters {
            //Propriété permetant d'inverser l'index pour charger les zones de paramètres dans le désordre
            //(pour ne pas cacher les bordures du combobox par le composant du dessous) mais pour charger les données dans le bon ordre
            property int real_index: page_rb8.windows_name.length - index - 1

            position_index: real_index

            screens_size: page_rb8.screens_size

            window_name : page_rb8.windows_name.length > real_index ? windows_name[real_index].toString() : ""
            minimum_width: page_rb8.minimum_wh.length > real_index && page_rb8.minimum_wh[real_index].length >= 2 ? page_rb8.minimum_wh[real_index][0] : 0
            minimum_height: page_rb8.minimum_wh.length > real_index && page_rb8.minimum_wh[real_index].length >= 2 ? page_rb8.minimum_wh[real_index][1] : 0
            initial_settings: page_rb8.initial_settings.length > real_index ? page_rb8.initial_settings[real_index] : []

            is_activable : page_rb8.windows_activable.length > real_index && page_rb8.window_name != "" ? page_rb8.windows_activable[real_index] : false
        }
    }

    //checkbutton pour savoir si l'application doit éteindre les écrans qui ne sont pas utilisés
    INI_checkbutton {
        id: immersion_check
        objectName: "immersion_check"

        default_x: 15
        default_y: 379
        box_length: 20
        title: page_rb8.immersion_text

        is_activable: true
        is_positive: false
        is_checked: true
    }

    //Flèche de droite pour naviguer sur la liste des écrans d'une même catégorie
    INI_button {
        id: left_window_button
        objectName: "left_window_button"

        default_x: 54 + 46 + 380 - 46
        default_y: 400 - 41
        default_width: 46
        default_height: 40

        image_activable: "Navigation/grey_left_arrow.bmp"
        image_not_activable: "Navigation/dark_grey_left_arrow.bmp"

        is_activable: false
        is_positive: true
        is_visible: false
    }

    //Flèche de droite pour naviguer sur la liste des écrans d'une même catégorie
    INI_button {
        id: right_window_button
        objectName: "right_window_button"

        default_x: 54 + 46 + 380
        default_y: 400 - 41
        default_width: 46
        default_height: 40

        image_activable: "Navigation/grey_right_arrow.bmp"
        image_not_activable: "Navigation/dark_grey_right_arrow.bmp"

        is_activable: false
        is_positive: true
        is_visible: false
    }
}