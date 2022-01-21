import QtQuick 2.0
import QtQuick.Controls 2.15


//https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
//Comment créer un élément personalisé

//https://doc.qt.io/qt-5/qtquickcontrols2-customize.html#customizing-stackview
//Comment personaliser un stackview


Item {
    id: root


    //Propriétés liés à la position et à la taille du MouseArea permettant de récupérer le focus
    property double default_x: 0               //position du bouton pour les dimensions minimales de la fenêtre (640*480)
    property double default_y: 0
    property double default_width: 0           //dimensions du bouton pour les dimensions minimales de la fenêtre (640*480)
    property double default_height: 0
    anchors.fill: parent

    //permet à partir des valeurs de positions et dimensions par défauts de calculer la position et la taille peu importe la dimension de la fenêtre
    readonly property double ratio:  (parent.width >= 640 && parent.height >= 480) ? parent.width/640 * (parent.width/640 < parent.height/480) + parent.height/480 * (parent.width/640 >= parent.height/480) : 1  //parent.height et parent.width représentent la taille de la fenêtre


    //Fonction à appeler en python pour changer la page active
    function set_active_page(page){
        body.clear()
        body.push(page)
    }



    //MouseArea permettant de récupérer le focus lorsque le fond de l'application est cliqué (utile pour mettre à jour les valueinput)
    //La MouseArea doit rester avant le stackview au risque de rendre tous les composants inutilisables
    MouseArea{
        id: area

        x: root.default_x * root.ratio
        y: root.default_y * root.ratio
        width: root.default_width * root.ratio
        height: root.default_height * root.ratio

        hoverEnabled: false
        enabled: true


        //Signal permettant de faire perdre le focus au composant édité lorsque le fond est cliqué
        onPressed: {
            forceActiveFocus()
        }
    }

    //stackview permettant de rendre la série de composants insérée visible
    StackView {
        id: body

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