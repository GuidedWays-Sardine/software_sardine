import QtQuick 2.0
import QtQuick.Controls 2.15


// https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
// Comment créer un élément personalisé

// https://doc.qt.io/qt-5/qtquickcontrols2-customize.html#customizing-stackview
// Comment personaliser un stackview


Item {
    id: root

    // Propriétés liées à la position et à la taille du MouseArea permettant de récupérer le focus
    property double default_x: 0               // Position du bouton pour les dimensions minimales de la fenêtre (640*480)
    property double default_y: 0
    property double default_width: 0           // Dimensions du bouton pour les dimensions minimales de la fenêtre (640*480)
    property double default_height: 0
    anchors.fill: parent

    // Calcule la taille et position réelle du composant à partir des dimensions de la fenêtre (parent) et de la taille minimale de celle-ci
    readonly property int w_min: 640
    readonly property int h_min: 480
    readonly property real ratio:  (parent.width >= w_min && parent.height >= h_min) ? parent.width/w_min * (parent.width/w_min < parent.height/h_min) + parent.height/h_min * (parent.width/w_min >= parent.height/h_min) : 1
    // Si le ratio n'est pas le même que celui de la fenêtre en taille minimale, décalle les composants pour qu'ils restent centrés
    readonly property double x_offset: (parent.width/parent.height > w_min/h_min) && (parent.width >= w_min && parent.height >= h_min) ? (parent.width - w_min * root.ratio) / 2 : 0
    readonly property double y_offset: (parent.width/parent.height < w_min/h_min) && (parent.width >= w_min && parent.height >= h_min) ? (parent.height - h_min * root.ratio) / 2 : 0


    // Fonction pour changer la page active
    function set_active_page(page){
        body.clear()
        body.push(page)
    }



    // MouseArea permettant de récupérer le focus lorsque le fond de l'application est cliqué (utile pour mettre à jour les valueinput)
    // La MouseArea doit rester avant le stackview au risque de rendre tous les composants inutilisables
    MouseArea{
        id: area

        x: root.x_offset + root.default_x * root.ratio
        y: root.y_offset + root.default_y * root.ratio
        width: root.default_width * root.ratio
        height: root.default_height * root.ratio

        hoverEnabled: false
        enabled: true


        // Détecte quand la zone est appuyé (pour récupérer le focus)
        onPressed: forceActiveFocus()
    }

    // Stackview permettant de rendre la série de composants insérée visible
    StackView {
        id: body

        anchors.fill: parent

        // Supression des différentes animations de transitions
        pushEnter: Transition {
            enabled: false
        }
        pushExit: Transition {
            enabled: false
        }
        popEnter: Transition {
            enabled: false
        }
        popExit: Transition {
            enabled: false
        }
    }
}