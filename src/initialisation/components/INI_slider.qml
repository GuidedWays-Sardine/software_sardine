import QtQuick 2.15
import QtQuick.Controls 2.15


// On zone changed
// On value changed
// Addmark
// change position

// https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
// Comment créer un élément personalisé

// https://doc.qt.io/qt-5/qtquickcontrols2-customize.html#customizing-slider
// Comment personaliser un bouton (Le INI_checkbutton se base surtout sur le INI_button)


Item {
    id: root

    // Propriétés liées à la position et à la taille du slider
    property double default_x: 0            // Position du INI_slider pour les dimensions minimales de la fenêtre (w_min*h_min)
    property double default_y: 0            // Ne prend pas en compte la
    property double default_bar_length: 400 // Longueur et épaisseur de la barre (ne prend pas en compte les composants adjacents)
    property double default_bar_height: 2
    property double default_button_size: 20 // taille par défaut des boutons d'ajout et d'enlèvement sections
    // Taille officielle du composant : x = default_bar_length + 2 * default_button_size ; 2 * default_button_size
    anchors.fill: parent

    // Calcule la taille et position réelle du composant à partir des dimensions de la fenêtre (parent) et de la taille minimale de celle-ci
    readonly property int w_min: 640
    readonly property int h_min: 480
    readonly property real ratio:  (parent.width >= w_min && parent.height >= h_min) ? parent.width/w_min * (parent.width/w_min < parent.height/h_min) + parent.height/h_min * (parent.width/w_min >= parent.height/h_min) : 1
    onRatioChanged: slider_graphic.requestPaint()
    // Si le ratio n'est pas le même que celui de la fenêtre en taille minimale, décalle les composants pour qu'ils restent centrés
    readonly property double x_offset: (parent.width/parent.height > w_min/h_min) && (parent.width >= w_min && parent.height >= h_min) ? (parent.width - w_min * root.ratio) / 2 : 0
    readonly property double y_offset: (parent.width/parent.height < w_min/h_min) && (parent.width >= w_min && parent.height >= h_min) ? (parent.height - h_min * root.ratio) / 2 : 0

    // Propriétés liées aux valeurs likmites et la valeur actuelle
    property double minimum_value: 0.0
    property double maximum_value: 0.0
    readonly property double visible_minimum_value: slider_floatinput.visible_minimum_value
    readonly property double visible_maximum_value: slider_floatinput.visible_maximum_value
    property int decimals: 2
    readonly property double visible_value: slider_floatinput.value
    readonly property double value: (root.visible_value - root.unit_offset) / root.unit_factor

    // Propriétés sur les unités
    property string unit: ""
    property var conversion_list: []
    property string unit_name: slider_floatinput.unit_name
    property double unit_factor: slider_floatinput.unit_factor
    property double unit_offset: slider_floatinput.unit_offset
    property string title: ""
    property int font_size: 12

    // Propriétés liées à l'état du INI_slider
    property bool is_editable: true
    onIs_editableChanged: { if (root.is_editable) { root.is_activable } }           // Le INI_slider ne peut pas être
    property bool is_activable: true
    onIs_activableChanged: { if (!root.is_activable) { root.is_editable = false } }
    property bool is_visible: true
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
    signal floatinput_focus_gained()
    signal floatinput_focus_lost()
    signal zone_changed()
    signal value_changed()
    signal unit_changed()


    // Fonction permettant de réinitialiser la valeur (valeur minimale par défaut)
    function clear() {
        // Vide le  la valeur du INI_floatinput
        slider_floatinput.clear()
        // La position du slider sera changée automatiquement
    }

    // Fonction permettant de changer la valeur
    function change_value(new_value) {
        // Cas où la valeur est trop faible ou trop élevée
        if (new_value < root.minimum_value || new_value > root.maximum_value) {
            // Laisse un message de registre et met la valeur dans les limites
            console.log(`Nouvelle valeur pour le INI_slider : \"${root.objectName}\" invalide (${root.visible_minimum_value} < ${new_value} < ${root.visible_maximum_value} non vérifié)`)
            new_value = new_value < root.minimum_value ? root.minimum_value : root.maximum_value
            // La vérification est aussi effectuée dans le INI_floatinput, cependant le message d'erreur indiquerait le INI_floatinput et non le INI_slider (plus compliqué à corriger)
        }

        // Change la valeur sur le slider
        slider_floatinput.change_value(new_value)
    }



    // Détecte quand la valeur minimale change
    onMinimum_valueChanged: {
        // Cas où la valeur minimale est supérieure à la valeur maximale
        if ( root.minimum_value > root.maximum_value ) {
            // Change la borne maximale pour être identique à la nouvelle borne minimale
            console.log(`Nouvelle limite inférieure pour le INI_slider : \"${root.objectName}\" trop grande (min : ${root.minimum_value}(SI) > ${root.maximum_value}(SI) : max)`)
            root.maximum_value = root.minimum_value
            slider_floatinput.maximum_value = root.maximum_value
        }

        // Indique la nouvelle valeur minimale au slider
        slider_floatinput.minimum_value = root.minimum_value
    }

    // Détecte quand la valeur minimale change
    onMaximum_valueChanged: {
        // Cas où la valeur minimale est supérieure à la valeur maximale
        if ( root.maximum_value < root.minimum_value ) {
            // Change la borne maximale pour être identique à la nouvelle borne minimale
            console.log(`Nouvelle limite supérieure pour le INI_slider : \"${root.objectName}\" trop faible (max : ${root.maximum_value}(SI) < ${root.minimum_value}(SI) : min)`)
            root.minimum_value = root.maximum_value
            slider_floatinput.minimum_value = root.minimum_value
        }

        // Indique la nouvelle valeur minimale au slider
        slider_floatinput.maximum_value = root.maximum_value
    }

    // Détecte le changement d'unité
    onUnitChanged: {
        // Cas où une unité est entrée
        if (root.unit !== "") {
            root.conversion_list = [[root.unit, 1.0, 0.0]]
            root.unit = ""
        }
    }



    // Partie principale du slider
    Slider {
        id: control

        // x -> début de la structure du slider ; y -> centre de la structure du slider
        x: root.x_offset + root.default_x * root.ratio
        y: root.y_offset + (root.default_y - 2 * root.default_button_size + root.default_bar_height * 6 / 2) * root.ratio
        width: root.default_bar_length * root.ratio
        height: 2 * root.default_button_size * root.ratio * root.is_activable
        // Multiplie par root.is_activable pour rendre la hauteur nul si le composant n'est pas activable et éviter que la valeur puisse être changée

        // Enlève les marges
        topPadding: 0
        bottomPadding: 0
        leftPadding: 0
        rightPadding: 0

        // limites (dépendent de celles qui ont été envoyées et de l'unité actuelle)
        from: root.minimum_value
        to: root.maximum_value

        // Indique le nombre de pas possibles (selon le nombre de décimales) facilite les coupures
        stepSize: Math.min(Math.pow(10, - root.decimals + parseInt(Math.log10(root.unit_factor))), 1)
        snapMode: Slider.SnapAlways


        // Appelé lorsque le slider est sélectionné ou relaché
        onPressedChanged: {
            // Refais le rendu de la partie déplaçable du slider
            slider_graphic.requestPaint()
        }

        // Appelé lorsque la valeur change
        onValueChanged: {
            // change la valeur sur le slider aussi et appelle le signal
            slider_floatinput.change_value(value)
            root.value_changed()
        }



        // Rectangles permettant de faire la structure statique du slider (bar horizontale et limites)
        background: Rectangle {
            id: body

            x: 0
            y: (2 * root.default_button_size - root.default_bar_height * 6 / 2) * root.ratio
            width: root.default_bar_length * root.ratio
            height: root.default_bar_height * root.ratio
            color: root.is_editable ? root.grey : root.dark_grey



            // Rectangles pour les deux limites de la barre
            Rectangle {
                x: 0
                y: root.default_bar_height * (1 - 6) / 2 * root.ratio
                width: root.default_bar_height / 2 * root.ratio
                height: root.default_bar_height * 6 * root.ratio

                color: body.color
            }

            Rectangle {
                x: root.default_bar_length * root.ratio - width
                y: root.default_bar_height * (1 - 6) / 2 * root.ratio
                width: root.default_bar_height / 2 * root.ratio
                height: root.default_bar_height * 6 * root.ratio

                color: body.color
            }
        }


        // Element permettant de correctement positioner la partie déplaçable du slider
        // La partie graphique de la partie
        handle: Item {
            id: slider_anchors
            x: control.visualPosition * (control.availableWidth - width)
            y: root.default_bar_height / 2 * root.ratio + (2 * root.default_button_size - root.default_bar_height * 6 / 2) * root.ratio
            width: 0
            height: 0
        }

        // Partie graphique de la partie déplaçable du slider
        Canvas {
            id: slider_graphic

            anchors.bottom: slider_anchors.bottom
            anchors.horizontalCenter: slider_anchors.horizontalCenter

            width: 2 * root.default_button_size * root.ratio
            height: (root.default_button_size - root.default_bar_height * 6 / 2) * root.ratio



            // Fonction permettant de refaire le rendu de la flèche lorsque son état change
            onPaint: {
                var ctx = getContext("2d")
                ctx.reset()
                ctx.moveTo(0, 0)
                ctx.lineTo(width , 0)
                ctx.lineTo(width / 2 , height)
                ctx.closePath()
                ctx.fillStyle = root.is_activable ? (control.pressed || slider_floatinput.is_editing ? root.medium_grey : root.grey) : root.dark_grey
                ctx.fill()
            }
        }
    }

    // floatinput pour indiquer et montrer la valeur
    INI_floatinput {
        id: slider_floatinput

        default_x: root.default_x - root.default_button_size + control.visualPosition * control.availableWidth / root.ratio
        default_y: root.default_y - 2 * root.default_button_size + root.default_bar_height* 6 / 2
        default_width: 2 * root.default_button_size
        default_height: root.default_button_size

        // Les valeurs minimales et maximales sont définies lors du chagement de celles-ci
        decimals: root.decimals
        conversion_list: root.conversion_list


        // Appelé lorsque le signal est en train d'être édité ou non
        onIs_editingChanged: {
            // Indique à la forme déplaçable du slider de se rerendre pour changer la couleur
            slider_graphic.requestPaint()

            // Cas où la valeur commence à être éditée, appelle le signal pour montrer/déplacer le clavier virtuel
            if (is_editing) {
                root.floatinput_focus_gained()
            }
            // Cas où la valeur arrête d'être éditée, appelle le signal pour cacher le clavier virtuel
            else {
                root.floatinput_focus_lost()
            }
        }

        // Appelé lorsque la valeur du INI_floatinput change (attention est aussi changé avec le drag)
        onValueChanged: {
            // Cas où le floatinput est sélectioné, et que la valeur est changé grâce à elle
            if (is_editing) {
                // Change la valeur sur le slider (pour le déplacer) et appelle le signal pour déplacer le clavier
                control.value = value
                root.floatinput_focus_gained()
            }
        }

        onUnit_changed: root.unit_changed()
    }


    // Textes pour indiquer la valeur minimale and maximale
    // Texte pour la valeur minimale
    INI_text {
        id: minimum_value_text

        default_x: root.default_x - default_text_width / 2
        default_y: root.default_y + root.default_bar_height * 6 / 2

        text: root.visible_minimum_value
        font_size: root.font_size

        is_dark_grey: !root.is_editable
    }

    // Texte pour la valeur maximale
    INI_text {
        id: maximum_value_text

        default_x: root.default_x + root.default_bar_length - default_text_width / 2
        default_y: root.default_y + root.default_bar_height * 6 / 2

        text: root.visible_maximum_value
        font_size: root.font_size

        is_dark_grey: !root.is_editable
    }


    // Texte pour le titre du INI_slider
    INI_text {
        id: title_text

        default_x: root.default_x + (root.default_bar_length - default_text_width) / 2
        default_y:  root.default_y + root.default_bar_height * 6 / 2

        // Titre + unité si un titre fourné, sinon just le titre
        text: `${root.title} (${root.unit_name})`
        font_size: root.font_size

        is_dark_grey: !root.is_activable
        is_visible: root.title !== ""
    }
}
