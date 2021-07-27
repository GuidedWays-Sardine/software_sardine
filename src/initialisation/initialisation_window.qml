import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import "../DMI_default"

Window {
    id: window
    minimumWidth: 640
    minimumHeight: 480
    visible: true
    color: "#031122"
    title: qsTr("Initialisation Sardine")
    //flags: Qt.FramelessWindowHint | Qt.Window
    //FIXME : trouver une façons d'avoir une fenètre sans bordure mais avec les fonctions de "snap" et "resize"

    //affiche les différentes pages de settings de l'application d'initialisation
    DMI_stackview{
        id: settings_pages
        objectName: "settings_pages"
    }

    //Bouton rb1
    DMI_button{
        id: rb1
        objectName: "rb1"
        text: "Général"

        defaultX: 580
        defaultY: 15
        defaultHeight: 50
        defaultWidth: 60

        isActivable: true
        isPositive: true
        isVisible: true
    }

    //Bouton rb2
    DMI_button{
        id: rb2
        objectName: "rb2"
        text: "Train"

        defaultX: 580
        defaultY: 65
        defaultHeight: 50
        defaultWidth: 60

        isActivable: true
        isPositive: true
        isVisible: true
    }

    //Bouton rb3
    DMI_button{
        id: rb3
        objectName: "rb3"
        text: "Trajet"

        defaultX: 580
        defaultY: 115
        defaultHeight: 50
        defaultWidth: 60

        isActivable: true
        isPositive: true
        isVisible: true
    }

    //Bouton rb4
    DMI_button{
        id: rb4
        objectName: "rb4"
        text: "Ecrans"

        defaultX: 580
        defaultY: 165
        defaultHeight: 50
        defaultWidth: 60

        isActivable: true
        isPositive: true
        isVisible: true
    }

    //Bouton rb5
    DMI_button{
        id: rb5
        objectName: "rb5"
        text: ""

        defaultX: 580
        defaultY: 215
        defaultHeight: 50
        defaultWidth: 60

        isActivable: true
        isPositive: true
        isVisible: true
    }

    //Bouton rb6
    DMI_button{
        id: rb6
        objectName: "rb6"
        text: ""

        defaultX: 580
        defaultY: 265
        defaultHeight: 50
        defaultWidth: 60

        isActivable: true
        isPositive: true
        isVisible: true
    }

    //Bouton rb7
    DMI_button{
        id: rb7
        objectName: "rb7"
        text: ""

        defaultX: 580
        defaultY: 315
        defaultHeight: 50
        defaultWidth: 60

        isActivable: true
        isPositive: true
        isVisible: true
    }

    //Bouton rb8
    DMI_button{
        id: rb8
        objectName: "rb8"
        text: ""

        defaultX: 580
        defaultY: 365
        defaultHeight: 50
        defaultWidth: 60

        isActivable: true
        isPositive: true
        isVisible: true
    }

    //Bouton quitter
    DMI_button{
        id: quitter
        objectName: "quitter"
        text: "Quitter"

        defaultX: 0
        defaultY: 415
        defaultHeight: 50
        defaultWidth: 120

        isActivable: true
        isPositive: true
        isVisible: true
    }


    //Bouton ouvrir
    DMI_button{
        id: ouvrir
        objectName: "ouvrir"
        text: "Ouvrir"

        defaultX: 280
        defaultY: 415
        defaultHeight: 50
        defaultWidth: 120

        isActivable: true
        isPositive: true
        isVisible: true
    }

    //Bouton sauvegarder
    DMI_button{
        id: sauvegarder
        objectName: "sauvegarder"
        text: "Sauvegarder"

        defaultX: 400
        defaultY: 415
        defaultHeight: 50
        defaultWidth: 120

        isActivable: true
        isPositive: true
        isVisible: true
    }

    //Bouton lancer
    DMI_button{
        id: lancer
        objectName: "lancer"
        text: "Lancer"

        defaultX: 520
        defaultY: 415
        defaultHeight: 50
        defaultWidth: 120

        isActivable: true
        isPositive: true
        isVisible: true
    }
}
