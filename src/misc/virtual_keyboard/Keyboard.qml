import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.3
import QtQml 2.15
import QtQuick.Window 2.15


Window {
    id: root

    // Propriétés sur les dimensions du clavier virtuel
    x: 0
    y: 0
    width: 240   // Dimensions conseillées pour un NUMPAD -> changer manuellement selon le type de clavier et la taille disponible
    height: 300

    // Propriétés pour définir la fenêtre sans bordure et toujours au dessus de tout.
    flags: Qt.FramelessWindowHint | Qt.Window | Qt.WindowStaysOnTopHint | Qt.WindowDoesNotAcceptFocus
    color: keyboard_background_color


    // Propriétés sur le mode du clavier
    property var keyboard: []           // Numpad si vide
    property var skip_list: []          // Liste des touches à désactiver (par exemple pour les noms de fichiers)

    property bool is_caps: false        // Si le sous-clavier actif est celui des majuscules (valeurs supérieures, gauches)
    property bool is_altgr: false       // Si le sous-clavier actif est celui des valeurs tierces (valeurs inférieures, droites)
    // Seule l'une des propriétés peut-être activée en même temps. Si aucune ne l'est le sous_clavier normale est actif (valeurs inférieures gauches)

    // Couleurs nécessaires pour le clavier et ses touches
    readonly property string keyboard_background_color: "#000000"
    readonly property string key_background_default_color: "#333333"
    readonly property string key_background_hover_color: "#E5E5E5"
    readonly property string key_background_hold_color: "#0076D7"
    readonly property string key_text_inactive_color: "#838383"
    readonly property string key_text_active_color: "#FFFFFF"
    readonly property string key_text_inactive_hovered_color: "#838383"
    readonly property string key_text_active_hovered_color: "#000000"


    // Signal à surcharger en QML ou en Python
    signal key_clicked(var key)         // Appelé lorsqu'une touche est cliquée, envoie la touche (si non push_locked)
    signal key_pushed(var key)          // Appelé lorsqu'une touche spéciale () est cliquée, envoye la touche (si non push_locked)
    signal key_pressed(var key)         // Appelé lorsqu'une touche est cliquée et passe en mode pressé (si push_locked)
    signal key_released(var key)        // Appelé lorsqu'une touche est cliquée et sort du mode pressé (si push_locked)


    // Fonction permettant de redonner le focus à la fenêtre
    function give_focus() {
        root.requestActivate()
    }


    // Appelé lorsque le mode majuscule du clavier change
    onIs_capsChanged: {
        // Cas où le clavier passe en mode majuscules
        if (root.is_caps) {
            // Désactive le mode alt_gr (les deux modes ne sont pas compatibles ensemble)
            root.is_altgr = false
            bottom_repeater.itemAt(1).change_press_state(false)
        }
    }

    // Appelé lorsque le mode alt_gr du clavier change
    onIs_altgrChanged: {
        // Cas où le clavier passe en mode alt_gr
        if (root.is_altgr) {
            // Désactive le mode majuscules (les deux modes ne sont pas compatibles ensemble)
            root.is_caps = false
            bottom_repeater.itemAt(0).change_press_state(false)
        }
    }


    // Liste de toutes les touches envoyées par l'utilisateur (visible que si des touches sont envoyées)
    Repeater {      // Lignes
       id: row_repeater

       model: root.keyboard.length    // Nombre de lignes de touches (dépend du nombre de lignes envoyées)


       Repeater {   // Touches de chaque lignes
           id: column_repeater

           readonly property int row: index   // Permet de stocker le numéro de ligne actuelle

           model: root.keyboard.length > 0 ? root.keyboard[row].length : 0    // Nombre de touches sur chaque lignes


           KeyButton {
                id: keyboard_key

                readonly property int column: index   // Permet de stocker le numéro de touche de la ligne actuelle

                x: root.width / (root.keyboard[row].length + row % 2) * (column + 0.5 * (row % 2))
                y: root.height / (root.keyboard.length + 1) * row
                width: root.width / (root.keyboard[row].length + row % 2)
                height: root.height / (root.keyboard.length + 1)

                keys: root.keyboard[row][column]
                skip_list: root.skip_list

                is_caps: root.is_caps
                is_altgr: root.is_altgr
                is_pushbutton: true
                is_special_key: false

                background_default_color: root.key_background_default_color
                background_hover_color: root.key_background_hover_color
                background_hold_color: root.key_background_hold_color
                text_inactive_color: root.key_text_inactive_color
                text_active_color: root.key_text_active_color
                text_inactive_hovered_color: root.key_text_inactive_hovered_color
                text_active_hovered_color: root.key_text_active_hovered_color


                // Rappelle les signaux du clavier lorsque la touche est cliquée
                onClicked: { root.key_clicked(key) }
                onPressed: { root.key_pressed(key) }
                onReleased: { root.key_released(key) }
           }
       }
    }

    // Liste des touches pour la barre du bas ; format : [["valeur visible", "valeur envoyée", espace utilisé], ...
    readonly property var bottom_keys: [["⇧", "shiftleft", 2], ["Alt Gr", "altright", 2], [" ", " ", 5], ["←", "left", 1], ["→", "right", 1], ["⇐", "delete", 2]]

    // Repeater pour chacunes des touches ci-dessus
    Repeater {
        id: bottom_repeater

        model: root.keyboard.length > 0 ? root.bottom_keys.length : 0

        KeyButton {
            id: bottom_key

             readonly property int row: index   // Permet de stocker le numéro de touche de la ligne du bas

             x: root.width / 13 * [0, 2, 4, 9, 10, 11][row]
             y: root.height / (root.keyboard.length + 1) * root.keyboard.length
             width: root.width / 13 * root.bottom_keys[row][2]
             height: root.height / (root.keyboard.length + 1)

             keys: root.bottom_keys[row][0]
             skip_list: root.skip_list

             is_caps: root.is_caps
             is_altgr: root.is_altgr
             is_pushbutton: row >= 2        // Seul la touche maj et alt_gr sont en commutateur
             is_special_key: true

             background_default_color: root.key_background_default_color
             background_hover_color: root.key_background_hover_color
             background_hold_color: root.key_background_hold_color
             text_inactive_color: root.key_text_inactive_color
             text_active_color: root.key_text_active_color
             text_inactive_hovered_color: root.key_text_inactive_hovered_color
             text_active_hovered_color: root.key_text_active_hovered_color


             // Appelé lorsque la touche est cliquée, renvoie la valeur caché derrière la touche
             onPushed: { root.key_pushed(root.bottom_keys[row][1]) }

             // Appelé lorsqu'une touche de type commutateur passe en mode enfoncé (touche maj et alt gr)
             onPressed: {
                 // Cas où la touche est la touche maj, indique à toutes les touches de passer au sous-clavier majuscules
                 if (bottom_key.keys === root.bottom_keys[0][0]) {
                     root.is_caps = true
                 }
                 // Cas où la touche est la touche alt gr, indique à toutes les touches de passer au sous-clavier alt gr
                 else if (bottom_key.keys === root.bottom_keys[1][0]) {
                     root.is_altgr = true
                 }
             }

             // Appelé lorsqu'une touche de type commutateur passe en mode relaché (touche maj et alt gr)
             onReleased: {
                // Cas où la touche est la touche maj, indique à toutes les touches de repasser au sous-clavier classique
                 if (bottom_key.keys === root.bottom_keys[0][0]) {
                     root.is_caps = false
                 }
                 // Cas où la touche est la touch alt gr, indique à toutes les touches de repasser au sous-clavier classique
                 else if (bottom_key.keys === root.bottom_keys[1][0]) {
                     root.is_altgr = false
                 }
             }
         }
     }

    // Liste de toutes les touches contenues dans le numpad
    readonly property var numpad_keyboard: [["7", "8", "9"],
                                            ["4", "5", "6"],
                                            ["1", '2', "3"],
                                            ["-", "0", "."]]

   // Repeater pour chacunes des touches du numpad
    Repeater {
        id: numpad_row_repeater

        model: root.keyboard.length === 0 ? root.numpad_keyboard.length : 0


        Repeater {
            id: numpad_column_repeater

            readonly property int row: index     // Permet de stocket le numéro de la ligne actuelle

            model : root.numpad_keyboard[row].length


            KeyButton {
                 id: numpad_key

                 readonly property int column: index   // Permet de stocker le numéro de touche de la ligne actuelle

                 x: root.width / root.numpad_keyboard[row].length * column
                 y: root.height / root.numpad_keyboard.length * row
                 width: root.width / root.numpad_keyboard[row].length
                 height: root.height / root.numpad_keyboard.length

                 keys: root.numpad_keyboard[row][column]
                 skip_list: root.skip_list

                 is_pushbutton: true
                 is_special_key: false

                 background_default_color: root.key_background_default_color
                 background_hover_color: root.key_background_hover_color
                 background_hold_color: root.key_background_hold_color
                 text_inactive_color: root.key_text_inactive_color
                 text_active_color: root.key_text_active_color
                 text_inactive_hovered_color: root.key_text_inactive_hovered_color
                 text_active_hovered_color: root.key_text_active_hovered_color


                 // Rappelle les signaux du clavier lorsque la touche est cliquée
                 onClicked: { root.key_clicked(key) }
            }
        }
    }
}
