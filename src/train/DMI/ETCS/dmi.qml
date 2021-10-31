import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import "ETCS/components"


Window {
    id: window
    minimumWidth: 640
    minimumHeight: 480
    visible: true
    color: "#031122"
    title: "Driver Machine Interface"
    flags: Qt.FramelessWindowHint | Qt.Window | Qt.WindowStaysOnTopHint

    //stackview pour contenir les différentes zones du Driver Machine Interface (voir section 6.1.1.1)
    ETCS_stackview{
        id: a
        objectName: "a"
    }

    ETCS_stackview{
        id: b
        objectName: "b"
    }

    ETCS_stackview{
        id: c
        objectName: "c"
    }

    ETCS_stackview{
        id: d
        objectName: "d"
    }

    ETCS_stackview{
        id: e
        objectName: "e"
    }

    ETCS_stackview{
        id: f
        objectName: "f"
    }

    ETCS_stackview{
        id: g
        objectName: "g"
    }
}
