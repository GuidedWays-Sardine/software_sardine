import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.3
import QtQml 2.15


// https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
// Comment créer un élément personalisé

// https://doc.qt.io/qt-5/qtquickcontrols2-customize.html#customizing-button
// Comment personaliser un bouton

Item {
    id: root

    // Propriétés liées à la position et à la taille du bouton
    property double default_x: 30             // Position du INI_railcarview pour les dimensions minimales de la fenêtre (w_min*h_min)
    property double default_y: 0
    property double default_width: 580        // Dimensions du INI_railcar_view pour les dimensions minimales de la fenêtre (w_min*h_min)
    property double default_height: 132
    anchors.fill: parent

    // Calcule la taille et position réelle du composant à partir des dimensions de la fenêtre (parent) et de la taille minimale de celle-ci
    readonly property int w_min: 640
    readonly property int h_min: 480
    readonly property real ratio:  (parent.width >= w_min && parent.height >= h_min) ? parent.width/w_min * (parent.width/w_min < parent.height/h_min) + parent.height/h_min * (parent.width/w_min >= parent.height/h_min) : 1
    // Si le ratio n'est pas le même que celui de la fenêtre en taille minimale, décalle les composants pour qu'ils restent centrés
    readonly property double x_offset: (parent.width/parent.height > w_min/h_min) && (parent.width >= w_min && parent.height >= h_min) ? (parent.width - w_min * root.ratio) / 2 : 0
    readonly property double y_offset: (parent.width/parent.height < w_min/h_min) && (parent.width >= w_min && parent.height >= h_min) ? (parent.height - h_min * root.ratio) / 2 : 0

    // Propriétés liées à l'état du INI_railcarview
    property bool is_positive: false          // Si le visualiseur doit-être visible en couche positive (sinon négatif)
    property bool is_visible: true            // Si le visualiseur est visible
    visible: root.is_visible
    onIs_visibleChanged: { if (root.is_visible) { root.view_changed() } }

    // Propriétés nécessaires à la configuration de la voiture centrale
    property string central_railcar_mission: ""
    property string central_railcar_position: "middle"
    property bool central_railcar_left_bogie_axles_count: 0
    onCentral_railcar_left_bogie_axles_countChanged: { if (root.central_railcar_left_bogie_axles_count <= 0) { root.central_railcar_left_bogie_jacob = false } }
    property bool central_railcar_left_bogie_jacob: false
    property int central_railcar_central_bogies_count: 0
    onCentral_railcar_central_bogies_countChanged: { if (central_railcar_central_bogies_count % 2 != 1) { root.central_railcar_central_bogie_axles_count = 0 } }
    property int central_railcar_central_bogie_axles_count: 0
    property bool central_railcar_right_bogie_axles_count: 0
    onCentral_railcar_right_bogie_axles_countChanged: { if (root.central_railcar_left_bogie_axles_count <= 0) { root.central_railcar_left_bogie_jacob = false } }
    property bool central_railcar_right_bogie_jacob: false
    property int doors_count: 0
    property int levels_count: 0
    property int pantographs_count: 0
    property int thermics_count: 0

    // Propriétés nécessaires à la configuration de la voiture de gauche
    property bool left_railcar: false
    property string left_railcar_mission: ""
    property string left_railcar_position: "middle"
    // On ne considère pas les portes et l'intérieur, trop loins pour être visibles
    readonly property bool left_railcar_bogie_jacob: root.central_railcar_left_bogie_jacob
    onLeft_railcar_bogie_jacobChanged: { if (root.left_railcar_bogie_jacob) { root.left_railcar_bogie_axles_count = 0 } }
    property int left_railcar_bogie_axles_count: 0

    // Propriétés nécessaires à la configuration de la voiture de droite
    property bool right_railcar: false
    property string right_railcar_mission: ""
    property string right_railcar_position: "middle"
    // On ne considère pas les portes et l'intérieur, trop loins pour être visibles
    readonly property bool right_railcar_bogie_jacob: root.central_railcar_right_bogie_jacob
    onRight_railcar_bogie_jacobChanged: { if (root.right_railcar_bogie_jacob) { root.right_railcar_bogie_axles_count = 0 } }
    property int right_railcar_bogie_axles_count: 0


    // Chemin d'accès vers les icones utiles pour le INI_button
    readonly property string symbols_path: "../assets/symbols/"
    readonly property string sounds_path: "../assets/sounds/"


    // Signaux à surchager en QML ou en Python
    signal view_changed()                   // Appelé lorsque un élément du railcarview change


    //INI_button de structure du composant
    INI_button {
        id: body

        default_x: root.default_x
        default_y: root.default_y
        default_width: root.default_width
        default_height: root.default_height

        is_activable: false
        is_positive: root.is_positive



        //Rectangle transparent permettant de correctement placer toutes les images
        Rectangle {
            id: anchor_point

            x: root.default_x * root.ratio
            y: root.default_y * root.ratio
            width: root.default_width * root.ratio
            height root.default_height * root.ratio

            // définit le rectangle comme transparent (utilisé uniquement pour correctement placer les images)
            border.width: 0
            border.color: "transparent"
            color: "transparent"
        }


        // voitures suivantes et précédentes
        // Image pour la voiture de gauche
        Image {
            id: left_railcar

            anchors.bottom: anchor_point.bottom
            anchors.left: anchor_point.left
            anchors.right: anchor_point.right

            source: root.symbols_path + "Railcar_view/" +               // Chemin d'accès de vers toutes les images
                    root.left_railcar_mission + "/left_railcar_" +      // Mission de la voiture de gauche et début du nom du fichier
                    root.left_railcar_position + "_" +                  // Position de la voiture de gauche dans le train
                    root.left_railcar_bogie_jacob ? "jacob_bogie.png" : // Cas où le bogie est jacobien fini le chemin correspondant
                    (["without_bogie.png", "with_axle.png", "with_bogie"][Math.min(Math.max(root.left_railcar_bogie_axles_count, 0), 2)])
                    // Sinon, charge selon le nombre d'essieux (0, 1 2+) (min_max pour rester dans les index correspondantts)


            // Visible si une voiture est envoyée et que son type est non vide
            visible: root.is_visible && (root.left_railcar && root.left_railcar_mission != "")


            onSourceChanged: { if(visible) { root.view_changed() } }
        }

        // Image pour la voiture de droite
        Image {
            id: right_railcar

            anchors.bottom: anchor_point.bottom
            anchors.left: anchor_point.left
            anchors.right: anchor_point.right

            source: root.symbols_path + "Railcar_view/" +                 // Chemin d'accès de vers toutes les images
                    root.right_railcar_mission + "/right_railcar_" +      // Mission de la voiture de droite et début du nom du fichier
                    root.right_railcar_position + "_" +                   // Position de la voiture de droite dans le train
                    root.right_railcar_bogie_jacob ? "jacob_bogie.png" :  // Cas où le bogie est jacobien fini le chemin correspondant
                    (["without_bogie.png", "with_axle.png", "with_bogie"][Math.min(Math.max(root.right_railcar_bogie_axles_count, 0), 2)])
                    // Sinon, charge selon le nombre d'essieux (0, 1 2+) (min_max pour rester dans les index correspondantts)


            // Visible si une voiture est envoyée et que son type est non vide
            visible: root.is_visible && (root.left_railcar && root.left_railcar_mission != "")


            onSourceChanged: { if(visible) { root.view_changed() } }
        }


        // Structure de la voiture centrale
        // Image pour la structure supérieure de la voiture centrale
        Image {
            id: central_railcar_top_structure

            anchors.bottom: anchor_point.bottom
            anchors.left: anchor_point.left
            anchors.right: anchor_point.right

            source: root.symbols_path + "Railcar_view/" +                 // Chemin d'accès vers toutes les images
                    root.central_railcar_mission + "/" +                  // Mission de la voiture centrale
                    root.central_railcar_position + "_top_structure.png"  // Position de la voiture dans le train et fin du fichier

            visible: root.is_visible && (root.central_railcar_mission != "")


            onSourceChanged: { if(visible) { root.view_changed() } }
        }

        // Image pour l'emplacement bogie gauche
        Image {
            id: central_railcar_left_bogie_structure

            anchors.bottom: anchor_point.bottom
            anchors.left: anchor_point.left
            anchors.right: anchor_point.right

            source: root.symbols_path + "Railcar_view/" +                 // Chemin d'accès vers toutes les images
                    root.central_railcar_mission + "/" +                  // Mission de la voiture centrale
                    root.central_railcar_left_bogie_jacob ? "jacob" :     // Cas où le bogie est jacobien, laisse une encoche sur le coin
                    (root.central_railcar_left_bogie_axles_count > 0 ? "classic" : "no") +
                    // Cas où le bogie n'est pas jacobien, vérifie s'il y en a un ou si ce côté de la rame est suspendue
                    "_left_bogie.png"                                     // Fini le chemin d'accès


            visible: root.is_visible && (root.central_railcar_mission != "")


            onSourceChanged: { if(visible) { root.view_changed() } }
        }

        // Image pour l'emplacement bogie gauche
        Image {
            id: central_railcar_central_bogie_structure

            anchors.bottom: anchor_point.bottom
            anchors.left: anchor_point.left
            anchors.right: anchor_point.right

            source: root.symbols_path + "Railcar_view/" +                 // Chemin d'accès vers toutes les images
                    root.central_railcar_mission + "/" +                  // Mission de la voiture centrale
                    root.central_railcar_central_bogies_count <= 1 ? ["no", "one"][Math.max(root.central_railcar_central_bogies_count, 0)] :
                    // Cas où le nombre de bogies centraux vaut 0 ou 1, accède directement au bon bogie par index
                    ["even", "odd"][root.central_railcar_central_bogies_count % 2] +
                    // Sinon accède aux bogies paires ou impaires selon le reste de la division par 2
                    "_central_bogie.png"                                  // Fini le chemin d'accès

            visible: root.is_visible && (root.central_railcar_mission != "")


            onSourceChanged: { if(visible) { root.view_changed() } }
        }

        // Image pour l'emplacement bogie droite
        Image {
            id: central_railcar_right_bogie_structure

            anchors.bottom: anchor_point.bottom
            anchors.left: anchor_point.left
            anchors.right: anchor_point.right

            source: root.symbols_path + "Railcar_view/" +                 // Chemin d'accès vers toutes les images
                    root.central_railcar_mission + "/" +                  // Mission de la voiture centrale
                    root.central_railcar_right_bogie_jacob ? "jacob" :    // Cas où le bogie est jacobien, laisse une encoche sur le coin
                    (root.central_railcar_right_bogie_axles_count > 0 ? "classic" : "no") +
                    // Cas où le bogie n'est pas jacobien, vérifie s'il y en a un ou si ce côté de la rame est suspendue
                    "_right_bogie.png"                                    // Fini le chemin d'accès


            visible: root.is_visible && (root.central_railcar_mission != "")


            onSourceChanged: { if(visible) { root.view_changed() } }
        }


        // Bogies de la voiture centrale
        // Image pour le bogie de gauche
        Image {
            id: central_railcar_left_bogie

            anchors.bottom: anchor_point.bottom
            anchors.left: anchor_point.left
            anchors.right: anchor_point.right

            source: root.symbols_path + "Railcar_view/" +                 // Chemin d'accès vers toutes les images
                    root.central_railcar_mission + "/front_" +            // Mission de la voiture centrale et début du nom du fichier
                    root.central_railcar_left_bogie_jacob ? "jacob_" : "classic_" +
                    // Définit si le bogie est classique ou articulé
                    ["one", "two", "three", "more"][Math.max(Math.min(root.central_railcar_left_bogie_axles_count, 4), 1) - 1] +
                    // Définit le nombre d'essieux sur le bogie
                    "_axles.png"                                          // Fini le chemin d'accès


            visible: root.is_visible && (root.central_railcar_mission != "" && root.central_railcar_left_bogie_axles_count > 0)


            onSourceChanged: { if(visible) { root.view_changed() } }
        }

        // Image pour le bogie centrale
        Image {
            id: central_railcar_central_bogie

            anchors.bottom: anchor_point.bottom
            anchors.left: anchor_point.left
            anchors.right: anchor_point.right

            source: root.symbols_path + "Railcar_view/" +                 // Chemin d'accès vers toutes les images
                    root.central_railcar_mission + "/front_" +            // Mission de la voiture centrale et début du nom du fichier
                    ["one", "two", "three", "more"][Math.max(Math.min(root.central_railcar_central_bogie_axles_count, 4), 1) - 1] +
                    // Définit le nombre d'essieux sur le bogie
                    "_axles.png"                                          // Fini le chemin d'accès


            visible: root.is_visible && (root.central_railcar_mission != "" && root.central_railcar_central_bogies_count > 0 && root.central_railcar_central_bogies_count % 2 == 1)


            onSourceChanged: { if(visible) { root.view_changed() } }
        }

        // Image pour le bogie de droite
        Image {
            id: central_railcar_right_bogie

            anchors.bottom: anchor_point.bottom
            anchors.left: anchor_point.left
            anchors.right: anchor_point.right

            source: root.symbols_path + "Railcar_view/" +                 // Chemin d'accès vers toutes les images
                    root.central_railcar_mission + "/front_" +            // Mission de la voiture centrale et début du nom du fichier
                    root.central_railcar_right_bogie_jacob ? "jacob_" : "classic_" +
                    // Définit si le bogie est classique ou articulé
                    ["one", "two", "three", "more"][Math.max(Math.min(root.central_railcar_right_bogie_axles_count, 4), 1) - 1] +
                    // Définit le nombre d'essieux sur le bogie
                    "_axles.png"                                          // Fini le chemin d'accès


            visible: root.is_visible && (root.central_railcar_mission != "" && root.central_railcar_right_bogie_axles_count > 0)


            onSourceChanged: { if(visible) { root.view_changed() } }
        }


        // Intérieur et portes
        // Portes
        Image {
            id: doors

            anchors.bottom: anchor_point.bottom
            anchors.left: anchor_point.left
            anchors.right: anchor_point.right

            source: root.symbols_path + "Railcar_view/" +                 // Chemin d'accès vers toutes les images
                    root.central_railcar_mission + "/" +                  // Mission de la voiture centrale
                    root.central_railcar_position + "_"                   // Position de la voiture dans le train
                    root.doors_count.toString() + "_doors.png"            // Indication du nombre de portes et fini le chemin du fichier


            visible: root.is_visible && (root.central_railcar_mission != "" && root.doors_count > 0)


            onSourceChanged: { if(visible) { root.view_changed() } }
        }

        // Intérieur
        Image {
            id: interior

            anchors.bottom: anchor_point.bottom
            anchors.left: anchor_point.left
            anchors.right: anchor_point.right

            source: root.symbols_path + "Railcar_view/" +                 // Chemin d'accès vers toutes les images
                    root.central_railcar_mission + "/" +                  // Mission de la voiture centrale
                    root.central_railcar_position + "_"                   // Position de la voiture dans le train
                    root.doors_count.toString() + "_doors_" +             // Indication du nombre de portes
                    root.levels_count.toString() + "_levels.png"          // Indication du nombre de niveaux et fini le chemin du fichier


            visible: root.is_visible && (root.central_railcar_mission != "" && root.doors_count >= 0 && root.levels_count >= 0)


            onSourceChanged: { if(visible) { root.view_changed() } }
        }


        // Systèmes d'alimentations électriques et combustibles
        // Pantographes
        Image {
            id: interior

            anchors.bottom: anchor_point.bottom
            anchors.left: anchor_point.left
            anchors.right: anchor_point.right

            source: root.symbols_path + "Railcar_view/" +                 // Chemin d'accès vers toutes les images
                    root.central_railcar_mission + "/" +                  // Mission de la voiture centrale
                    root.central_railcar_position + "_"                   // Position de la voiture dans le train
                    ["one", "two", "more"][Math.max(Math.min(root.pantographs_count, 3),1) - 1] +
                    // Indique le nombre de pantographes (1, 2 3+)
                    "_pantographs.png"                                    // Fini le chemin du fichier


            visible: root.is_visible && (root.central_railcar_mission != "" && root.pantographs_count > 0)


            onSourceChanged: { if(visible) { root.view_changed() } }
        }

        // Thermiques
        Image {
            id: interior

            anchors.bottom: anchor_point.bottom
            anchors.left: anchor_point.left
            anchors.right: anchor_point.right

            source: root.symbols_path + "Railcar_view/" +                 // Chemin d'accès vers toutes les images
                    root.central_railcar_mission + "/" +                  // Mission de la voiture centrale
                    root.central_railcar_position + "_thermic.png"        // Position de la voiture dans le train et fini le fichier


            visible: root.is_visible && (root.central_railcar_mission != "" && root.thermics_count > 0)


            onSourceChanged: { if(visible) { root.view_changed() } }
        }
    }
}