import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

import "../../../DMI_default/ETCS_3.6.0"


DMI_page {
    id: page_rb2
    objectName: "page_rb2"
    anchors.fill: parent

    background: Rectangle {
        color: "transparent"
    }

    DMI_valueinput {
        default_x: 100
        default_y: 100

        default_height: 40
        default_width: 120

        maximum_value: 100

        is_activable: false

    }
}