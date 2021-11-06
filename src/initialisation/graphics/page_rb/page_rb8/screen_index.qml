import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

import "../../../components"


Window {
    id: screen_window

    minimumWidth: 288
    minimumHeight: 162
    visible: true
    color: "#031122"
    flags: Qt.FramelessWindowHint | Qt.Window | Qt.WindowStaysOnTopHint

    //Propriétés à définir lors de l'initialisation
    property int index: -1

    //Boutton inactivable contenant le numéro de la fenètre
     INI_button{
        id: screen_index
        objectName: "screen_index"

        anchors.fill: parent

        text: index
        font_size: 128

        is_activable: false
        is_positive: true
        is_visible: true
        is_dark_grey: false
    }
}