import QtQuick 2.15
import QtQuick.Controls 2.15


Item {
    id:root

    //Propriétés liés à la position et à la taille de l'objet
    property int defaultX: 0          //Position du texte
    property int defaultY: 0

    //Propriétés liés au texte du DMI_text
    property string text: ""
    property int fontSize: 12

    //Propriétés liés à l'état du texte
    property bool isDarkGrey: false         //si le bouton peut être activée
    property bool isVisible: true           //si le bouton est visible


    //Couleurs (ne peuvent pas être modifiés mais permet une mise à jour facile si nécessaire)
    readonly property string grey: "#C3C3C3"        //partie 5.2.1.3.3  Nr 3
    readonly property string darkGrey: "#969696"    //partie 5.2.1.3.3  Nr 5


    //permet à partir des valeurs de positions et dimensions par défauts de calculer
    readonly property real ratio:  (parent.width >= 640 && parent.height >= 480) ? parent.width/640 * (parent.width/640 < parent.height/480) + parent.height/480 * (parent.width/640 >= parent.height/480) : 1  //parent.height et parent.width représentent la taille de la fenêtre
    visible: root.isVisible

    //Texte à afficher
    Text {
        id: body

        font.family: "Verdana"
        font.pixelSize: root.fontSize * root.ratio

        x: root.defaultX * root.ratio
        y: root.defaultY * root.ratio
        color: root.isDarkGrey ? root.darkGrey : root.grey
        text: root.text
    }

}