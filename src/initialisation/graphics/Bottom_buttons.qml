import QtQuick 2.0
import QtQuick.Controls 2.15

import "../components"


Item {
    id: bottom_buttons
    objectName: "bottom_buttons"

    anchors.fill: parent



    // Bouton quitter
    INI_button {
        id: quit_button
        objectName: "quit_button"

        default_x: 0
        default_y: 415
        default_height: 50
        default_width: 120

        text: "Quitter"

        is_activable: true
        is_positive: true
        is_visible: true
    }


    // Checkbutton pour le clavier virtuel
    INI_checkbutton {
        id: virtual_keyboard_check
        objectName: "virtual_keyboard_check"

        default_x: 120
        default_y: 425 // 415 + (50 - 30) / 2
        box_length: 30

        title: "Clavier virtuel"

        is_checked: true
        is_activable: true
        is_positive: true
        is_visible: true
    }

    // Bouton ouvrir
    INI_button {
        id: open_button
        objectName: "open_button"

        default_x: 280
        default_y: 415
        default_height: 50
        default_width: 120

        text: "Ouvrir"

        is_activable: true
        is_positive: true
        is_visible: true
    }

    // Bouton sauvegarder
    INI_button {
        id: save_button
        objectName: "save_button"

        default_x: 400
        default_y: 415
        default_height: 50
        default_width: 120

        text: "Sauvegarder"

        is_activable: true
        is_positive: true
        is_visible: true



        // Popup utile pour entrer le nom du fichier lorsque le clavier virtuel est activé
        // Cela permet d'utiliser en tout temps l'outil de sauvegarde propre à l'OS mais permettre l'entrée d'un nom de fichier
        // Le module de clavier virtuel n'étant pas utilisable pour les fenêtres extérieur
        Popup {
            id: save_popup
            objectName: "save_popup"

            x: 120 * parent.ratio + parent.x_offset
            y: 365 * parent.ratio + parent.y_offset     // 415 - 50
            width: 400 * parent.ratio                   // 400 + 120 - 120
            height: 50 * parent.ratio

            rightPadding: 0
            leftPadding: 0
            topPadding: 0
            bottomPadding: 0

            modal: true
            focus: true
            closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside    // Sort lorsque la touche Echap ou le dehors du composant est cliqué

            background: Rectangle {
                color: save_button.dark_blue
            }

            // stringinput pour entrer la valeur
            INI_stringinput {
                id: file_name_stringinput
                objectName: "file_name_stringinput"

                default_x: 0
                default_y: 0
                default_width: 280 * save_button.ratio
                default_height: 50 * save_button.ratio

                placeholder_text: "Entrer le nom du fichier"
                max_text_length: 48
                font_size: 12 * save_button.ratio

                is_positive: true
                is_activable: true
            }

            // bouton pour valider la valeur
            INI_button {
                id: confirm_button
                objectName: "confirm_button"

                default_x: 280 * save_button.ratio
                default_y: 0
                default_width: 120 * save_button.ratio
                default_height: 50 * save_button.ratio

                text: "Valider"
                font_size: 12 * save_button.ratio

                is_activable: file_name_stringinput.value.length > 0
                is_positive: true
            }
        }
    }

    // Bouton lancer
    INI_button {
        id: launch_button
        objectName: "launch_button"

        default_x: 520
        default_y: 415
        default_height: 50
        default_width: 120

        text: "Lancer"

        is_activable: true
        is_positive: true
        is_visible: true
    }
}