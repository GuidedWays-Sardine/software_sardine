import QtQuick 2.15
import QtQuick.Controls 2.15


// https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
// Comment créer un élément personalisé

// https://doc.qt.io/qt-5/qtquickcontrols2-customize.html#customizing-button
// Comment personaliser un bouton (Le INI_checkbutton se base surtout sur le INI_button)


Item {
    id: root

    // Propriétés liées à la position et à la taille du INI_checkbutton
    property double default_x: 0              // Position du INI_checkbutton pour les dimensions minimales (640x480)
    property double default_y: 0
    property double box_length: 20            // Dimensions de la partie cochable du INI_checkbutton quand la fenêtre fait du 640x480
    anchors.fill: parent

    // Calcule la taille et position réelle du composant à partir des dimensions de la fenêtre (parent) et de la taille minimale de celle-ci
    // le INI_checkbutton ne contenant uniquement des composants INI, ces valeurs ne sont pas utilisées mais restent présentent par souci de normalisation
    readonly property int w_min: 640
    readonly property int h_min: 480
    readonly property real ratio:  (parent.width >= w_min && parent.height >= h_min) ? parent.width/w_min * (parent.width/w_min < parent.height/h_min) + parent.height/h_min * (parent.width/w_min >= parent.height/h_min) : 1
    // Si le ratio n'est pas le même que celui de la fenêtre en taille minimale, décalle les composants pour qu'ils restent centrés
    readonly property double x_offset: (parent.width/parent.height > w_min/h_min) && (parent.width >= w_min && parent.height >= h_min) ? (parent.width - w_min * root.ratio) / 2 : 0
    readonly property double y_offset: (parent.width/parent.height < w_min/h_min) && (parent.width >= w_min && parent.height >= h_min) ? (parent.height - h_min * root.ratio) / 2 : 0

    // Propriétés liées au titre du INI_checkbutton
    property string title: ""                 // Texte à afficher à côté du corp du INI_checkbutton
    property int font_size: 12                // Police du texte

    // Propriétés liées à l'état du INI_checkbutton
    property bool is_checked: false           // Si le bouton est activé
    onIs_checkedChanged : root.value_changed()
    property bool is_activable: true          // Si le bouton peut être activée
    property bool is_dark_grey: !is_activable // Si le texte doit-être en gris foncé ?
    property bool is_positive: false          // Si le bouton doit-être visible en couche positive (sinon négatif)
    property bool is_visible: true            // Si le bouton est visible
    visible : root.is_visible

    // Couleurs (ne peuvent pas être modifiés mais permet une mise à jour facile si nécessaire)
    readonly property string white: "#FFFFFF"       //partie 5.2.1.3.3  Nr 1
    readonly property string black: "#000000"       //partie 5.2.1.3.3  Nr 2
    readonly property string grey: "#C3C3C3"        //partie 5.2.1.3.3  Nr 3
    readonly property string medium_grey: "#969696" //partie 5.2.1.3.3  Nr 4
    readonly property string dark_grey: "#555555"   //partie 5.2.1.3.3  Nr 5
    readonly property string dark_blue : "#031122"  //partie 5.2.1.3.3  Nr 6
    readonly property string shadow: "#08182F"      //partie 5.2.1.3.3  Nr 7
    readonly property string yellow: "#DFDF00"      //partie 5.2.1.3.3  Nr 8
    readonly property string orange: "#EA9100"      //partie 5.2.1.3.3  Nr 9
    readonly property string red: "#BF0002"         //partie 5.2.1.3.3  Nr 10


    // Signaux à surcharger en QML ou en python
    signal clicked()                          // Appelé lorsque le INI_checkbutton est relaché
    signal value_changed()                    // Appelé lorsque l'état du INI_checkbutton change (par fonction ou clic)


    // Fonction de clignotement des bordures (met le INI_checkbutton en valeur)
    function blink(time=3, period=0.5, color=root.yellow) {
        // Appelle la fonction de clignotement du corp (la boite)
        body.blink(time, period, color)
    }

    // Fonction pour arréter le clignotement des bordures
    function stop_blink() {
        // Appelle la fonction de clignotement du corp (la boite)
        body.stop_blink()
    }



    // INI_button permettant de créer le corp du INI_checkbutton
    INI_button {
        id: body

        default_x: root.default_x
        default_y: root.default_y
        default_width: root.box_length
        default_height: root.box_length

        image_activable: root.is_checked ? "Navigation/grey_cross.bmp" : ""
        image_not_activable: root.is_checked ? "Navigation/dark_grey_cross.bmp" : ""

        is_activable: root.is_activable
        is_dark_grey: root.is_dark_grey
        is_positive: root.is_positive


        // Détecte quand le corp est cliqué
        onClicked: {
            // Arrête le clignotement, inverse l'état et appel le bon valuechanged
            body.stop_blink()
            root.is_checked = !root.is_checked
            root.clicked()
            // Le signal value_changed est appelé grâce à onIs_checkedChanged
        }
    }


    // INI_text pour le titre du INI_checkbutton
    INI_text {
        id: title_text

        default_x: root.default_x + root.box_length + root.font_size
        default_y: root.default_y + (root.box_length - root.font_size) * 0.5 - 2

        text: root.title
        font_size: root.font_size

        is_dark_grey: root.is_dark_grey
        is_clickable: root.is_activable


        // Détecte lorsque le texte est cliqué (similairement au clic sur le corp du INI_checkbutton
        onClicked: {
            // Arrête le clignotement, inverse l'état et appel le bon valuechanged
            body.stop_blink()
            root.is_checked = !root.is_checked
            root.clicked()
            // Le signal value_changed est appelé grâce à onIs_checkedChanged
        }
    }
}
