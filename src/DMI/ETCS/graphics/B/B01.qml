import QtQuick 2.15
import QtQuick.Controls 2.15
import "../../../../DMI_default/ETCS"


Item {
    id: root
    objectName: "root"


    //Propriétés lié à l'état de la jauge de vitesse
    property double max_speed: 200
    property double speed: 0

    //Propriétés liées au mode de conduite et aux vitesses permises (utile pour gérer les couleurs et différentes sections de la jauge)
    property double target_speed: 0
    property double release_speed: 0
    property double permitted_speed: 0
    property string operating_mode: "FS"
    property string speed_monitoring:  "CSM"
    property string status_information: "NoS"


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

        operating_mode: root.operating_mode
        speed_monitoring: root.speed_monitoring
        status_information: root.status_information

        max_speed: root.max_speed
        release_speed: root.release_speed
        target_speed: root.target_speed
        permitted_speed: root.permitted_speed
        speed: root.speed
    }
}
