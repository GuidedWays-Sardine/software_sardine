import QtQuick 2.15
import QtQuick.Controls 2.15


// https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
// Comment créer un élément personalisé

Item {
    id: root

    // Propriétés liées à la position et à la taille du INI_switchbutton
    property double default_x: 0              // Position du INI_switchbouton pour les dimensions minimales de la fenêtre (w_min*h_min)
    property double default_y: 0
    property double default_width: 100        // Dimensions du INI_switchbouton pour les dimensions minimales de la fenêtre (w_min*h_min)
    property double default_height: 40
    anchors.fill: parent

    // Propriétés liées à l'image et au texte que l'utilisateur peut rajouter sur le bouton
    property var elements: []
    onElementsChanged: {
        // Cas où la nouvelle liste est vide (vide le texte et n'appelle pas le signal selection_changed)
        if(root.elements.length === 0) {
            body.text = ""
            body.image = ""
        }
        // Cas où la valeur actuelle n'est pas dans la nouvelle liste (met le texte au premier élément et appelle le signal selection_changed)
        else if((!root.elements.includes(body.text) && !image_mode) || (!root.elements.includes(body.image) && image_mode)) {
            body.image = image_mode ? root.elements[0] : ""
            body.text = image_mode ? "" : root.elements[0]
            root.selection_changed()
        }
    }
    readonly property int elements_count: elements.length
    property bool image_mode: false
    onImage_modeChanged: {
        // Swap both the image and the text
        if(image_mode) {
            body.image = body.text
            body.text = ""
        }
        else {
            body.text = body.image
            body.image = ""
        }
    }

    // Propriétés sur les textes valides (texte visible sur le switchbutton et titre)
    readonly property string selection_text: image_mode ? body.image : body.text
    readonly property int selection_index: image_mode ? (elements.includes(body.image) ? elements.indexOf(body.image) : -1) :
                                                        (elements.includes(body.text) ? elements.indexOf(body.text) : -1)
    property string title: ""                 // Texte à afficher au dessus du INI_switchbutton
    property int font_size: 12                // Taille de la police du texte

    // Propriétés liées à l'état du bouton
    property bool is_activable: true          // Si le bouton peut être activée
    property bool is_dark_grey: !is_activable // Si le texte doit-être en gris foncé ?
    property bool is_positive: false          // Si le bouton doit-être visible en couche positive (sinon négatif)
    property bool is_visible: true            // Si le bouton est visible
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
    signal clicked()                        // Appelé lorsque le INI_switchbutton est cliqué
    signal selection_changed()              // Appelé si la sélection été changée du INI_switchbutton change (par sélection de l'utilisateur ou par fonction)


    //Fonction permettant de changer la valeur active (peut prendre l'index de l'élément ou sa valeur)
    function change_selection(new_selection){
        // Cas où la liste d'éléments n'est pas vide
        if (root.elements_count > 0) {
            // Cas où la nouvelle sélection est un entier
            if(typeof new_selection == typeof 1) {
                // Cas où le nouvel index est valide
                if (new_selection >= 0 && new_selection < root.elements_count) {
                    // regarde si la nouvelle sélection diffère de l'ancienne
                    if ((image_mode ? body.image : body.text).toLowerCase() != root.elements[new_selection].toLowerCase()) {
                        // Change le texte et/ou l'image et appelle le signal selection_changed
                        body.text = image_mode ? "" : root.elements[new_selection]
                        body.image = image_mode ? root.elements[new_selection] : ""
                        root.selection_changed()
                    }
                }
                // Cas où le nouvel index est invalide
                else {
                    console.log(`Le nouvel index de sélection pour le INI_switchbutton : \"${root.objectName}\" n'est pas dans les limites (0 <= ${new_selection} < ${root.elements_count} non satisfait).`)
                }
            }
            // Cas où la sélection est un string (ou autre mais automatiquement convertit en string)
            else {
                // Récupère la liste des éléments sans les majuscules (pour rendre la recherche non sensible aux minuscules et majuscules)
                var lowercased_elements = root.elements.map(name => name.toLowerCase())

                // Cas où la nouvelle sélection se trouve dans la liste (sans prise en compte des minuscules et majuscules)
                if (lowercased_elements.includes(new_selection.toString().toLowerCase())) {
                    // Récupère l'index de la sélection et met la nouvelle sélection
                    var new_index = lowercased_elements.indexOf(new_selection.toString().toLowerCase())

                    if ((image_mode ? body.image : body.text).toLowerCase() != root.elements[new_index].toLowerCase()) {
                        // Change le texte et/ou l'image et appelle le signal selection_changed
                        body.text = image_mode ? "" : root.elements[new_index]
                        body.image = image_mode ? root.elements[new_index] : ""
                        root.selection_changed()
                    }
                }
                // Cas où la nouvelle sélection ne se trouve pas dans la liste (sans prise en compte des minuscules et majuscules)
                else {
                    console.log(`La nouvelle sélection pour le INI_switchbutton : \"${root.objectName}\" n'est pas dans la liste des éléments (${new_selection} =/= ${root.elements}).`)
                }
            }
        }
        // Cas où la liste ne contient aucun élément de sélection
        else {
            console.log(`Le INI_switchbutton : \"${root.objectName}\" n'a aucun élément à sélectionner. Impossible de changer la sélection à ` + ((typeof new_selection == typeof 1) ? `${new_selection}.` : `\"${new_selection}\".`))
        }
    }


    // Fonction de clignotement des bordures (met le INI_switchbutton en valeur)
    function blink(time=3, period=0.5, color=root.yellow) {
        // Appelle la fonction de clignotement du corp (la INI_button utilisé pour le switchbutton)
        body.blink(time, period, color)
    }

    // Fonction pour arréter le clignotement des bordures
    function stop_blink() {
        // Appelle la fonction de clignotement du corp (le INI_button utilisé pour le switchbutton)
        body.stop_blink()
    }



    // Bouton utilisé pour le corp du switchbutton
    INI_button {
        id: body

        default_x: root.default_x
        default_y: root.default_y
        default_height: root.default_height
        default_width: root.default_width

        text: ""
        image: ""

        is_activable: root.is_activable && root.elements.length > 1
        is_dark_grey: root.is_dark_grey || root.elements.length <= 1
        is_positive: root.is_positive

        // Appelé lorsque le bouton est cliqué
        onClicked: {
            // Arrête le clignotement
            body.stop_blink()

            // Cas où le INI_switchbutton contient plus d'un élément
            if (root.elements.length > 1) {
                // Récupère l'index de l'éméent active et passe au suivant
                var index = root.elements.indexOf(root.image_mode ? image : text)
                index = (index + 1) % root.elements.length

                // Cas où le INI_switchbutton est en mode image -> change l'image
                if(image_mode) {
                    image = root.elements[index]
                    text = ""
                }
                // Cas où le INI_switchbutton est en mode texte -> change le texte
                else {
                    text = root.elements[index]
                    image = ""
                }

                // Appelle les signaux reliés au switchbutton
                root.clicked()
                root.selection_changed()
            }
        }
    }

    // Titre du switchbutton
    INI_text {
        id: title_text

        default_x: root.default_x
        default_y: root.default_y - 4 - font_size

        text: root.title
        font_size: root.font_size

        is_dark_grey: root.is_dark_grey || root.elements.length <= 1
    }
}
