import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import "../../DMI_default/ETCS"


Window {
    id: window
    minimumWidth: 640
    minimumHeight: 480
    visible: true
    color: "#031122"
    title: qsTr("Driver Machine Interface")
    flags: Qt.FramelessWindowHint | Qt.Window | Qt.WindowStaysOnTopHint

    //stackview pour contenir les différentes zones du Driver Machine Interface (voir section 6.1.1.1)
    DMI_stackview{
        id: a
        objectName: "a"
    }

    DMI_stackview{
        id: b
        objectName: "b"
    }

    DMI_stackview{
        id: c
        objectName: "c"
    }

    DMI_stackview{
        id: d
        objectName: "d"
    }

    DMI_stackview{
        id: e
        objectName: "e"
    }

    DMI_stackview{
        id: f
        objectName: "f"
    }

    DMI_stackview{
        id: g
        objectName: "g"
    }
}
