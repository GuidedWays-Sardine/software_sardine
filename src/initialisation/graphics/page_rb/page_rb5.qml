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

    //fonctions utiles pour la traduction des textes de la page (actuellement, que le fullscreen)
    function translate_fullscreen(translation)
    {
        screen1.translate_fullscreen(translation)
        screen2.translate_fullscreen(translation)
        screen3.translate_fullscreen(translation)
        screen4.translate_fullscreen(translation)
    }


    //Flèche de droite pour naviguer à gauche sur les catégories d'écrans
    DMI_button {
        id: left_category_button
        objectName: "left_category_button"

        defaultX: 54
        defaultY: 15
        defaultWidth: 46
        defaultHeight: 40

        imageActivable: "Navigation/NA_18.bmp"
        imageNotActivable: "Navigation/NA_19.bmp"

        isActivable: false
        isPositive: true
    }

    //Encadré permettant d'afficher le nom de la catégorie d'écrans
    DMI_button {
        id: category_title
        objectName: "category_title"

        defaultX: 54 + 46
        defaultY: 15
        defaultWidth: 380
        defaultHeight: 40

        text: "NaN"

        isActivable: false
        isPositive: true
        isDarkGrey: true
    }

    //Flèche de droite pour naviguer à droite sur les catégories d'écran
    DMI_button {
        id: right_category_button
        objectName: "right_category_button"

        defaultX: 380 + 54 + 46
        defaultY: 15
        defaultWidth: 46
        defaultHeight: 40

        imageActivable: "Navigation/NA_17.bmp"
        imageNotActivable: "Navigation/NA_18.2.bmp"

        isActivable: false
        isPositive: true
    }

    Screen_Parameters_Item {
        id: screen4
        index: 4

        screenList: page_rb5.screenList
        screenSize: page_rb5.screenSize

        screenName: screenNames.length >= index ? screenNames[index - 1].toString() : ""
        minimumWidth: page_rb5.screenNames.length >= index && page_rb5.minimumWH.length >= index && page_rb5.minimumWH[index - 1].length >= 2 ? page_rb5.minimumWH[index - 1][0] : 0
        minimumHeight: page_rb5.screenNames.length >= index && page_rb5.minimumWH.length >= index && page_rb5.minimumWH[index - 1].length >= 2 ? page_rb5.minimumWH[index - 1][1] : 0

        isActivable: page_rb5.screenActivable.length >= index && page_rb5.screenName != "" ? page_rb5.screenActivable[index - 1] : false
    }

    Screen_Parameters_Item {
        id: screen3
        index: 3

        screenList: page_rb5.screenList
        screenSize: page_rb5.screenSize

        screenName: screenNames.length >= index ? screenNames[index - 1].toString() : ""
        minimumWidth: page_rb5.screenNames.length >= index && page_rb5.minimumWH.length >= index && page_rb5.minimumWH[index - 1].length >= 2 ? page_rb5.minimumWH[index - 1][0] : 0
        minimumHeight: page_rb5.screenNames.length >= index && page_rb5.minimumWH.length >= index && page_rb5.minimumWH[index - 1].length >= 2 ? page_rb5.minimumWH[index - 1][1] : 0

        isActivable: page_rb5.screenActivable.length >= index ? page_rb5.screenActivable[index - 1] : false
    }

    Screen_Parameters_Item {
        id: screen2
        index: 2

        screenList: page_rb5.screenList
        screenSize: page_rb5.screenSize

        screenName: screenNames.length >= index ? screenNames[index - 1].toString() : ""
        minimumWidth: page_rb5.screenNames.length >= index && page_rb5.minimumWH.length >= index && page_rb5.minimumWH[index - 1].length >= 2 ? page_rb5.minimumWH[index - 1][0] : 0
        minimumHeight: page_rb5.screenNames.length >= index && page_rb5.minimumWH.length >= index && page_rb5.minimumWH[index - 1].length >= 2 ? page_rb5.minimumWH[index - 1][1] : 0

        isActivable: page_rb5.screenActivable.length >= index && page_rb5.screenName != "" ? page_rb5.screenActivable[index - 1] : false
    }

    Screen_Parameters_Item {
        id: screen1
        index: 1

        screenList: page_rb5.screenList
        screenSize: page_rb5.screenSize

        screenName: page_rb5.screenNames.length >= index ? page_rb5.screenNames[index - 1].toString() : ""
        minimumWidth: page_rb5.screenNames.length >= index && page_rb5.minimumWH.length >= index && page_rb5.minimumWH[index - 1].length >= 2 ? page_rb5.minimumWH[index - 1][0] : 0
        minimumHeight: page_rb5.screenNames.length >= index && page_rb5.minimumWH.length >= index && page_rb5.minimumWH[index - 1].length >= 2 ? page_rb5.minimumWH[index - 1][1] : 0

        isActivable: page_rb5.screenActivable.length >= index && page_rb5.screenName != "" ? page_rb5.screenActivable[index - 1] : false
    }

    //checkbutton pour savoir si l'application doit éteindre les écrans qui ne sont pas utilisés
    DMI_checkbutton {
        id: black_screens
        objectName: "black_screens"

        defaultX: 15
        defaultY: 379
        boxLenght: 20
        text: "Eteindre les écrans qui ne sont pas utilisés"

        isActivable: true
        isPositive: false
        isChecked: true
    }

    //Flèche de droite pour naviguer sur la liste des écrans d'une même catégorie
    DMI_button {
        id: left_screen_button
        objectName: "left_screen_button"

        defaultX: 54 + 46 + 380 - 46
        defaultY: 400 - 41
        defaultWidth: 46
        defaultHeight: 40

        imageActivable: "Navigation/NA_18.bmp"
        imageNotActivable: "Navigation/NA_19.bmp"

        isActivable: false
        isPositive: true
        isVisible: false
    }

    //Flèche de droite pour naviguer sur la liste des écrans d'une même catégorie
    DMI_button {
        id: right_screen_button
        objectName: "right_screen_button"

        defaultX: 54 + 46 + 380
        defaultY: 400 - 41
        defaultWidth: 46
        defaultHeight: 40

        imageActivable: "Navigation/NA_17.bmp"
        imageNotActivable: "Navigation/NA_18.2.bmp"

        isActivable: false
        isPositive: true
        isVisible: false

    }
}