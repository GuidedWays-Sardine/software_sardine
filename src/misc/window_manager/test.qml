import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    id: window
    color: "#031122"
    title: "test_window"

    //Flags pour au choix laisser la fenêtre avec ou sans titlebar et  toujours au dessus
    //flags: Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint | Qt.CustomizeWindowHint | Qt.Dialog | Qt.WindowTitleHint
    flags: Qt.FramelessWindowHint | Qt.Window | Qt.WindowStaysOnTopHint
}