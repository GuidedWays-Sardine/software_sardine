import QtQuick 2.0
import QtQuick.Controls 2.15


//https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
//Comment créer un élément personalisé

//https://doc.qt.io/qt-5/qtquickcontrols2-customize.html#customizing-combobox
//Comment personaliser un combobox


Item {
    id:root


    //Propriétés liés à la position et à la taille de l'objet
    property int default_width: 100          //dimensions de la combobox quand celle-ci est fermée et que la fenêtre fait du 640x480
    property int default_height: 40
    property int default_x: 0                //position du bouton pour les dimensions quand la fenêtre fait du 640x480
    property int default_y: 0

    //Propriétés liés aux donnés de la combobox
    property var elements: ["NaN"]          //définit les éléments sélectionables de la combobox
    readonly property int elementsCount: combo.count
    property int amountElementsDisplayed: 4 //définit le nombre d'éléments visibles dans la popup
    readonly property string selection: combo.displayText
    readonly property int selectionIndex: combo.currentIndex + 1
    property int font_size: 12
    property bool is_dark_grey: !is_activable  //est ce que le texte doit-être en gris foncé ?

    //Propriétés liés à l'état de la combobox
    property bool is_activable: true        //si la combobox peut être activée (Elle le sera que si is_activable est à true et qu'il y a plus d'un élément dans la combobox)
    property bool is_positive: false        //si la combobox doit-être visible en couche positive (sinon négative)
    property bool is_visible: true          //si le bouton est visible


    //Différents signal handlers (à écrire en python)
    signal combobox_opened()                        //détecte quand le popup de la combobox s'ouvre
    signal combobox_closed()                        //détecte quand le popup de la combobox se ferme
    signal selection_changed()                      //détecte quand l'utilisateur changed la sélection de la combobox (selection_changed() appelé après combobox_closed())

    //Fonction pour changer l'index de la combobox en fonction du texte
    function change_selection(new_selection){
        // Si la nouvelle sélection est un int, change le currentIndex en fonction de l'index envoyé
        if(typeof new_selection === typeof root.font_size){
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
    }

    //Couleurs (ne peuvent pas être modifiés mais permet une mise à jour facile si nécessaire)
    readonly property string dark_blue : "#031122"   //partie 5.2.1.3.3  Nr 6
    readonly property string black: "#000000"       //partie 5.2.1.3.3  Nr 2
    readonly property string grey: "#C3C3C3"        //partie 5.2.1.3.3  Nr 3
    readonly property string dark_grey: "#969696"    //partie 5.2.1.3.3  Nr 5
    readonly property string shadow: "#08182F"      //partie 5.2.1.3.3  Nr 7


    //permet à partir des valeurs de positions et dimensions par défauts de calculer le ratio à appliquer aux dimensions
    readonly property real ratio:  (parent.width >= 640 && parent.height >= 480) ? parent.width/640 * (parent.width/640 < parent.height/480) + parent.height/480 * (parent.width/640 >= parent.height/480) : 1  //parent.height et parent.width représentent la taille de la fenêtre
    width: (root.default_width - 2) * root.ratio
    height: (root.default_height - 2) * root.ratio
    x: (root.default_x + 1) * root.ratio
    y: (root.default_y + 1) * root.ratio
    visible: is_visible



    //Inline component : combobox (crée une templace de la combobox)
    component DMI_combo: ComboBox {
        id: body
        font.pixelSize: root.font_size * root.ratio
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
                    forceActiveFocus()
                    canvas.requestPaint()
                    if(root.is_activable && body.count > 1 && !body.pressed && !popup.visible)
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
                ctx.fillStyle = !body.pressed && !root.is_dark_grey && body.count > 1 ? root.grey : root.dark_grey
                ctx.fill()
            }
        }

        //Texte visible quand la combobox est fermée
        contentItem: Text {
            text: body.displayText
            font: body.font
            color: !body.pressed && !root.is_dark_grey && body.count > 1 ? root.grey : root.dark_grey
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
            color: root.dark_blue
            anchors.fill: parent
        }

        //Menu de popup quand la combobox est ouverte
        popup: Popup {
            id: popup
            y: (root.default_height - 2) * root.ratio
            x: (root.is_positive ? 4 : 2) * root.ratio
            width: root.width - (is_positive ? 6 : 2) * root.ratio
            implicitHeight: ((body.count < root.amountElementsDisplayed ? body.height*body.count : body.height * root.amountElementsDisplayed) + (root.is_positive ? 6 : 8) * root.ratio) * (root.is_activable && body.count > 1)
            padding: 1 * root.ratio

            //Détecte quand celui-ci est fermé (peu importe la façon)
            onClosed: {
                if(root.is_activable && body.count > 1 && !body.pressed && !popup.visible)
                {
                    root.combobox_closed()
                }
            }

            //Permet de lister les différents éléments, ajoute aussi une scrollbar s'il y a plus de 4 éléments
            contentItem: ListView {
                clip: true
                implicitHeight: contentHeight
                model: body.popup.visible && is_activable && body.count > 1 ? body.delegateModel : null
                currentIndex: body.highlightedIndex

                ScrollIndicator.vertical: ScrollIndicator { }
            }

            //Rectangle de fond
            background: Rectangle {
                color: root.dark_blue
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
                color: combo.highlightedIndex === index ? root.dark_grey : root.grey
                font: combo.font
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
            }
        }
    }


    //Ombre extérieure
    //Rectangle pour l'ombre extérieure supérieure
    Rectangle {
        id: out_top_shadow
        color: root.black
        width: root.width
        height: 2 * root.ratio
        anchors.verticalCenter: body.top
        anchors.left: body.left
        anchors.leftMargin: - 1 * root.ratio
    }

    //Rectangle pour l'ombre extérieure droite
    Rectangle {
        id: out_right_shadow
        color: root.shadow
        width: 2 * root.ratio
        height: combo.popup.visible && is_activable && combo.count > 1 ? combo.height*((combo.count < root.amountElementsDisplayed ? combo.count : root.amountElementsDisplayed) + 1) + 10 * root.ratio : combo.height
        anchors.top: out_top_shadow.top
        anchors.left: out_top_shadow.right
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

    //Rectangle pour l'ombre extérieure inférieure
    Rectangle {
        id: out_bottom_shadow
        color: root.shadow
        height: 2 * root.ratio
        anchors.right: out_right_shadow.right
        anchors.bottom: out_right_shadow.bottom
        anchors.left: out_top_shadow.left
    }

    //Ombre intérieure
    //Rectangle pour l'ombre extérieure inférieure
    Rectangle {
        id: in_bottom_shadow
        color: root.is_positive ? root.black : "transparent"
        height: 2 * root.ratio
        anchors.bottom: out_bottom_shadow.top
        anchors.left: out_left_shadow.right
        anchors.right: out_right_shadow.left
    }

    //Rectangle pour l'ombre extérieure droite
    Rectangle {
        id: in_right_shadow
        color: root.is_positive ? root.black : "transparent"
        width: 2 * root.ratio
        anchors.right: out_right_shadow.left
        anchors.bottom: out_bottom_shadow.top
        anchors.top: out_top_shadow.bottom
    }

    //Rectangle pour l'ombre extérieure supérieure
    Rectangle {
        id: in_top_shadow
        color: root.is_positive ? root.shadow : "transparent"
        height: 2 * root.ratio
        anchors.top: out_top_shadow.bottom
        anchors.left: out_left_shadow.right
        anchors.right: in_right_shadow.left
    }

    //Rectangle pour l'ombre extérieure gauche
    Rectangle {
        id: in_left_shadow
        color: root.is_positive ? root.shadow : "transparent"
        width: 2 * root.ratio
        anchors.left: out_left_shadow.right
        anchors.top: out_top_shadow.bottom
        anchors.bottom: in_bottom_shadow.top
    }
}