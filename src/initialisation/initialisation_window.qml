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
    visible: false
    color: "#031122"
    title: "Initialisation Sardine"


    //Signal utilisé pour détecter quand le fenêtre est fermée et quitter l'application
    signal closed()

    onVisibilityChanged: {
        if(!window.visible) {
            closed()
        }
    }

    //affiche les différentes pages de settings de l'application d'initialisation
    INI_stackview{
        id: settings_pages
        objectName: "settings_pages"

        default_x: 0
        default_y: 15
        default_width: 580
        default_height: 400
    }

    //stoque tous les boutons à droite de la page et affichant les différentes pages de settings
    Right_buttons{
        id: right_buttons
        objectName: "right_buttons"
    }

    //stoque tous les boutons en bas de la page permettant de quitter/lancer l'applition et d'ouvrir un fichier settings
    Bottom_buttons{
        id: bottom_buttons
        objectName: "right_buttons"
    }
}
