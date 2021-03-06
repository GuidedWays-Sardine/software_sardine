import QtQuick 2.15


//https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
//Comment créer un élément personalisé


Item {
    id: root

    //Propriétés liés à la position et à la taille de l'objet
    property int default_width: 280             //dimensions du bouton pour les dimensions minimales de la fenêtre (640*480)
    property int default_height: 300
    property int default_x: 0                   //position du bouton pour les dimensions minimales de la fenêtre (640*480)
    property int default_y: 0

    //permet à partir des valeurs de positions et dimensions par défauts de calculer la position et la taille peu importe la dimension de la fenêtre
    readonly property real ratio:  (parent.width >= 640 && parent.height >= 480) ? parent.width/640 * (parent.width/640 < parent.height/480) + parent.height/480 * (parent.width/640 >= parent.height/480) : 1  //parent.height et parent.width représentent la taille de la fenêtre
    width: default_width * root.ratio
    height: default_height * root.ratio
    x: default_x * root.ratio
    y: default_y * root.ratio

    //Propriétés liées à la vitesse maximale du speeddial
    property int max_speed: 400                 //vitesse maximale du matériel roulant (utile pour déduire le t ype de cadran)
    readonly property int speed_dial_index: (max_speed > 140) + (max_speed > 180) + (max_speed > 250)   //index correspondant à la vitesse maximal affichable (0:140/1:180/2:250/3:400)
                                            //Permet à partir de la vitesse max de savoir le type de speeddial à montrer

    // Propriétés liées au format du speeddial
    property double start_angle: 144            //angle de début
    readonly property int separation_count: [15, 19, 26, 61][speed_dial_index]  //nombre de divisions à mesurer
    readonly property double separation_angle: 2 * start_angle/(separation_count - 1) //angle entre chaque séparations
    property int default_line_width: 1          //largeur de chaque ligne
    property int default_radius : 125           //rayon maximal du speeddial
    property int default_short_line_length: 15  //longueur du trais court
    property int default_long_line_length: 25   //longueur du trais long
    property int font_size: 12                  //taille de la police de charactère

    //propriété lié à la visibilité du speeddial
    property bool is_visible: true
    visible: is_visible

    // Propriété contenant la liste de toutes les valeurs à afficher selon le type
    readonly property var speed_values: [[0, 20, 40, 60, 80, 100, 120, 140],
                                         [0, 20, 40, 60, 80, 100, 120, 140, 160, 180],
                                         [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240],
                                         [0, 50, 100, 150, 200, 300, 400]]


    //Couleurs (ne peuvent pas être modifiés mais permet une mise à jour facile si nécessaire)
    readonly property string white: "#FFFFFF"        //partie 5.2.1.3.3  Nr 1



    //tracé des marqueurs (petits et grands
    Repeater {
        anchors.fill: parent
        model: root.separation_count

        Item {
            id: markers


            x: root.width/2
            y: root.height/2
            height: root.default_line_width * root.ratio
            width: root.default_radius * root.ratio

            transformOrigin: Item.Left
            rotation: 270 - root.start_angle + index * root.separation_angle


            //Rectangle créant le marqueur
            Rectangle {
                id: marker


                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.right: parent.right

                antialiasing: true
                color: root.white
                width: root.ratio * (root.speed_dial_index !== 3
                                     ?         //cas des jauges 140/180/250 km/h
                                     (index % 2 == 1 ? root.default_short_line_length : root.default_long_line_length)
                                     :         //cas de la jauge 400 km/h
                                     (index % 10 == 0 || (index % 10 === 5 && index >= 40) ? root.default_long_line_length : root.default_short_line_length * !(index <= 40 && index % 2 == 1)))
            }
        }
    }


    // Ci-dessous les marqueurs avec le texte
    Repeater {
        model: root.speed_values[root.speed_dial_index].length

        Item {
            //propriétés
            property int angleDepart: 270-144 // angle de départ avec origine axe des x
            property int differenceAngle: 144*2/6 // angle entre chaque élements

            id: speeds

            x: root.width/2
            y: root.height/2
            height: root.default_line_width * root.ratio
            width: root.default_radius * root.ratio

            transformOrigin: Item.Left                  //cas général             cas (pour le 250km/h) où la dernière graduation n'a pas de valeurs
            rotation: 270 - root.start_angle + index * (((2 * root.start_angle) - root.separation_angle * (root.speed_dial_index === 2))/(root.speed_values[root.speed_dial_index].length - 1))


            //Permet de connaitre la taille du texte afin de pouvoir placer une MouseArea dessus pour pouvoir sélectioner l'option en cliquant sur le text
            TextMetrics {
                id: speed_metrics

                readonly property double w: speed_metrics.tightBoundingRect.width
                readonly property double h: speed_metrics.tightBoundingRect.height
                readonly property double offset: (Math.tan(Math.PI / 2 + 2 * Math.PI * speeds.rotation / 360) < w/h && Math.tan(Math.PI / 2 + 2 * Math.PI * speeds.rotation / 360) > -w/h)
                                                 ?
                                                 Math.sqrt(h*h + w*w)/2 - Math.sqrt(h*h + h*h * Math.tan(2 * Math.PI * (90 + speeds.rotation) / 360) * Math.tan(2 * Math.PI * (90 + speeds.rotation) / 360))/2
                                                 :
                                                 Math.sqrt(h*h + w*w)/2 - Math.sqrt(w*w + w*w * Math.tan(2 * Math.PI * speeds.rotation / 360.0) * Math.tan(2 * Math.PI * speeds.rotation / 360.0))/2

                font: speed.font
                text: speed.text
            }

            //Texte contenant la valeur de la vitesse
            Text {
                id: speed

                anchors.verticalCenter: parent.verticalCenter
                anchors.right: parent.right
                anchors.rightMargin: (root.default_long_line_length + 2) * root.ratio - speed_metrics.offset


                text: root.speed_values[root.speed_dial_index][index]
                font.pointSize: (root.font_size - 2) * root.ratio
                font.family: "Verdana"
                font.weight: Font.DemiBold
                color: root.white
                rotation: - speeds.rotation //pour annuler la rotation du texte
            }
        }
    }
}
