import QtQuick 2.15
import QtQuick.Controls 2.15

import "../../../../DMI_default/ETCS_3.6.0"

Item {
    id: root

    //information sur le positionnement de l'encadré et sur son utilisabilité
    property int index: 0
    readonly property real ratio:  (parent.width >= 640 && parent.height >= 480) ? parent.width/640 * (parent.width/640 < parent.height/480) + parent.height/480 * (parent.width/640 >= parent.height/480) : 1  //parent.height et parent.width représentent la taille de la fenêtre
    anchors.fill: parent

    //informations sur la validité de l'écran sélectionné (s'il est suffisament grand), et si l'écran sera activé
    property bool screen_valid: false
    property bool is_activable: true
    onIs_activableChanged: { //fonction permettant de changer l'activabilité de l'écran si demandé
        //Cas où l'écran a été mis comme activable : change la sélection de l'écran à aucun et rend le screen non valide (tous lew widgets sont grisés et désactivés automatiquement)
        if(!root.is_activable){
            screen_index_combo.change_selection(0)
            root.screen_valid = false
        }
    }

    //Informations et fonctions sur l'écran affiché et fonction pour mettre à jour l'encadré de paramètres
    property var initial_settings: [] //Format [screen_index, fullscreen_on, [x, y], [width, height]]
    onInitial_settingsChanged: {
        //Si une sélection d'un écran spécifique a été donnée
        if(root.is_activable && initial_settings.length >= 1) {
            screen_index_combo.change_selection(initial_settings[0])

            //Si un écran particulier a été sélectionné et que plus d'informations ont été données
            if(screen_index_combo.selection_index > 0 && initial_settings.length >= 2) {
                fullscreen_on.is_checked = initial_settings[1]

                //Si l'écran n'est pas en fullscreen et que des données ont été fournis pour la position et la taille de l'écran
                if(!initial_settings[1] && initial_settings.length >= 4 && initial_settings[2].length >= 2 && initial_settings[3].length >= 2){
                    x_input.change_value(initial_settings[2][0])
                    y_input.change_value(initial_settings[2][1])
                    width_input.change_value(initial_settings[3][0])
                    height_input.change_value(initial_settings[3][1])
                }
            }
        }
        else {
            screen_index_combo.change_selection(0)
        }
    }

    //Indication sur l'utilisation de l'écran paramétré
    property string screen_name: ""
    property int font_size: 12

    //Liste des écrans disponibles pour l'utilisateur et leurs tailles (liste de paires de dimensions [width, height]
    property var screen_size: []

    //Liste des écrans disponibles pour l'utilisateur
    property var screen_list: ["Aucun"]

    //Valeurs dans le cas où la fenêtre doit avoir une taille minimale
    property int minimum_width: 0
    property int minimum_height: 0

    //Valeur à récupérer (les dimensions, la position, l'écran sélectionné)
    property int selected_screen: screen_index_combo.selection_index
    property bool is_fullscreen: fullscreen_on.is_checked
    property int input_x: x_input.value
    property int input_y: y_input.value
    property int input_width: width_input.value
    property int input_height: height_input.value

    // propriétés permettant de mettre à jour les différents texts communs de la page (ici que le texte du fullscreen_on)
    property string fullscreen_text: ""


    //Bouton permettant de créer l'encadré du combobox
    DMI_button {
        id: body

        default_x: 54
        default_y: 15 + 40 + (root.index - 1) * body.default_height
        default_width: 380 + 2*46
        default_height: 76

        is_activable: false
        is_positive: false
        is_visible: root.screen_name != ""
    }

    //Texte affichant l'utilisation de l'écran
    DMI_text{
        id: screen_text

        default_x: body.default_x + 2 + root.font_size
        default_y: body.default_y + 2 + root.font_size

        text: root.screen_name
        font_size: root.font_size

        is_dark_grey: !root.is_activable
        is_visible: root.screen_name != ""
    }

    //Combobox pour sélectioner l'écran d'affichage
    DMI_combobox {
        id: screen_index_combo
        objectName: "screen_index_combo"

        default_x: body.default_x + 1
        default_y: body.default_y + 45
        default_width: 100
        default_height: 30

        elements: root.screen_list
        elements_displayed: 3
        font_size: root.font_size

        is_positive: false
        is_activable: root.is_activable
        is_visible: root.screen_name != ""


        //Signal handler pour griser les textes pour l'emplacement de l'écran et changer les valeurs/valeurs par défaut des DMI_valueinput
        onSelection_changed: {

            //cas si l'écran est passé à aucun
            if(screen_index_combo.selection_text === screen_index_combo.elements[0]) {
                //décoche l'option fullscreen et remet à 0 les valeurs des input pour les dimensions de la fenêtre
                fullscreen_on.is_checked = false
                x_input.clear()
                y_input.clear()
                width_input.clear()
                height_input.clear()
            }
            //cas si un écran a été sélectioné
            else {
                //Si les valeurs pour l'écran sélectionné ont été rentrées et que la résolution de l'écran est suffisante
                if(selection_index <= root.screen_size.length && root.screen_size[selection_index - 1].length >= 2 && root.screen_size[selection_index - 1][0] >= root.minimum_width && root.screen_size[selection_index - 1][1] >= root.minimum_height){
                    x_input.maximum_value = root.screen_size[selection_index - 1][0] - root.minimum_width
                    y_input.maximum_value = root.screen_size[selection_index - 1][1] - root.minimum_height
                    width_input.maximum_value = root.screen_size[selection_index - 1][0]
                    height_input.maximum_value = root.screen_size[selection_index - 1][1]

                    root.screen_valid = true
                }
                //Si la résolution de l'écran n'a pas été donnée ou est trop petite
                else {
                    root.screen_valid = false
                }

                //Active la combobox plein écran si l'écran sélectionné est valide
                fullscreen_on.is_checked = root.screen_valid
            }
        }
    }


    //Checkbutton pour savoir si l'écran sera en fullscreen
    DMI_checkbutton {
        id: fullscreen_on

        box_length: 16
        default_x: 400
        default_y: screen_text.default_y - (box_length - root.font_size) * 0.5

        text: root.fullscreen_text
        font_size: root.font_size

        is_checked: false
        is_activable: root.screen_valid && screen_index_combo.selection_index !== 0
        is_positive: false
        is_visible: root.screen_name != ""


        //fonction permettant de vider les DMI_valueinput quand le mode fullscreen est activé
        onIs_checkedChanged: {
            x_input.clear()
            y_input.clear()
            width_input.clear()
            height_input.clear()
        }
    }


    //position x de la fenêtre
    DMI_text {
        id: x_text

        default_x: x_input.default_x - root.font_size * 1.2
        default_y: x_input.default_y + (x_input.default_height - font_size)/2

        text: "x:"
        font_size: root.font_size

        is_dark_grey: !root.screen_valid || !(screen_index_combo.selection_index !== 0 && !fullscreen_on.is_checked)
        is_visible: root.screen_name != ""
    }

    DMI_valueinput {
        id: x_input
        objectName: "x_input"

        default_x: body.default_x + 378 + 2*46 - default_width * 4 - 8 * root.font_size
        default_y: screen_index_combo.default_y
        default_width: default_height * 2
        default_height: screen_index_combo.default_height - 1

        minimum_value: 0
        font_size: root.font_size

        is_max_default: false
        is_activable: root.screen_valid && screen_index_combo.selection_index !== 0 && !fullscreen_on.is_checked
        is_positive: false
        is_visible: root.screen_name != ""


        //permet de changer la hauteur maximale quand la position y a été changée
        onValue_changed: {
            if(root.screen_valid){
                width_input.maximum_value = root.screen_size[screen_index_combo.selection_index - 1][0] - x_input.value
            }
        }
    }

    //position y de la fenêtre
    DMI_text {
        id: y_text

        default_x: y_input.default_x - root.font_size * 1.2
        default_y: y_input.default_y + (y_input.default_height - font_size)/2

        text: "y:"
        font_size: root.font_size

        is_dark_grey: !root.screen_valid || !(screen_index_combo.selection_index !== 0 && !fullscreen_on.is_checked)
        is_visible: root.screen_name != ""
    }

    DMI_valueinput {
        id: y_input
        objectName: "y_input"

        default_x: body.default_x + 378 + 2*46 - default_width * 3 - 6 * root.font_size
        default_y: screen_index_combo.default_y
        default_width: default_height * 2
        default_height: screen_index_combo.default_height - 1

        minimum_value: 0
        font_size: root.font_size

        is_max_default: false
        is_activable: root.screen_valid && screen_index_combo.selection_index !== 0 && !fullscreen_on.is_checked
        is_positive: false
        is_visible: root.screen_name != ""


        //permet de changer la hauteur maximale quand la position y a été changée
        onValue_changed: {
            if(root.screen_valid){
                height_input.maximum_value = root.screen_size[screen_index_combo.selection_index - 1][1] - y_input.value
            }
        }
    }


    //hauteur de la fenètre
    DMI_text {
        id: height_text

        default_x: height_input.default_x - root.font_size * 1.2
        default_y: height_input.default_y + (height_input.default_height - font_size)/2

        text: "h:"
        font_size: root.font_size

        is_visible: root.screen_name != ""
        is_dark_grey: !root.screen_valid || !(screen_index_combo.selection_index !== 0 && !fullscreen_on.is_checked)
    }

    DMI_valueinput {
        id: height_input
        objectName: "height_input"

        default_x: body.default_x + 378 + 2*46 - default_width
        default_y: screen_index_combo.default_y
        default_width: default_height * 2
        default_height: screen_index_combo.default_height - 1

        minimum_value: root.screen_valid && screen_index_combo.selection_index !== 0 ? root.minimum_height : 0
        font_size: root.font_size

        is_max_default: root.screen_valid && screen_index_combo.selection_index !== 0
        is_activable: root.screen_valid && screen_index_combo.selection_index !== 0 && !fullscreen_on.is_checked
        is_positive: false
        is_visible: root.screen_name != ""
    }

    //largeur de la fenètre
    DMI_text {
        id: width_text

        default_x: width_input.default_x - root.font_size * 1.2
        default_y: width_input.default_y + (width_input.default_height - font_size)/2

        text: "w:"
        font_size: root.font_size

        is_dark_grey: !root.screen_valid || !(screen_index_combo.selection_index !== 0 && !fullscreen_on.is_checked)
        is_visible: root.screen_name != ""
    }

    DMI_valueinput {
        id: width_input
        objectName: "width_input"

        default_x: body.default_x + 378 + 2*46 - default_width * 2 - 2 * root.font_size
        default_y: screen_index_combo.default_y
        default_width: default_height * 2
        default_height: screen_index_combo.default_height - 1

        minimum_value: root.screen_valid && screen_index_combo.selection_index !== 0 ? root.minimum_width : 0
        font_size: root.font_size

        is_max_default: root.screen_valid && screen_index_combo.selection_index !== 0
        is_activable: root.screen_valid && screen_index_combo.selection_index !== 0 && !fullscreen_on.is_checked
        is_positive: false
        is_visible: root.screen_name != ""
    }
}