import QtQuick 2.15
import QtQuick.Controls 2.15


Item {
    id: root


    //Propriétés liés à la position et à la taille de l'objet
    property double default_x: 0               //position du switchbouton pour les dimensions minimales de la fenêtre (640*480)
    property double default_y: 0
    property double default_width: 100         //dimensions du switchbouton pour les dimensions minimales de la fenêtre (640*480)
    property double default_height: 40
    anchors.fill: parent

    //Propriétés liés à l'image et au texte que l'utilisateur peut rajouter sur le bouton
    property var elements: []
    onElementsChanged: {
        //Cas où la nouvelle liste est vide (vide le texte et n'appelle pas le signal selection_changed)
        if(root.elements.length === 0) {
            body.text = ""
        }
        //Cas où la valeur actuelle n'est pas dans la nouvelle liste (met le texte au premier élément et appelle le signal selection_changed)
        else if(!root.elements.includes(body.text)) {
            body.text = root.elements[0]
            root.selection_changed()
        }
    }
    readonly property int elements_count: elements.length

    //Propriétés sur les textes valides (texte visible sur le switchbutton et titre)
    readonly property string selection_text: body.text
    readonly property string selection_index: elements.includes(body.text) ? elements.indexOf(body.text) : -1
    property string title: ""
    property int font_size: 12              //police du texte

    //Propriétés liés à l'état du bouton
    property bool is_activable: true         //si le bouton peut être activée
    property bool is_dark_grey: !is_activable//est ce que le texte doit-être en gris foncé ?
    property bool is_positive: false         //si le bouton doit-être visible en couche positive (sinon négatif)
    property bool is_visible: true           //si le bouton est visible
    visible: root.is_visible



    //Différents signal handlers (à écrire en python)
    signal clicked()                        //détecte quand le bouton est cliqué
    signal selection_changed()                  //détecte si la valeur a été changée



    //Fonction permettant de changer la valeur active (peut prendre l'index de l'élément ou sa valeur)
    function change_selection(new_selection){
        // Si la nouvelle sélection est un int et que la valeur à l'index n'est pas la même que celle déjà visible, change la valeur et appelle le signal associé
        if(typeof new_active === typeof root.font_size && new_active < root.elements.length && root.elements[new_active].toUpperCase() !== body.text.toUpperCase()){
            body.text = root.elements[new_active]
            root.selection_changed()
        }
        //Si la nouvelle sélection est un string et que la valeur ne correspond pas à celle déjà entrée, cherche l'élément avec le même index (recherche sans prendre en compte les majuscules et minuscules)
        else if(typeof new_active === typeof root.selection_text && new_active.toUpperCase() !== body.text.toUpperCase()){
            var uppercased = root.elements.map(name => name.toUpperCase())
            //Vérifie que le texte en majuscule est dans la liste, si oui, le change et appelle le signal associé
            if(uppercased.includes(new_active.toUpperCase())) {
                var new_index = uppercased.indexOf(new_active.toUpperCase())
                body.text = root.elements[new_index]
                root.selection_changed()
            }
        }
    }



    //INI_button permettant de réaliser le switchbutton
    INI_button {
        id: body

        default_x: root.default_x
        default_y: root.default_y
        default_height: root.default_height
        default_width: root.default_width

        text: ""

        is_activable: root.is_activable && root.elements.length > 1
        is_dark_grey: root.is_dark_grey || root.elements.length <= 1
        is_positive: root.is_positive

        //signal activé lorsque le bouton est cliqué
        onClicked: {
            //récupère l'index de l'élément actuel et affiche le suivant (ou le premier s'il est au bout du tableau)
            var index = root.elements.indexOf(text)
            index = (index + 1) % root.elements.length
            text = root.elements[index]

            //Appelle les signaux reliés au switchbutton
            root.clicked()
            root.selection_changed()
        }
    }

    //titre du switchbutton
    INI_text {
        id: title_text

        text: root.title
        font_size: root.font_size

        default_x: root.default_x + 2
        default_y: root.default_y - 4 - font_size

        is_dark_grey: root.is_dark_grey || root.elements.length <= 1
    }
}
