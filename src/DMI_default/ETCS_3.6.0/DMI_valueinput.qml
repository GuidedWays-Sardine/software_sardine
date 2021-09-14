import QtQuick 2.0
import QtQuick.Controls 2.15


//https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
//Comment créer un élément personalisé

//https://doc.qt.io/qt-5/qtquickcontrols2-customize.html#customizing-stackview
//Comment personaliser un stackview

Item{
    id: root


    //Propriétés liés à la position et à la taille de l'objet
    property int defaultWidth: 100          //dimensions du bouton quand la fenêtre fait du 640x480
    property int defaultHeight: 40
    property int defaultX: 0                //position du bouton pour les dimensions quand la fenêtre fait du 640x480
    property int defaultY: 0

    //Propriétés liés aux valeurs limites
    property int minimumValue: 0
    property int maximumValue: 1

    //Propriétés liés à l'état du DMI_valueinput
    property bool isMaxDefault: false       //définit si la valeur par défaut (dans le placeholder) est la valeur max (ou mini si mis sur false)
    property int fontSize: 12
    property bool isDarkGrey: !isActivable  //est ce que le texte doit-être en gris foncé ?
    readonly property int value: body.text != "" ? parseInt(body.text) : (isMaxDefault ? root.maximumValue : root.minimumValue)


    //Propriétés liés à l'état du bouton
    property bool isActivable: true         //si le bouton peut être activée
    property bool isPositive: false         //si le bouton doit-être visible en couche positive (sinon négatif)
    property bool isVisible: true           //si le bouton est visible


    //Différents signal handlers (à écrire en python)
    signal value_changed()

    //Fonction pour remettre la valeur par défaut dans le valueinput
    function clear(){
        // Vérifie si la valeur actuellement visible est différente que la valeur quand vidé, change la valeur et appelle le signal value_changed si c'est le cas
        var changed = root.isMaxDefault ? root.value !== root.maximumValue : root.value !== root.minimumValue
        body.text = ""
        if(changed){
            value_changed()
        }
    }

    function change_value(new_value){
        //Si la valeur n'est pas valide (trop grand ou trop petite) la change
        if(new_value < root.minimumValue){
            new_value = root.minimumValue
        }
        else if(new_value > root.maximumValue){
            new_value = root.maximumValue
        }

        // Vérifie si la nouvelle valeur change de l'ancienne
        var changed = (root.value !== new_value)
        body.text = new_value.toString()
        if(changed){
            value_changed()
            root.old_value = new_value
        }
    }

    //Couleurs (ne peuvent pas être modifiés mais permet une mise à jour facile si nécessaire)
    readonly property string darkBlue: "#031122"   //partie 5.2.1.3.3  Nr 6
    readonly property string black: "#000000"       //partie 5.2.1.3.3  Nr 2
    readonly property string grey: "#C3C3C3"        //partie 5.2.1.3.3  Nr 3
    readonly property string darkGrey: "#969696"    //partie 5.2.1.3.3  Nr 5
    readonly property string shadow: "#08182F"      //partie 5.2.1.3.3  Nr 7


    //permet à partir des valeurs de positions et dimensions par défauts de calculer
    readonly property real ratio:  (parent.width >= 640 && parent.height >= 480) ? parent.width/640 * (parent.width/640 < parent.height/480) + parent.height/480 * (parent.width/640 >= parent.height/480) : 1  //parent.height et parent.width représentent la taille de la fenêtre
    width: (root.defaultWidth - 2) * root.ratio
    height: (root.defaultHeight - 2) * root.ratio
    x: (root.defaultX + 1) * root.ratio
    y: (root.defaultY + 1) * root.ratio
    visible: root.isVisible


    TextField {
        id: body

        echoMode: TextInput.Normal

        // Propriété gardant le précédent nombre rentré afin de savoir s'il est nécessaire d'appeler le signal value_changed()
        property int old_value: root.isMaxDefault ? root.maximumValue : root.minimumValue

        color: root.isDarkGrey ? root.darkGrey : (body.text != "" ? root.grey : root.darkGrey)
        placeholderText: root.isMaxDefault ? root.maximumValue.toString() : root.minimumValue.toString()
        placeholderTextColor: root.darkGrey
        font.pixelSize: root.fontSize * root.ratio

        anchors.fill: parent
        readOnly: !root.isActivable

        background: Rectangle {
            anchors.fill: parent
            color: root.darkBlue
        }

        validator: IntValidator {
            bottom: root.minimumValue
            top: root.maximumValue
        }

        onFocusChanged: {
            if(body.text != "" && !body.focus){
                if(parseInt(body.text) > root.maximumValue) {
                    body.text = root.maximumValue.toString()
                }
                else if (parseInt(body.text) < root.minimumValue) {
                    body.text = root.minimumValue.toString()
                }

                if(parseInt(body.text) != old_value){
                    value_changed()
                }
            }
            else if(!body.focus && ((root.isMaxDefault && body.old_value != root.maximumValue) || (!root.isMaxDefault && body.old_value != root.minimumValue))) {
                body.old_value = root.isMaxDefault ? root.maximumValue : root.minimumValue
                value_changed()
            }
        }
    }

    onMinimumValueChanged: {
        if(body.text != "" && parseInt(body.text) < root.minimumValue){
            body.text = root.minimumValue.toString()
            value_changed()
            body.old_value = root.minimumValue
        }
    }

    onMaximumValueChanged: {
        if(body.text != "" && parseInt(body.text) > root.maximumValue){
            body.text = root.maximumValue.toString()
            value_changed()
            body.old_value = root.maximumValue
        }
    }


    //Ombre extérieure
    //Rectangle pour l'ombre extérieure inférieure
    Rectangle {
        id: outbottomshadow
        color: root.shadow
        width: root.width + 2 * root.ratio
        height: 2 * root.ratio
        anchors.horizontalCenter: body.horizontalCenter
        anchors.verticalCenter: body.bottom
    }

    //Rectangle pour l'ombre extérieure droite
    Rectangle {
        id: outrightshadow
        color: root.shadow
        width: 2 * root.ratio
        height: root.height + 2 * root.ratio
        anchors.right: outbottomshadow.right
        anchors.bottom: outbottomshadow.bottom
    }

    //Rectangle pour l'ombre extérieure supérieure
    Rectangle {
        id: outtopshadow
        color: root.black
        height: 2 * root.ratio
        anchors.top: outrightshadow.top
        anchors.right: outrightshadow.left
        anchors.left: outbottomshadow.left
    }

    //Rectangle pour l'ombre extérieure gauche
    Rectangle {
        id: outleftshadow
        color: root.black
        width: 2 * root.ratio
        anchors.top: outtopshadow.top
        anchors.left: outtopshadow.left
        anchors.bottom: outbottomshadow.top
    }


    //Ombre intérieure
    //Rectangle pour l'ombre intérieure inférieure
    Rectangle {
        id: inbottomshadow
        color: isPositive ? root.black : "transparent"
        height: 2 * root.ratio
        anchors.bottom: outbottomshadow.top
        anchors.left: outleftshadow.right
        anchors.right: outrightshadow.left
    }

    //Rectangle pour l'ombre intérieure droite
    Rectangle {
        id: inrightshadow
        color: isPositive ? root.black : "transparent"
        width: 2 * root.ratio
        anchors.right: outrightshadow.left
        anchors.bottom: outbottomshadow.top
        anchors.top: outtopshadow.bottom
    }

    //Rectangle pour l'ombre intérieure supérieure
    Rectangle {
        id: intopshadow
        color: isPositive ? root.shadow : "transparent"
        height: 2 * root.ratio
        anchors.top: outtopshadow.bottom
        anchors.left: outleftshadow.right
        anchors.right: inrightshadow.left
    }

    //Rectangle pour l'ombre intérieure gauche
    Rectangle {
        id: inleftshadow
        color: isPositive ? root.shadow : "transparent"
        width: 2 * root.ratio
        anchors.left: outleftshadow.right
        anchors.top: outtopshadow.bottom
        anchors.bottom: inbottomshadow.top
    }
}





