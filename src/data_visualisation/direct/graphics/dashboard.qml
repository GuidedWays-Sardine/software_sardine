import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

import "components"
import "charts"

Window {
    id: window
    minimumWidth: 1280
    minimumHeight: 720
    visible: true
    color: "#F5F5F5"
    title: "Dashboard graphiques en direct"

    /*
    //Signal utilisé pour détecter quand le fenêtre est fermée et quitter l'application
    signal closed()

    onVisibilityChanged: {
        if(!window.visible) {
            closed()
        }
    }
    */
}
