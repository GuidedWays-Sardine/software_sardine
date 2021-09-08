import QtQuick 2.15
import QtQuick.Controls 2.15

import "../../../../DMI_default/ETCS_3.6.0"

Item {
    id: root

    //Valeurs pour le positionnement et l'utilisation de l'écran et les écrans où il peut se situer
    property int index: 1
    property string screenName: ""
    property int fontSize: 12
    property var screenSize: [[1080, 1920], [0, 0]] //FIXME : à vider
    ComboBox {
        id: screen_size
        model: root.screenSize
        visible: false
    }
    property var screenList: ["Aucun", "1"] //FIXME : enlever l'option 1
    readonly property bool screenValid: false

    //Valeurs dans le cas où la fenêtre doit avoir une taille minimum
    property int minimumWidth: 0
    property int minimumHeight: 0

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
        onSelection_changed: {
            //vide les cases pour les dimensions (car celles-ci changent avec les écrans
            x_input.clear()
            y_input.clear()
            height_input.clear()
            width_input.clear()

            //cas si l'écran est passé à aucun
            if(screen_index_combo.selection === screen_index_combo.elements[0]) {
                //décoche l'option fullscreen
                fullscreen_on.isChecked = false
            }
            //cas si un écran a été sélectioné
            else {
                //Si les valeurs pour l'écran sélectionné ont été rentrées et que la résolution de l'écran est suffisante
                fullscreen_on.text = screen_size.count.toString()
                if(selectionIndex - 1 <= root.screenSize.lenght ){//&& root.sceenSize[selectionIndex - 2][0] >= root.minimumWidth && root.screenSize[selectionIndex - 2][1] >= root.minimumHeight){
                    //Change les valeurs pour chaque DMI_valueinput
                    //x_input.maximumValue =


                    root.screenValid = true
                }
                else {
                    root.screenValid = false
                }



                //Active la combobox plein écran si l'écran sélectionné est valide
                fullscreen_on.isChecked = root.screenValid
            }
        }
    }

    //Checkbutton pour savoir si l'écran sera en fullscreen
    DMI_checkbutton {
        id: fullscreen_on

        boxLenght: 16
        defaultX: 400
        defaultY: screen_name.defaultY - (boxLenght - root.fontSize) * 0.5

        text: "plein écran ?"

        isChecked: false
        isActivable: root.screenValid && screen_index_combo.selection != screen_index_combo.elements[0]
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
        isDarkGrey: !root.screenValid || !(screen_index_combo.selection != screen_index_combo.elements[0] && !fullscreen_on.isChecked)
    }

    DMI_valueinput {
        id: height_input
        objectName: "height_input"

        defaultX: body.defaultX + 378 + 2*46 - defaultWidth
        defaultY: screen_index_combo.defaultY
        defaultWidth: defaultHeight * 2
        defaultHeight: screen_index_combo.defaultHeight - 1

        minimumValue: root.screenValid ? root.minimumHeight : 0

        isMaxDefault: root.screenValid && screen_index_combo.selection != screen_index_combo.elements[0]
        isActivable: root.screenValid && screen_index_combo.selection != screen_index_combo.elements[0] && !fullscreen_on.isChecked
        isPositive: false
        isVisible: root.screenName != ""
    }

    //hlargeur de la fenètre
    DMI_text {
        id: width_text

        defaultX: width_input.defaultX - root.fontSize * 1.2
        defaultY: width_input.defaultY + (width_input.defaultHeight - fontSize)/2

        text: "w:"

        isDarkGrey: !root.screenValid || !(screen_index_combo.selection != screen_index_combo.elements[0] && !fullscreen_on.isChecked)
        isVisible: root.screenName != ""
    }

    DMI_valueinput {
        id: width_input
        objectName: "width_input"

        defaultX: body.defaultX + 378 + 2*46 - defaultWidth * 2 - 2 * root.fontSize
        defaultY: screen_index_combo.defaultY
        defaultWidth: defaultHeight * 2
        defaultHeight: screen_index_combo.defaultHeight - 1

        minimumValue: root.screenValid ? root.minimumWidth : 0

        isMaxDefault: root.screenValid && screen_index_combo.selection != screen_index_combo.elements[0]
        isActivable: root.screenValid && screen_index_combo.selection != screen_index_combo.elements[0] && !fullscreen_on.isChecked
        isPositive: false
        isVisible: root.screenName != ""
    }

    //position y de la fenêtre
    DMI_text {
        id: y_text

        defaultX: y_input.defaultX - root.fontSize * 1.2
        defaultY: y_input.defaultY + (y_input.defaultHeight - fontSize)/2

        text: "y:"

        isDarkGrey: !root.screenValid || !(screen_index_combo.selection != screen_index_combo.elements[0] && !fullscreen_on.isChecked)
        isVisible: root.screenName != ""
    }

    DMI_valueinput {
        id: y_input
        objectName: "y_input"

        defaultX: body.defaultX + 378 + 2*46 - defaultWidth * 3 - 6 * root.fontSize
        defaultY: screen_index_combo.defaultY
        defaultWidth: defaultHeight * 2
        defaultHeight: screen_index_combo.defaultHeight - 1

        minimumValue: 0

        isMaxDefault: false
        isActivable: root.screenValid && screen_index_combo.selection != screen_index_combo.elements[0] && !fullscreen_on.isChecked
        isPositive: false
        isVisible: root.screenName != ""
    }

    //position x de la fenêtre
    DMI_text {
        id: x_text

        defaultX: x_input.defaultX - root.fontSize * 1.2
        defaultY: x_input.defaultY + (x_input.defaultHeight - fontSize)/2

        text: "x:"

        isDarkGrey: !root.screenValid || !(screen_index_combo.selection != screen_index_combo.elements[0] && !fullscreen_on.isChecked)
        isVisible: root.screenName != ""
    }

    DMI_valueinput {
        id: x_input
        objectName: "x_input"

        defaultX: body.defaultX + 378 + 2*46 - defaultWidth * 4 - 8 * root.fontSize
        defaultY: screen_index_combo.defaultY
        defaultWidth: defaultHeight * 2
        defaultHeight: screen_index_combo.defaultHeight - 1

        minimumValue: 0

        isMaxDefault: false
        isActivable: root.screenValid && screen_index_combo.selection != screen_index_combo.elements[0] && !fullscreen_on.isChecked
        isPositive: false
        isVisible: root.screenName != ""
    }
}