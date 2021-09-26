import QtQuick 2.15
import QtQuick.Controls 2.15


//https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
//Comment créer un élément personalisé

//https://doc.qt.io/qt-5/qtquickcontrols2-customize.html#customizing-button
//Comment personaliser un bouton
//Ici le DMI_checkbutton utilise une structure similaire au DMI_button. on déplace juste le texte en dehors du bouton, et l'image d'une croix apparait quand le checkbutton est activé


Item {
    id: root

    //Propriétés liés à la position et à la taille de l'objet
    property int box_length: 20              //dimensions de la partie cochable du checkbutton quand la fenêtre fait du 640x480
    property int default_x: 0                //position du bouton pour les dimensions minimales (640x480)
    property int default_y: 0

    //permet à partir des valeurs de positions et dimensions par défauts de calculer
    readonly property real ratio:  (parent.width >= 640 && parent.height >= 480) ? parent.width/640 * (parent.width/640 < parent.height/480) + parent.height/480 * (parent.width/640 >= parent.height/480) : 1  //parent.height et parent.width représentent la taille de la fenêtre
    x: (root.default_x + 1) * root.ratio
    y: (root.default_y + 1) * root.ratio
    width: (root.box_length - 2) * root.ratio
    height: (root.box_length - 2) * root.ratio

    //Propriétés liés à l'image et au texte que l'utilisateur peut rajouter sur le bouton
    property string text: ""                 //texte à afficher
    property int font_size: 12               //police du texte

    //Propriétés liés à l'état de la combobox
    property bool is_checked: false          //si le bouton est activé
    property bool is_activable: true         //si le bouton peut être activée
    property bool is_dark_grey: !is_activable//est ce que le texte doit-être en gris foncé ?
    property bool is_positive: false         //si le bouton doit-être visible en couche positive (sinon négatif)
    property bool is_visible: true           //si le bouton est visible
    visible : root.is_visible

    //Couleurs (ne peuvent pas être modifiés mais permet une mise à jour facile si nécessaire)
    readonly property string dark_blue : "#031122"  //partie 5.2.1.3.3  Nr 6
    readonly property string black: "#000000"       //partie 5.2.1.3.3  Nr 2
    readonly property string grey: "#C3C3C3"        //partie 5.2.1.3.3  Nr 3
    readonly property string dark_grey: "#969696"   //partie 5.2.1.3.3  Nr 5
    readonly property string shadow: "#08182F"      //partie 5.2.1.3.3  Nr 7

    //Chemin d'accès vers les icones utiles pour le check_button
    readonly property string icon_path : "../../../assets/DMI_symbols/ETCS/"


    //Différents signal handlers (à écrire en python)
    signal clicked()                         //détecte quand le bouton est cliqué (après que l'état ait été changé)



    //Rectangle pour la couleur du fond du bouton (pas nécessaire ici sachant que la couleur du bouton est la même que la couleur de fond de l'application)
    Rectangle{
        id: body

        anchors.fill: root

        color: root.dark_blue
    }

    //Texte visible à côté du checkbutton
    Rectangle {
        id: text_rectangle

        width: text_metrics.tightBoundingRect.width
        height: text_metrics.tightBoundingRect.height
        anchors.verticalCenter: body.verticalCenter
        anchors.left: body.right
        anchors.leftMargin: root.font_size * ratio

        color: "transparent"

        //Permet d'afficher le texte
        Text{
            id: button_text

            anchors.verticalCenter: text_rectangle.verticalCenter

            text: root.text
            font.pixelSize: root.font_size * ratio
            font.family: "Verdana"
            color: root.is_dark_grey ? root.dark_grey : root.grey
        }

        //Permet de connaitre la taille du texte afin de pouvoir placer une MouseArea dessus pour pouvoir sélectioner l'option en cliquant sur le text
        TextMetrics {
            id: text_metrics

            font: button_text.font
            text: button_text.text
        }
    }

    //Image permettant d'indiquer à l'utilisateur si le checkbutton est actif ou non (visible avec un croix)
    Image {
        id: image

        anchors.fill: parent

        source: root.is_checked ? root.icon_path + (root.is_dark_grey ? "Navigation/NA_12.bmp" : "Navigation/NA_11.bmp") : ""
    }


    //Ombre extérieure
    //Rectangle pour l'ombre extérieure inférieure
    Rectangle {
        id: out_bottom_shadow

        width: root.width + 2 * root.ratio
        height: 2 * root.ratio
        anchors.horizontalCenter: body.horizontalCenter
        anchors.verticalCenter: body.bottom

        color: !is_activable || !(box_area.pressed || text_area.pressed) ? root.shadow : "transparent"
    }

    //Rectangle pour l'ombre extérieure droite
    Rectangle {
        id: out_right_shadow

        width: 2 * root.ratio
        height: root.height + 2 * root.ratio
        anchors.right: out_bottom_shadow.right
        anchors.bottom: out_bottom_shadow.bottom

        color: !is_activable || !(box_area.pressed || text_area.pressed) ? root.shadow : "transparent"
    }

    //Rectangle pour l'ombre extérieure supérieure
    Rectangle {
        id: out_top_shadow

        height: 2 * root.ratio
        anchors.top: out_right_shadow.top
        anchors.right: out_right_shadow.left
        anchors.left: out_bottom_shadow.left

        color: !is_activable || !(box_area.pressed || text_area.pressed) ? root.black : "transparent"
    }

    //Rectangle pour l'ombre extérieure gauche
    Rectangle {
        id: out_left_shadow

        width: 2 * root.ratio
        anchors.top: out_top_shadow.top
        anchors.left: out_top_shadow.left
        anchors.bottom: out_bottom_shadow.top

        color: !is_activable || !(box_area.pressed || text_area.pressed) ? root.black : "transparent"
    }


    //Ombre intérieure
    //Rectangle pour l'ombre intérieure inférieure
    Rectangle {
        id: in_bottom_shadow

        height: 2 * root.ratio
        anchors.bottom: out_bottom_shadow.top
        anchors.left: out_left_shadow.right
        anchors.right: out_right_shadow.left

        color: is_positive && !((box_area.pressed || text_area.pressed) && is_activable) ? root.black : "transparent"
    }

    //Rectangle pour l'ombre intérieure droite
    Rectangle {
        id: in_right_shadow

        width: 2 * root.ratio
        anchors.right: out_right_shadow.left
        anchors.bottom: out_bottom_shadow.top
        anchors.top: out_top_shadow.bottom

        color: is_positive && !((box_area.pressed || text_area.pressed) && is_activable) ? root.black : "transparent"
    }

    //Rectangle pour l'ombre intérieure supérieure
    Rectangle {
        id: in_top_shadow

        height: 2 * root.ratio
        anchors.top: out_top_shadow.bottom
        anchors.left: out_left_shadow.right
        anchors.right: in_right_shadow.left

        color: is_positive && !((box_area.pressed || text_area.pressed) && is_activable) ? root.shadow : "transparent"
    }

    //Rectangle pour l'ombre intérieure gauche
    Rectangle {
        id: in_left_shadow

        width: 2 * root.ratio
        anchors.left: out_left_shadow.right
        anchors.top: out_top_shadow.bottom
        anchors.bottom: in_bottom_shadow.top

        color: is_positive && !((box_area.pressed || text_area.pressed) && is_activable) ? root.shadow : "transparent"
    }


    //Zone de détection de souris pour la boite (utile pour détecter les cliques)
    MouseArea{
        id: box_area

        anchors.fill: parent

        hoverEnabled: false


        //Détecte quand la zone de la case du checkbutton est relaché
        onReleased: {
            forceActiveFocus()
            if(is_activable){
                root.is_checked = !root.is_checked
                root.clicked()
            }
        }
    }

    //Zone de détection de souris pour le texte (utile pour détecter les cliques)
    MouseArea{
        id: text_area

        anchors.fill: text_rectangle

        hoverEnabled: false


        //Détecte quand la zone du texte du checkbutton est relaché
        onReleased: {
            forceActiveFocus()
            if(is_activable){
                root.is_checked = !root.is_checked
                root.clicked()
            }
        }
    }
}