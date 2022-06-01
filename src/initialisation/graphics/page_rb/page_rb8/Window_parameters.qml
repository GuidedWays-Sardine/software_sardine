import QtQuick 2.15
import QtQuick.Controls 2.15

import "../../../components"

Item {
    id: root

    //information sur le positionnement de l'encadré et sur son utilisabilité
    property int position_index: 0
    anchors.fill: parent

    //informations sur la validité de l'écran sélectionné (s'il est suffisament grand), et si l'écran sera activé
    property bool screen_valid: false
    property bool is_activable: true
    onIs_activableChanged: { //fonction permettant de changer l'activabilité de l'écran si demandé
        //Cas où l'écran a été mis comme non activable : change la sélection de l'écran à aucun et rend le window non valide (tous les widgets sont grisés et désactivés automatiquement)
        if(!root.is_activable){
            window_index_combo.change_selection(0)
            root.screen_valid = false
        }
    }

    //Informations et fonctions sur l'écran affiché et fonction pour mettre à jour l'encadré de paramètres
    property var initial_settings: [] //Format [window_index, fullscreen_check, [x, y], [width, height]]
    onInitial_settingsChanged: {
        //Si au moins un argument a été donné, change la sélection pour l'écran sélectionné
        if(root.is_activable && root.initial_settings.length >= 1) {
            window_index_combo.change_selection(root.initial_settings[0])

            //Si un écran particulier a été sélectionné et que plus d'informations ont été données, change si l'écran est en plein écran
            if(window_index_combo.selection_index > 0 && initial_settings.length >= 2) {
                fullscreen_check.is_checked = initial_settings[1]

                //Si la fenêtre n'est pas en plein écran et que des données ont été fournis pour la position et la taille de l'écran
                if(!initial_settings[1] && initial_settings.length >= 4 && initial_settings[2].length >= 2 && initial_settings[3].length >= 2){
                    x_input.change_value(initial_settings[2][0])
                    y_input.change_value(initial_settings[2][1])
                    width_input.change_value(initial_settings[3][0])
                    height_input.change_value(initial_settings[3][1])
                }
            }
        }
        //Si les informations par défaut ne sont pas valides, réinitialise les arguments par défaut
        else {
            window_index_combo.change_selection(0)
        }
    }

    //Indication sur l'utilisation de l'écran paramétré
    property string window_name: ""
    property int font_size: 12

    //Liste des écrans disponibles pour l'utilisateur et leurs tailles (liste de paires de dimensions [width, height]
    property var screens_size: []

    //Liste des écrans disponibles pour l'utilisateur et fonction permettant de la changer quand le nombre d'écrans augmente
    property var screens_list: ["Aucun"]
    onScreens_sizeChanged : {
        while((screens_list.length - 1) > screens_size.length) {
            screens_list.pop()
        }
        while((screens_list.length - 1) < screens_size.length) {
            screens_list.push(screens_list.length.toString())
        }
    }

    //Valeurs dans le cas où la fenêtre doit avoir une taille minimale
    property int minimum_width: 0
    property int minimum_height: 0

    //Valeur à récupérer (les dimensions, la position, l'écran sélectionné)
    property int selected_window: window_index_combo.selection_index
    property bool is_fullscreen: fullscreen_check.is_checked
    property int input_x: x_input.value
    property int input_y: y_input.value
    property int input_width: width_input.value
    property int input_height: height_input.value

    // propriétés permettant de mettre à jour les différents texts communs de la page (ici que le texte du fullscreen_check)
    property string fullscreen_text: "Plein écran ?"
    property string window_index_text: "Index écran :"
    property string none_text: "Aucun"
    onNone_textChanged: {screens_list[0] = root.none_text}


    //Fonction permettant de faire clignoter l'encadré du paramétrage écran
    function blink() {
        body.blink()
    }



    //Bouton permettant de créer l'encadré du combobox et contenant tous les éléments de paramétrage
    INI_button {
        id: body

        default_x: 54
        default_y: 15 + 40 + root.position_index * body.default_height
        default_width: 380 + 2*46
        default_height: 76

        is_activable: false
        is_positive: false
        is_visible: root.window_name != ""


        //Texte affichant l'utilisation de l'écran
        INI_text{
            id: window_index_text

            default_x: body.default_x + root.font_size / 2
            default_y: body.default_y + root.font_size / 2

            text: root.window_name
            font_size: root.font_size

            is_dark_grey: !root.is_activable
            is_visible: root.window_name != ""
        }


        //Combobox pour sélectioner l'écran d'affichage
        INI_combobox {
            id: window_index_combo
            objectName: "window_index_combo"

            default_x: body.default_x + 1 + root.font_size / 2
            default_y: body.default_y + 51 - root.font_size / 2
            default_width: 100
            default_height: 24

            elements: root.screens_list
            elements_displayed: 3
            title: root.window_index_text
            font_size: root.font_size 

            is_positive: false
            is_activable: root.is_activable
            is_visible: root.window_name != ""


            //Signal handler pour griser les textes pour l'emplacement de l'écran et changer les valeurs/valeurs par défaut des INI_integerinput
            onSelection_changed: {

                //cas si l'écran est passé à aucun
                if(window_index_combo.selection_text === window_index_combo.elements[0]) {
                    //décoche l'option fullscreen et remet à 0 les valeurs des input pour les dimensions de la fenêtre
                    fullscreen_check.is_checked = false
                    x_input.clear()
                    y_input.clear()
                    width_input.clear()
                    height_input.clear()
                }
                //cas si un écran a été sélectioné
                else {
                    //Si les valeurs pour l'écran sélectionné ont été rentrées et que la résolution de l'écran est suffisante
                    if(selection_index <= root.screens_size.length && root.screens_size[selection_index - 1].length >= 2 && root.screens_size[selection_index - 1][0] >= root.minimum_width && root.screens_size[selection_index - 1][1] >= root.minimum_height){
                        x_input.maximum_value = root.screens_size[selection_index - 1][0] - root.minimum_width
                        y_input.maximum_value = root.screens_size[selection_index - 1][1] - root.minimum_height
                        width_input.maximum_value = root.screens_size[selection_index - 1][0]
                        height_input.maximum_value = root.screens_size[selection_index - 1][1]

                        root.screen_valid = true
                    }
                    //Si la résolution de l'écran n'a pas été donnée ou est trop petite
                    else {
                        root.screen_valid = false
                    }

                    //Active le combobox plein écran si l'écran sélectionné est valide
                    fullscreen_check.is_checked = root.screen_valid
                }
            }
        }


        //Checkbutton pour savoir si l'écran sera en fullscreen
        INI_checkbutton {
            id: fullscreen_check
            objectName: "fullscreen_check"

            box_length: 16
            default_x: 396 - root.font_size / 2
            default_y: window_index_text.default_y + 2

            title: root.fullscreen_text
            font_size: root.font_size

            is_checked: false
            is_activable: root.screen_valid && window_index_combo.selection_index !== 0
            is_positive: false
            is_visible: root.window_name != ""


            //fonction permettant de vider les INI_integerinput quand le mode fullscreen est activé
            onIs_checkedChanged: {
                x_input.clear()
                y_input.clear()
                width_input.clear()
                height_input.clear()
            }
        }


        //integerinput pour la position x de la fenêtre
        INI_integerinput {
            id: x_input

            default_x: body.default_x + 370 + 2*46 - default_width * 4 - 8 * root.font_size - root.font_size / 2
            default_y: window_index_combo.default_y
            default_width: default_height * 2
            default_height: window_index_combo.default_height

            minimum_value: 0
            title: "x :"
            unit: "px"
            font_size: root.font_size 

            is_max_default: false
            is_activable: root.screen_valid && window_index_combo.selection_index !== 0 && !fullscreen_check.is_checked
            is_positive: false
            is_visible: root.window_name != ""


            //permet de changer la hauteur maximale quand la position y a été changée
            onValue_changed: {
                if(root.screen_valid){
                    width_input.maximum_value = root.screens_size[window_index_combo.selection_index - 1][0] - x_input.value
                }
            }
        }

        //integerinput pour la position y de la fenêtre
        INI_integerinput {
            id: y_input

            default_x: body.default_x + 370 + 2*46 - default_width * 3 - 6 * root.font_size - root.font_size / 2
            default_y: window_index_combo.default_y
            default_width: default_height * 2
            default_height: window_index_combo.default_height

            minimum_value: 0
            title: "y :"
            unit: "px"
            font_size: root.font_size 

            is_max_default: false
            is_activable: root.screen_valid && window_index_combo.selection_index !== 0 && !fullscreen_check.is_checked
            is_positive: false
            is_visible: root.window_name != ""


            //permet de changer la hauteur maximale quand la position y a été changée
            onValue_changed: {
                if(root.screen_valid){
                    height_input.maximum_value = root.screens_size[window_index_combo.selection_index - 1][1] - y_input.value
                }
            }
        }


        //integerinput pour la hauteur de la fenêtre
        INI_integerinput {
            id: width_input

            default_x: body.default_x + 370 + 2*46 - default_width * 2 - 2 * root.font_size - root.font_size / 2
            default_y: window_index_combo.default_y
            default_width: default_height * 2
            default_height: window_index_combo.default_height

            minimum_value: root.screen_valid && window_index_combo.selection_index !== 0 ? root.minimum_width : 0
            title: "w :"
            unit: "px"
            font_size: root.font_size 

            is_max_default: root.screen_valid && window_index_combo.selection_index !== 0
            is_activable: root.screen_valid && window_index_combo.selection_index !== 0 && !fullscreen_check.is_checked
            is_positive: false
            is_visible: root.window_name != ""
        }

        //integerinput pour la hauteur de la fenêtre
        INI_integerinput {
            id: height_input

            default_x: body.default_x + 370 + 2*46 - default_width - root.font_size / 2
            default_y: window_index_combo.default_y
            default_width: default_height * 2
            default_height: window_index_combo.default_height

            minimum_value: root.screen_valid && window_index_combo.selection_index !== 0 ? root.minimum_height : 0
            title: "h :"
            unit: "px"
            font_size: root.font_size 

            is_max_default: root.screen_valid && window_index_combo.selection_index !== 0
            is_activable: root.screen_valid && window_index_combo.selection_index !== 0 && !fullscreen_check.is_checked
            is_positive: false
            is_visible: root.window_name != ""
        }
    }
}
