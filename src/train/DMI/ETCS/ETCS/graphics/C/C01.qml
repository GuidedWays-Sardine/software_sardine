import QtQuick 2.15
import QtQuick.Controls 2.15
import "../../components"


Item {
    id: root
    objectName: "root"

    property bool emergency_brake: false
    property string ertms_level: ""

    ETCS_button {
        id: ertms_level_button
        objectName: "ertms_level_button"

        default_x: 0
        default_y: 15 + 300
        default_width: 54
        default_height: 50/2

        default_image: "Level/" + (root.ertms_level.toUpperCase() === "NTC" ? "LE_02" : (!isNaN(parseInt(root.ertms_level)) && root.ertms_level != "0" ? ("LE_0" + (parseInt(root.ertms_level) + 2).toString()) : "LE_01")) + ".bmp"

        is_activable: false
        is_positive: false
    }

    ETCS_button {
        id: emergency_brake_button
        objectName: "emergency_brake_button"

        default_x: 0
        default_y: 15 + 300 + 50/2
        default_width: 54
        default_height: 50/2

        default_image: emergency_brake ? "Status/ST_01.bmp" : ""

        is_activable: false
        is_positive: false
    }


}