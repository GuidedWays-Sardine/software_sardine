import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

import "page_rb5"
import "../../../DMI_default/ETCS_3.6.0"


DMI_page{
    id: page_rb5
    objectName: "page_rb5"

    //Propriété pour avoir la liste des écrans et leurs dimensions
    property var screenList: ["Aucun"]
    property var screenSize: []

    //propriétés sur le nom, les dimensions minimales de chaque écran
    property var screenNames: []
    property var screenActivable: []
    property var minimumWH: []

    //propriété pour les informations lors de l'initialisation d'une nouvelle série de paramètres écrans
    property var initialSettings: []
    property string fullscreenText: "Plein écran ?"



    function get_values() {
        var values = []
        if(screen1.screenName != "") {
             values.push([screen1.screenName,
                          [screen1.selectedScreen - 1,
                           screen1.isFullScreen,
                           [screen1.inputX, screen1.inputY],
                           [screen1.inputWidth, screen1.inputHeight]]])
        }
        if(screen2.screenName != "") {
             values.push([screen2.screenName,
                          [screen2.selectedScreen - 1,
                           screen2.isFullScreen,
                           [screen2.inputX, screen2.inputY],
                           [screen2.inputWidth, screen2.inputHeight]]])
        }
        if(screen3.screenName != "") {
             values.push([screen3.screenName,
                          [screen3.selectedScreen - 1,
                           screen3.isFullScreen,
                           [screen3.inputX, screen3.inputY],
                           [screen3.inputWidth, screen3.inputHeight]]])
        }
        if(screen4.screenName != "") {
             values.push([screen4.screenName,
                          [screen4.selectedScreen - 1,
                           screen4.isFullScreen,
                           [screen4.inputX, screen4.inputY],
                           [screen4.inputWidth, screen4.inputHeight]]])
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

        screenList: page_rb5.screenList
        screenSize: page_rb5.screenSize

        screenName: screenNames.length >= index ? screenNames[index - 1].toString() : ""
        initialSettings: page_rb5.initialSettings.length >= index ? page_rb5.initialSettings[index - 1] : []
        minimumWidth: page_rb5.screenNames.length >= index && page_rb5.minimumWH.length >= index && page_rb5.minimumWH[index - 1].length >= 2 ? page_rb5.minimumWH[index - 1][0] : 0
        minimumHeight: page_rb5.screenNames.length >= index && page_rb5.minimumWH.length >= index && page_rb5.minimumWH[index - 1].length >= 2 ? page_rb5.minimumWH[index - 1][1] : 0
        fullscreenText: page_rb5.fullscreenText

        is_activable: page_rb5.screenActivable.length >= index && page_rb5.screenName != "" ? page_rb5.screenActivable[index - 1] : false
    }

    Screen_Parameters_Item {
        id: screen3
        index: 3

        screenList: page_rb5.screenList
        screenSize: page_rb5.screenSize

        screenName: screenNames.length >= index ? screenNames[index - 1].toString() : ""
        initialSettings: page_rb5.initialSettings.length >= index ? page_rb5.initialSettings[index - 1] : []
        minimumWidth: page_rb5.screenNames.length >= index && page_rb5.minimumWH.length >= index && page_rb5.minimumWH[index - 1].length >= 2 ? page_rb5.minimumWH[index - 1][0] : 0
        minimumHeight: page_rb5.screenNames.length >= index && page_rb5.minimumWH.length >= index && page_rb5.minimumWH[index - 1].length >= 2 ? page_rb5.minimumWH[index - 1][1] : 0
        fullscreenText: page_rb5.fullscreenText

        is_activable: page_rb5.screenActivable.length >= index ? page_rb5.screenActivable[index - 1] : false
    }

    Screen_Parameters_Item {
        id: screen2
        index: 2

        screenList: page_rb5.screenList
        screenSize: page_rb5.screenSize

        screenName: page_rb5.screenNames.length >= index ? page_rb5.screenNames[index - 1].toString() : ""
        initialSettings: page_rb5.initialSettings.length >= index ? page_rb5.initialSettings[index - 1] : []
        minimumWidth: page_rb5.screenNames.length >= index && page_rb5.minimumWH.length >= index && page_rb5.minimumWH[index - 1].length >= 2 ? page_rb5.minimumWH[index - 1][0] : 0
        minimumHeight: page_rb5.screenNames.length >= index && page_rb5.minimumWH.length >= index && page_rb5.minimumWH[index - 1].length >= 2 ? page_rb5.minimumWH[index - 1][1] : 0
        fullscreenText: page_rb5.fullscreenText

        is_activable: page_rb5.screenActivable.length >= index && page_rb5.screenName != "" ? page_rb5.screenActivable[index - 1] : false
    }

    Screen_Parameters_Item {
        id: screen1
        index: 1

        screenList: page_rb5.screenList
        screenSize: page_rb5.screenSize

        screenName: page_rb5.screenNames.length >= index ? page_rb5.screenNames[index - 1].toString() : ""
        initialSettings: page_rb5.initialSettings.length >= index ? page_rb5.initialSettings[index - 1] : []
        minimumWidth: page_rb5.screenNames.length >= index && page_rb5.minimumWH.length >= index && page_rb5.minimumWH[index - 1].length >= 2 ? page_rb5.minimumWH[index - 1][0] : 0
        minimumHeight: page_rb5.screenNames.length >= index && page_rb5.minimumWH.length >= index && page_rb5.minimumWH[index - 1].length >= 2 ? page_rb5.minimumWH[index - 1][1] : 0
        fullscreenText: page_rb5.fullscreenText

        is_activable: page_rb5.screenActivable.length >= index && page_rb5.screenName != "" ? page_rb5.screenActivable[index - 1] : false
    }

    //checkbutton pour savoir si l'application doit éteindre les écrans qui ne sont pas utilisés
    DMI_checkbutton {
        id: black_screens
        objectName: "black_screens"

        default_x: 15
        default_y: 379
        box_length: 20
        text: "Eteindre les écrans qui ne sont pas utilisés"

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