import QtQuick 2.0
import QtQuick.Controls 2.15
import "../../../../DMI_default/ETCS"


Item {
    id: root
    objectName: "root"


    //Bouton délimitant le conrtour de la zone
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
        id: speeddial
        objectName: "speeddial"

        max_speed: 170

        default_x: 54
        default_y: 15

    }


}
