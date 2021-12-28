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
    x: root.default_x * root.ratio
    y: root.default_y * root.ratio
    width: root.default_width * root.ratio
    height: root.default_height * root.ratio
    visible: root.is_visible

    //Propriétés liés aux valeurs limites et la valeur actuellement sélectionnée
    property string placeholder_text: ""
    property int max_text_length: 1000
    readonly property string text: body.text

    property int font_size: 12

    //Propriétés liés à l'état du valueinput
    property bool is_dark_grey: !is_activable//est ce que le texte doit-être en gris foncé ?
    property bool is_activable: true         //si le valueinput peut être activée
    property bool is_positive: false         //si le valueinput doit-être visible en couche positive (sinon négatif)
    property bool is_visible: true           //si le valueinput est visible

    //Couleurs (ne peuvent pas être modifiés mais permet une mise à jour facile si nécessaire)
    readonly property string dark_blue: "#031122"   //partie 5.2.1.3.3  Nr 6
    readonly property string black: "#000000"       //partie 5.2.1.3.3  Nr 2
    readonly property string grey: "#C3C3C3"        //partie 5.2.1.3.3  Nr 3
    readonly property string medium_grey: "#969696" //partie 5.2.1.3.3  Nr 4
    readonly property string dark_grey: "#555555"   //partie 5.2.1.3.3  Nr 5
    readonly property string shadow: "#08182F"      //partie 5.2.1.3.3  Nr 7


    //Différents signal handlers (à écrire en python)
    signal text_changed()


    //Fonction pour remettre la valeur par défaut dans le valueinput (maximum_calue si is_max_default est vrai sinon minimum_value)
    function clear(){
        // Vérifie si la valeur actuellement visible est différente que la valeur quand vidé, change la valeur et appelle le signal value_changed si c'est le cas
        var changed = body.text != ""
        body.text = ""
        if(changed){
            text_changed()
        }
    }

    //Fonction permettant de changer la valeur du valueinput (de manière sécurisée)
    function change_text(new_text){
        var changed = new_text != body.text
        body.text = new_text
        if(changed){
            text_changed()
        }
    }

    //Zone d'entrée de texte
    TextField {
        id: body

        anchors.fill: parent

        color: root.is_dark_grey ? root.dark_grey : (body.text != "" ? root.grey : root.medium_grey)
        font.pixelSize: root.font_size * root.ratio
        readOnly: !root.is_activable
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
            text_changed()
        }
    }


    //Ombre extérieure
    //Rectangle pour l'ombre extérieure inférieure
    Rectangle {
        id: out_bottom_shadow

        height: 1 * root.ratio
        anchors.right: body.right
        anchors.bottom: body.bottom
        anchors.left: body.left

        color: root.shadow
    }

    //Rectangle pour l'ombre extérieure droite
    Rectangle {
        id: out_right_shadow

        width: 1 * root.ratio
        anchors.right: body.right
        anchors.bottom: body.bottom
        anchors.top: body.top

        color: root.shadow
    }

    //Rectangle pour l'ombre extérieure supérieure
    Rectangle {
        id: out_top_shadow

        height: 1 * root.ratio
        anchors.top: body.top
        anchors.left: body.left
        anchors.right: out_right_shadow.left

        color: root.black
    }

    //Rectangle pour l'ombre extérieure gauche
    Rectangle {
        id: out_left_shadow

        width: 1 * root.ratio
        anchors.top: body.top
        anchors.left: body.left
        anchors.bottom: out_bottom_shadow.top

        color: root.black
    }


    //Ombre intérieure
    //Rectangle pour l'ombre intérieure inférieure
    Rectangle {
        id: in_bottom_shadow

        height: 1 * root.ratio
        anchors.bottom: out_bottom_shadow.top
        anchors.left: out_left_shadow.right
        anchors.right: out_right_shadow.left

        color: is_positive ? root.black : "transparent"
    }

    //Rectangle pour l'ombre intérieure droite
    Rectangle {
        id: in_right_shadow

        width: 1 * root.ratio
        anchors.right: out_right_shadow.left
        anchors.bottom: out_bottom_shadow.top
        anchors.top: out_top_shadow.bottom

        color: is_positive ? root.black : "transparent"
    }

    //Rectangle pour l'ombre intérieure supérieure
    Rectangle {
        id: in_top_shadow

        height: 1 * root.ratio
        anchors.top: out_top_shadow.bottom
        anchors.left: out_left_shadow.right
        anchors.right: in_right_shadow.left

        color: is_positive ? root.shadow : "transparent"
    }

    //Rectangle pour l'ombre intérieure gauche
    Rectangle {
        id: in_left_shadow

        width: 1 * root.ratio
        anchors.left: out_left_shadow.right
        anchors.top: out_top_shadow.bottom
        anchors.bottom: in_bottom_shadow.top

        color: is_positive ? root.shadow : "transparent"
    }
}




