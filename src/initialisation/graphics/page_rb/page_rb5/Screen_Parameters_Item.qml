import QtQuick 2.15
import QtQuick.Controls 2.15

import "../../../../DMI_default/ETCS_3.6.0"

Item {
    id: root

    //Arguments supplémentaires
    property int defaultX: 15
    property int defaultY: 45
    property string screen_name: "t"
    property int fontSize: 12
    property var screenlist: ["Aucun", "1"]

    property bool isFullscreen: false


    visible: root.screen_name === "" ? false : true
    anchors.fill: parent
    readonly property real ratio:  (parent.width >= 640 && parent.height >= 480) ? parent.width/640 * (parent.width/640 < parent.height/480) + parent.height/480 * (parent.width/640 >= parent.height/480) : 1  //parent.height et parent.width représentent la taille de la fenêtre

    //contour de l'encadré des paramètres écrans
    DMI_button {
        id: body

        defaultWidth: 550
        defaultHeight: 44
        defaultX: root.defaultX
        defaultY: root.defaultY

        isActivable: false
        isPositive: false
    }

    //Texte indiquant l'utilité de l'écran
    Text{
        id: screen_name
        text: root.screen_name
        font.pixelSize: root.fontSize * root.ratio
        font.family: "Verdana"
        color: "#C3C3C3"
        anchors.left: body.left
        anchors.leftMargin: root.fontSize * root.ratio
        anchors.verticalCenter: body.verticalCenter
    }

    //Texte indiquant la combobox pour le numéro de l'écran
    Text{
        id: screen_index_text
        objectName: "screen_index_text"

        text: "Écran"
        font.pixelSize: root.fontSize * root.ratio
        font.family: "Verdana"
        color: "#C3C3C3"
        anchors.left: screen_index_combo.left
        anchors.leftMargin: 2 * root.ratio
        anchors.bottom: screen_index_combo.top
        anchors.topMargin: - 4 * root.ratio
    }

    DMI_combobox {
        id: screen_index_combo
        objectName: "screen_index_combo"

        defaultX: root.defaultX + 260
        defaultY: root.defaultY + 16
        defaultWidth: 100
        defaultHeight: 24
        elements: root.screenlist
        isPositive: false
    }

}