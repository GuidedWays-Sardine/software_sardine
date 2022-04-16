import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

Window {
    id: window
    //minimumWidth: 640
    //minimumHeight: 480
    color: "#031122"
    title: "Initialisation Sardine"

    //Flags permettant de laisser la fenêtre toujours au dessus et de laisser uniquement le bouton de fermeture
    //flags: Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint | Qt.CustomizeWindowHint | Qt.Dialog | Qt.WindowTitleHint
    flags: Qt.FramelessWindowHint | Qt.Window | Qt.WindowStaysOnTopHint
}