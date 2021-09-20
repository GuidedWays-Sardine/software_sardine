import QtQuick 2.0
import QtQuick.Controls 2.15


//https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
//Comment créer un élément personalisé

//https://doc.qt.io/qt-5/qtquickcontrols2-customize.html#customizing-stackview
//Comment personaliser un stackview


Item{
    id: root

    //Propriétés liés à la position et à la taille de l'objet
    property int default_width: 100          //dimensions du bouton quand la fenêtre fait du 640x480
    property int default_height: 40
    property int default_x: 0                //position du bouton pour les dimensions quand la fenêtre fait du 640x480
    property int default_y: 0

    //permet à partir des valeurs de positions et dimensions par défauts de calculer
    readonly property real ratio:  (parent.width >= 640 && parent.height >= 480) ? parent.width/640 * (parent.width/640 < parent.height/480) + parent.height/480 * (parent.width/640 >= parent.height/480) : 1  //parent.height et parent.width représentent la taille de la fenêtre
    width: (root.default_width - 2) * root.ratio
    height: (root.default_height - 2) * root.ratio
    x: (root.default_x + 1) * root.ratio
    y: (root.default_y + 1) * root.ratio
    visible: root.is_visible

    //Propriétés liés aux valeurs limites et la valeur actuellement sélectionnée
    property int minimum_value: 0
    property int maximum_value: 1
    readonly property int value: body.text != "" ? parseInt(body.text) : (is_max_default ? root.maximum_value : root.minimum_value)   //Valeur actuelle
    property int previous_value: root.is_max_default ? root.maximum_value : root.minimum_value    //Ancienne valeur ; nécessaire pour détecter le changement de valeur et appeler value_changed()

    property int font_size: 12

    //Propriétés liés à l'état du valueinput
    property bool is_max_default: false      //définit si la valeur par défaut (dans le placeholder) est la valeur max (ou mini si mis sur false)
    property bool is_dark_grey: !is_activable//est ce que le texte doit-être en gris foncé ?
    property bool is_activable: true         //si le bouton peut être activée
    property bool is_positive: false         //si le bouton doit-être visible en couche positive (sinon négatif)
    property bool is_visible: true           //si le bouton est visible

    //Couleurs (ne peuvent pas être modifiés mais permet une mise à jour facile si nécessaire)
    readonly property string dark_blue: "#031122"   //partie 5.2.1.3.3  Nr 6
    readonly property string black: "#000000"       //partie 5.2.1.3.3  Nr 2
    readonly property string grey: "#C3C3C3"        //partie 5.2.1.3.3  Nr 3
    readonly property string dark_grey: "#969696"   //partie 5.2.1.3.3  Nr 5
    readonly property string shadow: "#08182F"      //partie 5.2.1.3.3  Nr 7


    //Différents signal handlers (à écrire en python)
    signal value_changed()


    //Fonction pour remettre la valeur par défaut dans le valueinput (maximum_calue si is_max_default est vrai sinon minimum_value)
    function clear(){
        // Vérifie si la valeur actuellement visible est différente que la valeur quand vidé, change la valeur et appelle le signal value_changed si c'est le cas
        var changed = root.is_max_default ? root.value !== root.maximum_value : root.value !== root.minimum_value
        body.text = ""
        if(changed){
            value_changed()
            root.previous_value = root.is_max_default ? root.maximum_value : root.minimum_value
        }
    }

    //Fonction permettant de changer la valeur du valueinput (de manière sécurisée)
    function change_value(new_value){
        //Si la valeur n'est pas valide (trop grand ou trop petite) la change
        if(new_value < root.minimum_value){
            new_value = root.minimum_value
        }
        else if(new_value > root.maximum_value){
            new_value = root.maximum_value
        }

        // Vérifie si la nouvelle valeur change de l'ancienne
        var changed = (root.value !== new_value)
        body.text = new_value.toString()
        if(changed){
            value_changed()
            root.previous_value = new_value
        }
    }


    //Signal détectant quand la valeur minimale est changée
    onMinimum_valueChanged: {
        //cas où la valeur actuelle rentrée est inférieure à la nouvelle valeur minimale
        if(body.text != "" && parseInt(body.text) < root.minimum_value){
            body.text = root.minimum_value.toString()
            value_changed()
            root.previous_value = root.minimum_value
        }
        //cas où aucune valeur n'est entrée et que is_max_default faux
        else if(body.text === "" && !root.is_max_default){
            value_changed()
            root.previous_value = root.minimum_value
        }
    }

    //Signal détectant quand la valeur maximale est changée
    onMaximum_valueChanged: {
        //cas où la valeur actuelle rentrée est supériere à la nouvelle valeur maximale
        if(body.text != "" && parseInt(body.text) > root.maximum_value){
            body.text = root.maximum_value.toString()
            value_changed()
            root.previous_value = root.maximum_value
        }
        //cas où aucune valeur n'est entrée et que is_max_default vrai
        else if(body.text === "" && root.ix_max_default) {
            value_changed()
            root.previous_value = root.maximum_value
        }
    }

    //Zone d'entrée de texte
    TextField {
        id: body

        anchors.fill: parent

        color: root.is_dark_grey ? root.dark_grey : (body.text != "" ? root.grey : root.dark_grey)
        font.pixelSize: root.font_size * root.ratio
        readOnly: !root.is_activable
        echoMode: TextInput.Normal

        placeholderText: root.is_max_default ? root.maximum_value.toString() : root.minimum_value.toString()
        placeholderTextColor: root.dark_grey

        //rectangle de fond
        background: Rectangle {
            anchors.fill: parent
            color: root.dark_blue
        }

        //indique que seul des valeurs entières peuvent être entrées
        validator: IntValidator {
            bottom: root.minimum_value
            top: root.maximum_value
        }

        //détecte quand le focus change (quand l'utilisateur valide son entrée) et vérifie si la valeur entrée rentre dans le validateur
        onFocusChanged: {
            if(body.text != "" && !body.focus){
                //cas où la valeur entrée est supérieur à la valeur maximale ou inférieur à la valeur minimale (remet la valeur dans les limites)
                if(parseInt(body.text) > root.maximum_value) {
                    body.text = root.maximum_value.toString()
                }
                else if (parseInt(body.text) < root.minimum_value) {
                    body.text = root.minimum_value.toString()
                }

                //vérifie si la nouvelle valeur est différente de l'ancienne, si oui appelle le signal value_changed
                if(parseInt(body.text) !== root.previous_value){
                    value_changed()
                    root.previous_value = parseInt(body.text)
                }
            }
            else if(!body.focus && ((root.is_max_default && root.previous_value != root.maximum_value) || (!root.is_max_default && root.previous_value != root.minimum_value))) {
                value_changed()
                root.previous_value = root.is_max_default ? root.maximum_value : root.minimum_value
            }
        }
    }


    //Ombre extérieure
    //Rectangle pour l'ombre extérieure inférieure
    Rectangle {
        id: out_bottom_shadow
        color: root.shadow
        width: root.width + 2 * root.ratio
        height: 2 * root.ratio
        anchors.horizontalCenter: body.horizontalCenter
        anchors.verticalCenter: body.bottom
    }

    //Rectangle pour l'ombre extérieure droite
    Rectangle {
        id: out_right_shadow
        color: root.shadow
        width: 2 * root.ratio
        height: root.height + 2 * root.ratio
        anchors.right: out_bottom_shadow.right
        anchors.bottom: out_bottom_shadow.bottom
    }

    //Rectangle pour l'ombre extérieure supérieure
    Rectangle {
        id: out_top_shadow
        color: root.black
        height: 2 * root.ratio
        anchors.top: out_right_shadow.top
        anchors.right: out_right_shadow.left
        anchors.left: out_bottom_shadow.left
    }

    //Rectangle pour l'ombre extérieure gauche
    Rectangle {
        id: out_left_shadow
        color: root.black
        width: 2 * root.ratio
        anchors.top: out_top_shadow.top
        anchors.left: out_top_shadow.left
        anchors.bottom: out_bottom_shadow.top
    }


    //Ombre intérieure
    //Rectangle pour l'ombre intérieure inférieure
    Rectangle {
        id: in_bottom_shadow
        color: is_positive ? root.black : "transparent"
        height: 2 * root.ratio
        anchors.bottom: out_bottom_shadow.top
        anchors.left: out_left_shadow.right
        anchors.right: out_right_shadow.left
    }

    //Rectangle pour l'ombre intérieure droite
    Rectangle {
        id: in_right_shadow
        color: is_positive ? root.black : "transparent"
        width: 2 * root.ratio
        anchors.right: out_right_shadow.left
        anchors.bottom: out_bottom_shadow.top
        anchors.top: out_top_shadow.bottom
    }

    //Rectangle pour l'ombre intérieure supérieure
    Rectangle {
        id: in_top_shadow
        color: is_positive ? root.shadow : "transparent"
        height: 2 * root.ratio
        anchors.top: out_top_shadow.bottom
        anchors.left: out_left_shadow.right
        anchors.right: in_right_shadow.left
    }

    //Rectangle pour l'ombre intérieure gauche
    Rectangle {
        id: in_left_shadow
        color: is_positive ? root.shadow : "transparent"
        width: 2 * root.ratio
        anchors.left: out_left_shadow.right
        anchors.top: out_top_shadow.bottom
        anchors.bottom: in_bottom_shadow.top
    }
}





