import QtQuick 2.15
import QtQuick.Controls 2.15


//https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
//Comment créer un élément personalisé

//https://doc.qt.io/qt-5/qtquickcontrols2-customize.html#customizing-button
//Comment personaliser un bouton


Item {
    id: root


    //Propriétés liés à la position et à la taille de l'objet
    property int defaultWidth: 100          //dimensions du bouton quand la fenêtre fait du 640x480
    property int defaultHeight: 40
    property int defaultX: 0                //position du bouton pour les dimensions quand la fenêtre fait du 640x480
    property int defaultY: 0

    //Propriétés liés à l'image et au texte que l'utilisateur peut rajouter sur le bouton
    property string image: ""               //image à afficher
    property string text: ""                //texte à afficher
    property int fontSize: 12
    property bool isDarkGrey: !isActivable    //est ce que le texte doit-être en gris foncé ?

    //Propriétés liés à l'état du bouton
    property bool isActivable: true         //si le bouton peut être activée
    property bool isPositive: false         //si le bouton doit-être visible en couche positive (sinon négatif)
    property bool isVisible: true           //si le bouton est visible


    //Différents signal handlers (à écrire en python)
    signal clicked()                //détecte quand le bouton est cliqué
    signal click_start()            //détecte quand l'utilisateur commence à appuyer sur le bouton
    signal click_end()              //détecte quand l'utilisateur relache le bouton (similaire à .clicked())

    //Couleurs (ne peuvent pas être modifiés mais permet une mise à jour facile si nécessaire)
    readonly property string darkBlue : "#031122"   //partie 5.2.1.3.3  Nr 6
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



    //Rectangle pour la couleur du fond du bouton
    Rectangle{
        id: body
        color: root.darkBlue
        anchors.fill: parent
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
    }

    //Image visible sur le bouton
    Image {
        id: image
        source: root.source
        anchors.fill: parent
        anchors.bottom: body.bottom
        anchors.right: body.right
        anchors.top: body.top
        anchors.left: body.left
    }

    //Texte visible sur le bouton
    Text{
        id: button_text
        text: root.text
        font.pixelSize: root.fontSize * ratio
        font.family: "Verdana"
        color: root.isDarkGrey ? root.darkGrey : root.grey
        anchors.horizontalCenter: body.horizontalCenter
        anchors.verticalCenter: body.verticalCenter
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

        onPressed: {                //Détecte quand la zone (le bouton) commence à être appuyée
            if(isActivable){
                root.click_start()
            }
        }

        onReleased: {               //Détecte quand la zone (le bouton) est relachée
            if(isActivable){
                root.click_end()
                root.clicked()
            }
        }
    }
}