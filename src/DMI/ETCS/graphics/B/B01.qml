import QtQuick 2.15
import QtQuick.Controls 2.15
import "../../../../DMI_default/ETCS"


Item {
    id: root
    objectName: "root"


    //Propriétés lié à l'état de la jauge de vitesse
    property int max_speed: 350
    property int speed: 0


    //Bouton délimitant le contour de la zone
    DMI_button {
        id: body

        default_x: 54
        default_y: 15
        default_width: 280
        default_height: 300

        is_positive: false
        is_activable: false
    }


    DMI_speeddial {
        id: dial
        objectName: "speeddial"

        max_speed: root.max_speed

        default_x: body.default_x
        default_y: body.default_y
    }

    DMI_speedpointer {
        id: pointer

        default_x: body.default_x + body.default_width * 0.5
        default_y: body.default_y + body.default_height * 0.5

        max_speed: root.max_speed
    }
}
