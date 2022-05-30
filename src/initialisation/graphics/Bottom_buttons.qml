import QtQuick 2.0

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