import QtQuick 2.15


//https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
//Comment créer un élément personalisé


Item {
    id: root

    //Propriétés liés à la position et à la taille de l'objet
    property int radius: 125                      //Rayon du DMI_speeddial
    property int default_x: 300                   //position du bouton pour les dimensions minimales de la fenêtre (640*480)
    property int default_y: 300
    anchors.fill: parent

    //permet à partir des valeurs de positions et dimensions par défauts de calculer la position et la taille peu importe la dimension de la fenêtre
    readonly property real ratio:  (parent.width >= 640 && parent.height >= 480) ? parent.width/640 * (parent.width/640 < parent.height/480) + parent.height/480 * (parent.width/640 >= parent.height/480) : 1  //parent.height et parent.width représentent la taille de la fenêtre
    onRatioChanged: {pointer.requestPaint()}

    //Propriétés liées à la vitesse maximale du speeddial
    property double speed: 0
    property int max_speed: 400                 //vitesse maximale du matériel roulant (utile pour déduire le type de cadran)
    readonly property int speed_dial_index: (max_speed > 140) + (max_speed > 180) + (max_speed > 250)


    // Propriétés liées au format du speeddial
    property double start_angle: 144            //angle de début
    property int font_size: 18

    //propriétés pour la couleur du pointeur
    property double permitted_speed: 0
    onPermitted_speedChanged: {pointer.requestPaint()}
    property double target_speed: -1
    onTarget_speedChanged: {pointer.requestPaint()}
    property double release_speed: 0
    onRelease_speedChanged: {pointer.requestPaint()}
    property string operating_mode: "FS"
    onOperating_modeChanged: {pointer.requestPaint()}
    property string speed_monitoring:  "CSM"
    onSpeed_monitoringChanged: {pointer.requestPaint()}
    property string status_information: "NoS"
    onStatus_informationChanged: {pointer.requestPaint()}


    //Couleurs (ne peuvent pas être modifiés mais permet une mise à jour facile si nécessaire)
    readonly property string grey: "#C3C3C3"        //partie 5.2.1.3.3  Nr 3
    readonly property string red: "#BF0003"         //partie 5.2.1.3.3  Nr 10
    readonly property string orange: "#EA9109"      //partie 5.2.1.3.3  Nr 9
    readonly property string yellow: "#DFDF00"      //partie 5.2.1.3.3  Nr 8
    readonly property string black: "#000000"       //partie 5.2.1.3.3  Nr 2
    readonly property string white: "#FFFFFF"       //partie 4.2.1.3.3  Nr 1


    Canvas {
        id:pointer

        transformOrigin: Item.center

        transform: Rotation {
            origin.x: default_x * root.ratio
            origin.y: default_y * root.ratio
            angle: 90 - root.start_angle + 2 * root.start_angle *
                   (root.speed >= [140, 180, 250, 400][root.speed_dial_index % 4] ? 1.0 :     //Prise en compte du cas où la vitesse est supérieure à la vitesse limite affichable
                        (root.speed_dial_index % 4) !== 3
                        ?       //cas des jauges 140/180/250 km/h
                        root.speed/([140, 180, 250][root.speed_dial_index % 4])
                        :       //cas de la jauge 400km/h
                        root.speed/300 - (root.speed > 200) * (root.speed - 200)/600)
        }

        anchors.fill: parent

        onPaint: {
            console.log("paint")
            var ctx = pointer.getContext("2d")
            ctx.reset()

            //Le centre sera en 0, 0 pour simplifier le placement du speedpointer
            ctx.moveTo(root.default_x * root.ratio, root.default_y * root.ratio)
            ctx.arc(root.default_x * root.ratio, root.default_y * root.ratio, 25 * root.ratio, Math.PI + Math.asin(4.5/25), Math.PI - Math.asin(4.5/25))
            ctx.lineTo((root.default_x - root.radius + 43) * root.ratio, (root.default_y + 4.5) * root.ratio)
            ctx.lineTo((root.default_x - root.radius + 35) * root.ratio, (root.default_y + 1.5) * root.ratio)
            ctx.lineTo((root.default_x - root.radius + 20) * root.ratio, (root.default_y + 1.5) * root.ratio)
            ctx.lineTo((root.default_x - root.radius + 20) * root.ratio, (root.default_y - 1.5) * root.ratio)
            ctx.lineTo((root.default_x - root.radius + 35) * root.ratio, (root.default_y - 1.5) * root.ratio)
            ctx.lineTo((root.default_x - root.radius + 43) * root.ratio, (root.default_y - 4.5) * root.ratio)
            ctx.lineTo((root.default_x) * root.ratio, (root.default_y - 4.5) * root.ratio)

            ctx.closePath()
            switch(root.status_information.toUpperCase()){
                case "INTS":
                    if(root.speed >= root.permitted_speed){
                        ctx.fillStyle = root.red
                    }
                    else if (root.speed < root.permitted_speed && root.speed >= root.target_speed) {
                        ctx.fillStyle = root.yellow
                    }
                    else {
                        ctx.fillStyle = root.grey
                    }
                    break
                case "WAS":
                    ctx.fillStyle = root.orange
                    break
                case "OVS":
                    ctx.fillStyle = root.yellow
                    break
                case "INDS":
                    if(root.speed < root.release_speed || (root.operating_mode.toUpperCase() !== "LS" && root.speed <= root.permitted_speed && root.speed >= root.target_speed)) {
                        ctx.fillStyle = root.yellow
                    }
                    else {
                        ctx.fillStyle = root.grey
                    }
                    break
                case "NOS":
                    if(root.target_speed >= 0 && root.speed >= root.target_speed && root.speed <= root.permitted_speed) {
                        ctx.fillStyle = root.white
                    }
                    else if(root.target_speed >= 0 && root.speed > root.permitted_speed) {
                        ctx.fillStyle = root.red
                    }
                    else {
                        ctx.fillStyle = root.grey
                    }
                    break
                default:
                    ctx.fillStyle = root.grey
            }
            ctx.fill()
        }
    }

    //textes indiquant la vitesse (divisé en 3 éléments
    Text {
        id: units_digit

        x: (root.default_x + 6) * root.ratio
        y: (root.default_y - root.font_size * 0.5 - 2) * root.ratio

        text: Math.round(root.speed) % 10
        color: (root.status_information.toUpperCase() === "INTS" ||
                root.operating_mode.toUpperCase() == "TR" ||
                root.status_information.toUpperCase() === "ALLS" && root.speed > root.permitted_speed)
                ? root.white : root.black
        font.pixelSize: root.font_size * root.ratio
        font.family: "Verdana"
        font.bold: true
    }

    Text {
        id: tens_digit

        x: (root.default_x - 6) * root.ratio
        y: (root.default_y - root.font_size * 0.5 - 2) * root.ratio

        //Rien ne sera montré si la valeur arrondis n'est pas d'au moins 10
        text: Math.round(root.speed) >= 10 ? ((root.speed - root.speed % 10) % 100)/10 : ""
        color: (root.status_information.toUpperCase() === "INTS" ||
                root.operating_mode.toUpperCase() == "TR" ||
                root.status_information.toUpperCase() === "ALLS" && root.speed > root.permitted_speed)
                ? root.white : root.black
        font.pixelSize: root.font_size * root.ratio
        font.family: "Verdana"
        font.bold: true
    }

    Text {
        id: hundreds_digit

        x: (root.default_x - 18) * root.ratio
        y: (root.default_y - root.font_size * 0.5 - 2) * root.ratio

        //Rien ne sera montré si la valeur arrondis n'est pas d'au moins 100
        text: Math.round(root.speed) >= 100 ? ((root.speed - root.speed % 100) % 1000)/100 : ""
        color: (root.status_information.toUpperCase() === "INTS" ||
                root.operating_mode.toUpperCase() == "TR" ||
                root.status_information.toUpperCase() === "ALLS" && root.speed > root.permitted_speed)
                ? root.white : root.black
        font.pixelSize: root.font_size * root.ratio
        font.family: "Verdana"
        font.bold: true
    }
}