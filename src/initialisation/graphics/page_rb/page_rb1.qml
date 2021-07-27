import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

Pane {
    id: page_rb1
    objectName: "page_rb1"
    anchors.fill: parent

    background: Rectangle {
        color: "transparent"
    }


    Label {
        text: "Page 1"
        anchors.fill: parent
        horizontalAlignment: Label.AlignHCenter
        verticalAlignment: Label.AlignVCenter
        wrapMode: Label.Wrap
    }

}