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
    property double default_width: 580        // Dimensions du INI_railcarview pour les dimensions minimales de la fenêtre (w_min*h_min)
    property double default_height: 132
    anchors.fill: parent

    // Chemin d'accès vers les icones utiles pour les différentes images du INI_railcarview
    readonly property string symbols_path: "../assets/symbols/INI_railcarview/"

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

    // Propriétés sur la position de la voiture dans le train et comment celui-ci est visualisé dans le train_preview relié
    // Permet de charger les intérieurs full/empty selon celles montrés dans les vignettes
    readonly property var prime_list: [2, 3, 5, 7, 11, 13, 17]
    property int railcar_count: 1
    property int railcar_index: 0
    property int train_preview_visible_count: 10

    // Propriétés nécessaires à la configuration de la voiture actuellement paramétrée
    property string current_railcar_mission: ""                 // Informations générales
    property string current_railcar_position: "middle"

    property int current_railcar_front_bogie_axles_count: 0     // Bogie avant (à gauche)
    onCurrent_railcar_front_bogie_axles_countChanged: { if (root.current_railcar_front_bogie_axles_count <= 0) { root.current_railcar_front_bogie_jacob = false } }
    property bool current_railcar_front_bogie_jacob: false
    onCurrent_railcar_front_bogie_jacobChanged: { if (root.current_railcar_back_bogie_jacob) { root.previous_railcar_axles_count = 0 } }

    property int current_railcar_middle_bogies_count: 0         // Bogies centraux
    onCurrent_railcar_middle_bogies_countChanged: { if (current_railcar_middle_bogies_count % 2 != 1) { root.current_railcar_middle_bogie_axles_count = 0 } }
    property int current_railcar_middle_bogie_axles_count: 0

    property int current_railcar_back_bogie_axles_count: 0      // Bogie arrière (à droite)
    onCurrent_railcar_back_bogie_axles_countChanged: { if (root.current_railcar_front_bogie_axles_count <= 0) { root.current_railcar_front_bogie_jacob = false } }
    property bool current_railcar_back_bogie_jacob: false
    onCurrent_railcar_back_bogie_jacobChanged: { if (root.current_railcar_back_bogie_jacob) { root.next_railcar_axles_count = 0 } }

    property int doors_count: 0                                 // Autres informations sur la voiture actuelle
    property int levels_count: 0
    property int pantographs_count: 0
    property int thermics_count: 0

    // Propriétés nécessaires à la configuration de la voiture de gauche
    property string previous_railcar_mission: ""                // Informations générales
    property string previous_railcar_position: "middle"

    property int previous_railcar_axles_count: 0                // Informations sur le nombre de bogies de l'essieu arrière de la voiture précédente
    onPrevious_railcar_axles_countChanged: { if (root.current_railcar_front_bogie_jacob) { root.previous_railcar_axles_count = 0 } }
    // Les autres éléments ne sont pas visible (permet une simplification des images)

    // Propriétés nécessaires à la configuration de la voiture de droite
    property string next_railcar_mission: ""                    // Informations générales
    property string next_railcar_position: "middle"

    property int next_railcar_axles_count: 0
    onNext_railcar_axles_countChanged: { if (root.current_railcar_back_bogie_jacob) { root.next_railcar_axles_count = 0 } }
    // Les autres éléments ne sont pas visible (permet une simplification des images)


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

            x: root.x_offset + (root.default_x + 1 + root.is_positive) * root.ratio
            y: root.y_offset + (root.default_y + 1 + root.is_positive) * root.ratio
            width: (root.default_width - 2 - 2 * root.is_positive) * root.ratio
            height: (root.default_height - 2 - 2 * root.is_positive) * root.ratio

            // Définit le rectangle comme transparent (utilisé uniquement pour correctement placer les images)
            border.width: 0
            border.color: "transparent"
            color: "transparent"
        }


        // Images pour les attelages
        // Attelage entre la voiture précédente (à gauche) et actuelle (visible si la voiture paramétrée n'est pas la première)
        Image {
            id: previous_coupler

            anchors.bottom: anchor_point.bottom
            anchors.left: anchor_point.left
            anchors.right: anchor_point.right
            fillMode: Image.PreserveAspectFit

            source: root.symbols_path + "previous_coupler.png"

            visible: root.railcar_index != 0


            // Appelé lorsque l'icone est cachée ou montrée
            onVisibleChanged: root.view_changed()
        }

        // Attelage entre la voiture suivante (à droite) et actuelle (visible si la voiture paramétrée n'est pas la dernière)
        Image {
            id: next_coupler

            anchors.bottom: anchor_point.bottom
            anchors.left: anchor_point.left
            anchors.right: anchor_point.right
            fillMode: Image.PreserveAspectFit

            source: root.symbols_path + "next_coupler.png"

            visible: root.railcar_index < root.railcar_count - 1


            // Appelé lorsque l'icone est cachée ou montrée
            onVisibleChanged: root.view_changed()
        }


        // Voitures suivantes et précédentes
        // Image pour la voiture de gauche
        Image {
            id: previous_railcar

            anchors.bottom: anchor_point.bottom
            anchors.left: anchor_point.left
            anchors.right: anchor_point.right
            fillMode: Image.PreserveAspectFit

            source: root.symbols_path +                                             // Chemin vers les images
                    root.previous_railcar_mission + "/" +                           // Dossier selon la mission de la voiture précédente
                    "Previous_railcar/previous_railcar_" +                          // Dossier de la voiture précédente
                    root.previous_railcar_position + "_" +                          // Type de position de la voiture
                    root.current_railcar_front_bogie_jacob ? "jacob_bogie.png" :    // Indique si le bogie est articulé
                    (["no", "one", "two", "three", "more"][Math.min(root.previous_railcar_axles_count, 4)] + "_axles.png")
                    // Sinon indique le nombre d'essieux dans le bogie

            // Visible si une voiture est envoyée et que son type est non vide
            visible: root.is_visible && (root.previous_railcar_exist && root.previous_railcar_mission != "")


            // Appelé lorsque l'image visible change (même si l'image n'existe pas)
            onSourceChanged: { if(visible) { root.view_changed() } }

            // Appelé lorsque l'icone est cachée ou montrée
            onVisibleChanged: root.view_changed()
        }

        // Image pour la voiture de droite
        Image {
            id: next_railcar

            anchors.bottom: anchor_point.bottom
            anchors.left: anchor_point.left
            anchors.right: anchor_point.right
            fillMode: Image.PreserveAspectFit

            source: root.symbols_path +                                             // Chemin vers les images
                    root.next_railcar_mission + "/" +                               // Dossier selon la mission de la voiture suivante
                    "Next_railcar/next_railcar_" +                                  // Dossier de la voiture suivante
                    root.next_railcar_position + "_" +                              // Type de position de la voiture
                    root.current_railcar_back_bogie_jacob ? "jacob_bogie.png" :     // Indique si le bogie est articulé
                    (["no", "one", "two", "three", "more"][Math.min(root.previous_railcar_axles_count, 4)] + "_axles.png")
                    // Sinon indique le nombre d'essieux dans le bogie

            // Visible si une voiture est envoyée et que son type est non vide
            visible: root.is_visible && (root.current_railcar_back_bogie_jacob && root.next_railcar_mission != "")


            // Appelé lorsque l'image visible change (même si l'image n'existe pas)
            onSourceChanged: { if(visible) { root.view_changed() } }

            // Appelé lorsque l'icone est cachée ou montrée
            onVisibleChanged: root.view_changed()
        }


        // Structure de la voiture centrale
        // Image pour la structure supérieure de la voiture centrale
        Image {
            id: current_railcar_top_structure

            anchors.bottom: anchor_point.bottom
            anchors.left: anchor_point.left
            anchors.right: anchor_point.right
            fillMode: Image.PreserveAspectFit

            source: root.symbols_path +                                             // Chemin vers les images
                    root.current_railcar_mission + "/" +                            // Dossier selon la mission de la voiture centrale
                    "Frame/Top/" +                                                  // Dossier de la structure supérieure
                    root.current_railcar_position + "_top_structure.png"            // Position de la voiture dans le train et fin du fichier

            // Visible si une mission pour la voiture centrale a été envoyée
            visible: root.is_visible && (root.current_railcar_mission != "")


            // Appelé lorsque l'image visible change (même si l'image n'existe pas)
            onSourceChanged: { if(visible) { root.view_changed() } }

            // Appelé lorsque l'icone est cachée ou montrée
            onVisibleChanged: root.view_changed()
        }

        // Image pour l'emplacement bogie gauche
        Image {
            id: current_railcar_front_bogie_structure

            anchors.bottom: anchor_point.bottom
            anchors.left: anchor_point.left
            anchors.right: anchor_point.right
            fillMode: Image.PreserveAspectFit

            source: root.symbols_path +                                             // Chemin vers les images
                    root.current_railcar_mission +                                  // Dossier selon la mission de la voiture centrale
                    "/Frame/Front/front_" +                                         // Dossier de la structure inférieure avant (gauche)
                    (root.current_railcar_front_bogie_jacob ? "jacob" :             // Indique si le bogie est articulé
                    (root.current_railcar_front_bogie_axles_count > 0 ? "classic" : "no")) +
                    // Sinon indique si le bogie est classique où s'il n'existe pas
                    "_bogie.png"                                                    // Fin du fichier

            // Visible si une mission pour la voiture centrale a été envoyée
            visible: root.is_visible && (root.current_railcar_mission != "")

            // Appelé lorsque l'image visible change (même si l'image n'existe pas)
            onSourceChanged: { if(visible) { root.view_changed() } }

            // Appelé lorsque l'icone est cachée ou montrée
            onVisibleChanged: root.view_changed()
        }

        // Image pour l'emplacement bogie gauche
        Image {
            id: current_railcar_middle_bogie_structure

            anchors.bottom: anchor_point.bottom
            anchors.left: anchor_point.left
            anchors.right: anchor_point.right
            fillMode: Image.PreserveAspectFit

            source: root.symbols_path +                                             // Chemin vers les images
                    root.current_railcar_mission +                                  // Dossier selon la mission de la voiture centrale
                    "/Frame/Middle/middle_" +                                       // Dossier de la structure inférieure centrale
                    (root.current_railcar_middle_bogies_count <= 1 ? ["no", "one"][Math.max(root.current_railcar_middle_bogies_count, 0)] :
                    // Cas où le nombre de bogies centraux vaut 0 ou 1, accède directement au bon bogie par index
                    ["even", "odd"][root.current_railcar_middle_bogies_count % 2]) +
                    // Sinon accède aux bogies paires ou impaires selon le reste de la division par 2
                    "_bogie.png"                                                    // Fin du fichier

            visible: root.is_visible && (root.current_railcar_mission != "")


            // Appelé lorsque l'image visible change (même si l'image n'existe pas)
            onSourceChanged: { if(visible) { root.view_changed() } }

            // Appelé lorsque l'icone est cachée ou montrée
            onVisibleChanged: root.view_changed()
        }

        // Image pour l'emplacement bogie gauche
        Image {
            id: current_railcar_back_bogie_structure

            anchors.bottom: anchor_point.bottom
            anchors.left: anchor_point.left
            anchors.right: anchor_point.right
            fillMode: Image.PreserveAspectFit

            source: root.symbols_path +                                             // Chemin vers les images
                    root.current_railcar_mission +                                  // Dossier selon la mission de la voiture centrale
                    "/Frame/Back/back_" +                                           // Dossier de la structure inférieure arrière (droite)
                    (root.current_railcar_back_bogie_jacob ? "jacob" :              // Indique si le bogie est articulé
                    (root.current_railcar_back_bogie_axles_count > 0 ? "classic" : "no")) +
                    // Sinon indique si le bogie est classique où s'il n'existe pas
                    "_bogie.png"                                                    // Fin du fichier

            // Visible si une mission pour la voiture centrale a été envoyée
            visible: root.is_visible && (root.current_railcar_mission != "")


            // Appelé lorsque l'image visible change (même si l'image n'existe pas)
            onSourceChanged: { if(visible) { root.view_changed() } }

            // Appelé lorsque l'icone est cachée ou montrée
            onVisibleChanged: root.view_changed()
        }

        // Bogies de la voiture centrale
        // Image pour le bogie de gauche
        Image {
            id: current_railcar_front_bogie

            anchors.bottom: anchor_point.bottom
            anchors.left: anchor_point.left
            anchors.right: anchor_point.right
            fillMode: Image.PreserveAspectFit

            source: root.symbols_path +                                             // Chemin vers les images
                    (root.current_railcar_front_bogie_jacob ? root.previous_railcar_mission : root.current_railcar_mission) +
                    // Dossier selon la mission de la voiture centrale si bogie classic, sinon mission de la voiture précédente si articulé
                    // Cela permet une cohérence lors du paramétrage d'un bogie articulé entre deux voitures de missions différentes
                    "/Bogies/Front/front_" +                                        // Dossier du bogie avant (gauche)
                    (root.current_railcar_front_bogie_jacob ? "jacob_" : "classic_") +
                    // Définit si le bogie est classique ou articulé
                    ["one", "two", "three", "more"][Math.max(Math.min(root.current_railcar_front_bogie_axles_count, 4), 1) - 1] +
                    // Définit le nombre d'essieux sur le bogie
                    "_axles.png"                                                    // Fin du fichier

            // Visible si une mission pour la voiture centrale a été envoyée et qu'un bogie existe sur cet emplacement
            visible: root.is_visible && (root.current_railcar_mission != "" && root.current_railcar_front_bogie_axles_count > 0)


            // Appelé lorsque l'image visible change (même si l'image n'existe pas)
            onSourceChanged: { if(visible) { root.view_changed() } }

            // Appelé lorsque l'icone est cachée ou montrée
            onVisibleChanged: root.view_changed()
        }

        // Image pour le bogie centrale
        Image {
            id: current_railcar_middle_bogie

            anchors.bottom: anchor_point.bottom
            anchors.left: anchor_point.left
            anchors.right: anchor_point.right
            fillMode: Image.PreserveAspectFit

            source: root.symbols_path +                                             // Chemin d'accès vers toutes les images
                    root.current_railcar_mission +                                  // Dossier selon la mission de la voiture centrale
                    "/Bogies/Middle/middle_" +                                      // Dossier du bogie central
                    ["one", "two", "three", "more"][Math.max(Math.min(root.current_railcar_middle_bogie_axles_count, 4), 1) - 1] +
                    // Définit le nombre d'essieux sur le bogie
                    "_axles.png"                                                    // Fin du fichier

            // Visible si une mission valide a été fourni et que le nombre de bogies centraux est impaire
            visible: root.is_visible && (root.current_railcar_mission != "" && root.current_railcar_middle_bogies_count > 0 && root.current_railcar_middle_bogies_count % 2 == 1)


            // Appelé lorsque l'image visible change (même si l'image n'existe pas)
            onSourceChanged: { if(visible) { root.view_changed() } }

            // Appelé lorsque l'icone est cachée ou montrée
            onVisibleChanged: root.view_changed()
        }

        // Image pour le bogie de droite
        Image {
            id: current_railcar_back_bogie

            anchors.bottom: anchor_point.bottom
            anchors.left: anchor_point.left
            anchors.right: anchor_point.right
            fillMode: Image.PreserveAspectFit

            source: root.symbols_path +                                             // Chemin vers les images
                    root.current_railcar_mission +                                  // Dossier selon la mission de la voiture centrale
                    "/Bogies/Back/back_" +                                          // Dossier du bogie avant (gauche)
                    (root.current_railcar_back_bogie_jacob ? "jacob_" : "classic_") +
                    // Définit si le bogie est classique ou articulé
                    ["one", "two", "three", "more"][Math.max(Math.min(root.current_railcar_back_bogie_axles_count, 4), 1) - 1] +
                    // Définit le nombre d'essieux sur le bogie
                    "_axles.png"                                                    // Fin du fichier

            // Visible si une mission pour la voiture centrale a été envoyée et qu'un bogie existe sur cet emplacement
            visible: root.is_visible && (root.current_railcar_mission != "" && root.current_railcar_front_bogie_axles_count > 0)


            // Appelé lorsque l'image visible change (même si l'image n'existe pas)
            onSourceChanged: { if(visible) { root.view_changed() } }

            // Appelé lorsque l'icone est cachée ou montrée
            onVisibleChanged: root.view_changed()
        }


        // Intérieur et portes
        // Portes
        Image {
            id: doors

            anchors.bottom: anchor_point.bottom
            anchors.left: anchor_point.left
            anchors.right: anchor_point.right
            fillMode: Image.PreserveAspectFit

            source: root.symbols_path +                                         // Chemin vers les images
                    root.current_railcar_mission + "/" +                        // Dossier selon la mission de la voiture centrale
                    root.current_railcar_position + "_" +                       // Position de la voiture dans le train
                    root.doors_count.toString() + "_doors.png"                  // Indication du nombre de portes et fin du fichier

            // Visible si une mission pour la voiture centrale a été envoyée et que le nombre de porte est positif
            visible: root.is_visible && (root.current_railcar_mission != "" && root.doors_count > 0)


            // Appelé lorsque l'image visible change (même si l'image n'existe pas)
            onSourceChanged: { if(visible) { root.view_changed() } }

            // Appelé lorsque l'icone est cachée ou montrée
            onVisibleChanged: root.view_changed()
        }

        // Intérieur
        Image {
            id: interior

            anchors.bottom: anchor_point.bottom
            anchors.left: anchor_point.left
            anchors.right: anchor_point.right
            fillMode: Image.PreserveAspectFit

            source: root.symbols_path +                                             // Chemin vers les images
                    root.current_railcar_mission + "/" +                            // Dossier selon la mossion de la voiture centrale
                    root.current_railcar_position + "_" +                           // Position de la voiture dans le train
                    root.doors_count.toString() + "_doors_" +                       // Indication du nombre de portes
                    root.levels_count.toString() + "_levels.png"                    // Indication du nombre de niveaux et fin du fichier

            // Visible si une mission pour la voiture centrale a été envoyée et que le nombre de porte et de niveaux est positif
            visible: root.is_visible && (root.current_railcar_mission != "" && root.doors_count >= 0 && root.levels_count >= 0)


            // Appelé lorsque l'image visible change (même si l'image n'existe pas)
            onSourceChanged: { if(visible) { root.view_changed() } }

            // Appelé lorsque l'icone est cachée ou montrée
            onVisibleChanged: root.view_changed()
        }


        // Systèmes d'alimentations électriques et combustibles
        // Pantographes
        Image {
            id: pantograph

            anchors.bottom: anchor_point.bottom
            anchors.left: anchor_point.left
            anchors.right: anchor_point.right
            fillMode: Image.PreserveAspectFit

            source: root.symbols_path +                                             // Chemin vers les images
                    root.current_railcar_mission + "/" +                            // Dossier selon la mission de la voiture centrale
                    root.current_railcar_position + "_"                             // Position de la voiture dans le train
                    ["one", "two", "more"][Math.max(Math.min(root.pantographs_count, 3),1) - 1] +
                    // Indique le nombre de pantographes (1, 2, 3+)
                    "_pantographs.png"                                              // Fin du fichier

            // Visible si une mission pour la voiture centrale a été envoyée et que le nombre de pantographes est strictement positif
            visible: root.is_visible && (root.current_railcar_mission != "" && root.pantographs_count > 0)


            // Appelé lorsque l'image visible change (même si l'image n'existe pas)
            onSourceChanged: { if(visible) { root.view_changed() } }

            // Appelé lorsque l'icone est cachée ou montrée
            onVisibleChanged: root.view_changed()
        }

        // Thermiques
        Image {
            id: thermic

            anchors.bottom: anchor_point.bottom
            anchors.left: anchor_point.left
            anchors.right: anchor_point.right
            fillMode: Image.PreserveAspectFit

            source: root.symbols_path +                                                 // Chemin vers les images
                    root.current_railcar_mission + "/" +                                // Dossier selon la mission de la voiture centrale
                    root.current_railcar_position + "_thermic.png"                      // Position de la voiture dans le train et fin du fichier

            // Visible si une mission pour la voiture centrale a été envoyée et que le nombre de systèmes thermiques est positif
            visible: root.is_visible && (root.current_railcar_mission != "" && root.thermics_count > 0)


            // Appelé lorsque l'image visible change (même si l'image n'existe pas)
            onSourceChanged: { if(visible) { root.view_changed() } }

            // Appelé lorsque l'icone est cachée ou montrée
            onVisibleChanged: root.view_changed()
        }
    }
}
