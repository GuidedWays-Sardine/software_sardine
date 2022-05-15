import QtQuick 2.0
import QtQuick.Controls 2.15


//https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
//Comment créer un élément personalisé

//https://doc.qt.io/qt-5/qtquickcontrols2-customize.html#customizing-stackview
//Comment personaliser un stackview


Item{
    id: root

    //Propriétés liés à la position et à la taille de l'objet
    property double default_x: 0                //position du integer_input pour les dimensions minimales de la fenêtre (w_min*h_min)
    property double default_y: 0
    property double default_width: 100          //dimensions du integer_input pour les dimensions minimales de la fenêtre (w_min*h_min)
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
    property int minimum_value: 0
    property int maximum_value: 1
    property int visible_value: 0
    readonly property int value: (root.visible_value - root.unit_offset) / root.unit_factor

    //propriétés sur les textes d'habillages
    property string title: ""
    property string unit: ""
    property var conversion_list: []    // format [[name, factor, offset], ...]
    property string unit_name: unit_text.text
    property double unit_factor: 1.0
    property double unit_offset: 0.0
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
        var changed = root.is_max_default ? (root.visible_value !== validator.top) : (root.visible_value !== validator.bottom)
        body.text = ""
        
        if(changed){
            root.visible_value = root.is_max_default ? validator.bottom : validator.top
            value_changed()
        }
    }

    //Fonction permettant de changer la valeur du valueinput (de manière sécurisée)
    function change_value(new_value){   //l'unité toujours en équivalent SI
        //convertit l'unité du système international au système actuel
        new_value = new_value * root.unit_factor + root.unit_offset

        //Si la valeur n'est pas valide (trop grand ou trop petite) la change
        if(new_value < validator.bottom || new_value > validator.top) {
            console.log(`Nouvelle valeur pour le INI_integerinput : \"${root.objectName}\" invalide (${validator.bottom} < ${new_value} < ${validator.top} non vérifié)`)
            new_value = new_value < validator.bottom ? validator.bottom: validator.top
        }
        
        // Si la valeur vaut la valeur min sans is_max_default ou max avec is_max_default, vide la zone de texte, sinon met la valeur envoyée
        body.text = ((new_value === validator.bottom && !root.is_max_default) || (new_value === validator.top && root.is_max_default)) ? "" : new_value

        //Si la valeur a été changée, appelle le signal value_changed
        if(value !== new_value){
            root.visible_value = new_value
            value_changed()
        }
    }

    function next_unit() {
        //Cas où la liste de conversion n'est pas vide
        if(root.conversion_list.length > 1) {
            //trouve l'index de l'élément qui suit l'élément actuel
            var index = 0
            while(index < root.conversion_list.length && root.conversion_list[index][0] != unit_text.text) {
                index += 1
            }
            index = (index + 1) % root.conversion_list.length

            //Change l'unité aparente
            unit_text.text = root.conversion_list[index][0]

            //convertit la valeur en unité SI, puis change les facteurs et offset ainsi que la valeur actuelle
            var converted_value = (root.visible_value - root.unit_offset) / root.unit_factor
            root.unit_factor = root.conversion_list[index][1]
            root.unit_offset = root.conversion_list[index][2]
            change_value(converted_value)
        }
    }

    function change_unit(new_unit) {
        //Cas où la liste de conversion n'est pas vide
        if(root.conversion_list.length > 1) {
            //trouve l'index de l'élément qui suit l'élément actuel
            var index = 0
            while(index < root.conversion_list.length && root.conversion_list[index][0] != new_unit) {
                index += 1
            }
            // Cas où l'unité a été trouvée
            if (index < root.conversion_list.length) {
                //Change l'unité aparente
                unit_text.text = root.conversion_list[index][0]

                //convertit la valeur en unité SI, puis change les facteurs et offset ainsi que la valeur actuelle
                var converted_value = (root.visible_value - root.unit_offset) / root.unit_factor
                root.unit_factor = root.conversion_list[index][1]
                root.unit_offset = root.conversion_list[index][2]
                change_value(converted_value)
            }
            // Cas où l'unité n'a pas été trouvée
            else {
                // Laisse un message de debug
                console.log(`L'unité \"${new_unit}\" pour le INI_integerinput : \"${root.objectName}\" inexistante. \n ${root.conversion_list}`)
            }
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
        //cas où la valeur minimale est supérieure à la valeur maximale
        if(root.minimum_value > root.maximum_value){
            // Change la borne maximale pour être identique à la nouvelle borne minimale
            console.log(`Nouvelle limite inférieure pour le INI_integerinput : \"${root.objectName}\" trop grande (min : ${validator.bottom} > ${validator.top} : max)`)
            root.maximum_value = root.minimum_value
            // Change la valeur pour qu'elle reste dans les bornes
            body.text = root.is_max_default ? validator.bottom : ""
            root.visible_value = validator.top
            value_changed()
        }
        //cas où la valeur actuelle rentrée est inférieure à la nouvelle valeur minimale
        else if(body.text != "" && root.visible_value < validator.bottom){
            root.visible_value = validator.bottom
            body.text = (!root.is_max_default || root.maximum_value === root.minimum_value) ? "" : validator.bottom
            value_changed()
        }
        //Cas où aucune valeur n'est entrée et que is_max_default faux
        else if(body.text === "" && root.is_max_default) {
            root.visible_value = validator.bottom
            value_changed()
        }
        //Sinon la valeur est toujours dans les bornes
    }

    //Signal détectant quand la valeur maximale est changée
    onMaximum_valueChanged: {
        //cas où la valeur maximale est inférieure à la valeur minimale
        if(root.maximum_value < root.minimum_value){
            // Change la borne minimale pour être identique à la nouvelle borne maximale
            console.log(`Nouvelle limite supérieure pour le INI_integerinput : \"${root.objectName}\" trop faible (max : ${validator.top} < ${validator.bottom} : min)`)
            root.minimum_value = root.maximum_value
            // Change la valeur pour qu'elle reste dans les bornes
            body.text = root.is_max_default ? "" : validator.top
            root.visible_value = validator.top
            value_changed()
        }
        //cas où la valeur actuelle rentrée est supériere à la nouvelle valeur maximale
        else if(body.text != "" && root.visible_value > validator.top){
            root.visible_value = validator.top
            body.text = (root.is_max_default || root.maximum_value === root.minimum_value) ? "" : validator.top
            value_changed()
        }
        //cas où aucune valeur n'est entrée et que is_max_default vrai
        else if(body.text === "" && root.is_max_default) {
            root.visible_value = validator.top
            value_changed()
        }
        // Sinon la valeur est toujours dans les bornes
    }

    //Signal détectact lorsque is_max_default est changé
    onIs_max_defaultChanged: {
        //Dans le cas où aucune valeur n'est entrée et que la valeur min et max diffèrent (la valeur va changer de borne)
        if(body.text == "") {
            root.visible_value = root.is_max_default ? validator.top : validator.bottom
            value_changed()
        }
    }

    //Signal appelé lorsque l'unité est changée
    onUnitChanged: {
        // Dans le cas où une unité est envoyée
        if (root.unit != "") {
            // Crée une liste de conversion contenant l'unité et un facteur 1 et un décallage 0
            root.conversion_list = [[root.unit, 1, 0]]
            // Le signa onConversion_listChanged s'occupera du reste
        }
    }

    //signal appelé lorsque la liste d'unité est change
    onConversion_listChanged: {
        // Si la liste n'est pas vide, initialise l'unité à utiliser
        if (root.conversion_list.length > 0) {
            //Vérifie pour chacune des conversions si le facteur et le décallage sont des entiers
            var bad_conversions = ""
            for(var i = 0; i < root.conversion_list.length; i++) {
                // Si le facteur de conversion ou le décallage ne sont pas des entiers, ajoute la ligne dans le warning
                if(parseInt(root.conversion_list[i][1]) != root.conversion_list[i][1] ||
                   parseInt(root.conversion_list[i][2]) != root.conversion_list[i][2]) {
                    bad_conversions = bad_conversions + `\n  -  ${root.conversion_list[i][0]} : ${root.conversion_list[i][1]} -> ${root.conversion_list[i][2]}`
                }
            }
            if (bad_conversions != "") {
                // Indique des conversions qui ne sont pas des entiers
                console.log(`Les facteurs et décallages du composant INI_integerinput : \"${root.objectName}\" doivent être des entiers : ${bad_conversions}`)

                //prend la valeur approchée de tous les coeficients et décalages
                var new_conversion_list = []
                for(var i = 0; i < root.conversion_list.length; i++) {
                    new_conversion_list.push([root.conversion_list[i][0], Math.round(root.conversion_list[i][1]), Math.round(root.conversion_list[i][2])])
                }
                //Met à jour la liste avec toutes les valeurs en entiers
                root.conversion_list = new_conversion_list
                // Ce signal sera appelé de nouveau, mais cette fois, aucune mauvais conversion ne sera détecté et le else sera executé
            }
            else {
                // Remet le facteur a 1 et le décallage à 0
                var converted_value = root.value

                // Regarde si l'unité actuelle se trouve dans la liste
                var index = 0
                while(index < root.conversion_list.length && root.conversion_list[index][0] != unit_text.text) {
                    index += 1
                }
                //si l'unité n'a pas été trouvée, repasse l'index à 0
                index = index % root.conversion_list.length

                //Définit la nouvelle unité comme celle trouvée (ou la première si non trouvée)
                unit_text.text = root.conversion_list[index][0]
                root.unit_factor = root.conversion_list[index][1]
                root.unit_offset = root.conversion_list[index][2]
                change_value(converted_value)
            }

        }
        // Si la liste est vide, change le texte pour un texte vide ainsi que le facteur et le décallage à 0
        else {
            var converted_value = root.value
            unit_text.text = ""
            root.unit_factor = 1.0
            root.unit_offset = 0.0
            change_value(converted_value)
        }

        // Repasse la valeur root.unit comme un string vide
        root.unit = ""



        //remet le facteur a 1 et le décallage à 0
        var converted_value = root.value
        root.unit_factor = 1
        root.unit_offset = 0
        change_value(converted_value)

        //si la liste n'est pas vide, regarde si l'unité se trouve dans la liste de conversion envoyée
        if (root.conversion_list.length > 0) {
            //Vérifie pour chacune des conversions si le facteur et le décallage sont des entiers
            var bad_conversions = ""
            for(var i = 0; i < root.conversion_list.length; i++) {
                // Si le facteur de conversion ou le décallage ne sont pas des entiers, ajoute la ligne dans le warning
                if(parseInt(root.conversion_list[i][1]) != root.conversion_list[i][1] ||
                   parseInt(root.conversion_list[i][2]) != root.conversion_list[i][2]) {
                    bad_conversions = bad_conversions + `\n  -  ${root.conversion_list[i][0]} : ${root.conversion_list[i][1]} -> ${root.conversion_list[i][2]}`
                }
            }
            if (bad_conversions != "") {
                console.log(`Les facteurs et décallages du composant INI_integerinput : \"${root.objectName}\" doivent être des entiers : ${bad_conversions}`)
            }

            var index = 0
            while(index < root.conversion_list.length && root.conversion_list[index][0] != unit_text.text) {
                index += 1
            }
            //si l'unité n'a pas été trouvée, repasse l'index à 0
            index = index % root.conversion_list.length

            //Définit la nouvelle unité comme celle trouvée (ou la première si non trouvée)
            unit_text.text = root.conversion_list[index][0]
            root.unit_factor = root.conversion_list[index][1]
            root.unit_offset = root.conversion_list[index][2]
        }
    }

    //Sécurité dans le cas où l'utilisateur change la variable visible_value (déconseillé)
    onVisible_valueChanged: {
        //Si la valeur visible n'est pas dans le rang correct
        if (root.visible_value < validator.bottom || root.visible_value > validator.top) {
            console.log(`Nouvelle valeur pour le INI_integerinput : \"${root.objectName}\" invalide (${validator.bottom} < ${root.visible_value} < ${validator.top} non vérifié)`)
            root.visible_value < validator.bottom ? (root.is_max_default ? validator.bottom : "") : (root.is_max_default ? "" : validator.top)
        }
        // Change le texte et appelle le signal value changed
        body.text = root.visible_value
        value_changed()
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
        readOnly: !root.is_activable
        echoMode: TextInput.Normal

        placeholderText: root.is_max_default ? validator.top : validator.bottom
        placeholderTextColor: root.is_dark_grey ? root.dark_grey : root.medium_grey

        //rectangle de fond
        background: Rectangle {
            anchors.fill: parent
            color: root.dark_blue
        }

        //indique que seul des valeurs entières peuvent être entrées
        validator: IntValidator {
            id: validator

            bottom: root.minimum_value * root.unit_factor + root.unit_offset
            top: root.maximum_value * root.unit_factor + root.unit_offset
        }

        //Mouse area permettant de détecter le double clic (et de changer d'unité)
        MouseArea
        {
            anchors.fill: parent
            propagateComposedEvents: true

            //Signal appelé, lorsque le valueinput est cloqué, permet de démarrer l'édition de la valeur
            onClicked: {
                if (root.is_activable) {
                    body.forceActiveFocus()
                }
            }

            //Signal appelé lorsque le valueinput est double cliqué (permet de changer l'unité active)
            onDoubleClicked: {
                // Passe à l'unité suivante
                next_unit()
            }
        }

        //détecte quand le texte entrée est changé et vérifie si la valeur entrée est valide
        onDisplayTextChanged: {
            //Dans le cas où une valeur a été entrée
            if(body.text != ""){
                //Récupère la valeur
                var input_value = parseInt(body.text)

                //Si la valeur est supérieur à la valeur maximale (s'occupe de remettre la valeur dans les limites
                if(input_value > 0 && input_value > validator.top) {
                    input_value = validator.top
                    body.text = root.is_max_default ? "" : input_value
                }
                // On vérifira que la valeur entrée est supérieur à la valeur minimale dans onCursorVisibleChanged
                else if(input_value < 0 && input_value < validator.bottom) {
                    input_value = validator.bottom
                    body.text = root.is_max_default ? input_value : ""
                }

                //vérifie si la nouvelle valeur est différente de l'ancienne, si oui appelle le signal value_changed et la change
                if(root.visible_value !== input_value && input_value >= validator.bottom && input_value <= validator.top){
                    root.visible_value = input_value
                    value_changed()
                }
            }
            //Dans le cas où la case a été vidée
            else if((root.is_max_default && root.visible_value != validator.top) || (!root.is_max_default && root.visible_value != validator.bottom)) {
                root.visible_value = root.is_max_default ? validator.top : validator.bottom
                value_changed()
            }
        }

        //Détecte lorsque le composant perd le focus (lorsque la barre clignotante disparait de l'encadré)
        onCursorVisibleChanged: {
            //Commence par arréter le clignotement (s'il y en a un)
            root.stop_blink()

            //Dans le cas où une valeur a été entrée
            if(body.text != ""){
                //Récupère la valeur
                var input_value = parseInt(body.text)

                //S'assure que la valeur actuelle n'est pas trop faible
                if(input_value < validator.bottom) {
                    input_value = validator.bottom
                    body.text = root.is_max_default ? input_value : ""
                }

                // S'assure que la valeur actuelle n'est pas trop élevée
                if(input_value > validator.top) {
                    input_value = validator.top
                    body.text = root.is_max_default ? "" : input_value
                }

                //vérifie si la nouvelle valeur est différente de l'ancienne, si oui appelle le signal value_changed et la change
                if(root.visible_value !== input_value){
                    root.visible_value = input_value
                    value_changed()
                }
            }
        }
    }


    //Titre du integerinput
    INI_text {
        id: title_text

        default_x: root.default_x
        default_y: root.default_y - 4 - font_size

        text: root.title
        font_size: root.font_size

        is_dark_grey: root.is_dark_grey
    }

    //Unité du integerinput
    INI_text {
        id: unit_text

        default_x: root.default_x + root.default_width + 2
        default_y: root.default_y + root.default_height - 2 - font_size

        text: ""
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
