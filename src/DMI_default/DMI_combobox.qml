import QtQuick 2.0
import QtQuick.Controls 2.15


//https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
//Comment créer un élément personalisé

//https://doc.qt.io/qt-5/qtquickcontrols2-customize.html#customizing-combobox
//Comment personaliser un combobox

Item {
    id:root

    //Arguments supplémentaires (en plus de la position et de la taille)
    property int defaultWidth: 200   //dimensions de la combobox quand celle-ci est fermée et que la fenêtre fait du 640x480
    property int defaultHeight: 60
    property int defaultX: 0        //position du bouton pour les dimensions quand la fenêtre fait du 640x480
    property int defaultY: 0
    property int fontSize: 12
    property bool darkGrey: !isActivable //est ce que le texte doit-être en gris foncé ?
    property var elements: ["NaN"]
    property int amountElementsDisplayed: 4 //définit le nombre d'éléments visibles dans la popup
    property string selection: combo.displayText
    property bool isActivable: true //si la combobox peut être activée (Elle le sera que si isActivable est à true et qu'il y a plus d'un élément dans la combobox)
    property bool isPositive: false
    property bool isVisible: true   //si le bouton est visible
    visible: isVisible

    //Différents signal handlers (à écrire en python)
    signal combobox_opened()                        //détecte quand le popup de la combobox s'ouvre
    signal combobox_closed()                        //détecte quand le popup de la combobox se ferme
    signal selection_changed()                      //détecte quand l'utilisateur changed la sélection de la combobox (selection_changed() appelé avant combobox_closed())

    //permet à partir des valeurs de positions et dimensions par défauts de calculer le ratio à appliquer aux dimensions
    readonly property real ratio:  parent.width/640 * (parent.width/640 < parent.height/480) + parent.height/480 * (parent.width/640 >= parent.height/480)  //parent.height et parent.width représentent la taille de la fenêtre
    width: (root.defaultWidth - 2) * root.ratio
    height: (root.defaultHeight - 2) * root.ratio
    x: (root.defaultX + 1) * root.ratio
    y: (root.defaultY + 1) * root.ratio

    //Inline component : combobox (crée une templace de la combobox)
    component DMI_combo: ComboBox {
        id: body
        font.pixelSize: root.fontSize * root.ratio
        flat: true
        font.family: "Verdana"

        anchors.fill: parent

        //Flèche visible lorsque la combobox est fermée
        indicator: Canvas {
            id: canvas
            height: 8 * root.ratio
            width: 12 * root.ratio
            x: root.width - width - body.rightPadding
            y: body.topPadding + (body.availableHeight - height) / 2

            //Permet d'ouvrir le popup quand la combobox est sélectionné et appelle le signal handler
            Connections {
                target: body
                function onPressedChanged() {
                    if(root.isActivable && body.count > 1 && !body.pressed && !popup.visible)
                    {
                        root.combobox_opened();
                    }
                }
            }

            //Gère la couleur et le placement de la flèche
            onPaint: {
                var ctx = getContext("2d");
                ctx.reset();
                ctx.moveTo(0, 0);
                ctx.lineTo(width, 0);
                ctx.lineTo(width / 2, height);
                ctx.closePath();
                ctx.fillStyle = !body.pressed && root.isActivable && body.count > 1 ? "#c3c3c3" : "#969696";
                ctx.fill();
            }
        }

        //Texte visible quand la combobox est fermée
        contentItem: Text {
            text: body.displayText
            font: body.font
            color: !body.pressed && root.isActivable && body.count > 1 ? "#c3c3c3" : "#969696"
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter

            anchors.fill: parent

            //Détecte quand la valeur du combobox est changé
            onTextChanged: {
                root.selection_changed();
            }
        }

        //Rectangle visible lorsque la combobox est fermée (ici peut utile car même couleur que le fond)
        background: Rectangle {
            id: text_zone
            color: "#031122"
            anchors.fill: parent
        }

        //Menu de popup quand la combobox est ouverte
        popup: Popup {
            id: popup
            y: (root.defaultHeight - 1) * root.ratio
            width: root.width * root.ratio
            implicitHeight: body.count < root.amountElementsDisplayed ? body.height*body.count : body.height * root.amountElementsDisplayed
            padding: 1 * ratio

            //Détecte quand celui-ci est fermé (peu importe la façon)
            onClosed: {
                root.combobox_closed();
            }

            //Permet de lister les différents éléments, ajoute aussi une scrollbar s'il y a plus de 4 éléments
            contentItem: ListView {
                clip: true
                implicitHeight: contentHeight
                model: body.popup.visible && isActivable && body.count > 1 ? body.delegateModel : null               //FIXME: enlever la couleur de fond quand élément sélectionné
                currentIndex: body.highlightedIndex

                ScrollIndicator.vertical: ScrollIndicator { }
            }

            //Rectangle de fond
            background: Rectangle {
                color: "transparent"
            }
        }
    }


    //Crée une instance de la combobox
    DMI_combo {
        id:combo
        model: root.elements
        anchors.fill: parent

        delegate: ItemDelegate {
            width: combo.width
            height: combo.height

            Rectangle{
                color: "#032211"
            }

            contentItem: Text {
                text: modelData
                color: combo.highlightedIndex === index ? "#969696" : "#c3c3c3"
                font: combo.font
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
            }
        }
    }

    //Rectangle pour l'ombre extérieure inférieure
        Rectangle {
            id: outbottomshadow
            color: "#08182f"
            width: root.width + 2 * root.ratio
            height: 2 * root.ratio
            anchors.horizontalCenter: combo.horizontalCenter
            anchors.bottom: outrightshadow.bottom
        }

        //Rectangle pour l'ombre extérieure droite
        Rectangle {
            id: outrightshadow
            color: "#08182f"
            width: 2 * root.ratio
            height: outleftshadow.height
            anchors.horizontalCenter: combo.right
            //anchors.verticalCenter: combo.verticalCenter
        }

        //Rectangle pour l'ombre extérieure supérieure
        Rectangle {
            id: outtopshadow
            color: "#000000"
            width: root.width
            height: 2 * root.ratio
            anchors.left: outbottomshadow.left
            anchors.verticalCenter: combo.top
        }

        //Rectangle pour l'ombre extérieure gauche
        Rectangle {
            id: outleftshadow
            color: "#000000"
            width: 2 * root.ratio
            height: combo.popup.visible && isActivable && combo.count > 1 ? combo.height*((combo.count < root.amountElementsDisplayed ? combo.count : root.amountElementsDisplayed) + 1) : combo.height
            anchors.horizontalCenter: combo.left
            //anchors.bottom: outbottomshadow.top
            anchors.top: outtopshadow.top
        }

        //Rectangle pour l'ombre extérieure inférieure
        Rectangle {
            id: inbottomshadow
            color: root.isPositive ? "#000000" : "transparent"
            height: 2 * root.ratio
            anchors.bottom: outbottomshadow.top
            anchors.left: outleftshadow.right
            anchors.right: outrightshadow.left
        }

        //Rectangle pour l'ombre extérieure droite
        Rectangle {
            id: inrightshadow
            color: root.isPositive ? "#000000" : "transparent"
            width: 2 * root.ratio
            anchors.right: outrightshadow.left
            anchors.bottom: outbottomshadow.top
            anchors.top: outtopshadow.bottom
        }

        //Rectangle pour l'ombre extérieure supérieure
        Rectangle {
            id: intopshadow
            color: root.isPositive ? "#08182f" : "transparent"
            height: 2 * root.ratio
            anchors.top: outtopshadow.bottom
            anchors.left: outleftshadow.right
            anchors.right: inrightshadow.left
        }

        //Rectangle pour l'ombre extérieure gauche
        Rectangle {
            id: inleftshadow
            color: root.isPositive ? "#08182f" : "transparent"
            width: 2 * root.ratio
            anchors.left: outleftshadow.right
            anchors.top: outtopshadow.bottom
            anchors.bottom: inbottomshadow.top
        }
}