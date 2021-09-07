import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

import "page_rb5"
import "../../../DMI_default/ETCS_3.6.0"


DMI_page{
    id: page_rb5
    objectName: "page_rb5"


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

        isActivable: true
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

        isActivable: true
        isPositive: true
    }

    Screen_Parameters_Item {
        index: 4
        screenName: "écran 4"
    }

    Screen_Parameters_Item {
        index: 3
        screenName: "écran 3"
    }

    Screen_Parameters_Item {
        index: 2
        screenName: "écran 2"
    }

    Screen_Parameters_Item {
        index: 1
        screenName: "écran 1"
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

        isActivable: true
        isPositive: true
        isVisible: true
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

        isActivable: true
        isPositive: true
        isVisible: true

    }
}