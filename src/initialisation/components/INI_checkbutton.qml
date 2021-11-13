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
    property int box_length: 20              //dimensions de la partie cochable du checkbutton quand la fenêtre fait du 640x480
    property int default_x: 0                //position du bouton pour les dimensions minimales (640x480)
    property int default_y: 0

    //permet à partir des valeurs de positions et dimensions par défauts de calculer
    readonly property real ratio:  (parent.width >= 640 && parent.height >= 480) ? parent.width/640 * (parent.width/640 < parent.height/480) + parent.height/480 * (parent.width/640 >= parent.height/480) : 1  //parent.height et parent.width représentent la taille de la fenêtre
    x: root.default_x * root.ratio
    y: root.default_y * root.ratio
    width: root.box_length * root.ratio
    height: root.box_length * root.ratio

    //Propriétés liés à l'image et au texte que l'utilisateur peut rajouter sur le checkbutton
    property string text: ""                 //texte à afficher
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

    //Chemin d'accès vers les icones utiles pour le check_button
    readonly property string symbols_path : "../assets/"


    //Différents signal handlers (à écrire en python)
    signal clicked()                         //détecte quand le bouton est cliqué (après que l'état ait été changé)
    signal value_changed()                   //détecte quand la valeur a été changée



    //Rectangle pour la couleur du fond du checkbouton
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
            id: checkbutton_text

            anchors.verticalCenter: text_rectangle.verticalCenter

            text: root.text
            font.pixelSize: root.font_size * ratio
            font.family: "Verdana"
            color: root.is_dark_grey ? root.dark_grey : root.grey
        }

        //Permet de connaitre la taille du texte afin de pouvoir placer une MouseArea dessus pour pouvoir sélectioner l'option en cliquant sur le text
        TextMetrics {
            id: text_metrics

            font: checkbutton_text.font
            text: checkbutton_text.text
        }
    }

    //Image permettant d'indiquer à l'utilisateur si le checkbutton est actif ou non (visible avec un croix)
    Image {
        id: image

        anchors.bottom: body.bottom
        anchors.bottomMargin: (1 + root.is_positive) * root.ratio
        anchors.right: body.right
        anchors.rightMargin: (1 + root.is_positive) * root.ratio
        anchors.top: body.top
        anchors.topMargin: (1 + root.is_positive) * root.ratio
        anchors.left: body.left
        anchors.leftMargin: (1 + root.is_positive) * root.ratio

        source: root.is_checked ? root.symbols_path + (root.is_dark_grey ? "dark_grey_cross.bmp" : "grey_cross.bmp") : ""
    }

    //Variable stockant si  le bouton est dans l'état appuyé (et donc si les bordures doivent êtres cachées
    property bool checkbutton_pressed: false

    //Ombre extérieure
    //Rectangle pour l'ombre extérieure inférieure
    Rectangle {
        id: out_bottom_shadow

        height: 1 * root.ratio
        anchors.right: body.right
        anchors.bottom: body.bottom
        anchors.left: body.left

        color: !root.checkbutton_pressed ? root.shadow : "transparent"
    }

    //Rectangle pour l'ombre extérieure droite
    Rectangle {
        id: out_right_shadow

        width: 1 * root.ratio
        anchors.right: body.right
        anchors.bottom: body.bottom
        anchors.top: body.top

        color: !root.checkbutton_pressed ? root.shadow : "transparent"
    }

    //Rectangle pour l'ombre extérieure supérieure
    Rectangle {
        id: out_top_shadow

        height: 1 * root.ratio
        anchors.top: body.top
        anchors.left: body.left
        anchors.right: out_right_shadow.left

        color: !root.checkbutton_pressed ? root.black : "transparent"
    }

    //Rectangle pour l'ombre extérieure gauche
    Rectangle {
        id: out_left_shadow

        width: 1 * root.ratio
        anchors.top: body.top
        anchors.left: body.left
        anchors.bottom: out_bottom_shadow.top

        color: !root.checkbutton_pressed ? root.black : "transparent"
    }


    //Ombre intérieure
    //Rectangle pour l'ombre intérieure inférieure
    Rectangle {
        id: in_bottom_shadow

        height: 1 * root.ratio
        anchors.bottom: out_bottom_shadow.top
        anchors.left: out_left_shadow.right
        anchors.right: out_right_shadow.left

        color: is_positive && !root.checkbutton_pressed ? root.black : "transparent"
    }

    //Rectangle pour l'ombre intérieure droite
    Rectangle {
        id: in_right_shadow

        width: 1 * root.ratio
        anchors.right: out_right_shadow.left
        anchors.bottom: out_bottom_shadow.top
        anchors.top: out_top_shadow.bottom

        color: is_positive && !root.checkbutton_pressed ? root.black : "transparent"
    }

    //Rectangle pour l'ombre intérieure supérieure
    Rectangle {
        id: in_top_shadow

        height: 1 * root.ratio
        anchors.top: out_top_shadow.bottom
        anchors.left: out_left_shadow.right
        anchors.right: in_right_shadow.left

        color: is_positive && !root.checkbutton_pressed ? root.shadow : "transparent"
    }

    //Rectangle pour l'ombre intérieure gauche
    Rectangle {
        id: in_left_shadow

        width: 1 * root.ratio
        anchors.left: out_left_shadow.right
        anchors.top: out_top_shadow.bottom
        anchors.bottom: in_bottom_shadow.top

        color: is_positive && !root.checkbutton_pressed ? root.shadow : "transparent"
    }

    MouseArea{
        id: area

        anchors.top: body.top
        anchors.left: body.left
        anchors.bottom: body.bottom
        anchors.right: text_rectangle.right
        
        hoverEnabled: false
        enabled: root.is_activable
        
        
        //Détecte quand le checkbutton commence à être pressé pour cacher les bordures de celui-ci s'il est activable
        onPressed: {
            //Récupère le focus et indique que le checkbutton est pressé
            forceActiveFocus()
            root.checkbutton_pressed = true
        }

        //détecte quand le checkbutton est relaché
        onReleased: {
            //Si le clic est valide (fait sur la zone) change l'état du checkbutton et appelle le signal clicked
            if(root.checkbutton_pressed){
                root.is_checked = !root.is_checked
                root.clicked()
                root.checkbutton_pressed = false
            }
        }

        //Fonction qui détecte lorsque l'utilisateur sort ou rentre sa souris du checkbouton alors qu'il clique dessus
        onContainsMouseChanged: {
            root.button_pressed = area.containsMouse
        }
    }
}