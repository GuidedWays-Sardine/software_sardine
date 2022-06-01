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

    // Propriétés liées à la position et à la taille du INI_integerinput
    property double default_x: 0              // Position du INI_integerinput pour les dimensions minimales de la fenêtre (w_min*h_min)
    property double default_y: 0
    property double default_width: 100        // Dimensions du INI_integerinput pour les dimensions minimales de la fenêtre (w_min*h_min)
    property double default_height: 40
    anchors.fill: parent

    // Calcule la taille et position réelle du composant à partir des dimensions de la fenêtre (parent) et de la taille minimale de celle-ci
    readonly property int w_min: 640
    readonly property int h_min: 480
    readonly property real ratio:  (parent.width >= w_min && parent.height >= h_min) ? parent.width/w_min * (parent.width/w_min < parent.height/h_min) + parent.height/h_min * (parent.width/w_min >= parent.height/h_min) : 1
    // Si le ratio n'est pas le même que celui de la fenêtre en taille minimale, décalle les composants pour qu'ils restent centrés
    readonly property double x_offset: (parent.width/parent.height > w_min/h_min) && (parent.width >= w_min && parent.height >= h_min) ? (parent.width - w_min * root.ratio) / 2 : 0
    readonly property double y_offset: (parent.width/parent.height < w_min/h_min) && (parent.width >= w_min && parent.height >= h_min) ? (parent.height - h_min * root.ratio) / 2 : 0

    // Propriétés liées aux valeurs limites et la valeur actuellement entrée
    property int minimum_value: 0             // Valeur minimale et maximale (en unité SI et en unité actuelle)
    property int maximum_value: 1
    readonly property int visible_minimum_value: validator.bottom
    readonly property int visible_maximum_value: validator.top
    property int visible_value: 0             // Valeur visible (prise en compte des taux de conversions)/Valeur enregistrée (équivalent unités SI)
    readonly property int value: (root.visible_value - root.unit_offset) / root.unit_factor

    // Propriétés sur les textes d'habillages ainsi que l'unité
    property string unit: ""                  // Valeur à changer pour le cas d'une unité non physique
    property var conversion_list: []          // Liste de conversions dans le cas d'unités physiques ; Format : [["name", factor(int), offset(int)], ...]
    property string unit_name: unit_text.text // Nom de l'unité actuellement utilisée
    property double unit_factor: 1.0          // Facteur de conversion (SI -> unité actuelle)
    property double unit_offset: 0.0          // Décalage de conversion (SI -> unité actuelle)
    property string title: ""                 // Texte à afficher au dessus du composant
    property int font_size: 12                // Taille de la police pour le titre (font_size) et pour les unités (unit_font_size)
    property int unit_font_size: root.font_size / 2

    // Propriétés liées à l'état du INI_integerinput
    property bool is_max_default: false       // Si la valeur par défaut (dans le placeholder) est la valeur max (ou min si mis sur false)
    property bool is_dark_grey: !is_activable // Si le texte doit-être en gris foncé ?
    property bool is_activable: true          // Si le INI_integerinput peut être activée
    property bool is_positive: false          // Si le INI_integerinput doit-être visible en couche positive (sinon négatif)
    property bool is_visible: true            // Si le INI_integerinput est visible
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
    signal value_changed()                    // Appelé lorsque la valeur a été changée (par l'utilisateur ou par une fonction)
    signal unit_changed()                     // Appelé lorsque l'unité a été changée (par l'utilisateur ou par une fonction)

    // Fonction pour remettre la valeur par défaut dans le INI_integerinput (maximum_value si is_max_default sinon minimum_value)
    function clear(){
        // Vérifie si la valeur actuellement visible est différente que la valeur quand vidé, change la valeur et appelle le signal value_changed si c'est le cas
        var changed = root.is_max_default ? (root.visible_value !== validator.top) : (root.visible_value !== validator.bottom)
        body.text = ""
        
        if(changed){
            root.visible_value = root.is_max_default ? validator.bottom : validator.top
            value_changed()
        }
    }

    // Fonction pour changer la valeur du INI_integerinput (de manière sécurisée)
    function change_value(new_value){   // L'unité toujours en équivalent SI
        // Convertit l'unité du système international au système actuel
        new_value = new_value * root.unit_factor + root.unit_offset

        // Si la valeur n'est pas valide (trop grand ou trop petite) la change
        if(new_value < validator.bottom || new_value > validator.top) {
            console.log(`Nouvelle valeur pour le INI_integerinput : \"${root.objectName}\" invalide (${validator.bottom} < ${new_value} < ${validator.top} non vérifié)`)
            new_value = new_value < validator.bottom ? validator.bottom: validator.top
        }
        
        // Si la nouvelle valeur est différente de l'actuelle, change la valeur, appelle le signal value_changed
        if(root.visible_value !== new_value){
            root.visible_value = new_value
            body.text = ((new_value === validator.bottom && !root.is_max_default) || (new_value === validator.top && root.is_max_default)) ? "" : new_value
            value_changed()
        }
    }

    // Fonction pour passer à l'unité suivante
    function next_unit() {
        // Cas où la liste de conversion n'est pas vide
        if(root.conversion_list.length > 1) {
            // Trouve l'index de l'élément qui suit l'élément actuel
            var index = 0
            while(index < root.conversion_list.length && root.conversion_list[index][0] != unit_text.text) {
                index += 1
            }
            index = (index + 1) % root.conversion_list.length

            // Change l'unité aparente
            unit_text.text = root.conversion_list[index][0]

            // Convertit la valeur en unité SI, puis change les facteurs et offset ainsi que la valeur actuelle
            var converted_value = (root.visible_value - root.unit_offset) / root.unit_factor
            root.unit_factor = root.conversion_list[index][1]
            root.unit_offset = root.conversion_list[index][2]
            change_value(converted_value)

            // Appelle le signal de changement d'unité
            root.unit_changed()
        }
    }

    // Fonction pour changer l'unité actuelle en une unité définie
    function change_unit(new_unit) {
        // Cas où la liste de conversion n'est pas vide et que l'unité n'est pas déjà l'unité utilisée
        if(root.conversion_list.length > 1 && new_unit != unit_text.text) {
            // Cherche l'index de l'unité envoyé
            var index = 0
            while(index < root.conversion_list.length && root.conversion_list[index][0] != new_unit) {
                index += 1
            }

            // Cas où l'unité a été trouvée (index inférieur à la taille de la liste)
            if (index < root.conversion_list.length) {
                // Change l'unité aparente
                unit_text.text = root.conversion_list[index][0]

                // Convertit la valeur en unité SI, puis change les facteurs et offset ainsi que la valeur actuelle
                var converted_value = (root.visible_value - root.unit_offset) / root.unit_factor
                root.unit_factor = root.conversion_list[index][1]
                root.unit_offset = root.conversion_list[index][2]
                change_value(converted_value)

                // Appelle le signal de changement d'unité
                root.unit_changed()
            }
            // Cas où l'unité n'a pas été trouvée, laisse un message de registre
            else {
                console.log(`L'unité \"${new_unit}\" pour le INI_integerinput : \"${root.objectName}\" inexistante. \n ${root.conversion_list}`)
            }
        }
    }

    // Fonction de clignotement des bordures (met le INI_integerinput en valeur)
    function blink(time=3, period=0.5, color=root.yellow) {
        // Si le temps et la période sont supérieurs à 0
        if(time > 0 && period > 0) {
            // Vérifie que la couleur envoyée est bonne, sinon la met en jaune
            var regex_color = new RegExp("^#(?:[0-9a-fA-F]{3}){1,2}$")
            if(!regex_color.test(color)) {
                console.log(`Valeur hex : \"${color}\" pour le clignotement du INI_integerinput : \"${root.objectName}\" invalide. Clignotement en jaune.`)
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
            console.log(`La période et le temps de clignotement du INI_integerinput : \"${root.objectName}\" ne peuvent pas être négatif (temps : ${time}s ; période : ${period}s)`)
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
            timer.time_left = timer.time_left - timer.period / 2.0

            // Si le temps de clignotement est inférieur à une demie période, change la période pour que le clignotement soit bon
            timer.period = Math.min(timer.period, timer.time_left * 2.0)

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


    // Détecte le changement de la valeur minimale
    onMinimum_valueChanged: {
        // Cas où la valeur minimale est supérieure à la valeur maximale
        if(root.minimum_value > root.maximum_value){
            // Change la borne maximale pour être identique à la nouvelle borne minimale
            console.log(`Nouvelle limite inférieure pour le INI_integerinput : \"${root.objectName}\" trop grande (min : ${validator.bottom} > ${validator.top} : max)`)
            root.maximum_value = root.minimum_value

            // Change la valeur pour qu'elle reste dans les bornes
            body.text = root.is_max_default ? validator.bottom : ""
            root.visible_value = validator.top
            value_changed()
        }
        // Cas où la valeur actuelle rentrée est inférieure à la nouvelle valeur minimale
        else if(body.text != "" && root.visible_value < validator.bottom){
            root.visible_value = validator.bottom
            body.text = (!root.is_max_default || root.maximum_value === root.minimum_value) ? "" : validator.bottom
            value_changed()
        }
        // Cas où aucune valeur n'est entrée et que is_max_default faux
        else if(body.text === "" && root.is_max_default) {
            root.visible_value = validator.bottom
            value_changed()
        }
        // Sinon la valeur est toujours dans les bornes, aucune action nécessaire
    }

    // Détecte le changement de la valeur maximale
    onMaximum_valueChanged: {
        // Cas où la valeur maximale est inférieure à la valeur minimale
        if(root.maximum_value < root.minimum_value){
            // Change la borne minimale pour être identique à la nouvelle borne maximale
            console.log(`Nouvelle limite supérieure pour le INI_integerinput : \"${root.objectName}\" trop faible (max : ${validator.top} < ${validator.bottom} : min)`)
            root.minimum_value = root.maximum_value

            // Change la valeur pour qu'elle reste dans les bornes
            body.text = root.is_max_default ? "" : validator.top
            root.visible_value = validator.top
            value_changed()
        }
        // Cas où la valeur actuelle rentrée est supériere à la nouvelle valeur maximale
        else if(body.text != "" && root.visible_value > validator.top){
            root.visible_value = validator.top
            body.text = (root.is_max_default || root.maximum_value === root.minimum_value) ? "" : validator.top
            value_changed()
        }
        // Cas où aucune valeur n'est entrée et que is_max_default vrai
        else if(body.text === "" && root.is_max_default) {
            root.visible_value = validator.top
            value_changed()
        }
        // Sinon la valeur est toujours dans les bornes, aucune action nécessaire
    }

    // Détecte le changement de la valeur à afficher par défaut (maximale ou minimale)
    onIs_max_defaultChanged: {
        // Cas où aucune valeur n'est entrée et que la valeur min et max diffèrent (la valeur va changer de borne)
        if(body.text == "") {
            root.visible_value = root.is_max_default ? validator.top : validator.bottom
            value_changed()
        }
    }

    // Détecte le changement de l'unité
    onUnitChanged: {
        // Cas où une unité est envoyée (sinon réinitialisée par onConversion_listChanged)
        if (root.unit != "") {
            // Crée une liste de conversion contenant l'unité et un facteur 1 et un décalage 0
            root.conversion_list = [[root.unit, 1, 0]]
            // Le signal onConversion_listChanged s'occupe du reste
        }
    }

    // Détecte le changement de la liste de conversion
    onConversion_listChanged: {
        // Cas où la liste contient au moins un élément
        if (root.conversion_list.length > 0) {
            // Vérifie pour chacune des conversions si le facteur et le décalage sont des entiers
            var bad_conversions = ""
            for(var i = 0; i < root.conversion_list.length; i++) {
                // Si le facteur de conversion ou le décalage ne sont pas des entiers, ajoute la ligne dans le message de registre
                if(parseInt(root.conversion_list[i][1]) != root.conversion_list[i][1] ||
                   parseInt(root.conversion_list[i][2]) != root.conversion_list[i][2]) {
                    bad_conversions = bad_conversions + `\n  -  ${root.conversion_list[i][0]} : ${root.conversion_list[i][1]} -> ${root.conversion_list[i][2]}`
                }
            }

            // Cas où au moins une mauvaise conversion a été détectée
            if (bad_conversions != "") {
                // Indique des conversions qui ne sont pas des entiers dans le registre
                console.log(`Les facteurs et décalages du composant INI_integerinput : \"${root.objectName}\" doivent être des entiers : ${bad_conversions}`)

                // Prend la valeur approchée de tous les coeficients et décalages
                var new_conversion_list = []
                for(var i = 0; i < root.conversion_list.length; i++) {
                    new_conversion_list.push([root.conversion_list[i][0], Math.round(root.conversion_list[i][1]), Math.round(root.conversion_list[i][2])])
                }
                // Met à jour la liste avec toutes les valeurs en entiers
                root.conversion_list = new_conversion_list
                // Ce signal sera appelé de nouveau, mais cette fois, aucune mauvais conversion ne sera détecté et le else sera executé
            }
            // Cas où aucune mauvaise conversion n'a été détectée
            else {
                // Regarde si l'unité actuelle se trouve dans la liste
                var index = 0
                while(index < root.conversion_list.length && root.conversion_list[index][0] != unit_text.text) {
                    index += 1
                }
                // L'unité a été changée si le nom ou le facteur ou le décalage sont différents
                var is_unit_changed = (index >= root.conversion_list.length || root.conversion_list[index][1] != root.unit_factor || root.conversion_list[index][2] != root.unit_offset)

                // Si l'unité n'a pas été trouvée, repasse l'index à 0
                index = index % root.conversion_list.length

                // Cas où l'unité a été changée
                if (is_unit_changed) {
                    // Définit la nouvelle unité comme celle trouvée (ou la première si non trouvée)
                    var converted_value = root.value
                    unit_text.text = root.conversion_list[index][0]
                    root.unit_factor = root.conversion_list[index][1]
                    root.unit_offset = root.conversion_list[index][2]
                    change_value(converted_value)

                    // Appelle le signal de changement d'unité
                    root.unit_changed()
                }
            }
        }
        // Cas où la liste de conversion est vide
        else {
            // Change la conversion list pour contenir une unité vide
            root.conversion_list = [["", 1, 0]]
            // Le signal sera appelé de nouveau, mais cette fois-ci le if sera appelé
        }

        // Repasse la valeur root.unit comme un string vide
        root.unit = ""
    }

    // Sécurité dans le cas où l'utilisateur change la variable visible_value (déconseillé)
    onVisible_valueChanged: {
        // Si la valeur visible n'est pas dans le rang correct
        if (root.visible_value < validator.bottom || root.visible_value > validator.top) {
            console.log(`Nouvelle valeur pour le INI_integerinput : \"${root.objectName}\" invalide (${validator.bottom} < ${root.visible_value} < ${validator.top} non vérifié)`)
            root.visible_value < validator.bottom ? (root.is_max_default ? validator.bottom : "") : (root.is_max_default ? "" : validator.top)
        }
        // Change le texte et appelle le signal value changed
        body.text = root.visible_value
        value_changed()
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
        readOnly: !root.is_activable
        echoMode: TextInput.Normal

        placeholderText: root.is_max_default ? validator.top : validator.bottom
        placeholderTextColor: root.is_dark_grey ? root.dark_grey : root.medium_grey

        // Rectangle de fond
        background: Rectangle {
            anchors.fill: parent
            color: root.dark_blue
        }

        // Indique que seul des valeurs entières peuvent être entrées
        validator: IntValidator {
            id: validator

            bottom: root.minimum_value * root.unit_factor + root.unit_offset
            top: root.maximum_value * root.unit_factor + root.unit_offset
        }

        // Mouse area permettant de détecter le double clic (et de changer d'unité)
        MouseArea
        {
            anchors.fill: parent
            propagateComposedEvents: true

            // Détecte lorsque le INI_integerinput est cliqué, permet de démarrer l'édition de la valeur
            onClicked: {
                if (root.is_activable) {
                    body.forceActiveFocus()
                    root.focus_gained()
                }
            }

            // Détecte lorsque le INI_integerinput est double cliqué, permet de changer l'unité active
            onDoubleClicked: {
                next_unit()
                root.focus_gained()
            }
        }

        // Détecte quand le texte entré est changé et vérifie si la valeur entrée est valide
        onDisplayTextChanged: {
            // Commence par arrêter le clignotement
            root.stop_blink()

            // Cas où une valeur a été entrée
            if(body.text != ""){
                // Récupère la valeur
                var input_value = parseInt(body.text)

                // Si la valeur est supérieur à la valeur maximale (s'occupe de remettre la valeur dans les limites
                if(input_value > 0 && input_value > validator.top) {
                    input_value = validator.top
                    body.text = root.is_max_default ? "" : input_value
                }
                // Vérifie que la valeur entrée est supérieur à la valeur minimale dans onCursorVisibleChanged
                else if(input_value < 0 && input_value < validator.bottom) {
                    input_value = validator.bottom
                    body.text = root.is_max_default ? input_value : ""
                }

                // Vérifie si la nouvelle valeur est différente de l'ancienne, si oui appelle le signal value_changed et la change
                if(root.visible_value !== input_value && input_value >= validator.bottom && input_value <= validator.top){
                    root.visible_value = input_value
                    value_changed()
                }
            }
            // Cas où la case a été vidée
            else if((root.is_max_default && root.visible_value != validator.top) || (!root.is_max_default && root.visible_value != validator.bottom)) {
                root.visible_value = root.is_max_default ? validator.top : validator.bottom
                value_changed()
            }
        }

        // Détecte lorsque le composant perd le focus (lorsque la barre clignotante disparait de l'encadré)
        onCursorVisibleChanged: {
            // Commence par arréter le clignotement (s'il y en a un)
            root.stop_blink()

            // Cas où une valeur a été entrée
            if(body.text != ""){
                // Récupère la valeur
                var input_value = parseInt(body.text)

                // Vérifie que la valeur actuelle n'est pas trop faible
                if(input_value < validator.bottom) {
                    input_value = validator.bottom
                    body.text = root.is_max_default ? input_value : ""
                }

                // Vérifie que la valeur actuelle n'est pas trop élevée
                if(input_value > validator.top) {
                    input_value = validator.top
                    body.text = root.is_max_default ? "" : input_value
                }

                // Vérifie si la nouvelle valeur est différente de l'ancienne, si oui appelle le signal value_changed et la change
                if(root.visible_value !== input_value){
                    root.visible_value = input_value
                    value_changed()
                }
            }

            // Indique que le composant a perdu le focus
            root.focus_lost()
        }
    }


    // Titre du integerinput
    INI_text {
        id: title_text

        default_x: root.default_x
        default_y: root.default_y - 4 - font_size

        text: root.title
        font_size: root.font_size

        is_dark_grey: root.is_dark_grey
    }

    // Unité du integerinput
    INI_text {
        id: unit_text

        default_x: root.default_x + root.default_width + 2
        default_y: root.default_y + root.default_height - 2 - font_size

        text: ""
        font_size: root.unit_font_size

        is_dark_grey: true
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
