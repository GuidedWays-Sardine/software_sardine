import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQml 2.15
//import QtMultimedia 5.15
//FIXME : librairie non trouvée, impossible de trouver le son approprié


//https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
//Comment créer un élément personalisé

//https://doc.qt.io/qt-5/qtquickcontrols2-customize.html#customizing-button
//Comment personaliser un bouton


Item {
    id: root

    //Propriétés liés à la position et à la taille de l'objet
    property int default_width: 100         //dimensions du bouton pour les dimensions minimales de la fenêtre (640*480)
    property int default_height: 40
    property int default_x: 0               //position du bouton pour les dimensions minimales de la fenêtre (640*480)
    property int default_y: 0

    //permet à partir des valeurs de positions et dimensions par défauts de calculer la position et la taille peu importe la dimension de la fenêtre
    readonly property real ratio:  (parent.width >= 640 && parent.height >= 480) ? parent.width/640 * (parent.width/640 < parent.height/480) + parent.height/480 * (parent.width/640 >= parent.height/480) : 1  //parent.height et parent.width représentent la taille de la fenêtre
    x: root.default_x * root.ratio
    y: root.default_y * root.ratio
    width: root.default_width * root.ratio
    height: root.default_height * root.ratio

    //Propriétés liés à l'image et au texte que l'utilisateur peut rajouter sur le bouton
    property string default_image: ""       //image à afficher en tout temps sur le bouton si image_activable et image_not_activable sont vides (peut rester vide)
    property string image_activable: ""     //image à afficher quand le bouton est cliquable (peut rester vide)
    property string image_not_activable: "" //image à afficher quand le bouton n'est pas cliquable (peut rester vide)
    property string text: ""                //texte à afficher
    property int font_size: 12              //police du texte

    //Propriétés liés à l'état du bouton
    property bool is_activable: true         //si le bouton peut être activée
    property bool is_dark_grey: !is_activable//est ce que le texte doit-être en gris foncé ?
    property bool is_positive: false         //si le bouton doit-être visible en couche positive (sinon négatif)
    property bool is_visible: true           //si le bouton est visible
    visible: root.is_visible

    //Couleurs (ne peuvent pas être modifiés mais permet une mise à jour facile si nécessaire)
    readonly property string dark_blue : "#031122"  //partie 5.2.1.3.3  Nr 6
    readonly property string black: "#000000"       //partie 5.2.1.3.3  Nr 2
    readonly property string grey: "#C3C3C3"        //partie 5.2.1.3.3  Nr 3
    readonly property string dark_grey: "#969696"   //partie 5.2.1.3.3  Nr 5
    readonly property string shadow: "#08182F"      //partie 5.2.1.3.3  Nr 7

    //Chemin d'accès vers les icones utiles pour le check_button
    readonly property string symbols_path : "../../../assets/DMI_symbols/ETCS/"
    readonly property string sounds_path: "../../../assets/DMI_sounds/ETCS/"


    //Différents signal handlers (à écrire en python)
    signal clicked()                        //détecte quand le bouton est cliqué
    signal click_start()                    //détecte quand l'utilisateur commence à appuyer sur le bouton
    signal click_end()                      //détecte quand l'utilisateur relache le bouton (similaire à .clicked())



    //Variable stockant le mode de fonctionnement du bouton ("UP", "DOWN", "DELAY")
    property string button_type: "UP"

    //Rectangle pour la couleur du fond du bouton
    Rectangle{
        id: body
        color: root.dark_blue
        anchors.fill: parent
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
    }

    //Image visible sur le bouton
    Image {
        id: image

        anchors.bottom: body.bottom
        anchors.bottomMargin: (1 + root.isPositive) * root.ratio
        anchors.right: body.right
        anchors.rightMargin: (1 + root.isPositive) * root.ratio
        anchors.top: body.top
        anchors.topMargin: (1 + root.isPositive) * root.ratio
        anchors.left: body.left
        anchors.leftMargin: (1 + root.isPositive) * root.ratio

        source: (root.image_activable != "" || root.image_not_activable != "") ? root.symbols_path + (root.is_activable ? image_activable : image_not_activable) : root.symbols_path + root.default_image
    }

    //Texte visible sur le bouton
    Text{
        id: button_text

        anchors.horizontalCenter: body.horizontalCenter
        anchors.verticalCenter: body.verticalCenter

        text: root.text
        font.pixelSize: root.font_size * ratio
        font.family: "Verdana"
        color: root.is_dark_grey ? root.dark_grey : root.grey
    }


    //Variable stockant si  le bouton est dans l'état appuyé (et donc si les bordures doivent êtres cachées
    property bool button_pressed: false

    //Ombre extérieure
    //Rectangle pour l'ombre extérieure inférieure
    Rectangle {
        id: out_bottom_shadow

        height: 1 * root.ratio
        anchors.right: body.right
        anchors.bottom: body.bottom
        anchors.left: body.left

        color: !root.button_pressed ? root.shadow : "transparent"
    }

    //Rectangle pour l'ombre extérieure droite
    Rectangle {
        id: out_right_shadow

        width: 1 * root.ratio
        anchors.right: body.right
        anchors.bottom: body.bottom
        anchors.top: body.top

        color: !root.button_pressed ? root.shadow : "transparent"
    }

    //Rectangle pour l'ombre extérieure supérieure
    Rectangle {
        id: out_top_shadow

        height: 1 * root.ratio
        anchors.top: body.top
        anchors.left: body.left
        anchors.right: out_right_shadow.left

        color: !root.button_pressed ? root.black : "transparent"
    }

    //Rectangle pour l'ombre extérieure gauche
    Rectangle {
        id: out_left_shadow

        width: 1 * root.ratio
        anchors.top: body.top
        anchors.left: body.left
        anchors.bottom: out_bottom_shadow.top

        color: !root.button_pressed ? root.black : "transparent"
    }


    //Ombre intérieure
    //Rectangle pour l'ombre intérieure inférieure
    Rectangle {
        id: in_bottom_shadow

        height: 1 * root.ratio
        anchors.bottom: out_bottom_shadow.top
        anchors.left: out_left_shadow.right
        anchors.right: out_right_shadow.left

        color: is_positive && !root.button_pressed ? root.black : "transparent"
    }

    //Rectangle pour l'ombre intérieure droite
    Rectangle {
        id: in_right_shadow

        width: 1 * root.ratio
        anchors.right: out_right_shadow.left
        anchors.bottom: out_bottom_shadow.top
        anchors.top: out_top_shadow.bottom

        color: is_positive && !root.button_pressed ? root.black : "transparent"
    }

    //Rectangle pour l'ombre intérieure supérieure
    Rectangle {
        id: in_top_shadow

        height: 1 * root.ratio
        anchors.top: out_top_shadow.bottom
        anchors.left: out_left_shadow.right
        anchors.right: in_right_shadow.left

        color: is_positive && !root.button_pressed ? root.shadow : "transparent"
    }

    //Rectangle pour l'ombre intérieure gauche
    Rectangle {
        id: in_left_shadow

        width: 1 * root.ratio
        anchors.left: out_left_shadow.right
        anchors.top: out_top_shadow.bottom
        anchors.bottom: in_bottom_shadow.top

        color: is_positive && !root.button_pressed ? root.shadow : "transparent"
    }


    //Timer utile pour le fonctionnement des différents mode sdes boutons
    Timer {
        id: timer

        interval: 1500
        repeat: false

        onTriggered: {
            if(root.button_type.toUpperCase() == "DOWN") {
                //Si le bouton est en état pressé
                if(root.button_pressed) {
                    //Indique l'état du bouton comme non pressé, et appelle la fonction clicked
                    root.button_pressed = false
                    area.repeat_count = area.repeat_count + 1
                    root.clicked()

                    //Si le bouton en est à son premier appui, relance un timer de 1.470s sinon relance un timer de 270s
                    if(area.repeat_count <=1) {
                        timer.interval = 1470
                        timer.restart()
                    }
                    else {
                        timer.interval = 270
                        timer.restart()
                    }
                }
                //Si le bouton n'était pas pressé
                else {
                    //Se met en état pressé, joue le son et lance une pression pendant 30ms
                    root.button_pressed = true
                    //FIXME : jouer le son du bouton cliqué
                    timer.interval = 30
                    timer.restart()
                }
            }
            else if(root.button_type.toUpperCase() == "DELAY") {
                //Incrément de 1 la répétition, inverse la visibilité de la préssabilité du bouton
                area.repeat_count = area.repeat_count + 1
                root.button_pressed = !(area.repeat_count % 2)

                //Recommence le timer si celui-ci a été appelé moins de 8 fois, sinon joue le son du clique
                if(area.repeat_count < 8) {
                    timer.restart()
                }
                else {
                    //FIXME : jouer le son du bouton cliqué
                    console.log("pour combler")
                }
            }
        }
    }


    //Zone de détection de souris (utile pour détecter les cliques)
    MouseArea{
        id: area

        //Propriété privée permettant à la zone de savoir le nombre de cycles "presses->enabled" pour les boutons down et delay
        property int repeat_count: 0

        anchors.fill: parent

        hoverEnabled: false


        //Détecte quand la zone (le bouton) commence à être appuyé
        onPressed: {
            //force le focus sur ce bouton pour qu'il soit prioritaire
            forceActiveFocus()

            //Vérifie que le bouton est activable
            if(root.is_activable) {
                //Cas du bouton de type Delay
                if(root.button_type.toUpperCase() == "DELAY"){
                    //remet à 0 le compteur de répétition, indique que le bouton est pressé, appel le signal et joue le clique du bouton
                    area.repeat_count = 0
                    root.button_pressed = true
                    root.click_start()

                    //Lance le timer (de 250ms)
                    timer.interval = 250
                    timer.restart()
                }
                //Cas du bouton de type down
                else if(root.button_type.toUpperCase() == "DOWN"){
                    //remet à 0 le compteur de répétition, indique que le bouton est pressé, appel le signal et joue le clique du bouton
                    area.repeat_count = 0
                    root.button_pressed = true
                    root.click_start()
                    //FIXME : jouer le son du bouton cliqué

                    //Lance le premier timer (de 30ms)
                    timer.interval = 30
                    timer.restart()
                }
                //Cas si le bouton est de type "UP" (par défaut)
                else {
                    //remet à 0 le compteur de répétition, indique que le bouton est pressé, appel le signal et joue le clique du bouton
                    area.repeat_count = 0
                    root.button_pressed = true
                    root.click_start()
                    //FIXME : jouer le son du bouton cliqué
                }
            }
        }

        //Détecte quand la zone (le bouton) est relachée
        onReleased: {
            if(root.is_activable){
                //Cas si la souris rerentre sur le bouton
                if(containsMouse){
                    //Cas du bouton de type Delay
                    if(root.button_type.toUpperCase() == "DELAY"){
                        //Le bouton n'est pas pressé et le timer désactivé
                        root.button_pressed = false
                        timer.stop()

                        //Si les 8 cycles ont été réalisés, considère le clique
                        if(area.repeat_count === 8) {
                            root.clicked()
                            root.click_end()
                        }
                    }
                    //Cas du bouton de type down
                    else if(root.button_type.toUpperCase() == "DOWN"){
                        //Seul le clik_end() est enregistré, arrête le timer
                        root.button_pressed = false
                        root.click_end()
                        timer.stop()
                    }
                    //Cas si le bouton est de type "UP" (par défaut)
                    else {
                        //Le clique est enregistré, aucun timer à arréter
                        root.button_pressed = false
                        root.clicked()
                        root.click_end()
                    }
                }
                //Cas où la souris resort du bouton
                else {
                    //Cas du bouton de type Delay
                    if(root.button_type.toUpperCase() == "DELAY"){
                        //Le bouton n'est pas pressé, aucun timer a arrété
                        root.button_pressed = false
                    }
                    //Cas du bouton de type down
                    else if(root.button_type.toUpperCase() == "DOWN"){
                        //Le bouton n'est pas pressé, arrête tous les timer
                        root.button_pressed = false
                        timer.stop()
                    }
                    //Cas si le bouton est de type "UP" (par défaut)
                    else {
                        //Le bouton n'est pas pressé, aucun timer à arréter
                        root.button_pressed = false
                    }
                }
            }
        }

        //Fonction qui détecte lorsque l'utilisateur sort ou rentre sa souris du bouton alors qu'il clique dessus
        onContainsMouseChanged: {
            //Si le bouton est activable
            if(root.is_activable){
                //Cas si la souris rerentre sur le bouton
                if(area.containsMouse){
                    //Cas du bouton de type Delay
                    if(root.button_type.toUpperCase() == "DELAY"){
                        //Remet le bouton comme pressé et recommence les 8 cycles de 250ms
                        root.button_pressed = true
                        timer.interval = 250
                        timer.restart()
                    }
                    //Cas du bouton de type down
                    else if(root.button_type.toUpperCase() == "DOWN"){
                        //Si le délai de 1500ms n'est pas passé, le recommence, sinon passe directement à la répétition
                        timer.interval = 270 + 1200 * (area.repeat_count <= 1)
                        timer.restart()
                    }
                    //Cas si le bouton est de type "UP" (par défaut)
                    else {
                        //Indique visuellement le bouton comme pressé
                        root.button_pressed = true
                    }
                }
                //Cas où la souris resort du bouton
                else {
                    //Cas du bouton de type Delay
                    if(root.button_type.toUpperCase() == "DELAY"){
                        //Le bouton n'est pas pressé, arrête le timer, réinitialise le compteur de répétition
                        root.button_pressed = false
                        timer.stop()
                        area.repeat_count = 0
                    }
                    //Cas du bouton de type down
                    else if(root.button_type.toUpperCase() == "DOWN"){
                        //Indique le bouton comme visuellement non pressé et arrête le timer
                        root.button_pressed = false
                        timer.stop()
                    }
                    //Cas si le bouton est de type "UP" (par défaut)
                    else {
                        //Indique visuellement le bouton comme non pressé
                        root.button_pressed = false
                    }
                }
            }
        }
    }

    //Son à jouer lorsque le bouton est cliqué
    //SoundEffect {
    //    id: click_sound
    //    source: sounds_path + "click.wav"
    //}

}