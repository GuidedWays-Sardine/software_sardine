import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import "components"
import "graphics"
import "graphics/page_rb"

Window {
    id: window
    minimumWidth: 640
    minimumHeight: 480
    color: "#031122"
    title: "Initialisation Sardine"
    visible: false

    // Flags permettant de laisser uniquement le bouton de fermeture de la fenêtre sur la titlebar
    flags: Qt.WindowCloseButtonHint | Qt.CustomizeWindowHint | Qt.Dialog | Qt.WindowTitleHint


    // Signaux à surcharger en QML ou en Python
    signal closed()             // Appelé quand la fenêtre est cachée/fermée


    // Signal permettant (quand surchargé en Python) de fermer l'application quand la fenêtre est fermée
    onVisibilityChanged: {
        if(!window.visible) {
            closed()
        }
    }



    // Stackview pour afficher les différentes pages de paramètres de l'application d'initialisation
    INI_stackview{
        id: settings_pages
        objectName: "settings_pages"

        default_x: 0
        default_y: 15
        default_width: 580
        default_height: 400
    }


    // Stocke tous les boutons à droite de la page et affichant les différentes pages de settings
    Right_buttons{
        id: right_buttons
        objectName: "right_buttons"

        // position: (580, 15)
        // size: (60, 400)
    }

    // Stocke tous les boutons en bas de la page permettant de quitter/lancer l'applition et d'ouvrir un fichier settings
    Bottom_buttons{
        id: bottom_buttons
        objectName: "bottom_buttons"

        // position: (0, 415)
        // size: (640, 50)
    }
}
