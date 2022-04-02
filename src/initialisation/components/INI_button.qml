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
    property double default_x: 0               //position du bouton pour les dimensions minimales de la fenêtre (w_min*h_min)
    property double default_y: 0
    property double default_width: 100         //dimensions du bouton pour les dimensions minimales de la fenêtre (w_min*h_min)
    property double default_height: 40
    anchors.fill: parent

    //permet à partir des valeurs de positions et dimensions par défauts de calculer la position et la taille peu importe la dimension de la fenêtre
    readonly property int w_min: 640
    readonly property int h_min: 480
    readonly property double ratio: (parent.width >= w_min && parent.height >= h_min) ? parent.width/w_min * (parent.width/w_min < parent.height/h_min) + parent.height/h_min * (parent.width/w_min >= parent.height/h_min) : 1  //parent.height et parent.width représentent la taille de la fenêtre
    //permet de centrer la fenêtre lorsque le ratio de la fenêtre n'est pas la même que celui utilisé
    readonly property double x_offset: (parent.width/parent.height > w_min/h_min) && (parent.width >= w_min && parent.height >= h_min) ? (parent.width - w_min * root.ratio) / 2 : 0
    readonly property double y_offset: (parent.width/parent.height < w_min/h_min) && (parent.width >= w_min && parent.height >= h_min) ? (parent.height - h_min * root.ratio) / 2 : 0

    //Propriétés liés à l'image et au texte que l'utilisateur peut rajouter sur le bouton
    property string image: ""       //image à afficher en tout temps sur le bouton si image_activable et image_not_activable sont vides (peut rester vide)
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

    //Propriétés sur les couleurs dans le cas où il faut les changer
    property string background_color: ""
    property string light_shadow_color: ""
    property string dark_shadow_color: ""

    //Couleurs (ne peuvent pas être modifiés mais permet une mise à jour facile si nécessaire)
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


    //Chemin d'accès vers les icones utiles pour le check_button
    readonly property string symbols_path : "../assets/"


    //Différents signal handlers (à écrire en python)
    signal clicked()                        //détecte quand le bouton est cliqué



    //Fonction permettant de faire clignoter les bordures (pour indiquer quelque chose à faire)
    function blink(time=3, period=0.5, color=root.yellow) {
        //Vérifie d'abord que la couleur envoyée est bonne, sinon la met en jaune
        var regex_color = new RegExp("^#(?:[0-9a-fA-F]{3}){1,2}$")
        if(!regex_color.test(color)) {
            color = root.yellow
        }

        //S'assure que la temps est au moins supérieur à la moitié de la période
        if(time < period * 0.5) {
            period = time * 2
        }

        if(time > 0) {
            //Indique au timer les différentes variables
            timer.time_left = parseInt(time * 1000)
            timer.period = period >= 0.001 ? parseInt(period * 1000) : 1
            timer.light_shadow_color = root.light_shadow_color
            timer.dark_shadow_color = root.dark_shadow_color
            timer.blink_color = color

            //Change la couleur des bordures
            root.light_shadow_color = color
            root.dark_shadow_color = color

            //Démarre la première itération du timer
            timer.start()
        }
    }

    //Fonction permettant d'arréter les clignotements
    function stop_blink() {
    if (timer.time_left >= 0.1) {
            timer.time_left = timer.period * 0.5
            timer.stop()
            timer.triggered()
        }
    }

    //Timer utile pour le fonctionnement des différents mode sdes boutons
    Timer {
        id: timer

        property int time_left: 0
        property int period: 0
        property string light_shadow_color: ""
        property string dark_shadow_color: ""
        property string blink_color: ""

        interval: period * 0.5
        repeat: false

        onTriggered: {
            //Réduit le temps restant de l'interval
            time_left = time_left - period

            //Si le temps restant est inférieur à la période /2 change la période pour ne pas fausser les délais
            if(time_left < period * 0.5){
                period = time_left * 2
            }

            //Si le temps est fini (< 0.1ms pour éviter les problèmes de float), remet les bordures originales
            if(time_left < 0.1){
                root.light_shadow_color = light_shadow_color
                root.dark_shadow_color = dark_shadow_color
            }
            //Sinon inverse les couleurs des bordures et redémarre le chronomètre
            else {
                root.light_shadow_color = root.light_shadow_color == blink_color ? light_shadow_color : blink_color
                root.dark_shadow_color = root.dark_shadow_color == blink_color ? dark_shadow_color : blink_color
                timer.start()
            }
        }
    }



    //Rectangle pour la couleur du fond du bouton
    Rectangle{
        id: body

        x: root.x_offset + root.default_x * root.ratio
        y: root.y_offset + root.default_y * root.ratio
        width: root.default_width * root.ratio
        height: root.default_height * root.ratio

        color: (root.background_color == "" ? root.dark_blue : root.background_color)
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

        source: (root.is_activable && root.image_activable) ? (root.symbols_path + root.image_activable) :
                (!root.is_activable && root.image_not_activable) ? (root.symbols_path + root.image_not_activable) :
                (root.image != "") ? (root.symbols_path + root.image) :
                ""
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


    //Variable stockant si le bouton est dans l'état appuyé (et donc si les bordures doivent êtres cachées
    property bool button_pressed: false

    //Ombre extérieure
    //Rectangle pour l'ombre extérieure inférieure
    Rectangle {
        id: out_bottom_shadow

        anchors.right: body.right
        anchors.bottom: body.bottom
        anchors.left: body.left
        height: 1 * root.ratio

        color: !root.button_pressed ? (root.light_shadow_color == "" ? root.shadow : root.light_shadow_color) : "transparent"
    }

    //Rectangle pour l'ombre extérieure droite
    Rectangle {
        id: out_right_shadow

        anchors.right: body.right
        anchors.bottom: body.bottom
        anchors.top: body.top
        width: 1 * root.ratio

        color: !root.button_pressed ? (root.light_shadow_color == "" ? root.shadow : root.light_shadow_color) : "transparent"
    }

    //Rectangle pour l'ombre extérieure supérieure
    Rectangle {
        id: out_top_shadow

        anchors.top: body.top
        anchors.left: body.left
        anchors.right: out_right_shadow.left
        height: 1 * root.ratio

        color: !root.button_pressed ? (root.dark_shadow_color == "" ? root.black : root.dark_shadow_color) : "transparent"
    }

    //Rectangle pour l'ombre extérieure gauche
    Rectangle {
        id: out_left_shadow

        anchors.top: body.top
        anchors.left: body.left
        anchors.bottom: out_bottom_shadow.top
        width: 1 * root.ratio

        color: !root.button_pressed ? (root.dark_shadow_color == "" ? root.black : root.dark_shadow_color) : "transparent"
    }


    //Ombre intérieure
    //Rectangle pour l'ombre intérieure inférieure
    Rectangle {
        id: in_bottom_shadow

        anchors.bottom: out_bottom_shadow.top
        anchors.left: out_left_shadow.right
        anchors.right: out_right_shadow.left
        height: 1 * root.ratio

        color: is_positive && !root.button_pressed ? (root.dark_shadow_color == "" ? root.black : root.dark_shadow_color) : "transparent"
    }

    //Rectangle pour l'ombre intérieure droite
    Rectangle {
        id: in_right_shadow

        anchors.right: out_right_shadow.left
        anchors.bottom: out_bottom_shadow.top
        anchors.top: out_top_shadow.bottom
        width: 1 * root.ratio

        color: is_positive && !root.button_pressed ? (root.dark_shadow_color == "" ? root.black : root.dark_shadow_color) : "transparent"
    }

    //Rectangle pour l'ombre intérieure supérieure
    Rectangle {
        id: in_top_shadow

        anchors.top: out_top_shadow.bottom
        anchors.left: out_left_shadow.right
        anchors.right: in_right_shadow.left
        height: 1 * root.ratio

        color: is_positive && !root.button_pressed ? (root.light_shadow_color == "" ? root.shadow : root.light_shadow_color) : "transparent"
    }

    //Rectangle pour l'ombre intérieure gauche
    Rectangle {
        id: in_left_shadow

        anchors.left: out_left_shadow.right
        anchors.top: out_top_shadow.bottom
        anchors.bottom: in_bottom_shadow.top
        width: 1 * root.ratio

        color: is_positive && !root.button_pressed ? (root.light_shadow_color == "" ? root.shadow : root.light_shadow_color) : "transparent"
    }

    //Zone de détection de souris (utile pour détecter les cliques)
    MouseArea{
        id: area

        x: root.x_offset + root.default_x * root.ratio
        y: root.y_offset + root.default_y * root.ratio
        width: root.default_width * root.ratio
        height: root.default_height * root.ratio

        hoverEnabled: false
        enabled: true


        //Détecte quand la zone (le bouton) commence à être appuyé
        onPressed: {
            //force le focus sur ce bouton pour qu'il soit prioritaire et indique que le bouton est cliqué
            forceActiveFocus()

            if(root.is_activable) {
                root.stop_blink()
                root.button_pressed = true
            }
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
            root.button_pressed = area.containsMouse && root.is_activable
        }
    }
}