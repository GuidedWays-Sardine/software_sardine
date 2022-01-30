import QtQuick 2.0
import QtQuick.Controls 2.15


//https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
//Comment créer un élément personalisé

//https://doc.qt.io/qt-5/qtquickcontrols2-customize.html#customizing-stackview
//Comment personaliser un stackview


Item{
    id: root

    //Propriétés liés à la position et à la taille de l'objet
    property double default_x: 0                //position du bouton pour les dimensions quand la fenêtre fait du 640x480
    property double default_y: 0
    property double default_width: 100          //dimensions du bouton quand la fenêtre fait du 640x480
    property double default_height: 40
    anchors.fill: parent

    //permet à partir des valeurs de positions et dimensions par défauts de calculer
    readonly property real ratio:  (parent.width >= 640 && parent.height >= 480) ? parent.width/640 * (parent.width/640 < parent.height/480) + parent.height/480 * (parent.width/640 >= parent.height/480) : 1  //parent.height et parent.width représentent la taille de la fenêtre

    //Propriétés liés aux valeurs limites et la valeur actuellement sélectionnée
    property double minimum_value: 0
    property double maximum_value: 1
    property int decimals: 1000
    property double value: 0

    //propriétés sur les textes d'habillages
    property string title: ""
    property string unit: ""
    property int font_size: 12
    property int unit_font_size: root.font_size / 2

    //Propriétés liés à l'état du valueinput
    property bool is_max_default: false      //définit si la valeur par défaut (dans le placeholder) est la valeur max (ou mini si mis sur false)
    property bool is_dark_grey: !is_activable//est ce que le texte doit-être en gris foncé ?
    property bool is_activable: true         //si le valueinput peut être activée
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
        var changed = root.is_max_default ? root.value !== root.maximum_value : root.value !== root.minimum_value
        body.text = ""

        //Si la valeur a changée appelle le signal associé et change la valeur
        if(changed){
            root.value = root.is_max_default ? root.maximum_value : root.minimum_value
            value_changed()
        }
    }

    //Fonction permettant de changer la valeur du valueinput (de manière sécurisée)
    function change_value(new_value){
        //Si la valeur n'est pas valide (trop grand ou trop petite) la change
        if(new_value < root.minimum_value || new_value > root.maximum_value) {
            new_value = new_value < root.minimum_value ? root.minimum_value : root.maximum_value
        }

        // Si la valeur vaut la valeur min sans is_max_default ou max avec is_max_default, vide la zone de texte, sinon la met à la valeur approchée au bon nombre de décimales
        body.text = ((new_value === root.minimum_value && !root.is_max_default) || (new_value === root.maximum_value && root.is_max_default)) ? "" : (Math.floor(new_value * Math.pow(10, root.decimals))/Math.pow(10, root.decimals)).toString()

        //Si la valeur a été changée, appelle le signal value_changed
        if(value !== new_value){
            root.value = new_value
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
    
    

    //Signal détectant quand la valeur minimale est changée
    onMinimum_valueChanged: {
        //Cas où la valeur minimale est inférieure à 0
        if(root.minimum_value < 0){
            root.minimum_value = 0
        }

        //Cas où la valeur minimale est supérieure à la valeur maximale
        if(root.minimum_value > root.maximum_value){
            root.minimum_value = root.maximum_value
        }

        //cas où la valeur actuelle rentrée est inférieure à la nouvelle valeur minimale
        if(body.text != "" && parseFloat(body.text.replace(",", ".")) < root.minimum_value){
            root.value = root.minimum_value
            body.text = (root.is_max_default && root.maximum_value !== root.minimum_value) ? root.minimum_value.toString() : ""
            value_changed()
        }
        //cas où aucune valeur n'est entrée et que is_max_default faux
        else if(body.text === "" && !root.is_max_default){
            root.value = root.minimum_value
            value_changed()
            body.text = ""
        }
    }

    //Signal détectant quand la valeur maximale est changée
    onMaximum_valueChanged: {
        //cas où la valeur maximale est inférieure à la valeur minimale
        if(root.maximum_value < root.minimum_value){
            root.maximum_value = root.minimum_value
        }
        
        //cas où la valeur actuelle rentrée est supériere à la nouvelle valeur maximale
        if(body.text != "" && parseFloat(body.text.replace(",", ".")) > root.maximum_value){
            root.value = root.maximum_value
            body.text = (root.is_max_default || root.maximum_value === root.minimum_value) ? "" : root.maximum_value.toString()
            value_changed()
        }
        //cas où aucune valeur n'est entrée et que is_max_default vrai
        else if(body.text === "" && root.is_max_default) {
            root.value = root.maximum_value
            body.text = ""
            value_changed()
        }
    }

    //Signal détectact lorsque is_max_default est changé
    onIs_max_defaultChanged: {
        //Dans le cas où aucune valeur n'est entrée et que la valeur min et max diffèrent (la valeur va changer de borne)
        if(body.text == "" && root.maximum_value > root.minimum_value) {
            root.value = root.is_max_default ? root.maximum_value : root.minimum_value
            value_changed()
        }
    }



    //Zone d'entrée de texte
    TextField {
        id: body

        x: root.default_x * root.ratio
        y: root.default_y * root.ratio
        width: root.default_width * root.ratio
        height: root.default_height * root.ratio

        color: root.is_dark_grey ? root.dark_grey : (body.text != "" ? root.grey : root.medium_grey)
        font.pixelSize: root.font_size * root.ratio
        readOnly: !root.is_activable
        echoMode: TextInput.Normal

        placeholderText: root.is_max_default ? (Math.floor(root.maximum_value * Math.pow(10, root.decimals))/Math.pow(10, root.decimals)).toString() : (Math.floor(root.minimum_value * Math.pow(10, root.decimals))/Math.pow(10, root.decimals)).toString()
        placeholderTextColor: root.is_dark_grey ? root.dark_grey : root.medium_grey

        //rectangle de fond
        background: Rectangle {
            anchors.fill: parent
            color: root.dark_blue
        }

        //indique que seul des valeurs entières peuvent être entrées
        validator: DoubleValidator {

            locale: "RejectGroupSeparator"

            decimals: root.decimals
            bottom: root.minimum_value
            top: root.maximum_value
        }

        //détecte quand le texte entrée est changé et vérifie si la valeur entrée est valide
        onDisplayTextChanged: {
            //Dans le cas où une valeur a été entrée
            if(body.text != ""){
                //Récupère la valeur
                var input_value = parseFloat(body.text.replace(",", "."))
                
                //Si la valeur est supérieur à la valeur maximale (s'occupe de remettre la valeur dans les limites
                if(input_value > root.maximum_value) {
                    input_value = root.maximum_value
                    body.text = is_max_default ? "" : root.maximum_value.toString()
                }
                // On vérifira que la valeur entrée est supérieur à la valeur minimale dans onCursorVisibleChanged

                //vérifie si la nouvelle valeur est différente de l'ancienne, si oui appelle le signal value_changed et la change
                if(root.value !== input_value && input_value >= root.minimum_value){
                    root.value = input_value
                    value_changed()
                }
            }
            //Dans le cas où la case a été vidée
            else if((root.is_max_default && root.value != root.maximum_value) || (!root.is_max_default && root.value != root.minimum_value)) {
                root.value = root.is_max_default ? root.maximum_value : root.minimum_value
                value_changed()
            }
        }

        //Détecte lorsque le composant perd le focus (lorsque la barre clignotante disparait de l'encadré
        onCursorVisibleChanged: {
            //Commence par arréter le clignotement (s'il y en a un)
            root.stop_blink()

            //Dans le cas où une valeur a été entrée
            if(body.text != "") {
                //Récupère la valeur
                var input_value = parseFloat(body.text.replace(",", "."))

                //S'assure que la valeur actuelle n'est pas trop faible
                if(input_value < root.minimum_value) {
                    input_value = root.minimum_value
                    body.text = root.is_max_default ? root.minimum_value.toString() : ""
                }

                //vérifie si la nouvelle valeur est différente de l'ancienne, si oui appelle le signal value_changed et la change
                if(root.value !== input_value){
                    root.value = input_value
                    value_changed()
                }
            }
        }
    }


    //Titre du floatinput
    INI_text {
        id: title_text

        default_x: root.default_x + 2
        default_y: root.default_y - 4 - font_size

        text: root.title
        font_size: root.font_size

        is_dark_grey: root.is_dark_grey
    }

    //Unité du floatinput
    INI_text {
        id: unit_text

        default_x: root.default_x + root.default_width + 2
        default_y: root.default_y + root.default_height - 2 - font_size

        text: root.unit
        font_size: root.unit_font_size

        is_dark_grey: true
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
