import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.3
import QtQml 2.15


//https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
//Comment créer un élément personalisé

//https://doc.qt.io/qt-5/qtquickcontrols2-customize.html#customizing-button
//Comment personaliser un bouton


Item {
    id: root

    //Propriétés liés à la position et à la taille de l'objet
    property int default_width: 100         //dimensions du bouton pour les dimensions minimales de la fenêtre (640*480)
    property int default_height: 40
    property int default_x: 0               //position du bouton pour les dimensions minimales de la fenêtre (640*480)
    property int default_y: 0

    //permet à partir des valeurs de positions et dimensions par défauts de calculer la position et la taille peu importe la dimension de la fenêtre
    readonly property real ratio:  (parent.width >= 640 && parent.height >= 480) ? parent.width/640 * (parent.width/640 < parent.height/480) + parent.height/480 * (parent.width/640 >= parent.height/480) : 1  //parent.height et parent.width représentent la taille de la fenêtre
    x: root.default_x * root.ratio
    y: root.default_y * root.ratio
    width: root.default_width * root.ratio
    height: root.default_height * root.ratio

    //Propriétés liés à l'image et au texte que l'utilisateur peut rajouter sur le bouton
    property string default_image: ""       //image à afficher en tout temps sur le bouton si image_activable et image_not_activable sont vides (peut rester vide)
    property string image_activable: ""     //image à afficher quand le bouton est cliquable (peut rester vide)
    property string image_not_activable: "" //image à afficher quand le bouton n'est pas cliquable (peut rester vide)
    property string text: ""                //texte à afficher
    property int font_size: 12              //police du texte

    //Propriétés liés à l'état du bouton
    property bool is_activable: true         //si le bouton peut être activée
    property bool is_dark_grey: !is_activable//est ce que le texte doit-être en gris foncé ?
    property bool is_positive: false         //si le bouton doit-être visible en couche positive (sinon négatif)
    property bool is_visible: true           //si le bouton est visible
    visible: root.is_visible

    //Couleurs (ne peuvent pas être modifiés mais permet une mise à jour facile si nécessaire)
    readonly property string dark_blue : "#031122"  //partie 5.2.1.3.3  Nr 6
    readonly property string black: "#000000"       //partie 5.2.1.3.3  Nr 2
    readonly property string grey: "#C3C3C3"        //partie 5.2.1.3.3  Nr 3
    readonly property string dark_grey: "#555555"   //partie 5.2.1.3.3  Nr 4
    readonly property string shadow: "#08182F"      //partie 5.2.1.3.3  Nr 7

    //Chemin d'accès vers les icones utiles pour le check_button
    readonly property string symbols_path : "../assets/"


    //Différents signal handlers (à écrire en python)
    signal clicked()                        //détecte quand le bouton est cliqué



    //Rectangle pour la couleur du fond du bouton
    Rectangle{
        id: body
        color: root.dark_blue
        anchors.fill: parent
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
    }

    //Image visible sur le bouton
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
        fillMode: Image.PreserveAspectFit

        source: (root.image_activable != "" || root.image_not_activable != "") ? root.symbols_path + (root.is_activable ? image_activable : image_not_activable) : root.symbols_path + root.default_image
    }

    //Texte visible sur le bouton
    Text{
        id: button_text

        anchors.horizontalCenter: body.horizontalCenter
        anchors.verticalCenter: body.verticalCenter

        text: root.text
        font.pixelSize: root.font_size * ratio
        font.family: "Verdana"
        color: root.is_dark_grey ? root.dark_grey : root.grey
    }


    //Variable stockant si  le bouton est dans l'état appuyé (et donc si les bordures doivent êtres cachées
    property bool button_pressed: false

    //Ombre extérieure
    //Rectangle pour l'ombre extérieure inférieure
    Rectangle {
        id: out_bottom_shadow

        height: 1 * root.ratio
        anchors.right: body.right
        anchors.bottom: body.bottom
        anchors.left: body.left

        color: !root.button_pressed ? root.shadow : "transparent"
    }

    //Rectangle pour l'ombre extérieure droite
    Rectangle {
        id: out_right_shadow

        width: 1 * root.ratio
        anchors.right: body.right
        anchors.bottom: body.bottom
        anchors.top: body.top

        color: !root.button_pressed ? root.shadow : "transparent"
    }

    //Rectangle pour l'ombre extérieure supérieure
    Rectangle {
        id: out_top_shadow

        height: 1 * root.ratio
        anchors.top: body.top
        anchors.left: body.left
        anchors.right: out_right_shadow.left

        color: !root.button_pressed ? root.black : "transparent"
    }

    //Rectangle pour l'ombre extérieure gauche
    Rectangle {
        id: out_left_shadow

        width: 1 * root.ratio
        anchors.top: body.top
        anchors.left: body.left
        anchors.bottom: out_bottom_shadow.top

        color: !root.button_pressed ? root.black : "transparent"
    }


    //Ombre intérieure
    //Rectangle pour l'ombre intérieure inférieure
    Rectangle {
        id: in_bottom_shadow

        height: 1 * root.ratio
        anchors.bottom: out_bottom_shadow.top
        anchors.left: out_left_shadow.right
        anchors.right: out_right_shadow.left

        color: is_positive && !root.button_pressed ? root.black : "transparent"
    }

    //Rectangle pour l'ombre intérieure droite
    Rectangle {
        id: in_right_shadow

        width: 1 * root.ratio
        anchors.right: out_right_shadow.left
        anchors.bottom: out_bottom_shadow.top
        anchors.top: out_top_shadow.bottom

        color: is_positive && !root.button_pressed ? root.black : "transparent"
    }

    //Rectangle pour l'ombre intérieure supérieure
    Rectangle {
        id: in_top_shadow

        height: 1 * root.ratio
        anchors.top: out_top_shadow.bottom
        anchors.left: out_left_shadow.right
        anchors.right: in_right_shadow.left

        color: is_positive && !root.button_pressed ? root.shadow : "transparent"
    }

    //Rectangle pour l'ombre intérieure gauche
    Rectangle {
        id: in_left_shadow

        width: 1 * root.ratio
        anchors.left: out_left_shadow.right
        anchors.top: out_top_shadow.bottom
        anchors.bottom: in_bottom_shadow.top

        color: is_positive && !root.button_pressed ? root.shadow : "transparent"
    }

    //Zone de détection de souris (utile pour détecter les cliques)
    MouseArea{
        id: area

        anchors.fill: parent

        hoverEnabled: false
        enabled: root.is_activable


        //Détecte quand la zone (le bouton) commence à être appuyé
        onPressed: {
            //force le focus sur ce bouton pour qu'il soit prioritaire et indique que le bouton est cliqué
            forceActiveFocus()
            root.button_pressed = true
        }

        //Détecte quand la zone (le bouton) est relaché
        onReleased: {
            //Appelle le signal clicked dans le cas où le bouton est relaché sur la zone et indique qu'il n'est plus appuyé
            if(root.button_pressed) {
                root.clicked()
                root.button_pressed = false
            }
        }

        //Fonction qui détecte lorsque l'utilisateur sort ou rentre sa souris du bouton alors qu'il clique dessus
        onContainsMouseChanged: {
            root.button_pressed = area.containsMouse
        }
    }
}