import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.3
import QtQml 2.15


// https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
// Comment créer un élément personalisé

// https://doc.qt.io/qt-5/qtquickcontrols2-customize.html#customizing-button
// Comment personaliser un bouton


Item {
    id: root

    // Propriétés liées à la position et à la taille du bouton
    property double default_x: 0              // Position du INI_button pour les dimensions minimales de la fenêtre (w_min*h_min)
    property double default_y: 0
    property double default_width: 100        // Dimensions du INI_button pour les dimensions minimales de la fenêtre (w_min*h_min)
    property double default_height: 40
    anchors.fill: parent

    // Calcule la taille et position réelle du composant à partir des dimensions de la fenêtre (parent) et de la taille minimale de celle-ci
    readonly property int w_min: 640
    readonly property int h_min: 480
    readonly property real ratio:  (parent.width >= w_min && parent.height >= h_min) ? parent.width/w_min * (parent.width/w_min < parent.height/h_min) + parent.height/h_min * (parent.width/w_min >= parent.height/h_min) : 1
    // Si le ratio n'est pas le même que celui de la fenêtre en taille minimale, décalle les composants pour qu'ils restent centrés
    readonly property double x_offset: (parent.width/parent.height > w_min/h_min) && (parent.width >= w_min && parent.height >= h_min) ? (parent.width - w_min * root.ratio) / 2 : 0
    readonly property double y_offset: (parent.width/parent.height < w_min/h_min) && (parent.width >= w_min && parent.height >= h_min) ? (parent.height - h_min * root.ratio) / 2 : 0

    // Propriétés liées à l'image et au texte que l'utilisateur peut rajouter sur le bouton
    property string image: ""                 // Image à afficher en tout temps sur le bouton si image_activable et image_not_activable sont vides (peut rester vide)
    property string image_activable: ""       // Image à afficher quand le bouton est cliquable (peut rester vide)
    property string image_not_activable: ""   // Image à afficher quand le bouton n'est pas cliquable (peut rester vide)
    property string text: ""                  // Texte à afficher
    property int font_size: 12                // Police du texte

    // Propriétés liées à l'état du INI_button
    property bool is_activable: true          // Si le bouton peut être activée
    property bool is_dark_grey: !is_activable // Si ce que le texte doit-être en gris foncé ?
    property bool is_positive: false          // Si le bouton doit-être visible en couche positive (sinon négatif)
    property bool is_visible: true            // Si le bouton est visible
    visible: root.is_visible

    // Propriétés sur les couleurs dans le cas où il faut les changer (par exemple lors du clignotement)
    property string background_color: ""
    property string light_shadow_color: ""
    property string dark_shadow_color: ""

    // Couleurs (ne peuvent pas être modifiés mais permet une mise à jour facile si nécessaire) Partie 5.2.1.3.3 de la documentation "DMI ETCS"
    readonly property string white: "#FFFFFF"
    readonly property string black: "#000000"
    readonly property string grey: "#C3C3C3"
    readonly property string medium_grey: "#969696"
    readonly property string dark_grey: "#555555"
    readonly property string dark_blue: "#031122"
    readonly property string shadow: "#08182F"
    readonly property string yellow: "#DFDF00"
    readonly property string orange: "#EA9100"
    readonly property string red: "#BF0002"

    // Chemin d'accès vers les icones utiles pour le INI_button
    readonly property string symbols_path: "../assets/symbols/"
    readonly property string sounds_path: "../assets/sounds/"


    // Signaux à surchager en QML ou en Python
    signal clicked()                        // Appelé lorsque le bouton est relaché


    // Fonction de clignotement des bordures (met le INI_button en valeur)
    function blink(time=3, period=0.5, color=root.yellow) {
        // Si le temps et la période sont supérieurs à 0
        if(time > 0 && period > 0) {
            // Vérifie que la couleur envoyée est bonne, sinon la met en jaune
            var regex_color = new RegExp("^#(?:[0-9a-fA-F]{3}){1,2}$")
            if(!regex_color.test(color)) {
                console.log(`Valeur hex : \"${color}\" pour le clignotement du INI_button : \"${root.objectName}\" invalide. Clignotement en jaune.`)
                color = root.yellow
            }

            // Si le temps de clignotement est inférieur à une demie période, change la période pour que le clignotement soit bon
            period = Math.min(period, time * 2.0)

            // Indique au timer les différentes variables (convertit en ms)
            timer.time_left = time * 1000
            timer.period = period * 1000
            timer.is_blinked = true
            timer.blink_color = color

            // Démarre la première itération du timer
            timer.start()
        }
        // Sinon, la période ou le temps de clignotement est négatif, l'indique
        else {
            console.log(`La période et le temps de clignotement du INI_button : \"${root.objectName}\" ne peuvent pas être négatif (temps : ${time}s ; période : ${period}s)`)
        }
    }

    // Fonction pour arréter le clignotements des bordures
    function stop_blink() {
        // Réinitialise le timer (qui l'arrêtera et réinitialisera ses données)
        timer.reset()
    }

    // Timer utile pour le fonctionnement des différents mode des boutons
    Timer {
        id: timer

        property double time_left: 0.0
        property double period: 0.0
        property bool is_blinked: false     // Indique si les couleurs des bordures doivent être celles par défaut ou la couleur du clignotement
        property string blink_color: ""

        interval: period / 2.0
        repeat: false

        // Détecte lorsque le timer est arrivé à sa fin
        onTriggered: {
            // Réduit le temps restant de l'interval
            time_left = timer.time_left - timer.period / 2.0

            // Si le temps de clignotement est inférieur à une demie période, change la période pour que le clignotement soit bon
            period = Math.min(timer.period, timer.time * 2.0)

            // Si le temps est fini (< 0.1ms pour éviter les problèmes de float), remet les bordures originales et se réinitialise
            if(timer.time_left < 0.1){
                timer.reset()
            }
            // Sinon inverse les couleurs des bordures (en inversant is_blinked) et redémarre le chronomètre
            else {
                timer.is_blinked = !timer.is_blinked
                timer.start()
            }
        }

        // Fonction permettant de réinitialiser le timer
        function reset() {
            // Vide chacun des paramètres du timer
            timer.stop()
            timer.time_left = 0.0
            timer.period = 0.0
            timer.is_blinked = false
            timer.blink_color = ""
        }
    }



    // Rectangle pour la couleur du fond du bouton
    Rectangle{
        id: body

        // Variable indiquant si le bouton est appuyé (bouton cliqué et souris sur la zone du bouton)
        property bool button_pressed: false

        x: root.x_offset + root.default_x * root.ratio
        y: root.y_offset + root.default_y * root.ratio
        width: root.default_width * root.ratio
        height: root.default_height * root.ratio

        color: (root.background_color == "" ? root.dark_blue : root.background_color)



        // Image centrée sur le bouton
        Image {
            id: image

            anchors.bottom: parent.bottom
            anchors.bottomMargin: (1 + root.is_positive) * root.ratio
            anchors.right: parent.right
            anchors.rightMargin: (1 + root.is_positive) * root.ratio
            anchors.top: parent.top
            anchors.topMargin: (1 + root.is_positive) * root.ratio
            anchors.left: parent.left
            anchors.leftMargin: (1 + root.is_positive) * root.ratio
            fillMode: Image.PreserveAspectFit

            // Si l'image activable ou non activable existe, la charge selon l'activabilité du bouton, sinon charge image si elle existe, sinon rien
            source: (root.is_activable && root.image_activable) ? (root.symbols_path + root.image_activable) :
                    (!root.is_activable && root.image_not_activable) ? (root.symbols_path + root.image_not_activable) :
                    (root.image != "") ? (root.symbols_path + root.image) :
                    ""
        }

        // Texte visible au centre du bouton
        Text{
            id: button_text

            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter

            text: root.text
            font.pixelSize: root.font_size * ratio
            font.family: "Verdana"
            color: root.is_dark_grey ? root.dark_grey : root.grey
        }

        // Zone de détection de souris pour détecter les cliques
        MouseArea{
            id: area

            anchors.fill: parent

            hoverEnabled: false
            enabled: true


            // Détecte quand la zone (le bouton) commence à être appuyé
            onPressed: {
                // Force le focus sur ce bouton pour qu'il soit prioritaire et indique que le bouton est cliqué
                forceActiveFocus()

                // Si le bouton est activable, arrête les clignotements et indique que le bouton est apputé
                if(root.is_activable) {
                    root.stop_blink()
                    body.button_pressed = true
                }
            }

            // Détecte quand la zone (le bouton) est relaché
            onReleased: {
                // Appelle le signal clicked si la souris se trouve encore sur le bouton
                if(body.button_pressed) {
                    root.clicked()
                    body.button_pressed = false
                }
            }

            // Détecte lorsque la souris rentre ou sort de la zone du bouton alors qu'il est cliqué
            onContainsMouseChanged: {
                // Cache ou montre les bordures
                body.button_pressed = area.containsMouse && root.is_activable
            }
        }
    }


    // Ombre extérieure
    // Rectangle pour l'ombre extérieure inférieure
    Rectangle {
        id: out_bottom_shadow

        anchors.right: body.right
        anchors.bottom: body.bottom
        anchors.left: body.left
        height: 1 * root.ratio

        color: timer.is_blinked ? timer.blink_color : (!body.button_pressed ? (root.light_shadow_color == "" ? root.shadow : root.light_shadow_color) : "transparent")
    }

    // Rectangle pour l'ombre extérieure droite
    Rectangle {
        id: out_right_shadow

        anchors.right: body.right
        anchors.bottom: body.bottom
        anchors.top: body.top
        width: 1 * root.ratio

        color: timer.is_blinked ? timer.blink_color : (!body.button_pressed ? (root.light_shadow_color == "" ? root.shadow : root.light_shadow_color) : "transparent")
    }

    // Rectangle pour l'ombre extérieure supérieure
    Rectangle {
        id: out_top_shadow

        anchors.top: body.top
        anchors.left: body.left
        anchors.right: out_right_shadow.left
        height: 1 * root.ratio

        color: timer.is_blinked ? timer.blink_color : (!body.button_pressed ? (root.dark_shadow_color == "" ? root.black : root.dark_shadow_color) : "transparent")
    }

    // Rectangle pour l'ombre extérieure gauche
    Rectangle {
        id: out_left_shadow

        anchors.top: body.top
        anchors.left: body.left
        anchors.bottom: out_bottom_shadow.top
        width: 1 * root.ratio

        color: timer.is_blinked ? timer.blink_color : (!body.button_pressed ? (root.dark_shadow_color == "" ? root.black : root.dark_shadow_color) : "transparent")
    }


    // Ombre intérieure
    // Rectangle pour l'ombre intérieure inférieure
    Rectangle {
        id: in_bottom_shadow

        anchors.bottom: out_bottom_shadow.top
        anchors.left: out_left_shadow.right
        anchors.right: out_right_shadow.left
        height: 1 * root.ratio

        color: timer.is_blinked ? timer.blink_color : (is_positive && !body.button_pressed ? (root.dark_shadow_color == "" ? root.black : root.dark_shadow_color) : "transparent")
    }

    // Rectangle pour l'ombre intérieure droite
    Rectangle {
        id: in_right_shadow

        anchors.right: out_right_shadow.left
        anchors.bottom: out_bottom_shadow.top
        anchors.top: out_top_shadow.bottom
        width: 1 * root.ratio

        color: timer.is_blinked ? timer.blink_color : (is_positive && !body.button_pressed ? (root.dark_shadow_color == "" ? root.black : root.dark_shadow_color) : "transparent")
    }

    // Rectangle pour l'ombre intérieure supérieure
    Rectangle {
        id: in_top_shadow

        anchors.top: out_top_shadow.bottom
        anchors.left: out_left_shadow.right
        anchors.right: in_right_shadow.left
        height: 1 * root.ratio

        color: timer.is_blinked ? timer.blink_color : (is_positive && !body.button_pressed ? (root.light_shadow_color == "" ? root.shadow : root.light_shadow_color) : "transparent")
    }

    // Rectangle pour l'ombre intérieure gauche
    Rectangle {
        id: in_left_shadow

        anchors.left: out_left_shadow.right
        anchors.top: out_top_shadow.bottom
        anchors.bottom: in_bottom_shadow.top
        width: 1 * root.ratio

        color: timer.is_blinked ? timer.blink_color : (is_positive && !body.button_pressed ? (root.light_shadow_color == "" ? root.shadow : root.light_shadow_color) : "transparent")
    }
}