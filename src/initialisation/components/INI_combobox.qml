import QtQuick 2.0
import QtQuick.Controls 2.15


//https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
//Comment créer un élément personalisé

//https://doc.qt.io/qt-5/qtquickcontrols2-customize.html#customizing-combobox
//Comment personaliser un combobox


Item {
    id:root

    // Propriétés liées à la position et à la taille du comobobox
    property double default_x: 0               //position du combobox pour les dimensions minimales de la fenêtre (w_min*h_min)
    property double default_y: 0
    property double default_width: 100         //dimensions du combobox pour les dimensions minimales de la fenêtre (w_min*h_min)
    property double default_height: 40
    //anchors.fill: parent

    // Permet à partir des valeurs de positions et dimensions par défauts de calculer le ratio à appliquer aux dimensions
    readonly property int w_min: 640
    readonly property int h_min: 480
    readonly property real ratio:  (parent.width >= w_min && parent.height >= h_min) ? parent.width/w_min * (parent.width/w_min < parent.height/h_min) + parent.height/h_min * (parent.width/w_min >= parent.height/h_min) : 1  //parent.height et parent.width représentent la taille de la fenêtre
    // Permet de centrer la fenêtre lorsque le ratio de la fenêtre n'est pas la même que celui utilisé
    readonly property double x_offset: (parent.width/parent.height > w_min/h_min) && (parent.width >= w_min && parent.height >= h_min) ? (parent.width - w_min * root.ratio) / 2 : 0
    readonly property double y_offset: (parent.width/parent.height < w_min/h_min) && (parent.width >= w_min && parent.height >= h_min) ? (parent.height - h_min * root.ratio) / 2 : 0

    //OPTIMIZE : passer le composant en mode anchors.fill : parent et passer chacun des composants en coordonées
    x: root.x_offset + root.default_x * root.ratio
    y: root.y_offset + root.default_y * root.ratio
    width: root.default_width * root.ratio
    height: root.default_height * root.ratio

    // Propriétés liées aux donnés du combobox
    property var elements: ["NaN"]                              // Définit les éléments sélectionables du combobox
    readonly property int elements_count: combo.count           // Retient le nombre d'éléments sélectionables dans le combobox
    property int elements_displayed: 4                          // Définit le nombre d'éléments visibles dans le popup
    readonly property string selection_text: combo.displayText  // Texte (et index) de la sélection actuelle et précédente
    readonly property int selection_index: root.elements_count !== 0 ? combo.currentIndex : -1
    property string title: ""                                   // Texte à afficher au dessus du composant
    property int font_size: 12                                  // Police du texte

    // Propriétés liées à l'état du combobox
    property bool is_activable: true          // Si le combobox peut être activée (Elle le sera que si is_activable est à true et qu'il y a plus d'un élément dans le combobox)
    property bool is_dark_grey: !is_activable // Si le texte doit-être en gris foncé ?
    property bool is_positive: false          // Si le combobox doit-être visible en couche positive (sinon négative)
    property bool is_visible: true            // Si le combobox est visible
    visible: is_visible

    // Couleurs (ne peuvent pas être modifiés mais permet une mise à jour facile si nécessaire)
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


    // Signaux à surcharger en QML ou en Python
    signal combobox_opened()                  // Appelé lorsque le combobox s'ouvre
    signal combobox_closed()                  // Appelé lorsque le combobox se ferme (même si la sélection ne change pas)
    signal selection_changed()                // Appelé lorsque la sélection du combobox change (par sélection de l'utilisateur ou par fonction)


    //Fonction pour changer l'index du combobox en fonction de l'index ou du texte de la sélection souhaité
    function change_selection(new_selection){
        // Si la liste d'éléments contient au moins un élément
        if (combo.count > 0) {
            // Si la nouvelle sélection est un entier
            if (typeof new_selection === typeof 1) {
                // Si l'index est valide, change l'index de sélection pour le nouvel index, sinon laisse un message de registre
                if (new_selection >= 0 && new_selection < combo.count) {
                    combo.currentIndex = new_selection
                }
                else {
                    console.log(`Le nouvel index de sélection pour le INI_combobox : \"${root.objectName}\" n'est pas dans les limites (0 <= ${new_selection} < ${combo.count} non satisfait).`)
                }
            }
            // Sinon (dans le cas où c'est un string)
            else {
                 // Cherche l'index de la sélection
                 var selection_upper = new_selection.toString().toUpperCase()   // transforme en string (par sécurité) et le met en majuscules
                 var index = 0
                 while (index < combo.count && root.elements[index].toUpperCase() !== selection_upper) {
                    index++
                 }

                 // Si l'élément avec le bon index a été trouvé, change la sélection sinon change un message de registre
                 if (index >= 0 && index < combo.count) {
                    combo.currentIndex = index
                 }
                 else {
                    console.log(`La nouvelle sélection pour le INI_combobox : \"${root.objectName}\" n'est pas dans la liste des éléments (${new_selection} =/= ${root.elements}).`)
                 }
            }
        }
        else {
            console.log(`Le INI_combobox : \"${root.objectName}\" n'a aucun élément à sélectionner. Impossible de changer la sélection à ` + ((typeof new_selection == typeof 1) ? `${new_selection}.` : `\"${new_selection}\".`))
        }
    }

    // Fonction de clignotement des bordures (met le button en valeur)
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
        property bool is_blinked: false     // Indique si les coueleurs des bordures doivent être celles par défaut ou la couleur du clignotement
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

    //FIXME : à dégager
    Rectangle {
        id: dummy

        anchors.fill: parent
        color: root.yellow
        visible: true
    }


    // Inline component : combobox (crée une templace du combobox) -> l'instance est créée plus bas
    component INI_combobox_template: ComboBox {
        id: body

        anchors.fill: parent

        font.pixelSize: root.font_size * root.ratio
        font.family: "Verdana"
        flat: true

        // Flèche visible lorsque le combobox est fermée
        indicator: Canvas {
            id: canvas

            x: root.width - width - body.height/3
            y: body.topPadding + (body.availableHeight - height) / 2
            width: 12 * root.ratio
            height: 8 * root.ratio


            // Permet d'ouvrir le popup quand le combobox est sélectionné et appelle le signal handler
            Connections {
                target: body

                // Fonction détectant quand le combobox fermé a été cliquée
                function onPressedChanged() {
                    forceActiveFocus()
                    canvas.requestPaint()
                    if(root.is_activable && body.count > 1 && !body.pressed && !popup.visible)
                    {
                        root.stop_blink()
                        root.combobox_opened()
                    }
                }
            }

            // Gère la couleur et le placement de la flèche, s'actualise à chaque changement de taille et de clique
            onPaint: {
                var ctx = getContext("2d")
                ctx.reset()
                ctx.moveTo(0, 0)
                ctx.lineTo(width, 0)
                ctx.lineTo(width / 2, height)
                ctx.closePath()
                ctx.fillStyle = !body.pressed && !root.is_dark_grey && body.count > 1 ? root.grey : root.dark_grey
                ctx.fill()
            }
        }

        // Texte visible quand le combobox est fermée
        contentItem: Text {
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter

            text: body.displayText
            font: body.font
            color: !body.pressed && !root.is_dark_grey && body.count > 1 ? root.grey : root.dark_grey


            //Détecte quand la valeur du combobox est changé
            onTextChanged: {
                root.selection_changed()
            }
        }

        // Rectangle visible lorsque le combobox est fermée
        background: Rectangle {
            id: text_zone

            anchors.fill: parent

            color: root.dark_blue
        }

        // Menu de popup quand le combobox est ouverte
        popup: Popup {
            id: popup

            x: (root.is_positive ? 2 : 1) * root.ratio
            y: (root.default_height - 2) * root.ratio
            width: root.width - (is_positive ? 4 : 2) * root.ratio
            implicitHeight: ((body.count < root.elements_displayed ? body.height*body.count : body.height * root.elements_displayed) + (root.is_positive ? 7 : 8) * root.ratio) * (root.is_activable && body.count > 1)
            padding: 1 * root.ratio


            // Détecte quand celui-ci est fermé (peu importe la façon)
            onClosed: {
                if(root.is_activable && body.count > 1 && !body.pressed && !popup.visible)
                {
                    root.stop_blink()
                    root.combobox_closed()
                }
            }

            // Permet de lister les différents éléments, ajoute aussi une scrollbar s'il y a plus de 4 éléments
            contentItem: ListView {
                implicitHeight: contentHeight

                clip: true
                model: body.popup.visible && is_activable && body.count > 1 ? body.delegateModel : null
                currentIndex: body.highlightedIndex

                ScrollIndicator.vertical: ScrollIndicator { }
            }

            // Rectangle de fond (cache les widgets lorsque le combobox est ouverte
            background: Rectangle {
                color: root.dark_blue
            }
        }
    }


    // Crée une instance du combobox
    INI_combobox_template {
        id:combo

        anchors.fill: parent

        model: root.elements

        // Le delegate permet de définir la composition et la forme des éléments du combobox
        delegate: ItemDelegate {
            width: combo.width
            height: combo.height

            background: Rectangle {
                color: "transparent"
            }

            contentItem: Text {
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter

                text: modelData
                color: combo.highlightedIndex === index ? root.dark_grey : root.grey
                font: combo.font
            }
        }
    }


    // Titre du combobox
    INI_text {
        id: title_text

        default_x: 0
        default_y: - (root.font_size + 4) * root.ratio

        text: root.title
        font_size: root.font_size * root.ratio

        is_dark_grey: root.is_dark_grey || root.elements.length <= 1
    }


    // Ombre extérieure
    // Rectangle pour l'ombre extérieure supérieure
    Rectangle {
        id: out_top_shadow

        anchors.left: combo.left
        anchors.top: combo.top
        anchors.right: out_right_shadow.left
        height: 1 * root.ratio

        color: timer.is_blinked ? timer.blink_color : root.black
    }

    // Rectangle pour l'ombre extérieure droite
    Rectangle {
        id: out_right_shadow

        height: combo.popup.visible && is_activable && combo.count > 1 ? combo.height*((combo.count < root.elements_displayed ? combo.count : root.elements_displayed) + 1) + 7 * root.ratio : combo.height
        anchors.right: combo.right
        anchors.top: combo.top
        width: 1 * root.ratio

        color: (timer.is_blinked ? timer.blink_color : root.shadow)
    }

    // Rectangle pour l'ombre extérieure gauche
    Rectangle {
        id: out_left_shadow

        anchors.top: combo.top
        anchors.left: combo.left
        anchors.bottom: out_bottom_shadow.top
        width: 1 * root.ratio

        color: timer.is_blinked ? timer.blink_color : root.black
    }

    // Rectangle pour l'ombre extérieure inférieure
    Rectangle {
        id: out_bottom_shadow

        anchors.right: combo.right
        anchors.bottom: out_right_shadow.bottom
        anchors.left: combo.left
        height: 1 * root.ratio

        color: (timer.is_blinked ? timer.blink_color : root.shadow)
    }


    // Ombre intérieure
    // Rectangle pour l'ombre intérieur inférieure
    Rectangle {
        id: in_bottom_shadow

        anchors.bottom: out_bottom_shadow.top
        anchors.left: out_left_shadow.right
        anchors.right: out_right_shadow.left
        height: 1 * root.ratio

        color: root.is_positive ? (timer.is_blinked ? timer.blink_color : root.black) : "transparent"
    }

    // Rectangle pour l'ombre intérieur droite
    Rectangle {
        id: in_right_shadow

        anchors.right: out_right_shadow.left
        anchors.bottom: out_bottom_shadow.top
        anchors.top: out_top_shadow.bottom
        width: 1 * root.ratio

        color: root.is_positive ? (timer.is_blinked ? timer.blink_color : root.black) : "transparent"
    }

    // Rectangle pour l'ombre intérieur supérieure
    Rectangle {
        id: in_top_shadow

        anchors.top: out_top_shadow.bottom
        anchors.left: out_left_shadow.right
        anchors.right: in_right_shadow.left
        height: 1 * root.ratio

        color: root.is_positive ? (timer.is_blinked ? timer.blink_color : root.shadow) : "transparent"
    }

    // Rectangle pour l'ombre extérieure supérieure
    Rectangle {
        id: in_left_shadow

        anchors.left: out_left_shadow.right
        anchors.top: out_top_shadow.bottom
        anchors.bottom: in_bottom_shadow.top
        width: 1 * root.ratio

        color: root.is_positive ? (timer.is_blinked ? timer.blink_color : root.shadow) : "transparent"
    }
}