import QtQuick 2.15
import QtQuick.Controls 2.15

import "../../../../DMI_default/ETCS_3.6.0"

Item {
    id: root

    //Valeurs pour le positionnement et l'utilisation de l'écran et les écrans où il peut se situer
    property int index: 1
    property string screenName: ""
    property int fontSize: 12
    property var screenList: ["Aucun", "1"]

    //Valeurs des DMI_valueinput sur le positionnement et la taille de la fenêtre
    property int minX: 0
    property int maxX: 0
    property int minY: 0
    property int maxY: 0
    property int minAbsoluteWidth: 0
    property int minWidth: 0
    property int maxWidth: 0
    property int maxAbsoluteHeight: 0
    property int minHeight: 0
    property int maxHeight: 0

    //Valeur à récupérer (les dimensions, la position, l'écran sélectionné)
    property int selectedScreen: 0
    property bool isFullScreen: false
    property int inputX: 0
    property int inputY: 0
    property int inputWidth: 0
    property int inputHeight: 0


    //fonctions utiles pour la traduction des textes de la page
    function translate_fullscreen(translation)
    {
        fullscreen_on.text = translation.toString()
    }


    //propriété pour le ratio de l'écran par rapport à sa taille originale(640*380)
    readonly property real ratio:  (parent.width >= 640 && parent.height >= 480) ? parent.width/640 * (parent.width/640 < parent.height/480) + parent.height/480 * (parent.width/640 >= parent.height/480) : 1  //parent.height et parent.width représentent la taille de la fenêtre
    anchors.fill: parent

    DMI_button {
        id: body

        defaultX: 54
        defaultY: 15 + 40 + (root.index - 1) * body.defaultHeight
        defaultWidth: 380 + 2*46
        defaultHeight: 76

        isActivable: false
        isPositive: false
        isVisible: root.screenName != ""
    }

    //Texte affichant l'utilisation de l'écran
    DMI_text{
        id: screen_name

        defaultX: body.defaultX + 2 + root.fontSize
        defaultY: body.defaultY + 2 + root.fontSize

        text: root.screenName
        fontSize: root.fontSize

        isVisible: root.screenName != ""
    }

    //Combobox pour sélectioner l'écran d'affichage
    DMI_combobox {
        id: screen_index_combo
        objectName: "screen_index_combo"

        defaultX: body.defaultX + 1
        defaultY: body.defaultY + 45
        defaultWidth: 100
        defaultHeight: 30

        elements: root.screenList
        amountElementsDisplayed: 3

        isPositive: false
        isActivable: true
        isVisible: root.screenName != ""

        //Signal handler pour griser les textes pour l'emplacement de l'écran et changer les valeurs/valeurs par défaut des DMI_valueinput

    }

    //Checkbutton pour savoir si l'écran sera en fullscreen
    DMI_checkbutton {
        id: fullscreen_on

        boxLenght: 16
        defaultX: 400
        defaultY: screen_name.defaultY - (boxLenght - root.fontSize) * 0.5

        text: "plein écran ?"

        isChecked: false
        isActivable: false
        isPositive: false
        isVisible: root.screenName != ""
    }

    //hauteur de la fenètre
    DMI_text {
        id: height_text

        defaultX: height_input.defaultX - root.fontSize * 1.2
        defaultY: height_input.defaultY + (height_input.defaultHeight - fontSize)/2

        text: "h:"

        isVisible: root.screenName != ""
        isDarkGrey: true
    }

    DMI_valueinput {
        id: height_input
        objectName: "height_input"

        defaultX: body.defaultX + 378 + 2*46 - defaultWidth
        defaultY: screen_index_combo.defaultY
        defaultWidth: defaultHeight * 2
        defaultHeight: screen_index_combo.defaultHeight - 1

        isActivable: false
        isPositive: false
        isVisible: root.screenName != ""
    }

    //hlargeur de la fenètre
    DMI_text {
        id: width_text

        defaultX: width_input.defaultX - root.fontSize * 1.2
        defaultY: width_input.defaultY + (width_input.defaultHeight - fontSize)/2

        text: "w:"

        isVisible: root.screenName != ""
        isDarkGrey: true
    }

    DMI_valueinput {
        id: width_input
        objectName: "width_input"

        defaultX: body.defaultX + 378 + 2*46 - defaultWidth * 2 - 2 * root.fontSize
        defaultY: screen_index_combo.defaultY
        defaultWidth: defaultHeight * 2
        defaultHeight: screen_index_combo.defaultHeight - 1

        isActivable: false
        isPositive: false
        isVisible: root.screenName != ""
    }

    //position y de la fenêtre
    DMI_text {
        id: y_text

        defaultX: y_input.defaultX - root.fontSize * 1.2
        defaultY: y_input.defaultY + (y_input.defaultHeight - fontSize)/2

        text: "y:"

        isVisible: root.screenName != ""
        isDarkGrey: true
    }

    DMI_valueinput {
        id: y_input
        objectName: "y_input"

        defaultX: body.defaultX + 378 + 2*46 - defaultWidth * 3 - 6 * root.fontSize
        defaultY: screen_index_combo.defaultY
        defaultWidth: defaultHeight * 2
        defaultHeight: screen_index_combo.defaultHeight - 1

        isActivable: false
        isPositive: false
        isVisible: root.screenName != ""
    }

    //position x de la fenêtre
    DMI_text {
        id: x_text

        defaultX: x_input.defaultX - root.fontSize * 1.2
        defaultY: x_input.defaultY + (x_input.defaultHeight - fontSize)/2

        text: "x:"

        isVisible: root.screenName != ""
        isDarkGrey: true
    }

    DMI_valueinput {
        id: x_input
        objectName: "x_input"

        defaultX: body.defaultX + 378 + 2*46 - defaultWidth * 4 - 8 * root.fontSize
        defaultY: screen_index_combo.defaultY
        defaultWidth: defaultHeight * 2
        defaultHeight: screen_index_combo.defaultHeight - 1

        isActivable: false
        isPositive: false
        isVisible: root.screenName != ""
    }
}