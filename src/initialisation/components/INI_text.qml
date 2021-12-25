import QtQuick 2.15
import QtQuick.Controls 2.15


//https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
//Comment créer un élément personalisé


Item {
    id:root

    //Propriétés liés à la position et à la taille de l'objet
    property int default_x: 0          //Position du texte
    property int default_y: 0

    //permet à partir des valeurs de positions et dimensions par défauts de calculer
    readonly property real ratio:  (parent.width >= 640 && parent.height >= 480) ? parent.width/640 * (parent.width/640 < parent.height/480) + parent.height/480 * (parent.width/640 >= parent.height/480) : 1  //parent.height et parent.width représentent la taille de la fenêtre
    visible: root.is_visible

    //Propriétés liés au texte du DMI_text
    property string text: ""
    property int font_size: 12
    readonly property int default_text_height: text_metrics.tightBoundingRect.height / root.ratio
    readonly property int default_text_width: text_metrics.tightBoundingRect.width / root.ratio

    //Propriétés liés à l'état du texte
    property bool is_dark_grey: false  //si le bouton peut être activée
    property bool is_visible: true     //si le bouton est visible

    //Couleurs (ne peuvent pas être modifiés mais permet une mise à jour facile si nécessaire)
    readonly property string grey: "#C3C3C3"        //partie 5.2.1.3.3  Nr 3
    readonly property string dark_grey: "#555555"   //partie 5.2.1.3.3  Nr 5



    //Texte à afficher
    Text {
        id: body

        x: root.default_x * root.ratio
        y: root.default_y * root.ratio

        font.family: "Verdana"
        font.pixelSize: root.font_size * root.ratio
        color: root.is_dark_grey ? root.dark_grey : root.grey
        text: root.text
    }

    //Permet de connaitre la taille du texte
    TextMetrics {
        id: text_metrics

        font: body.font
        text: body.text
    }
}