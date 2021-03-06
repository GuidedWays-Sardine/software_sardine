import QtQuick 2.0
import QtQuick.Controls 2.15


//https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
//Comment créer un élément personalisé

//https://doc.qt.io/qt-5/qtquickcontrols2-customize.html#customizing-combobox
//Comment personaliser un combobox


Item {
    id:root

    //Propriétés liés à la position et à la taille de l'objet
    property int default_width: 100         //dimensions de la combobox quand celle-ci est fermée et que la fenêtre fait du 640x480
    property int default_height: 40
    property int default_x: 0               //position du bouton pour les dimensions quand la fenêtre fait du 640x480
    property int default_y: 0

    //permet à partir des valeurs de positions et dimensions par défauts de calculer le ratio à appliquer aux dimensions
    readonly property real ratio:  (parent.width >= 640 && parent.height >= 480) ? parent.width/640 * (parent.width/640 < parent.height/480) + parent.height/480 * (parent.width/640 >= parent.height/480) : 1  //parent.height et parent.width représentent la taille de la fenêtre
    x: root.default_x * root.ratio
    y: root.default_y * root.ratio
    width: root.default_width * root.ratio
    height: root.default_height * root.ratio
    visible: is_visible

    //Propriétés liés aux donnés de la combobox
    property var elements: ["NaN"]          //définit les éléments sélectionables de la combobox
    readonly property int elements_count: combo.count //retient le nombre d'éléments sélectionables dans la combobox
    property int elements_displayed: 4      //définit le nombre d'éléments visibles dans la popup
    readonly property string selection_text: combo.displayText //retient le texte et l'index de la sélection actuelle et précédente
    readonly property int selection_index: combo.currentIndex
    //FEATURE : enregistres l'élément précédent sélectionné
    property int font_size: 12

    //Propriétés liés à l'état de la combobox
    property bool is_activable: true        //si la combobox peut être activée (Elle le sera que si is_activable est à true et qu'il y a plus d'un élément dans la combobox)
    property bool is_dark_grey: !is_activable//est ce que le texte doit-être en gris foncé ?
    property bool is_positive: false        //si la combobox doit-être visible en couche positive (sinon négative)
    property bool is_visible: true          //si le bouton est visible

    //Couleurs (ne peuvent pas être modifiés mais permet une mise à jour facile si nécessaire)
    readonly property string dark_blue : "#031122"  //partie 5.2.1.3.3  Nr 6
    readonly property string black: "#000000"       //partie 5.2.1.3.3  Nr 2
    readonly property string grey: "#C3C3C3"        //partie 5.2.1.3.3  Nr 3
    readonly property string dark_grey: "#555555"   //partie 5.2.1.3.3  Nr 5
    readonly property string shadow: "#08182F"      //partie 5.2.1.3.3  Nr 7


    //Différents signal handlers (à écrire en python)
    signal combobox_opened()                //détecte quand le popup de la combobox s'ouvre
    signal combobox_closed()                //détecte quand le popup de la combobox se ferme
    signal selection_changed()              //détecte quand l'utilisateur changed la sélection de la combobox (selection_changed() appelé après combobox_closed())


    //Fonction pour changer l'index de la combobox en fonction de l'index ou du texte de la sélection souhaité
    function change_selection(new_selection){
        // Si la nouvelle sélection est un int, change le currentIndex en fonction de l'index envoyé
        if(typeof new_selection === typeof root.font_size){
            if(new_selection < combo.count){
                combo.currentIndex = new_selection
            }
        }
        // Si la nouvelle sélection est un string, cherche l'élément avec le même index
        else if(typeof new_selection === typeof root.selection_text){
            for(var i = 0; i < combo.count; i++){
                if(root.elements[i].toUpperCase() === new_selection.toUpperCase()){
                    combo.currentIndex =  i
                }
            }
        }
    }



    //Inline component : combobox (crée une templace de la combobox)
    component DMI_combo: ComboBox {
        id: body

        anchors.fill: parent

        font.pixelSize: root.font_size * root.ratio
        font.family: "Verdana"
        flat: true

        //Flèche visible lorsque la combobox est fermée
        indicator: Canvas {
            id: canvas

            x: root.width - width - body.rightPadding
            y: body.topPadding + (body.availableHeight - height) / 2
            width: 12 * root.ratio
            height: 8 * root.ratio


            //Permet d'ouvrir le popup quand la combobox est sélectionné et appelle le signal handler
            Connections {
                target: body

                //Fonction détectant quand quand la combobox fermé a été cliquée
                function onPressedChanged() {
                    forceActiveFocus()
                    canvas.requestPaint()
                    if(root.is_activable && body.count > 1 && !body.pressed && !popup.visible)
                    {
                        root.combobox_opened()
                    }
                }
            }

            //Gère la couleur et le placement de la flèche, s'actualise à chaque changement de taille et de clique
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
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter

            text: body.displayText
            font: body.font
            color: !body.pressed && !root.is_dark_grey && body.count > 1 ? root.grey : root.dark_grey


            //Détecte quand la valeur du combobox est changé
            onTextChanged: {
                root.selection_changed()
            }
        }

        //Rectangle visible lorsque la combobox est fermée
        background: Rectangle {
            id: text_zone

            anchors.fill: parent

            color: root.dark_blue
        }

        //Menu de popup quand la combobox est ouverte
        popup: Popup {
            id: popup

            x: (root.is_positive ? 2 : 1) * root.ratio
            y: (root.default_height - 2) * root.ratio
            width: root.width - (is_positive ? 4 : 2) * root.ratio
            implicitHeight: ((body.count < root.elements_displayed ? body.height*body.count : body.height * root.elements_displayed) + (root.is_positive ? 7 : 8) * root.ratio) * (root.is_activable && body.count > 1)
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
                implicitHeight: contentHeight

                clip: true
                model: body.popup.visible && is_activable && body.count > 1 ? body.delegateModel : null
                currentIndex: body.highlightedIndex

                ScrollIndicator.vertical: ScrollIndicator { }
            }

            //Rectangle de fond (cache les widgets lorsque la combobox est ouverte
            background: Rectangle {
                color: root.dark_blue
            }
        }
    }


    //Crée une instance de la combobox
    DMI_combo {
        id:combo

        anchors.fill: parent

        model: root.elements

        //Le delegate permete de définir la composition et la forme des éléments de la combobox
        delegate: ItemDelegate {
            width: combo.width
            height: combo.height

            background: Rectangle {
                color: "transparent"
            }

            contentItem: Text {
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter

                text: modelData
                color: combo.highlightedIndex === index ? root.dark_grey : root.grey
                font: combo.font
            }
        }
    }


    //Ombre extérieure
    //Rectangle pour l'ombre extérieure supérieure
    Rectangle {
        id: out_top_shadow

        height: 1 * root.ratio
        anchors.left: combo.left
        anchors.top: combo.top
        anchors.right: out_right_shadow.left

        color: root.black
    }

    //Rectangle pour l'ombre extérieure droite
    Rectangle {
        id: out_right_shadow

        width: 1 * root.ratio
        height: combo.popup.visible && is_activable && combo.count > 1 ? combo.height*((combo.count < root.elements_displayed ? combo.count : root.elements_displayed) + 1) + 7 * root.ratio : combo.height
        anchors.right: combo.right
        anchors.top: combo.top

        color: root.shadow
    }

    //Rectangle pour l'ombre extérieure gauche
    Rectangle {
        id: out_left_shadow

        width: 1 * root.ratio
        anchors.top: combo.top
        anchors.left: combo.left
        anchors.bottom: out_bottom_shadow.top

        color: root.black
    }

    //Rectangle pour l'ombre extérieure inférieure
    Rectangle {
        id: out_bottom_shadow

        height: 1 * root.ratio
        anchors.right: combo.right
        anchors.bottom: out_right_shadow.bottom
        anchors.left: combo.left

        color: root.shadow
    }


    //Ombre intérieure
    //Rectangle pour l'ombre extérieure inférieure
    Rectangle {
        id: in_bottom_shadow

        height: 1 * root.ratio
        anchors.bottom: out_bottom_shadow.top
        anchors.left: out_left_shadow.right
        anchors.right: out_right_shadow.left

        color: root.is_positive ? root.black : "transparent"
    }

    //Rectangle pour l'ombre extérieure droite
    Rectangle {
        id: in_right_shadow

        width: 1 * root.ratio
        anchors.right: out_right_shadow.left
        anchors.bottom: out_bottom_shadow.top
        anchors.top: out_top_shadow.bottom

        color: root.is_positive ? root.black : "transparent"
    }

    //Rectangle pour l'ombre extérieure supérieure
    Rectangle {
        id: in_top_shadow

        height: 1 * root.ratio
        anchors.top: out_top_shadow.bottom
        anchors.left: out_left_shadow.right
        anchors.right: in_right_shadow.left

        color: root.is_positive ? root.shadow : "transparent"
    }

    //Rectangle pour l'ombre extérieure gauche
    Rectangle {
        id: in_left_shadow

        width: 1 * root.ratio
        anchors.left: out_left_shadow.right
        anchors.top: out_top_shadow.bottom
        anchors.bottom: in_bottom_shadow.top

        color: root.is_positive ? root.shadow : "transparent"
    }
}