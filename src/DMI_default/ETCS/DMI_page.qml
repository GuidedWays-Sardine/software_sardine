import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15


Pane {
    id: root

    //anchors.fill: parent

    //Définit les bordures à 0
    topPadding: 0
    rightPadding: 0
    bottomPadding: 0
    leftPadding: 0

    background: Rectangle {
        color: "transparent"
    }

    // Rajoute une MouseArea pour que les widget perdent le focus quand un endroit quelconque est selectioné (surtout pour les DMI_valueinput)
    MouseArea {
        anchors.fill: parent
        onClicked: forceActiveFocus()
    }
}