import QtQuick 2.0
import QtQuick.Controls 2.15


// https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
// Comment créer un élément personalisé

// https://doc.qt.io/qt-5/qtquickcontrols2-customize.html#customizing-textfield
// Comment personaliser un textfield

// https://doc.qt.io/archives/qt-4.8/texthandling.html
// Utilisation d'un validateur


Item{
    id: root

    // Propriétés liées à la position et à la taille du INI_stringinput
    property double default_x: 0              // Position du INI_stringinput pour les dimensions minimales de la fenêtre (w_min*h_min)
    property double default_y: 0
    property double default_width: 100        // Dimensions du INI_stringinput pour les dimensions minimales de la fenêtre (w_min*h_min)
    property double default_height: 40
    anchors.fill: parent

    // Calcule la taille et position réelle du composant à partir des dimensions de la fenêtre (parent) et de la taille minimale de celle-ci
    readonly property int w_min: 640
    readonly property int h_min: 480
    readonly property real ratio:  (parent.width >= w_min && parent.height >= h_min) ? parent.width/w_min * (parent.width/w_min < parent.height/h_min) + parent.height/h_min * (parent.width/w_min >= parent.height/h_min) : 1
    // Si le ratio n'est pas le même que celui de la fenêtre en taille minimale, décalle les composants pour qu'ils restent centrés
    readonly property double x_offset: (parent.width/parent.height > w_min/h_min) && (parent.width >= w_min && parent.height >= h_min) ? (parent.width - w_min * root.ratio) / 2 : 0
    readonly property double y_offset: (parent.width/parent.height < w_min/h_min) && (parent.width >= w_min && parent.height >= h_min) ? (parent.height - h_min * root.ratio) / 2 : 0

    // Propriétés liées aux valeurs limites et la valeur actuellement sélectionnée
    property int max_text_length: 1000        // Nombre de charactères maximum de la chaine de charactères
    onMax_text_lengthChanged: {root.max_text_length = Math.max(root.max_text_length, 0)}    // S'assure que la taille maximale est toujours positive
    readonly property string value: body.text  // Texte entré dans la zone de texte

    // Propriétés sur le titre et le texte
    property string title: ""                 // Texte à afficher au dessus du composant
    property string placeholder_text: ""      // Texte à afficher lorsqu'aucun texte n'est entré
    property int font_size: 12                // Taille de la police du text et placeholder_text

    // Propriétés liées à l'état du INI_stringinput
    property bool is_activable: true          // Si le INI_stringinput peut être activée
    property bool is_dark_grey: !is_activable // Si le texte doit-être en gris foncé ?
    property bool is_positive: false          // Si le INI_stringinput doit-être visible en couche positive (sinon négatif)
    property bool is_visible: true            // Si le INI_stringinput est visible
    visible: root.is_visible

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


    // Signaux à surcharger en QML ou en Python
    signal focus_gained()                     // Appelé lorsque le composant passe en mode édition (permet d'afficher le clavier virtuel)
    signal focus_lost()                       // Appelé lorsque le composant sort du mode édition (permet de cacher le clavier virtuel)
    signal value_changed()                    // Appelé lorsque le texte a été changé (par l'utilisateur ou par une fonction)


    // Fonction pour remettre la valeur par défaut dans le INI_stringinput (maximum_calue si is_max_default est vrai sinon minimum_value)
    function clear(){
        // Vérifie si la valeur actuellement visible est différente que la valeur quand vidé, change la valeur et appelle le signal value_changed si c'est le cas
        var changed = body.text != ""
        body.text = ""
        if(changed){
            value_changed()
        }
    }

    // Fonction permettant de changer la valeur du INI_stringinput (de manière sécurisée)
    function change_value(new_value){
        // S'assure que le texte envoyé suis bien la Regular Expression du validateur
        var new_corrected_value = new_value.replace(validator.regExp, "")

        // Si la nouvelle valeur corrigée est différente de la valeur envoyée laisse un message de registre
        if (new_corrected_value != new_value) {
            console.log(`Le nouveau texte pour le INI_stringinput : \"${root.objectName}\" contient des charactères interdits (\"${new_corrected_value}\" -> \"${new_value}\" [< > : “ / \\ | ? *])`)
        }

        // S'assure que le texte corrigé n'est pas trop long
        if (new_corrected_value.length > root.max_text_length) {
            console.log(`Le nouveau texte pour le INI_stringinput : \"${root.objectName}\" ; \"${new_corrected_value}\" est trop long (${new_corrected_value.length} charactères contre ${root.max_text_length} maximum).`)
            new_corrected_value = new_corrected_value.slice(0, root.max_text_length)
        }

        // Si la nouvelle valeur est différente de l'ancienne, la change et appelle le signal value_changed()
        if(new_corrected_value != body.text){
            body.text = new_corrected_value
            value_changed()
        }
    }


    // Fonction de clignotement des bordures (met le INI_stringinput en valeur)
    function blink(time=3, period=0.5, color=root.yellow) {
        // Si le temps et la période sont supérieurs à 0
        if(time > 0 && period > 0) {
            // Vérifie que la couleur envoyée est bonne, sinon la met en jaune
            var regex_color = new RegExp("^#(?:[0-9a-fA-F]{3}){1,2}$")
            if(!regex_color.test(color)) {
                console.log(`Valeur hex : \"${color}\" pour le clignotement du INI_stringinput : \"${root.objectName}\" invalide. Clignotement en jaune.`)
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
            console.log(`La période et le temps de clignotement du INI_stringinput : \"${root.objectName}\" ne peuvent pas être négatif (temps : ${time}s ; période : ${period}s)`)
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



    // Zone d'entrée de texte
    TextField {
        id: body

        x: root.x_offset + root.default_x * root.ratio
        y: root.y_offset + root.default_y * root.ratio
        width: root.default_width * root.ratio
        height: root.default_height * root.ratio

        color: root.is_dark_grey ? root.dark_grey : (body.text != "" ? root.grey : root.medium_grey)
        font.pixelSize: root.font_size * root.ratio
        readOnly: !root.is_activable || root.max_text_length <= 0
        echoMode: TextInput.Normal
        maximumLength: root.max_text_length

        placeholderText: root.placeholder_text
        placeholderTextColor: root.is_dark_grey ? root.dark_grey : root.medium_grey

        // Rectangle de fond
        background: Rectangle {
            anchors.fill: parent
            color: root.dark_blue
        }

        // Validateur pour enlever les charatères non permis dans les noms de fichiers (< > : “ / \ | ? *)
        validator: RegExpValidator{
            id: validator

            regExp: /^[^*|\":<>[\]{}`\\'\/]+$/
        }


        // Détecte quand le texte entrée est changé et vérifie si la valeur entrée est valide
        onDisplayTextChanged: {
            // Commence par arrêter le clignotement
            root.stop_blink()

            value_changed()
        }

        // Détecte lorsque le composant perd le focus (lorsque la barre clignotante disparait de l'encadré)
        onCursorVisibleChanged: {
            // Arrête le potentiel clignotement du composant
            root.stop_blink()

            // Si l'édition commence appelle le signal focus_gained, si l'édition s'arrête appelle le signal focus_list
            if (body.cursorVisible) {
                root.focus_gained()
            }
            else {
                root.focus_lost()
            }
        }
    }


    // Titre du stringinput
    INI_text {
        id: title_text

        default_x: root.default_x
        default_y: root.default_y - 4 - font_size

        text: root.title
        font_size: root.font_size

        is_dark_grey: root.is_dark_grey || root.max_text_length <= 0
    }


    // Ombre extérieure
    // Rectangle pour l'ombre extérieure inférieure
    Rectangle {
        id: out_bottom_shadow

        anchors.right: body.right
        anchors.bottom: body.bottom
        anchors.left: body.left
        height: 1 * root.ratio

        color: timer.is_blinked ? timer.blink_color : root.shadow
    }

    // Rectangle pour l'ombre extérieure droite
    Rectangle {
        id: out_right_shadow

        anchors.right: body.right
        anchors.bottom: body.bottom
        anchors.top: body.top
        width: 1 * root.ratio

        color: timer.is_blinked ? timer.blink_color : root.shadow
    }

    // Rectangle pour l'ombre extérieure supérieure
    Rectangle {
        id: out_top_shadow

        anchors.top: body.top
        anchors.left: body.left
        anchors.right: out_right_shadow.left
        height: 1 * root.ratio

        color: timer.is_blinked ? timer.blink_color : root.black
    }

    // Rectangle pour l'ombre extérieure gauche
    Rectangle {
        id: out_left_shadow

        anchors.top: body.top
        anchors.left: body.left
        anchors.bottom: out_bottom_shadow.top
        width: 1 * root.ratio

        color: timer.is_blinked ? timer.blink_color : root.black
    }


    // Ombre intérieure
    // Rectangle pour l'ombre intérieure inférieure
    Rectangle {
        id: in_bottom_shadow

        anchors.bottom: out_bottom_shadow.top
        anchors.left: out_left_shadow.right
        anchors.right: out_right_shadow.left
        height: 1 * root.ratio

        color: is_positive ? (timer.is_blinked ? timer.blink_color : root.black) : "transparent"
    }

    // Rectangle pour l'ombre intérieure droite
    Rectangle {
        id: in_right_shadow

        anchors.right: out_right_shadow.left
        anchors.bottom: out_bottom_shadow.top
        anchors.top: out_top_shadow.bottom
        width: 1 * root.ratio

        color: is_positive ? (timer.is_blinked ? timer.blink_color : root.black) : "transparent"
    }

    // Rectangle pour l'ombre intérieure supérieure
    Rectangle {
        id: in_top_shadow

        anchors.top: out_top_shadow.bottom
        anchors.left: out_left_shadow.right
        anchors.right: in_right_shadow.left
        height: 1 * root.ratio

        color: is_positive ? (timer.is_blinked ? timer.blink_color : root.shadow) : "transparent"
    }

    // Rectangle pour l'ombre intérieure gauche
    Rectangle {
        id: in_left_shadow

        anchors.left: out_left_shadow.right
        anchors.top: out_top_shadow.bottom
        anchors.bottom: in_bottom_shadow.top
        width: 1 * root.ratio

        color: is_positive ? (timer.is_blinked ? timer.blink_color : root.shadow) : "transparent"
    }
}
