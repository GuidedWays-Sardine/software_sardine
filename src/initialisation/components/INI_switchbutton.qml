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
    property var text_list: []
    onText_listChanged: {
        //Cas où la nouvelle liste est vide (vide le texte et n'appelle pas le signal value_changed)
        if(root.text_list.length === 0) {
            body.text = ""
        }
        //Cas où la valeur actuelle n'est pas dans la nouvelle liste (met le texte au premier élément et appelle le signal value_changed)
        else if(!root.text_list.includes(body.text)) {
            body.text = root.text_list[0]
            root.value_changed
        }
    }

    //Propriétés sur les textes valides (texte visible sur le switchbutton et titre)
    readonly property string current_text: body.text
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
    signal text_changed()                  //détecte si la valeur a été changée



    //Fonction permettant de changer la valeur active (peut prendre l'index de l'élément ou sa valeur)
    function change_active(new_active){
        // Si la nouvelle sélection est un int et que la valeur à l'index n'est pas la même que celle déjà visible, change la valeur et appelle le signal associé
        if(typeof new_active === typeof root.font_size && new_active < root.text_list.length && root.text_list[new_active].toUpperCase() !== body.text.toUpperCase()){
            body.text = root.text_list[new_active]
            root.value_changed()
        }
        //Si la nouvelle sélection est un string et que la valeur ne correspond pas à celle déjà entrée, cherche l'élément avec le même index (recherche sans prendre en compte les majuscules et minuscules)
        else if(typeof new_active === typeof root.current_text && new_active.toUpperCase() !== body.text.toUpperCase()){
            var uppercased = root.text_list.map(name => name.toUpperCase())
            //Vérifie que le texte en majuscule est dans la liste, si oui, le change et appelle le signal associé
            if(uppercased.includes(new_active.toUpperCase())) {
                var new_index = uppercased.indexOf(new_active.toUpperCase())
                body.text = root.text_list[new_index]
                root.value_changed()
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

        is_activable: root.is_activable && root.text_list.length > 1
        is_dark_grey: root.is_dark_grey
        is_positive: root.is_positive

        //signal activé lorsque le bouton est cliqué
        onClicked: {
            //récupère l'index de l'élément actuel et affiche le suivant (ou le premier s'il est au bout du tableau)
            var index = root.text_list.indexOf(text)
            index = (index + 1) % root.text_list.length
            text = root.text_list[index]

            //Appelle les signaux reliés au switchbutton
            root.clicked()
            root.text_changed()
        }
    }

    //floatinput pour connaitre la puissance totale du train (relié à la puissance moteur)
    INI_text {
        id: title_text
        objectName: "title_text"

        text: root.title
        font_size: root.font_size

        default_x: root.default_x + 2
        default_y: root.default_y - 4 - font_size

        is_dark_grey: root.is_dark_grey
    }
}
