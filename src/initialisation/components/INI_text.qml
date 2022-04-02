import QtQuick 2.15
import QtQuick.Controls 2.15


//https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
//Comment créer un élément personalisé


Item {
    id:root

    //Propriétés liés à la position et à la taille de l'objet
    property double default_x: 0          //Position du texte pour les dimensions minimales de la fenêtre (w_min*h_min)
    property double default_y: 0
    anchors.fill: parent

    //A partir des dimensions par défaut et actuelles de la fenêtre
    readonly property int w_min: 640
    readonly property int h_min: 480
    readonly property double ratio:  (parent.width >= w_min && parent.height >= h_min) ? parent.width/w_min * (parent.width/w_min < parent.height/h_min) + parent.height/h_min * (parent.width/w_min >= parent.height/h_min) : 1  //parent.height et parent.width représentent la taille de la fenêtre
    //permet de centrer la fenêtre lorsque le ratio de la fenêtre n'est pas la même que celui utilisé
    readonly property double x_offset: (parent.width/parent.height > w_min/h_min) && (parent.width >= w_min && parent.height >= h_min) ? (parent.width - w_min * root.ratio) / 2 : 0
    readonly property double y_offset: (parent.width/parent.height < w_min/h_min) && (parent.width >= w_min && parent.height >= h_min) ? (parent.height - h_min * root.ratio) / 2 : 0

    //Propriétés liés au texte du DMI_text
    property string text: ""
    property int font_size: 12
    readonly property int default_text_height: text_metrics.tightBoundingRect.height / root.ratio
    readonly property int default_text_width: text_metrics.tightBoundingRect.width / root.ratio

    //Propriétés liés à l'état du texte
    property bool is_dark_grey: false  //si le texte est à afficher en gris foncé
    property bool is_clickable: false  //si le texte est cliquable
    property bool is_visible: true     //si le text est visible
    visible: root.is_visible

    //Couleurs (ne peuvent pas être modifiés mais permet une mise à jour facile si nécessaire)
    readonly property string grey: "#C3C3C3"        //partie 5.2.1.3.3  Nr 3
    readonly property string dark_grey: "#555555"   //partie 5.2.1.3.3  Nr 5


    //Signal appelé lorsque le texte est cliqué (uniquement si is_clickable à true)
    signal clicked()



    //Texte à afficher
    Text {
        id: body

        x: root.x_offset + root.default_x * root.ratio
        y: root.y_offset + root.default_y * root.ratio

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

    //MouseArea permettant de cliquer sur le texte (utilisé par exemple dans le widget INI_checkbutton
    MouseArea {
        id: area

        anchors.horizontalCenter: body.horizontalCenter
        anchors.bottom: body.bottom
        width: text_metrics.tightBoundingRect.width
        height: text_metrics.tightBoundingRect.height

        enabled: root.is_clickable && root.is_visible


        //signal appelé lorsque la zone est relachée (après être cliquée), permet d'appeler le signal clicked du composant si la souris est encore sur la zone
        onReleased: {
            //Appelle le signal clicked dans le cas où le bouton est relaché sur la zone et indique qu'il n'est plus appuyé
            if(area.containsMouse) {
                root.clicked()
            }
        }
    }
}
