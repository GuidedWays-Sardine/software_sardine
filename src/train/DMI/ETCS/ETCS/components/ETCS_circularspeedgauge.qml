import QtQuick 2.15


//https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
//Comment créer un élément personalisé


Item {
    id: root

    //Propriétés liés à la position et à la taille de l'objet
    property int radius: 125                      //Rayon du DMI_speeddial
    property double indication_angle: 3.2         //angle (en °) de l'indication pour la vitesse permise
    property double hook_angle: 5                 //angle (en °) des crochets d'indication
    property int default_x: 300                   //position du bouton pour les dimensions minimales de la fenêtre (640*480)
    property int default_y: 300
    anchors.fill: parent

    //permet à partir des valeurs de positions et dimensions par défauts de calculer la position et la taille peu importe la dimension de la fenêtre
    readonly property real ratio:  (parent.width >= 640 && parent.height >= 480) ? parent.width/640 * (parent.width/640 < parent.height/480) + parent.height/480 * (parent.width/640 >= parent.height/480) : 1  //parent.height et parent.width représentent la taille de la fenêtre
    onRatioChanged: {root.update()}

    //Propriétés liées à la vitesse maximale du speeddial
    property double speed: 0
    onSpeedChanged: {root.update()}
    property int max_speed: 400                 //vitesse maximale du matériel roulant (utile pour déduire le type de cadran)
    onMax_speedChanged: {root.update()}
    readonly property int speed_dial_index: (max_speed > 140) + (max_speed > 180) + (max_speed > 250)


    // Propriétés liées au format du speeddial
    property double start_angle: 144            //angle de début
    property int font_size: 18

    //propriétés pour la couleur du pointeur
    property double permitted_speed: 50//0
    onPermitted_speedChanged: {root.update()}
    property double target_speed: 15
    onTarget_speedChanged: {root.update()}
    property double release_speed: 30//0
    onRelease_speedChanged: {root.update()}
    property double brake_speed: 70//-1
    property string operating_mode: "OS"//""FS"
    onOperating_modeChanged: {root.update()}
    property string speed_monitoring: "RSM"//"CSM"
    onSpeed_monitoringChanged: {root.update()}
    property string status_information: "IndS"//"NoS"
    onStatus_informationChanged: {root.update()}



    //Fonction qui remet à jour tous les éléments graphiques du pointeur
    function update(){
        over_permitted_limit.requestPaint()
        permitted_limit.requestPaint()
        target_limit.requestPaint()
        release_limit.requestPaint()
        permitted_speed_hook.requestPaint()
        target_speed_hook.requestPaint()
    }


    //Couleurs (ne peuvent pas être modifiés mais permet une mise à jour facile si nécessaire)
    readonly property string grey: "#C3C3C3"        //partie 5.2.1.3.3  Nr 3
    readonly property string red: "#BF0003"         //partie 5.2.1.3.3  Nr 10
    readonly property string orange: "#EA9109"      //partie 5.2.1.3.3  Nr 9
    readonly property string yellow: "#DFDF00"      //partie 5.2.1.3.3  Nr 8
    readonly property string black: "#000000"       //partie 5.2.1.3.3  Nr 2
    readonly property string white: "#FFFFFF"       //partie 4.2.1.3.3  Nr 1
    readonly property string dark_grey: "#555555"   //partie 5.2.1.3.3  Nr 5
    readonly property string medium_grey: "#969696" //partie 5.2.1.3.3  Nr 4


    Canvas {
        id: over_permitted_limit

        anchors.fill: parent

        //angle de la vitesse permise
        readonly property double permitted_angle: 270 - root.start_angle + 2 * root.start_angle *
                        (root.permitted_speed >= [140, 180, 250, 400][root.speed_dial_index % 4] ? 1.0 :     //Prise en compte du cas où la vitesse est supérieure à la vitesse limite affichable
                            (root.speed_dial_index % 4) !== 3
                            ?       //cas des jauges 140/180/250 km/h
                            root.permitted_speed/([140, 180, 250][root.speed_dial_index % 4])
                            :       //cas de la jauge 400km/h
                            root.permitted_speed/300 - (root.permitted_speed > 200) * (root.permitted_speed - 200)/600)

        //angle de la vitesse de freinage (d'urgence ou de service)
        readonly property double brake_angle: 270 - root.start_angle + 2 * root.start_angle *
                        (root.brake_speed >= [140, 180, 250, 400][root.speed_dial_index % 4] ? 1.0 :     //Prise en compte du cas où la vitesse est supérieure à la vitesse limite affichable
                            (root.speed_dial_index % 4) !== 3
                            ?       //cas des jauges 140/180/250 km/h
                            root.brake_speed/([140, 180, 250][root.speed_dial_index % 4])
                            :       //cas de la jauge 400km/h
                            root.brake_speed/300 - (root.brake_speed > 200) * (root.brake_speed - 200)/600)

        onPaint: {
            var ctx = over_permitted_limit.getContext("2d")
            ctx.reset()

            //condition pour remettre à jour l'élément
            if(root.operating_mode.toUpperCase() === "FS" &&            // Est ce qu'on est en mode fullsupervision ?
                    (root.status_information.toUpperCase() === "OVS" ||      // Est ce qu'on est en status OVS, WAS ou INTS
                     root.status_information.toUpperCase() === "WAS" ||
                     root.status_information.toUpperCase() === "INTS") &&
                    root.permitted_speed < root.brake_speed) {                 // Est ce que la vitesse permise est inférieure à la vitesse de freinage (de service ou d'urgence) ?

                //dessine
                ctx.arc(root.default_x * root.ratio, root.default_y * root.ratio,
                        (root.radius + 3 + 9 - 20) * root.ratio, brake_angle * Math.PI / 180, permitted_angle * Math.PI / 180, true)
                ctx.lineTo((root.default_x + (root.radius + 3 + 9) * Math.cos(permitted_angle * Math.PI / 180)) * root.ratio, (root.default_y + (root.radius + 3 + 9) * Math.sin(permitted_angle * Math.PI / 180)) * root.ratio)
                ctx.arc(root.default_x * root.ratio, root.default_y * root.ratio,
                        (root.radius + 3 + 9) * root.ratio, permitted_angle * Math.PI / 180, brake_angle * Math.PI / 180)
                ctx.lineTo((root.default_x + (root.radius + 3 + 9 - 20) * Math.cos(brake_angle * Math.PI / 180)) * root.ratio, (root.default_y + (root.radius + 3 + 9 - 20) * Math.sin(brake_angle * Math.PI / 180)) * root.ratio)
                ctx.closePath()
                if(root.status_information.toUpperCase() === "INTS") {
                    ctx.fillStyle = root.red
                }
                else {
                    ctx.fillStyle = root.orange
                }
                ctx.fill()
            }
        }
    }

    Canvas {
        id: release_limit

        transformOrigin: Item.center
        anchors.fill: parent

        //angle de début de la barre
        readonly property double begining_angle: 270 -  root.start_angle

        //angle de la vitesse de relachement
        readonly property double release_angle: root.release_speed <= 0 ? 0 : 270 - root.start_angle + 2 * root.start_angle *
                        (root.release_speed >= [140, 180, 250, 400][root.speed_dial_index % 4] ? 1.0 :     //Prise en compte du cas où la vitesse est supérieure à la vitesse limite affichable
                            (root.speed_dial_index % 4) !== 3
                            ?       //cas des jauges 140/180/250 km/h
                            root.release_speed/([140, 180, 250][root.speed_dial_index % 4])
                            :       //cas de la jauge 400km/h
                            root.release_speed/300 - (root.release_speed > 200) * (root.release_speed - 200)/600)

        //angle de la vitesse de freinage (d'urgence ou de service)
        readonly property double permitted_angle: 270 - root.start_angle + 2 * root.start_angle *
                        (root.permitted_speed >= [140, 180, 250, 400][root.speed_dial_index % 4] ? 1.0 :     //Prise en compte du cas où la vitesse est supérieure à la vitesse limite affichable
                            (root.speed_dial_index % 4) !== 3
                            ?       //cas des jauges 140/180/250 km/h
                            root.permitted_speed/([140, 180, 250][root.speed_dial_index % 4])
                            :       //cas de la jauge 400km/h
                            root.permitted_speed/300 - (root.permitted_speed > 200) * (root.permitted_speed - 200)/600)

        onPaint: {
            var ctx = release_limit.getContext("2d")
            ctx.reset()

            //condition pour remettre à jour l'élément
            if(root.operating_mode.toUpperCase() === "FS" && root.release_speed > 0) {   //Est ce qu'on est en mode FullSupervision

                //dessine
                if(root.permitted_speed < root.release_speed) {
                    ctx.arc(root.default_x * root.ratio, root.default_y * root.ratio,
                            (root.radius + 3 + 9) * root.ratio, begining_angle * Math.PI / 180, release_angle * Math.PI / 180)
                    ctx.lineTo((root.default_x + (root.radius + 3) * Math.cos(release_angle * Math.PI / 180)) * root.ratio, (root.default_y + (root.radius + 3) * Math.sin(release_angle * Math.PI / 180)) * root.ratio)
                    ctx.arc(root.default_x * root.ratio, root.default_y * root.ratio,
                            (root.radius + 3) * root.ratio, release_angle * Math.PI / 180, permitted_angle * Math.PI / 180, true)
                    ctx.lineTo((root.default_x + (root.radius + 3 + 5) * Math.cos(permitted_angle * Math.PI / 180)) * root.ratio, (root.default_y + (root.radius + 3 + 5) * Math.sin(permitted_angle * Math.PI / 180)) * root.ratio)
                    ctx.arc(root.default_x * root.ratio, root.default_y * root.ratio,
                            (root.radius + 3 + 5) * root.ratio, permitted_angle * Math.PI / 180, begining_angle * Math.PI / 180, true)
                }
                else {
                    ctx.arc(root.default_x * root.ratio, root.default_y * root.ratio,
                            (root.radius + 3 + 9) * root.ratio, begining_angle * Math.PI / 180, permitted_angle * Math.PI / 180)
                    ctx.lineTo((root.default_x + (root.radius + 3 + 5) * Math.cos(permitted_angle * Math.PI / 180)) * root.ratio, (root.default_y + (root.radius + 3 + 5) * Math.sin(permitted_angle * Math.PI / 180)) * root.ratio)
                    ctx.arc(root.default_x * root.ratio, root.default_y * root.ratio,
                            (root.radius + 3 + 5) * root.ratio, permitted_angle * Math.PI / 180, begining_angle * Math.PI / 180, true)
                }
                ctx.closePath()
                ctx.fillStyle = root.grey
                ctx.fill()
            }
        }
    }

    Canvas {
        id: permitted_limit

        transformOrigin: Item.center
        anchors.fill: parent

        //angle de début de la barre
        readonly property double begining_angle: 270 -  root.start_angle

        //angle de la vitesse de freinage (d'urgence ou de service)
        readonly property double permitted_angle: 270 - root.start_angle + 2 * root.start_angle *
                        (root.permitted_speed >= [140, 180, 250, 400][root.speed_dial_index % 4] ? 1.0 :     //Prise en compte du cas où la vitesse est supérieure à la vitesse limite affichable
                            (root.speed_dial_index % 4) !== 3
                            ?       //cas des jauges 140/180/250 km/h
                            root.permitted_speed/([140, 180, 250][root.speed_dial_index % 4])
                            :       //cas de la jauge 400km/h
                            root.permitted_speed/300 - (root.permitted_speed > 200) * (root.permitted_speed - 200)/600)

        //angle de la vitesse de relachement
        readonly property double release_angle: root.release_speed <= 0 ? 0 : 270 - root.start_angle + 2 * root.start_angle *
                        (root.release_speed >= [140, 180, 250, 400][root.speed_dial_index % 4] ? 1.0 :     //Prise en compte du cas où la vitesse est supérieure à la vitesse limite affichable
                            (root.speed_dial_index % 4) !== 3
                            ?       //cas des jauges 140/180/250 km/h
                            root.release_speed/([140, 180, 250][root.speed_dial_index % 4])
                            :       //cas de la jauge 400km/h
                            root.release_speed/300 - (root.release_speed > 200) * (root.release_speed - 200)/600)

        onPaint: {
            var ctx = permitted_limit.getContext("2d")
            ctx.reset()

            //condition pour remettre à jour l'élément
            if(root.operating_mode.toUpperCase() === "FS") {   //Est ce qu'on est en mode FullSupervision

                //dessine
                ctx.arc(root.default_x * root.ratio, root.default_y * root.ratio,
                        (root.radius + 3) * root.ratio, (permitted_angle - root.indication_angle) * Math.PI / 180, begining_angle * Math.PI / 180, true)
                if(root.release_speed <= 0){
                    ctx.lineTo((root.default_x + (root.radius + 3 + 9) * Math.cos(begining_angle * Math.PI / 180)) * root.ratio, (root.default_y + (root.radius + 3 + 9) * Math.sin(begining_angle * Math.PI / 180)) * root.ratio)
                    ctx.arc(root.default_x * root.ratio, root.default_y * root.ratio,
                            (root.radius + 3 + 9) * root.ratio, begining_angle * Math.PI / 180, permitted_angle * Math.PI / 180)
                    }
                else {
                    ctx.lineTo((root.default_x + (root.radius + 3 + 3) * Math.cos(begining_angle * Math.PI / 180)) * root.ratio, (root.default_y + (root.radius + 3 + 3) * Math.sin(begining_angle * Math.PI / 180)) * root.ratio)
                    if(root.release_speed <= root.permitted_speed) {
                        ctx.arc(root.default_x * root.ratio, root.default_y * root.ratio,
                                (root.radius + 3 + 3) * root.ratio, begining_angle * Math.PI / 180, release_angle * Math.PI / 180)
                        ctx.lineTo((root.default_x + (root.radius + 3 + 9) * Math.cos(release_angle * Math.PI / 180)) * root.ratio, (root.default_y + (root.radius + 3 + 9) * Math.sin(release_angle * Math.PI / 180)) * root.ratio)
                        ctx.arc(root.default_x * root.ratio, root.default_y * root.ratio,
                                (root.radius + 3 + 9) * root.ratio, release_angle * Math.PI / 180, permitted_angle * Math.PI / 180)

                    }
                    else {
                        ctx.arc(root.default_x * root.ratio, root.default_y * root.ratio,
                                (root.radius + 3 + 3) * root.ratio, begining_angle * Math.PI / 180, permitted_angle * Math.PI / 180)
                    }
                }
                ctx.lineTo((root.default_x + (root.radius + 3 + 9 - 20) * Math.cos(permitted_angle * Math.PI / 180)) * root.ratio, (root.default_y + (root.radius + 3 + 9 - 20) * Math.sin(permitted_angle * Math.PI / 180)) * root.ratio)
                ctx.arc(root.default_x * root.ratio, root.default_y * root.ratio,
                        (root.radius + 3 + 9 - 20) * root.ratio, permitted_angle * Math.PI / 180, (permitted_angle - root.indication_angle) * Math.PI / 180, true)
                ctx.lineTo((root.default_x + (root.radius + 3) * Math.cos((permitted_angle - root.indication_angle) * Math.PI / 180)) * root.ratio, (root.default_y + (root.radius + 3) * Math.sin((permitted_angle - root.indication_angle) * Math.PI / 180)) * root.ratio)
                ctx.closePath()

                if(root.permitted_speed < 0.1 + root.target_speed || root.target_speed < 0) {
                    ctx.fillStyle = root.dark_grey
                }
                else if(root.speed_monitoring.toUpperCase() === "CSM") {
                    ctx.fillStyle = root.white
                }
                else {
                    ctx.fillStyle = root.yellow
                }
                ctx.fill()
            }
        }
    }

    Canvas {
        id: target_limit

        anchors.fill: parent

        //angle de début de la barre
        readonly property double begining_angle: 270 -  root.start_angle - 5

        //Vitesse de référence vaut target_speed quand celle-ci existe sinon permitted_speed
        readonly property double reference_speed: ((root.target_speed < 0 || root.target_speed > root.permitted_speed) * root.permitted_speed + (root.target_speed >= 0 && root.target_speed <= root.permitted_speed) * root.target_speed)

        //angle de la vitesse de freinage (d'urgence ou de service)
        readonly property double target_angle: 270 - root.start_angle + 2 * root.start_angle *
                        (reference_speed >= [140, 180, 250, 400][root.speed_dial_index % 4] ? 1.0 :     //Prise en compte du cas où la vitesse est supérieure à la vitesse limite affichable
                            (root.speed_dial_index % 4) !== 3
                            ?       //cas des jauges 140/180/250 km/h
                            reference_speed/([140, 180, 250][root.speed_dial_index % 4])
                            :       //cas de la jauge 400km/h
                            reference_speed/300 - (reference_speed > 200) * (reference_speed - 200)/600)

        onPaint: {
            var ctx = target_limit.getContext("2d")
            ctx.reset()

            //condition pour remettre à jour l'élément
            if(root.operating_mode.toUpperCase() === "FS") {   //Est ce qu'on est en mode FullSupervision

                //dessine
                ctx.arc(root.default_x * root.ratio, root.default_y * root.ratio,
                        (root.radius + 3) * root.ratio, target_angle * Math.PI / 180, begining_angle * Math.PI / 180, true)
                ctx.lineTo((root.default_x + (root.radius + 3 + 9) * Math.cos(begining_angle * Math.PI / 180)) * root.ratio, (root.default_y + (root.radius + 3 + 9) * Math.sin(begining_angle * Math.PI / 180)) * root.ratio)
                ctx.arc(root.default_x * root.ratio, root.default_y * root.ratio,
                        (root.radius + 3 + 9) * root.ratio, begining_angle * Math.PI / 180, target_angle * Math.PI / 180)
                ctx.lineTo((root.default_x + (root.radius + 3) * Math.cos(target_angle * Math.PI / 180)) * root.ratio, (root.default_y + (root.radius + 3) * Math.sin(target_angle * Math.PI / 180)) * root.ratio)
                ctx.closePath()
                ctx.fillStyle = root.dark_grey
                ctx.fill()
            }
        }
    }

    //Pour les hooks
    Canvas {
        id: permitted_speed_hook
        visible: root.operating_mode.toUpperCase() === "OS" ||
                 root.operating_mode.toUpperCase() === "SR" ||
                 root.operating_mode.toUpperCase() === "SH" ||
                 root.operating_mode.toUpperCase() === "RV"


        anchors.fill: parent

        //angle de la vitesse permise
        readonly property double permitted_angle: 270 - root.start_angle + 2 * root.start_angle *
                        (root.permitted_speed >= [140, 180, 250, 400][root.speed_dial_index % 4] ? 1.0 :     //Prise en compte du cas où la vitesse est supérieure à la vitesse limite affichable
                            (root.speed_dial_index % 4) !== 3
                            ?       //cas des jauges 140/180/250 km/h
                            root.permitted_speed/([140, 180, 250][root.speed_dial_index % 4])
                            :       //cas de la jauge 400km/h
                            root.permitted_speed/300 - (root.permitted_speed > 200) * (root.permitted_speed - 200)/600)

        onPaint: {
            var ctx = permitted_speed_hook.getContext("2d")
            ctx.reset()

            //dessine
            ctx.arc(root.default_x * root.ratio, root.default_y * root.ratio,
                    (root.radius + 3 + 9 - 20) * root.ratio, permitted_angle * Math.PI / 180, (permitted_angle - root.hook_angle) * Math.PI / 180, true)
            ctx.lineTo((root.default_x + (root.radius + 3 + 9) * Math.cos((permitted_angle - root.hook_angle) * Math.PI / 180)) * root.ratio, (root.default_y + (root.radius + 3 + 9) * Math.sin((permitted_angle - root.hook_angle) * Math.PI / 180)) * root.ratio)
            ctx.arc(root.default_x * root.ratio, root.default_y * root.ratio,
                    (root.radius + 3 + 9) * root.ratio, (permitted_angle - root.hook_angle) * Math.PI / 180, permitted_angle * Math.PI / 180)
            ctx.lineTo((root.default_x + (root.radius + 3 + 9 - 20) * Math.cos(permitted_angle * Math.PI / 180)) * root.ratio, (root.default_y + (root.radius + 3 + 9 - 20) * Math.sin(permitted_angle * Math.PI / 180)) * root.ratio)
            ctx.closePath()
            ctx.fillStyle = root.white
            ctx.fill()
        }
    }

    Canvas {
        id: target_speed_hook
        visible: (root.operating_mode.toUpperCase() === "OS" ||
                 root.operating_mode.toUpperCase() === "SR") &&
                 root.target_speed >= 0 && root.target_speed < root.permitted_speed


        anchors.fill: parent

        //angle de la vitesse permise
        readonly property double target_angle: 270 - root.start_angle + 2 * root.start_angle *
                        (target_speed >= [140, 180, 250, 400][root.speed_dial_index % 4] ? 1.0 :     //Prise en compte du cas où la vitesse est supérieure à la vitesse limite affichable
                            (root.speed_dial_index % 4) !== 3
                            ?       //cas des jauges 140/180/250 km/h
                            target_speed/([140, 180, 250][root.speed_dial_index % 4])
                            :       //cas de la jauge 400km/h
                            target_speed/300 - (target_speed > 200) * (target_speed - 200)/600)

        onPaint: {
            var ctx = target_speed_hook.getContext("2d")
            ctx.reset()

            //dessine
            ctx.arc(root.default_x * root.ratio, root.default_y * root.ratio,
                    (root.radius + 3 + 9 - 20) * root.ratio, target_angle * Math.PI / 180, (target_angle - root.hook_angle) * Math.PI / 180, true)
            ctx.lineTo((root.default_x + (root.radius + 3 + 9) * Math.cos((target_angle - root.hook_angle) * Math.PI / 180)) * root.ratio, (root.default_y + (root.radius + 3 + 9) * Math.sin((target_angle - root.hook_angle) * Math.PI / 180)) * root.ratio)
            ctx.arc(root.default_x * root.ratio, root.default_y * root.ratio,
                    (root.radius + 3 + 9) * root.ratio, (target_angle - root.hook_angle) * Math.PI / 180, target_angle * Math.PI / 180)
            ctx.lineTo((root.default_x + (root.radius + 3 + 9 - 20) * Math.cos(target_angle * Math.PI / 180)) * root.ratio, (root.default_y + (root.radius + 3 + 9 - 20) * Math.sin(target_angle * Math.PI / 180)) * root.ratio)
            ctx.closePath()
            ctx.fillStyle = root.medium_grey
            ctx.fill()
        }
    }
}