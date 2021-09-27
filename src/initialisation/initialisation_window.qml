import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import "../DMI_default/ETCS"
import "graphics"
import "graphics/page_rb"

Window {
    id: window
    minimumWidth: 640
    minimumHeight: 480
    visible: true
    color: "#031122"
    title: qsTr("Initialisation Sardine")

    //affiche les différentes pages de settings de l'application d'initialisation
    DMI_stackview{
        id: settings_pages
        objectName: "settings_pages"
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
