import QtQuick 2.0
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import "../../../components"


Window{
    id: complex_popup

    minimumWidth: 640
    minimumHeight: 480
    visible: false
    color: "#031122"
    title: "Initialisation Sardine"



    // Propriété permettant de savoir si la fenêtre a été générée
    property bool generated: false

    //Signal utilisé pour détecter quand le fenêtre est fermée et quitter l'application
    signal closed()

    onVisibilityChanged: {
        if(!complex_popup.visible) {
            closed()
        }
    }



    INI_button {
        id: generate_button
        objectName: "generate_button"

        default_x: 520
        default_y: 0
        default_width: 120
        default_height: 50

        text: "Générer"

        is_activable: true
        is_positive: true
        is_visible: !complex_popup.generated
    }

    INI_button {
        id: save_button
        objectName: "save_button"

        default_x: generate_button.default_x
        default_y: generate_button.default_y
        default_width: generate_button.default_width
        default_height: generate_button.default_height

        text: "Sauvegarder"

        is_activable: true
        is_positive: true
        is_visible: complex_popup.generated
    }

    // Série de textes permettant d'indiquer le fonctionnement de la génération du train
    INI_text {
        id: generate_l1
        objectName: "generate_l1"

        default_x: 54
        default_y: 65

        text: "Avant de générer le fichier il est important de compléter le paramétrage simple."
        font_size: 12

        is_dark_grey: false
        is_visible: !complex_popup.generated
    }

    INI_text {
        id: generate_l2
        objectName: "generate_l2"

        default_x: generate_l1.default_x
        default_y: generate_l1.default_y + 2 * font_size

        text: "Une fois le train générer, il sera impossible ou long de changer certains paramètres."
        font_size: general_l1.font_size

        is_dark_grey: false
        is_visible: !complex_popup.generated
    }

    INI_text {
        id: generate_l3
        objectName: "generate_l3"

        default_x: generate_l2.default_x + 2 * font_size
        default_y: generate_l2.default_y + font_size

        text: "(nombre de voitures et type du train)"
        font_size: general_l2.font_size

        is_dark_grey: false
        is_visible: !complex_popup.generated
    }
}