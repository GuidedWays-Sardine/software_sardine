import QtQuick 2.0
import QtQuick.Controls 2.15


//https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
//Comment créer un élément personalisé

//https://doc.qt.io/qt-5/qtquickcontrols2-customize.html#customizing-stackview
//Comment personaliser un stackview


Item{
    id: root


    //Propriétés liés à la position et à la taille de l'objet
    property double default_x: 0                //position du string_input pour les dimensions minimales de la fenêtre (w_min*h_min)
    property double default_y: 0
    property double default_width: 100          //dimensions du string_input pour les dimensions minimales de la fenêtre (w_min*h_min)
    property double default_height: 40
    anchors.fill: parent

    //permet à partir des valeurs de positions et dimensions par défauts de calculer
    readonly property int w_min: 640
    readonly property int h_min: 480
    readonly property real ratio:  (parent.width >= w_min && parent.height >= h_min) ? parent.width/w_min * (parent.width/w_min < parent.height/h_min) + parent.height/h_min * (parent.width/w_min >= parent.height/h_min) : 1  //parent.height et parent.width représentent la taille de la fenêtre
    //permet de centrer la fenêtre lorsque le ratio de la fenêtre n'est pas la même que celui utilisé
    readonly property double x_offset: (parent.width/parent.height > w_min/h_min) && (parent.width >= w_min && parent.height >= h_min) ? (parent.width - w_min * root.ratio) / 2 : 0
    readonly property double y_offset: (parent.width/parent.height < w_min/h_min) && (parent.width >= w_min && parent.height >= h_min) ? (parent.height - h_min * root.ratio) / 2 : 0

    //Propriétés liés aux valeurs limites et la valeur actuellement sélectionnée
    property string placeholder_text: ""
    property int max_text_length: 1000
    onMax_text_lengthChanged: { if(root.max_text_length < 0){ root.max_text_length = 0 } }    //S'assure que la taille maximale est toujours positive
    readonly property string text: body.text

    //Propriétés sur le titre et le texte
    property string title: ""
    property int font_size: 12

    //Propriétés liés à l'état du valueinput
    property bool is_activable: true         //si le valueinput peut être activée
    property bool is_dark_grey: !is_activable//est ce que le texte doit-être en gris foncé ?
    property bool is_positive: false         //si le valueinput doit-être visible en couche positive (sinon négatif)
    property bool is_visible: true           //si le valueinput est visible
    visible: root.is_visible

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


    //Différents signal handlers (à écrire en python)
    signal value_changed()


    //Fonction pour remettre la valeur par défaut dans le valueinput (maximum_calue si is_max_default est vrai sinon minimum_value)
    function clear(){
        // Vérifie si la valeur actuellement visible est différente que la valeur quand vidé, change la valeur et appelle le signal value_changed si c'est le cas
        var changed = body.text != ""
        body.text = ""
        if(changed){
            value_changed()
        }
    }

    //Fonction permettant de changer la valeur du valueinput (de manière sécurisée)
    function change_value(new_value){
        var changed = new_value != body.text
        body.text = new_value
        if(changed){
            value_changed()
        }
    }


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
            timer.blink_color = color
            timer.is_blinked = true

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

    //Timer utile pour le fonctionnement des différents mode des boutons
    Timer {
        id: timer

        property int time_left: 0
        property int period: 0
        property string light_shadow_color: ""
        property string dark_shadow_color: ""
        property bool is_blinked: false  //Permet de savoir aux bordures si elles doivent être de la couleur du clignotement
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
                is_blinked = false
            }
            //Sinon inverse les couleurs des bordures et redémarre le chronomètre
            else {
                is_blinked = !is_blinked
                timer.start()
            }
        }
    }    




    //Zone d'entrée de texte
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

        //rectangle de fond
        background: Rectangle {
            anchors.fill: parent
            color: root.dark_blue
        }

        validator: RegExpValidator{
            regExp: /^[^*|\":<>[\]{}`\\'\/]+$/
        }

        //détecte quand le texte entrée est changé et vérifie si la valeur entrée est valide
        onDisplayTextChanged: {
            value_changed()
        }

        //Signal appelé lorsque le curseur apparait ou disparait de la zone de texte (permet d'arrêter les cligontements)
        onCursorVisibleChanged: {
            root.stop_blink()
        }
    }



    //Titre du stringinput
    INI_text {
        id: title_text

        default_x: root.default_x + 2
        default_y: root.default_y - 4 - font_size

        text: root.title
        font_size: root.font_size

        is_dark_grey: root.is_dark_grey || root.max_text_length <= 0
    }


    //Ombre extérieure
    //Rectangle pour l'ombre extérieure inférieure
    Rectangle {
        id: out_bottom_shadow

        anchors.right: body.right
        anchors.bottom: body.bottom
        anchors.left: body.left
        height: 1 * root.ratio

        color: timer.is_blinked ? timer.blink_color : root.shadow
    }

    //Rectangle pour l'ombre extérieure droite
    Rectangle {
        id: out_right_shadow

        anchors.right: body.right
        anchors.bottom: body.bottom
        anchors.top: body.top
        width: 1 * root.ratio

        color: timer.is_blinked ? timer.blink_color : root.shadow
    }

    //Rectangle pour l'ombre extérieure supérieure
    Rectangle {
        id: out_top_shadow

        anchors.top: body.top
        anchors.left: body.left
        anchors.right: out_right_shadow.left
        height: 1 * root.ratio

        color: timer.is_blinked ? timer.blink_color : root.black
    }

    //Rectangle pour l'ombre extérieure gauche
    Rectangle {
        id: out_left_shadow

        anchors.top: body.top
        anchors.left: body.left
        anchors.bottom: out_bottom_shadow.top
        width: 1 * root.ratio

        color: timer.is_blinked ? timer.blink_color : root.black
    }


    //Ombre intérieure
    //Rectangle pour l'ombre intérieure inférieure
    Rectangle {
        id: in_bottom_shadow

        anchors.bottom: out_bottom_shadow.top
        anchors.left: out_left_shadow.right
        anchors.right: out_right_shadow.left
        height: 1 * root.ratio

        color: is_positive ? (timer.is_blinked ? timer.blink_color : root.black) : "transparent"
    }

    //Rectangle pour l'ombre intérieure droite
    Rectangle {
        id: in_right_shadow

        anchors.right: out_right_shadow.left
        anchors.bottom: out_bottom_shadow.top
        anchors.top: out_top_shadow.bottom
        width: 1 * root.ratio

        color: is_positive ? (timer.is_blinked ? timer.blink_color : root.black) : "transparent"
    }

    //Rectangle pour l'ombre intérieure supérieure
    Rectangle {
        id: in_top_shadow

        anchors.top: out_top_shadow.bottom
        anchors.left: out_left_shadow.right
        anchors.right: in_right_shadow.left
        height: 1 * root.ratio

        color: is_positive ? (timer.is_blinked ? timer.blink_color : root.shadow) : "transparent"
    }

    //Rectangle pour l'ombre intérieure gauche
    Rectangle {
        id: in_left_shadow

        anchors.left: out_left_shadow.right
        anchors.top: out_top_shadow.bottom
        anchors.bottom: in_bottom_shadow.top
        width: 1 * root.ratio

        color: is_positive ? (timer.is_blinked ? timer.blink_color : root.shadow) : "transparent"
    }
}
