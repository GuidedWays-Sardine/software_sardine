import QtQuick 2.15
import QtQuick.Controls 2.15


//https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
//Comment créer un élément personalisé

//https://doc.qt.io/qt-5/qtquickcontrols2-customize.html#customizing-button
//Comment personaliser un bouton
//Ici le INI_checkbutton utilise une structure similaire au INI_button. on déplace juste le texte en dehors du bouton, et l'image d'une croix apparait quand le checkbutton est activé


Item {
    id: root


    //Propriétés liés à la position et à la taille de l'objet
    property int default_x: 0                //position du bouton pour les dimensions minimales (640x480)
    property int default_y: 0
    property int box_length: 20              //dimensions de la partie cochable du checkbutton quand la fenêtre fait du 640x480
    anchors.fill: parent

    //permet à partir des valeurs de positions et dimensions par défauts de calculer
    readonly property real ratio:  (parent.width >= 640 && parent.height >= 480) ? parent.width/640 * (parent.width/640 < parent.height/480) + parent.height/480 * (parent.width/640 >= parent.height/480) : 1  //parent.height et parent.width représentent la taille de la fenêtre

    //Propriétés liés à l'image et au texte que l'utilisateur peut rajouter sur le checkbutton
    property string title: ""                //texte à afficher à côté du corp du checkbutton
    property int font_size: 12               //police du texte

    //Propriétés liés à l'état de la combobox
    property bool is_checked: false          //si le bouton est activé
    onIs_checkedChanged : value_changed()
    property bool is_activable: true         //si le bouton peut être activée
    property bool is_dark_grey: !is_activable//est ce que le texte doit-être en gris foncé ?
    property bool is_positive: false         //si le bouton doit-être visible en couche positive (sinon négatif)
    property bool is_visible: true           //si le bouton est visible
    visible : root.is_visible

    //Couleurs (ne peuvent pas être modifiés mais permet une mise à jour facile si nécessaire)
    readonly property string dark_blue : "#031122"  //partie 5.2.1.3.3  Nr 6
    readonly property string black: "#000000"       //partie 5.2.1.3.3  Nr 2
    readonly property string grey: "#C3C3C3"        //partie 5.2.1.3.3  Nr 3
    readonly property string dark_grey: "#555555"   //partie 5.2.1.3.3  Nr 5
    readonly property string shadow: "#08182F"      //partie 5.2.1.3.3  Nr 7


    //Différents signal handlers (à écrire en python)
    signal clicked()                         //détecte quand le bouton est cliqué (après que l'état ait été changé)
    signal value_changed()                   //détecte quand la valeur a été changée



    //INI_button permettant de créer le corp du checkbutton
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


        //signal permettant de détecter quand le corp du checkbutton est cliqué pour changer l'état de celui-ci et appeler le signal associé
        onClicked: {
            root.is_checked = !root.is_checked
            root.clicked()
            //Le signal value_changed est appelé grâce à onIs_checkedChanged
        }
    }


    //text permettant d'afficher le texte du checkbutton
    INI_text {
        id: title_text

        default_x: root.default_x + root.box_length + root.font_size
        default_y: root.default_y + (root.box_length - root.font_size) * 0.5 - 2

        text: root.title
        font_size: root.font_size

        is_dark_grey: root.is_dark_grey
        is_clickable: true


        //signal permettant de détecter quand le corp du checkbutton est cliqué pour changer l'état de celui-ci et appeler le signal associé
        onClicked: {
            root.is_checked = !root.is_checked
            root.clicked()
            //Le signal value_changed est appelé grâce à onIs_checkedChanged
        }
    }
}
