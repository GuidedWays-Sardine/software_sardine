import QtQuick 2.15
import QtQuick.Controls 2.15


//https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
//Comment créer un élément personalisé


Item {
    id:root

    // Propriétés liées à la position et à la taille du INI_text
    property double default_x: 0          //Position du texte pour les dimensions minimales de la fenêtre (w_min*h_min)
    property double default_y: 0
    anchors.fill: parent

    // Calcule la taille et position réelle du composant à partir des dimensions de la fenêtre (parent) et de la taille minimale de celle-ci
    readonly property int w_min: 640
    readonly property int h_min: 480
    readonly property real ratio:  (parent.width >= w_min && parent.height >= h_min) ? parent.width/w_min * (parent.width/w_min < parent.height/h_min) + parent.height/h_min * (parent.width/w_min >= parent.height/h_min) : 1
    // Si le ratio n'est pas le même que celui de la fenêtre en taille minimale, décalle les composants pour qu'ils restent centrés
    readonly property double x_offset: (parent.width/parent.height > w_min/h_min) && (parent.width >= w_min && parent.height >= h_min) ? (parent.width - w_min * root.ratio) / 2 : 0
    readonly property double y_offset: (parent.width/parent.height < w_min/h_min) && (parent.width >= w_min && parent.height >= h_min) ? (parent.height - h_min * root.ratio) / 2 : 0

    // Propriétés liées au texte du DMI_text
    property string text: ""           // texte à afficher
    property int font_size: 12         // Taille de la police du texte
    readonly property int default_text_height: text_metrics.tightBoundingRect.height / root.ratio  // Dimensions du texte pour la taille minimale de la fenêtre
    readonly property int default_text_width: text_metrics.tightBoundingRect.width / root.ratio

    // Propriétés liées à l'état du texte
    property bool is_dark_grey: false  // Si le texte est à afficher en gris foncé
    property bool is_clickable: false  // Si le texte est cliquable
    property bool is_visible: true     // Si le text est visible
    visible: root.is_visible

    // Couleurs (ne peuvent pas être modifiés mais permet une mise à jour facile si nécessaire) Partie 5.2.1.3.3 de la documentation "DMI ETCS"
    readonly property string grey: "#C3C3C3"
    readonly property string medium_grey: "#969696"
    readonly property string dark_grey: "#555555"


    // Signaux à surcharger en QML ou en Python
    signal clicked()    // Appelé lorsque le texte est cliqué



    // Texte à afficher
    Text {
        id: body

        x: root.x_offset + root.default_x * root.ratio
        y: root.y_offset + root.default_y * root.ratio

        font.family: "Verdana"
        font.pixelSize: root.font_size * root.ratio
        color: root.is_dark_grey ? root.dark_grey : root.grey
        text: root.text
    }

    // Permet de connaitre la taille du texte
    TextMetrics {
        id: text_metrics

        font: body.font
        text: body.text
    }

    // MouseArea permettant de cliquer sur le texte (utilisé par exemple dans le widget INI_checkbutton
    MouseArea {
        id: area

        anchors.horizontalCenter: body.horizontalCenter
        anchors.bottom: body.bottom
        width: text_metrics.tightBoundingRect.width * root.is_visible
        height: text_metrics.tightBoundingRect.height * root.is_visible

        enabled: root.is_clickable && root.is_visible


        // Détecte quand le texte est appuyé et relaché (si la souris se trouve encore sur le texte)
        onReleased: {
            // Appelle le signal clicked dans le cas où le bouton est relaché sur la zone et indique qu'il n'est plus appuyé
            if(area.containsMouse) {
                root.clicked()
            }
        }
    }
}
