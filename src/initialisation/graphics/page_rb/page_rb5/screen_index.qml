import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

import "../../../../DMI_Default/ETCS_3.6.0"


Window {
    id: screen_window
    minimumWidth: 288
    minimumHeight: 162
    visible: true
    color: "#031122"
    flags: Qt.FramelessWindowHint | Qt.Window

    //Propriétés à définir lors de l'initialisation
    property int index: -1

    //Boutton inactivable contenant le numéro de la fenètre
     DMI_button{
        id: screen_index
        objectName: "screen_index"
        text: index

        fontSize: 128

        anchors.fill: parent

        isActivable: false
        isPositive: true
        isVisible: true
    }
}