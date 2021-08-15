import QtQuick 2.15
import QtQuick.Controls 2.15


//https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
//Comment créer un élément personalisé

//https://doc.qt.io/qt-5/qtquickcontrols2-customize.html#customizing-button
//Comment personaliser un bouton
//Ici le DMI_checkbutton utilise une structure similaire au DMI_button. on déplace juste le texte en dehors du bouton, et l'image d'une croix apparait quand le checkbutton est activé


Item {
    id: root


    //Propriétés liés à la position et à la taille de l'objet
    property int boxLenght: 20           //dimensions de la partie cochable du checkbutton quand la fenêtre fait du 640x480
    property int defaultX: 0             //position du bouton pour les dimensions quand la fenêtre fait du 640x480
    property int defaultY: 0

    //Propriétés liés à l'image et au texte que l'utilisateur peut rajouter sur le bouton
    property string text: ""            //texte à afficher
    property int fontSize: 12
    property bool isDarkGrey: !isActive   //est ce que le texte doit-être en gris foncé ?

    //Propriétés liés à l'état de la combobox
    property bool isChecked: false
    property bool isActivated: false  //si le bouton est activé
    property bool isActivable: true   //si le bouton peut être activée
    property bool isPositive: false   //si le bouton doit-être visible en couche positive (sinon négatif)
    property bool isVisible: true     //si le bouton est visible


    //Fonction pour changer la valeur de isChecked
    function set_checked(status) {
            root.isChecked = status;
    }

    //Différents signal handlers (à écrire en python)
    signal clicked()                //détecte quand le bouton est cliqué (après que l'état ait été changé)

    //Couleurs (ne peuvent pas être modifiés mais permet une mise à jour facile si nécessaire)
    readonly property string darkBlue : "#031122"   //partie 5.2.1.3.3  Nr 6
    readonly property string black: "#000000"       //partie 5.2.1.3.3  Nr 2
    readonly property string grey: "#C3C3C3"        //partie 5.2.1.3.3  Nr 3
    readonly property string darkGrey: "#969696"    //partie 5.2.1.3.3  Nr 5
    readonly property string shadow: "#08182F"      //partie 5.2.1.3.3  Nr 7


    //permet à partir des valeurs de positions et dimensions par défauts de calculer
    readonly property real ratio:  (parent.width >= 640 && parent.height >= 480) ? parent.width/640 * (parent.width/640 < parent.height/480) + parent.height/480 * (parent.width/640 >= parent.height/480) : 1  //parent.height et parent.width représentent la taille de la fenêtre
    width: (root.boxLenght - 2) * root.ratio
    height: (root.boxLenght - 2) * root.ratio
    x: (root.defaultX + 1) * root.ratio
    y: (root.defaultY + 1) * root.ratio
    visible : root.isVisible



    //Rectangle pour la couleur du fond du bouton (pas nécessaire ici sachant que la couleur du bouton est la même que la couleur de fond de l'application)
    Rectangle{
        id: body
        color: root.darkBlue
        anchors.fill: parent
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
    }

    //Texte visible à côté de la boite
    Text{
        id: button_text
        text: root.text
        font.pixelSize: root.fontSize * ratio
        font.family: "Verdana"
        color: root.isDarkGrey ? root.darkGrey : root.grey
        anchors.horizontalCenter: body.horizontalCenter
        anchors.left: body.right
        anchors.leftMargin: root.fontSize * ratio
    }

    //Image visible sur le bouton
    Image {
        id: image
        source: isChecked ? (isDarkGrey ? "../../assets/DMI_icons/dark_grey_cross.png" : "../../assets/DMI_icons/white_cross.png") : ""
        anchors.fill: parent
        anchors.bottom: body.bottom
        anchors.right: body.right
        anchors.top: body.top
        anchors.left: body.left
    }

    //Ombre extérieure
    //Rectangle pour l'ombre extérieure inférieure
    Rectangle {
        id: outbottomshadow
        color: !isActivable || !area.pressed ? root.shadow : "transparent"
        width: root.width + 2 * root.ratio
        height: 2 * root.ratio
        anchors.horizontalCenter: body.horizontalCenter
        anchors.verticalCenter: body.bottom
    }

    //Rectangle pour l'ombre extérieure droite
    Rectangle {
        id: outrightshadow
        color: !isActivable || !area.pressed ? root.shadow : "transparent"
        width: 2 * root.ratio
        height: root.height + 2 * root.ratio
        anchors.right: outbottomshadow.right
        anchors.bottom: outbottomshadow.bottom
    }

    //Rectangle pour l'ombre extérieure supérieure
    Rectangle {
        id: outtopshadow
        color: !isActivable || !area.pressed ? root.black : "transparent"
        height: 2 * root.ratio
        anchors.top: outrightshadow.top
        anchors.right: outrightshadow.left
        anchors.left: outbottomshadow.left
    }

    //Rectangle pour l'ombre extérieure gauche
    Rectangle {
        id: outleftshadow
        color: !isActivable || !area.pressed ? root.black : "transparent"
        width: 2 * root.ratio
        anchors.top: outtopshadow.top
        anchors.left: outtopshadow.left
        anchors.bottom: outbottomshadow.top
    }


    //Ombre intérieure
    //Rectangle pour l'ombre intérieure inférieure
    Rectangle {
        id: inbottomshadow
        color: isPositive && !(area.pressed && isActivable) ? root.black : "transparent"
        height: 2 * root.ratio
        anchors.bottom: outbottomshadow.top
        anchors.left: outleftshadow.right
        anchors.right: outrightshadow.left
    }

    //Rectangle pour l'ombre intérieure droite
    Rectangle {
        id: inrightshadow
        color: isPositive && !(area.pressed && isActivable) ? root.black : "transparent"
        width: 2 * root.ratio
        anchors.right: outrightshadow.left
        anchors.bottom: outbottomshadow.top
        anchors.top: outtopshadow.bottom
    }

    //Rectangle pour l'ombre intérieure supérieure
    Rectangle {
        id: intopshadow
        color: isPositive && !(area.pressed && isActivable) ? root.shadow : "transparent"
        height: 2 * root.ratio
        anchors.top: outtopshadow.bottom
        anchors.left: outleftshadow.right
        anchors.right: inrightshadow.left
    }

    //Rectangle pour l'ombre intérieure gauche
    Rectangle {
        id: inleftshadow
        color: isPositive && !(area.pressed && isActivable) ? root.shadow : "transparent"
        width: 2 * root.ratio
        anchors.left: outleftshadow.right
        anchors.top: outtopshadow.bottom
        anchors.bottom: inbottomshadow.top
    }

    //Zone de détection de souris (utile pour détecter les cliques)
    MouseArea{
        id: area
        anchors.fill: parent
        hoverEnabled: false

        onReleased: {
            if(isActivable){
                root.isActivated = !root.isActivated
                root.clicked()
            }
        }
    }
}
