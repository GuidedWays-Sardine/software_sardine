import QtQuick 2.0
import QtQuick.Controls 2.15


//https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
//Comment créer un élément personalisé

//https://doc.qt.io/qt-5/qtquickcontrols2-customize.html#customizing-stackview
//Comment personaliser un bouton

Item {
    id: root

    //fonction à appeler en python pour changer la page active
    function set_active_page(text){
        settings_pages.clear()
        settings_pages.push(text)
    }

    anchors.fill: parent

    //stackview permettant de superposer les différentes pages
    StackView {
        id: settings_pages
        objectName: "settings_pages"

        anchors.fill: parent

        //supression des différentes animations de transitions
        pushEnter: Transition {
            enabled: false
        }
        pushExit: Transition {
            enabled: false
        }
        popEnter: Transition {
            enabled: false
        }
        popExit: Transition {
            enabled: false
        }
    }
}