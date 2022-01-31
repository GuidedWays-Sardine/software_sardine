import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

import "../../../components"


Window {
    id: screen_index_window

    minimumWidth: 246
    minimumHeight: 143
    visible: false
    color: "#031122"
    flags: Qt.FramelessWindowHint | Qt.Window | Qt.WindowStaysOnTopHint

    //Propriétés à définir lors de l'initialisation
    property int index: -1


    //Signal permettant de faire clignoter les bordures à chaque fois que les popup apparaissent
    onVisibleChanged: {
        if(screen_index_window.visible) {
            screen_index.blink()
        }
    }


    //Boutton inactivable contenant le numéro de la fenètre
     INI_button{
        id: screen_index
        objectName: "screen_index"

        default_x: 0
        default_y: 0
        default_width: screen_index_window.width < 640 ? screen_index_window.width : 640        //Prise en compte des écrans aux résolutions pétés (8K)
        default_height: screen_index_window.height < 480 ? screen_index_window.height : 480

        text: index
        font_size: 128

        is_activable: false
        is_positive: true
        is_visible: true
        is_dark_grey: false
    }
}