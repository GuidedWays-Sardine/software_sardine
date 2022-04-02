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
    //Flags permettant de laisser la fenêtre toujours au dessus et de laisser uniquement le bouton de fermeture
    flags: Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint | Qt.CustomizeWindowHint | Qt.Dialog | Qt.WindowTitleHint


    //Signal utilisé pour détecter quand le fenêtre est fermée et quitter l'application
    signal closed()

    onVisibilityChanged: {
        if(!window.visible) {
            closed()
        }
    }

    //affiche les différentes pages de paramètres de l'application d'initialisation
    INI_stackview{
        id: settings_pages
        objectName: "settings_pages"

        default_x: 0
        default_y: 15
        default_width: 580
        default_height: 400
    }

    //stocke tous les boutons à droite de la page et affichant les différentes pages de settings
    Right_buttons{
        id: right_buttons

        //position: (580, 15)     size: (60, 400)
    }

    //stocke tous les boutons en bas de la page permettant de quitter/lancer l'applition et d'ouvrir un fichier settings
    Bottom_buttons{
        id: bottom_buttons

        //position: (0, 415)      size: (640, 50)
    }
}
