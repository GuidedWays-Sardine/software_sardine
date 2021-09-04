import QtQuick 2.0
import QtQuick.Controls 2.15


//https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
//Comment créer un élément personalisé

//https://doc.qt.io/qt-5/qtquickcontrols2-customize.html#customizing-combobox
//Comment personaliser un combobox


Item {
    id:root


    //Propriétés liés à la position et à la taille de l'objet
    property int defaultWidth: 100          //dimensions de la combobox quand celle-ci est fermée et que la fenêtre fait du 640x480
    property int defaultHeight: 40
    property int defaultX: 0                //position du bouton pour les dimensions quand la fenêtre fait du 640x480
    property int defaultY: 0

    //Propriétés liés aux donnés de la combobox
    property var elements: ["NaN"]          //définit les éléments sélectionables de la combobox
    property int amountElementsDisplayed: 4 //définit le nombre d'éléments visibles dans la popup
    property string selection: combo.displayText
    property int fontSize: 12
    property bool isDarkGrey: !isActivable  //est ce que le texte doit-être en gris foncé ?

    //Propriétés liés à l'état de la combobox
    property bool isActivable: true        //si la combobox peut être activée (Elle le sera que si isActivable est à true et qu'il y a plus d'un élément dans la combobox)
    property bool isPositive: false        //si la combobox doit-être visible en couche positive (sinon négative)
    property bool isVisible: true          //si le bouton est visible


    //Différents signal handlers (à écrire en python)
    signal combobox_opened()                        //détecte quand le popup de la combobox s'ouvre
    signal combobox_closed()                        //détecte quand le popup de la combobox se ferme
    signal selection_changed()                      //détecte quand l'utilisateur changed la sélection de la combobox (selection_changed() appelé après combobox_closed())

    //Fonction pour changer l'index de la combobox en fonction du texte
    function change_selection(new_selection){
        //récupère la sélection actuelle
        var old_selection = root.selection

        // Si la nouvelle sélection est un int, change le currentIndex en fonction de l'index envoyé
        if(typeof new_selection === typeof root.fontSize){
            if(new_selection <= combo.count){
                combo.currentIndex = new_selection - 1
            }
        }
        // Si la nouvelle sélection est un string, cherche l'élément avec le même index
        else if(typeof new_selection === typeof root.selection){
            for(var i = 0; i < combo.count; i++){
                if(root.elements[i].toUpperCase() === new_selection.toUpperCase()){
                    combo.currentIndex =  i
                }
            }
        }

        //Si la sélection a été changée, appelle le signal
        if(root.selection != old_selection){
            selection_changed()
        }
    }

    //Couleurs (ne peuvent pas être modifiés mais permet une mise à jour facile si nécessaire)
    readonly property string darkBlue : "#031122"   //partie 5.2.1.3.3  Nr 6
    readonly property string black: "#000000"       //partie 5.2.1.3.3  Nr 2
    readonly property string grey: "#C3C3C3"        //partie 5.2.1.3.3  Nr 3
    readonly property string darkGrey: "#969696"    //partie 5.2.1.3.3  Nr 5
    readonly property string shadow: "#08182F"      //partie 5.2.1.3.3  Nr 7


    //permet à partir des valeurs de positions et dimensions par défauts de calculer le ratio à appliquer aux dimensions
    readonly property real ratio:  (parent.width >= 640 && parent.height >= 480) ? parent.width/640 * (parent.width/640 < parent.height/480) + parent.height/480 * (parent.width/640 >= parent.height/480) : 1  //parent.height et parent.width représentent la taille de la fenêtre
    width: (root.defaultWidth - 2) * root.ratio
    height: (root.defaultHeight - 2) * root.ratio
    x: (root.defaultX + 1) * root.ratio
    y: (root.defaultY + 1) * root.ratio
    visible: isVisible



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
                    canvas.requestPaint()
                    if(root.isActivable && body.count > 1 && !body.pressed && !popup.visible)
                    {
                        root.combobox_opened()
                    }
                }
            }

            //Gère la couleur et le placement de la flèche
            onPaint: {
                var ctx = getContext("2d")
                ctx.reset()
                ctx.moveTo(0, 0)
                ctx.lineTo(width, 0)
                ctx.lineTo(width / 2, height)
                ctx.closePath()
                ctx.fillStyle = !body.pressed && !root.isDarkGrey && body.count > 1 ? root.grey : root.darkGrey
                ctx.fill()
            }
        }

        //Texte visible quand la combobox est fermée
        contentItem: Text {
            text: body.displayText
            font: body.font
            color: !body.pressed && !root.isDarkGrey && body.count > 1 ? root.grey : root.darkGrey
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter

            anchors.fill: parent

            //Détecte quand la valeur du combobox est changé
            onTextChanged: {
                root.selection_changed()
            }
        }

        //Rectangle visible lorsque la combobox est fermée
        background: Rectangle {
            id: text_zone
            color: root.darkBlue
            anchors.fill: parent
        }

        //Menu de popup quand la combobox est ouverte
        popup: Popup {
            id: popup
            y: (root.defaultHeight - 2) * root.ratio
            x: (root.isPositive ? 4 : 2) * root.ratio
            width: root.width - (isPositive ? 6 : 2) * root.ratio
            implicitHeight: ((body.count < root.amountElementsDisplayed ? body.height*body.count : body.height * root.amountElementsDisplayed) + (root.isPositive ? 6 : 8) * root.ratio) * (root.isActivable && body.count > 1)
            padding: 1 * root.ratio

            //Détecte quand celui-ci est fermé (peu importe la façon)
            onClosed: {
                if(root.isActivable && body.count > 1 && !body.pressed && !popup.visible)
                {
                    root.combobox_closed()
                }
            }

            //Permet de lister les différents éléments, ajoute aussi une scrollbar s'il y a plus de 4 éléments
            contentItem: ListView {
                clip: true
                implicitHeight: contentHeight
                model: body.popup.visible && isActivable && body.count > 1 ? body.delegateModel : null
                currentIndex: body.highlightedIndex

                ScrollIndicator.vertical: ScrollIndicator { }
            }

            //Rectangle de fond
            background: Rectangle {
                color: root.darkBlue
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

            background: Rectangle {
                color: "transparent"
            }

            contentItem: Text {
                text: modelData
                color: combo.highlightedIndex === index ? root.darkGrey : root.grey
                font: combo.font
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
            }
        }
    }


    //Ombre extérieure
    //Rectangle pour l'ombre extérieure supérieure
    Rectangle {
        id: outtopshadow
        color: root.black
        width: root.width
        height: 2 * root.ratio
        anchors.verticalCenter: body.top
        anchors.left: body.left
        anchors.leftMargin: - 1 * root.ratio
    }

    //Rectangle pour l'ombre extérieure droite
    Rectangle {
        id: outrightshadow
        color: root.shadow
        width: 2 * root.ratio
        height: combo.popup.visible && isActivable && combo.count > 1 ? combo.height*((combo.count < root.amountElementsDisplayed ? combo.count : root.amountElementsDisplayed) + 1) + 10 * root.ratio : combo.height
        anchors.top: outtopshadow.top
        anchors.left: outtopshadow.right
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

    //Rectangle pour l'ombre extérieure inférieure
    Rectangle {
        id: outbottomshadow
        color: root.shadow
        height: 2 * root.ratio
        anchors.right: outrightshadow.right
        anchors.bottom: outrightshadow.bottom
        anchors.left: outtopshadow.left
    }

    //Ombre intérieure
    //Rectangle pour l'ombre extérieure inférieure
    Rectangle {
        id: inbottomshadow
        color: root.isPositive ? root.black : "transparent"
        height: 2 * root.ratio
        anchors.bottom: outbottomshadow.top
        anchors.left: outleftshadow.right
        anchors.right: outrightshadow.left
    }

    //Rectangle pour l'ombre extérieure droite
    Rectangle {
        id: inrightshadow
        color: root.isPositive ? root.black : "transparent"
        width: 2 * root.ratio
        anchors.right: outrightshadow.left
        anchors.bottom: outbottomshadow.top
        anchors.top: outtopshadow.bottom
    }

    //Rectangle pour l'ombre extérieure supérieure
    Rectangle {
        id: intopshadow
        color: root.isPositive ? root.shadow : "transparent"
        height: 2 * root.ratio
        anchors.top: outtopshadow.bottom
        anchors.left: outleftshadow.right
        anchors.right: inrightshadow.left
    }

    //Rectangle pour l'ombre extérieure gauche
    Rectangle {
        id: inleftshadow
        color: root.isPositive ? root.shadow : "transparent"
        width: 2 * root.ratio
        anchors.left: outleftshadow.right
        anchors.top: outtopshadow.bottom
        anchors.bottom: inbottomshadow.top
    }
}