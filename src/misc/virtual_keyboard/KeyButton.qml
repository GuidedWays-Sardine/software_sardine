import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.3
import QtQml 2.15

Item {
    id: root

    // Propriétés liées à la taille
    x: 0
    y: 0
    width: 0
    height: 0

    // Propriétés sur les touches et touches à ne pas considérer
    property string keys: ""
    property var skip_list: []

    // Propriétés sur le mode de la touche
    property bool is_multikey: true     // Indique si chacune des lettre de keys représentent une valeur (normal, caps et altgr) ou si c'est une unique touche
    property bool is_pushbutton: true   // Indique si la touche est un bouton poussoir (s'il est enclenché que si appuyé) ou de type  commutateur (rest enfoncé quand appuyé et se relache quand appuyé de nouveau)
    // Une touche ne peut pas être multikey et un commutateur (pas un bouton poussoir)
    property bool is_caps: false        // Indique si la touche active est celle des majuscules (valeur supérieure, gauche)
    property bool is_altgr: false       // Indique si la touche active est celle des valeurs tierces (valeur inférieure, droite)
    // Seule l'une des propriétés peut-être activée en même temps. Si aucune ne l'est la touche normale est active (valeur inférieure gauche)

    // Couleurs de la touche
    property string background_default_color: "#333333"
    property string background_hover_color: "#E5E5E5"
    property string background_hold_color: "#0076D7"
    property string text_inactive_color: "#838383"
    property string text_active_color: "#FFFFFF"
    property string text_inactive_hovered_color: "#838383"
    property string text_active_hovered_color: "#000000"


    // Signal à surcharger en QML ou en Python
    signal clicked(var key)         // Appelé lorsque la touche est cliqué, envoie la touche (si non push_locked)
    signal pressed(var key)         // Appelé lorsque la touche est cliqué et passe en mode pressé (si push_locked)
    signal released(var key)        // Appelé lorsque la touche est cliqué et sort du mode pressé (si push_locked)


    // Fonctions permettant de changer l'état d'appui d'un commutateur
    function change_press_state(new_state) {
        // Cas où la touche est de type bouton poussoir
        if (!root.is_pushbutton) {
            // Cas où l'état actuel de la touche est différent de l'état envoyé et que la touche est actuellement appuyé
            if (new_state !== body.is_pressed && body.is_pressed) {
                // Change l'état de la touche et appelle le signal released
                body.is_pressed = false
                root.released(root.keys)
            }
            // Cas où l'état actuel de la touche est différent de l'état envoyé et que la touche est actuellement relaché
            else if (new_state !== body.is_pressed && ! body.is_pressed) {
                body.is_pressed = true
                root.pressed(root.keys)
            }
        }
        // Cas où la touche est de type commutateur
        else {
            // Laisse un message de Logging
            console.log(`Impossible de changer l'état du bouton pour un bouton poussoir (clés : ${root.keys})`)
        }
    }


    // Appelé lorsque la liste de touche est changée
    onKeysChanged: {
        // Cas où la touche était pressée, la relache
        if (!root.is_pushbutton && body.is_pressed) {
            body.is_pressed = false
        }
    }

    // Appelé lorsque la touche change son mode (clé multiple ou unique)
    onIs_multikeyChanged: {
        // Cas où le mode multiclé est passé alors que la touche est de type commutateur (incompatible), repasse en mode bouton poussoir
        if (root.is_multikey && !root.is_pushbutton) {
            root.is_pushbutton = true
            console.log(`Une touche ne peut pas être commutateur et multi-valeurs (touche : \"${root.keys}\").`)
        }
    }

    // Appelé lorsque la touche change de type (commutateur ou bouton poussoir)
    onIs_pushbuttonChanged: {
        // Cas où la touche est passé en mode boutton poussoir alors qu'elle était encore pressé
        if (root.is_pushbutton && body.is_pressed) {
            // Relache la touche et appelle le signal
            body.is_pressed = false
            root.released(root.keys)
        }
        // Cas où la touche passe en mode commutateur
        else if (!root.is_pushbutton) {
            // Définit le mode de la touche comme clé simple (désactive le mode multi-clé)
            root.is_multikey = false
        }
    }



    // Bouton de structure de la touche
    Button {
          id: body

          // Propriétés pour indiquer si la touche est appuyée (La touche est appuyé si l'utilisateur a initié une pression et que la souris reste sur la zone)
          property bool is_clicked: false
          property bool is_pressed: false

          anchors.fill: parent
          anchors.margins: Math.min(root.width, root.height) * 0.02

          enabled: root.is_multikey
                   ?     // Cas du mode multi-clé activée, la touche est active si la sous-clé active de celle-ci existe et n'est pas dans la liste des touches interdites
                    (root.keys.length > (1 * root.is_caps + 2 * root.is_altgr) && !root.skip_list.includes(root.keys[Math.min(1 * root.is_caps + 2 * root.is_altgr, root.keys.length - 1)]))
                   :     // Cas où le multi-touches n'est pas activé, active la touche si un texte a été envoyé
                    (root.keys.length > 0 && !root.skip_list.includes(root.keys))
          hoverEnabled: body.enabled
          focusPolicy: Qt.NoFocus


          // Appelé lorsque la touche commence à être appuyée
          onPressed: {
              // Indique que la touche est cliquée (et que le curseur se trouve sur celle-ci)
              body.is_clicked = true

              // Cas où la touche est en mode commutateur
              if (!root.is_pushbutton) {
                  // Inverse si la touche est pressée ou non
                  body.is_pressed = !body.is_pressed

                  // Cas où la touche est passée en mode pressée, appelle le signal de passage en mode pressé
                  if (body.is_pressed) {
                      root.pressed(root.keys)
                  }
                  // Cas où la touche est passée en mode pressée, appelle le signal de passage en mode relaché
                  else {
                      root.released(root.keys)
                  }
              }
              // Cas où la touche est de type poussoir, appelle le signal de clique en envoyant la sous-touche correspondante
              else {
                  root.clicked(root.keys[Math.min(1 * root.is_caps + 2 * root.is_altgr, root.keys.length - 1)])
              }
          }

          // Appelés lorsque la touche est relaché (sur la zone cliquable ou non). Permet de rechanger les couleurs des bordures et du texte
          onReleased: { body.is_clicked = false }
          onCanceled: { body.is_clicked = false }



          // Rectangle pour le fond de la touche
          background: Rectangle {
              color: (body.is_clicked && body.hovered) || body.is_pressed
                     ?      // Cas où la touche est cliquée et que le curseur se trouve sur la zone, utilise la couleur d'appui
                      root.background_hold_color
                     : (body.hovered || (body.is_clicked && !body.hovered)
                       ?    // Cas où la touche est survolée, ou qu'elle est cliquée mais le curseur ne se trouve pas dans la zone, utilise la couleur de survol
                        root.background_hover_color
                       :    // Cas où la touche n'est ni cliquée, ni survolée, utilise la couleur par défaut
                        root.background_default_color)

              radius: Math.min(root.width, root.height) * 0.05
          }


          // Liste des textes pour les différentes positions
          // Texte pour la lettre par défaut (bas, gauche) lorsque la touche est ni en mode majuscule ni en mode alt_gr (bouton poussoir)
          // Ou zone où le texte sera affiché (bouton commutateur)
          Text {
              id: default_key

              anchors.bottom: body.bottom
              anchors.bottomMargin: root.is_multikey ? root.height * 0.04 : (root.height - default_key.font.pixelSize) / 2.2    // En bas à droite si mode multi_key sinon centré
              anchors.left: body.left
              anchors.leftMargin: root.height * 0.1

              font.pixelSize: root.height * 0.36

              text: root.is_multikey ? (root.keys.length >= 1 ? root.keys[0] : "") :   // Cas de touche de type bouton poussoir, affiche la première lettre
                                       root.keys

              color: (root.is_caps || root.is_altgr || !body.enabled)
                     ?   // Cas où la touche ne peut pas être activé (mauvais sous clavier, touche interdite) + couleur du texte selon la couleur du fond
                         (((body.hovered && !body.is_clicked) || (body.is_clicked && !body.hovered)) ? root.text_inactive_hovered_color : root.text_inactive_color)
                     :   // Cas où la touche peut être activée (bon clavier et touche non interdite) + couleur du texte selon la couleur du fond
                         (((body.hovered && !body.is_clicked) || (body.is_clicked && !body.hovered)) ? root.text_active_hovered_color : root.text_active_color)
          }

          // Texte pour la lettre supérieure
          Text {
              id: caps_key

              anchors.top: body.top
              anchors.topMargin: root.height * 0.04
              anchors.left: body.left
              anchors.leftMargin: root.height * 0.1

              font.pixelSize: root.height * 0.36

              text: root.is_multikey && root.keys.length >= 2 ? root.keys[1] : ""  // Affiche le texte si lla touche est de type bouton poussoir et qu'il y a au moins deux lettres

              color: (!root.is_caps || root.is_altgr || !body.enabled)
                     ?   // Cas où la touche ne peut pas être activé (mauvais sous clavier, touche interdite) + couleur du texte selon la couleur du fond
                         (((body.hovered && !body.is_clicked) || (body.is_clicked && !body.hovered)) ? root.text_inactive_hovered_color : root.text_inactive_color)
                     :   // Cas où la touche peut être activée (bon clavier et touche non interdite) + couleur du texte selon la couleur du fond
                         (((body.hovered && !body.is_clicked) || (body.is_clicked && !body.hovered)) ? root.text_active_hovered_color : root.text_active_color)
          }

          // Texte pour la lettre supérieure
          Text {
              id: altgr_key

              anchors.bottom: body.bottom
              anchors.bottomMargin: root.height * 0.04
              anchors.right: body.right
              anchors.rightMargin: root.height * 0.1

              font.pixelSize: root.height * 0.36

              text: root.is_multikey && root.keys.length >= 3 ? root.keys[2] : ""
              color: (root.is_caps || !root.is_altgr || !body.enabled)
                     ?   // Cas où la touche ne peut pas être activé (mauvais sous clavier, touche interdite) + couleur du texte selon la couleur du fond
                         (((body.hovered && !body.is_clicked) || (body.is_clicked && !body.hovered)) ? root.text_inactive_hovered_color : root.text_inactive_color)
                     :   // Cas où la touche peut être activée (bon clavier et touche non interdite) + couleur du texte selon la couleur du fond
                         (((body.hovered && !body.is_clicked) || (body.is_clicked && !body.hovered)) ? root.text_active_hovered_color : root.text_active_color)
          }
     }
}
