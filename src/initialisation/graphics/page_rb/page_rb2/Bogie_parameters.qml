import QtQuick 2.15
import QtQuick.Controls 2.15
import "../../../components"


Item {
    id: root

    //propriétés sur la position ddu composant
    property int default_x: 0
    property int default_y: 0
    anchors.fill: parent

    // Propriétés pour savoir si la fenêtre est générée et s'il y a un bogie à paramétrer
    property bool generated: false
    property bool any: false
    // Signal activé quand l'élément any est changé, permet de montrer/de cacher le widget et de l'initialiser/le vider
    onAnyChanged: {
            // Just pour changer les valeurs dans le bon ordre
            if(root.any){
                bogies_count_integerinput.maximum_value = root.max_central_bogies
                bogies_count_integerinput.minimum_value = 1

                axle_power_floatinput.is_activable = root.motorized_axles[root.current_bogie_index][root.current_axle_index]
                axle_power_floatinput.change_value(root.motorized_axles_powers[root.current_bogie_index][root.current_axle_index])
            }
            else {
                bogies_count_integerinput.minimum_value = 0
                bogies_count_integerinput.maximum_value = 0

                axle_power_floatinput.change_value(0)
            }
        }
    
    //propriétés du bogie
    readonly property bool articulated: root.any && (root.position == "front" || root.position == "back") && articulated_check.is_checked
    function set_articulated(articulated) {articulated_check.is_checked = articulated;} //fonction pour correctement indiquer si le bogie est articulé ou non
    property var axles_count: []
    property var motorized_axles: []
    property var motorized_axles_powers: []
    property var brakes_counts: []

    //propriétés sur le bogie et l'essieu paramétré et sa position dans la voiture
    property string position: "middle"
    property int current_bogie_index: 0
    property int current_axle_index: 0

    //Données par défaut pour les bogies
    property int default_axle_count: 2
    property double default_axle_power: 750.0
    property int default_pad_brake_count: 0
    property int default_disk_brake_count: 0
    property int default_magnetic_brake_count: 0
    property int default_foucault_brake_count: 0

    // Valeurs limites pour les bogies
    property int max_central_bogies: (root.position == "front" || root.position == "back") ? 1 : 10
    property int max_axles_per_bogies: 10
    property double max_axle_power: 1e4
    property int max_pad_per_axle: 2
    property int max_disk_per_axle: 4
    property int max_magnetic_between_axle: 2       //Identique pour le freinage de foucault

    //Tous les textes nécessitant une traduction
    property string articulated_text: "Articulé ?"
    property string axle_text: "Nessieux"
    property string motor_text: "Pmoteur"
    property string pad_text: "Nplaquettes"
    property string disk_text: "Ndisques"
    property string magnetic_text: "Npatins"
    property string foucault_text: "Nfoucault"


    //Fonction pour réinitialiser le module
    function clear() {
        articulated_check.is_checked = false
        root.any = false
    }


    //Fonction permettant de changer les valeurs du module
    function change_values(axles_count, motorized_axles, motorized_axles_powers, brakes_counts, articulated=false) {
        if(axles_count.length != 0) {
            // Change le nombre de bogies selon la taille des tableaux
            bogies_count_integerinput.change_value(axles_count.length)

            //Change la valeur pour chacun des tableaux
            root.axles_count = axles_count
            root.motorized_axles = motorized_axles
            root.motorized_axles_powers = motorized_axles_powers
            root.brakes_counts = brakes_counts
            articulated_check.is_checked = articulated

            //Réinitialise les index
            root.current_bogie_index = 0
        }
        else {
            // Si les tableaux de valeurs sont vides, réinitialise le module
            clear()
        }
    }


    //Fonction permettant de récupérer les valeurs
    function get_values() {
        if(root.any) {
            // retourne un tableau avec toutes les informations sur le bogie
            return [root.axles_count, root.motorized_axles, root.motorized_axles_powers, root.brakes_counts, root.articulated]
        }
        else {
            // Si aucune valeur n'est inscrite retourne faux
            return false
        }
    }



    // Bouton permettant de donner des limites visibles au composant
    INI_button {
        id: body
        objectName: "body"

        default_x: root.default_x
        default_y: root.default_y
        default_height: root.any ? 104 : 16
        default_width: root.any ? 120 : 16

        is_activable: false
        is_positive: false
        is_visible: root.generated
    }

    // Bouton permettant de cacher ou de montrer l'entièreté des paramétrages
    INI_button {
        id: plus_minus_button
        objectName: "plus_minus_button"

        default_x: root.default_x
        default_y: root.default_y
        default_width: 16
        default_height: 16

        default_image: root.any ? "grey_minus.bmp" : "grey_plus.bmp"

        is_activable: true
        is_positive: false
        is_visible: root.generated

        onClicked: {
            root.any = !root.any
        }
    }

    // Ce composant sera affiché uniquement si la position vaut "front" ou "back"
    // Checkbutton pour savoir si le bogie est articulé ou non (uniquement pour les bogies "front" et "back")
    INI_checkbutton {
        id: articulated_check
        objectName: "articulated_check"

        default_x: plus_minus_button.default_x + plus_minus_button.default_width
        default_y: plus_minus_button.default_y
        box_length: plus_minus_button.default_height

        text: root.articulated_text
        font_size: 8

        is_checked: false
        is_activable: true
        is_positive: false
        is_visible: root.generated && root.any && (root.position == "front" || root.position == "back")
    }

    //Les composants qui suivent seront montrés uniquement en mode "middle" (où si la position est fausse)
    //button flèche permettant d'aller à gauche dans la liste des bogies
    INI_button {
        id: left_bogie_arrow_button
        objectName: "left_bogie_arrow_button"

        default_x: plus_minus_button.default_x + plus_minus_button.default_width
        default_y: plus_minus_button.default_y
        default_height: plus_minus_button.default_height
        default_width: plus_minus_button.default_width

        image_activable: "grey_left_arrow.bmp"
        image_not_activable: "dark_grey_left_arrow.bmp"

        is_activable: root.current_bogie_index > 0
        is_positive: false
        is_visible: root.generated && root.any && !(root.position == "front" || root.position == "back")

        //Quand cliqué enlève 1 à l'index à l'index de bogie (is_activable évite que l'index sorte du tableau de valeurs)
        onClicked: {
            root.current_bogie_index = root.current_bogie_index - 1
        }
    }

    //button indiquant l'index du bogie paramétré
    INI_button {
        id: bogie_index_button
        objectName: "bogie_index_button"

        default_x: left_bogie_arrow_button.default_x + left_bogie_arrow_button.default_width
        default_y: plus_minus_button.default_y
        default_width: 2 * plus_minus_button.default_width
        default_height: plus_minus_button.default_height

        text: root.current_bogie_index + root.any
        font_size: 8

        is_positive: false
        is_activable: false
        is_dark_grey: false
        is_visible: root.generated && root.any && !(root.position == "front" || root.position == "back")

        //signal appelé lorsque le text change (et donc lorsque l'index change)
        onTextChanged: {
            // S'assure qu'il y a bien un essieu de paramétré
            if(root.any) {
                //Change le nombre d'essieu pour celui du nouvel index
                axles_count_integerinput.change_value(root.axles_count[root.current_bogie_index])

                //Mets à jour les boutons de motorisations pour chacun des essieux
                for (let i = 0; i < root.motorized_axles[root.current_bogie_index].length; i++) {
                    motorisation.itemAt(i).text = root.motorized_axles[root.current_bogie_index][i] ? "x" : ""
                }

                //Repasse l'index de l'essieu à 0
                root.current_axle_index = 0

                //Change le nombre des différents systèmes de freinages
                pad_brake_integerinput.change_value(root.brakes_counts[root.current_bogie_index][0])
                disk_brake_integerinput.change_value(root.brakes_counts[root.current_bogie_index][1])
                // Pour les freinages magnétiques, comme ceux-ci sont liés, les passes d'abord à 0 pour éviter des erreurs lors des changement de valeurs
                magnetic_brake_integerinput.clear()
                foucault_brake_integerinput.clear()
                magnetic_brake_integerinput.change_value(root.brakes_counts[root.current_bogie_index][2])
                foucault_brake_integerinput.change_value(root.brakes_counts[root.current_bogie_index][3])
            }
        }
    }

    //button permettant juste de montrer un / (pour indiquer bogie x/y)
    INI_button {
        id: slash_button
        objectName: "slash_button"

        default_x: bogie_index_button.default_x + bogie_index_button.default_width
        default_y: plus_minus_button.default_y
        default_width: 0.5 * plus_minus_button.default_width
        default_height: plus_minus_button.default_height

        text: "/"
        font_size: 10

        is_positive: false
        is_visible: root.generated && root.any && !(root.position == "front" || root.position == "back")
    }

    //integerinput permettant d'indiquer le nombre de bogies centraux
    INI_integerinput {
        id: bogies_count_integerinput
        objectName: "bogies_count_integerinput"

        default_x: slash_button.default_x + slash_button.default_width
        default_y: plus_minus_button.default_y
        default_width: bogie_index_button.default_width
        default_height: bogie_index_button.default_height

        maximum_value: 0
        minimum_value: 0
        is_max_default: false
        font_size: 8

        is_activable: true
        is_positive: false
        is_visible: root.generated && root.any && !(root.position == "front" || root.position == "back")

        //Signal activé lorsque la valeur entrée dans le valueinput change
        onValue_changed: {
            //S'assure que l'index du bogie paramété est bon (et qu'il ne dépasse pas la valeur max) sinon le change
            if(root.current_bogie_index >= value){
                root.current_bogie_index = value != 0 ? value - 1 : 0
            }

            //Ajoute ou enlève des valeurs dans les tableaux de valeurs au besoins
            while(root.axles_count.length > value){
                root.axles_count.pop()
                root.motorized_axles.pop()
                root.motorized_axles_powers.pop()
                root.brakes_counts.pop()
            }
            while(root.axles_count.length < value){
                root.axles_count.push(root.default_axle_count)
                root.motorized_axles.push(Array(root.default_axle_count).fill(0))
                root.motorized_axles_powers.push(Array(root.default_axle_count).fill(0.0))
                root.brakes_counts.push([default_pad_brake_count <= pad_brake_integerinput.maximum_value ? default_pad_brake_count : pad_brake_integerinput.maximum_value,
                                         default_disk_brake_count <= disk_brake_integerinput.maximum_value ? default_disk_brake_count : disk_brake_integerinput.maximum_value,
                                         (default_magnetic_brake_count + default_foucault_brake_count) <= root.max_magnetic_between_axle * (root.default_axle_count - 1) ? default_magnetic_brake_count : (default_magnetic_brake_count >= default_foucault_brake_count ? root.max_magnetic_between_axle * (root.default_axle_count - 1) : 0),
                                         (default_magnetic_brake_count + default_foucault_brake_count) <= root.max_magnetic_between_axle * (root.default_axle_count - 1) ? default_foucault_brake_count : (default_magnetic_brake_count >= default_foucault_brake_count ? 0 : root.max_magnetic_between_axle * (root.default_axle_count - 1))])
            }

            // Change la valeur du nombre d'essieu à la valeur actuelle (utile dans le cas où root.any a changé)
            axles_count_integerinput.change_value(root.axles_count[root.current_bogie_index])
        }
    }

    //button flèche permettant d'aller à droite dans la liste des bogies
    INI_button {
        id: right_bogie_arrow_button
        objectName: "right_bogie_arrow_button"

        default_x: bogies_count_integerinput.default_x + bogies_count_integerinput.default_width
        default_y: plus_minus_button.default_y
        default_height: plus_minus_button.default_height
        default_width: plus_minus_button.default_width

        image_activable: "grey_right_arrow.bmp"
        image_not_activable: "dark_grey_right_arrow.bmp"

        is_activable: root.current_bogie_index < (bogies_count_integerinput.value - 1)
        is_positive: false
        is_visible: root.generated && root.any && !(root.position == "front" || root.position == "back")

        //Quand cliqué ajoute 1 à l'index de bogie (is_activable évite que l'index sorte du tableau de valeurs)
        onClicked: {
            root.current_bogie_index = root.current_bogie_index + 1
        }
    }

    //Tous les composants en dessous sont montrés peu importe le type de position
    //integerinput permettant de rentrer le nombre d'essieux sur le bogie
    INI_integerinput {
        id: axles_count_integerinput
        objectName: "axles_count_integerinput"

        default_x: plus_minus_button.default_x
        default_y: plus_minus_button.default_y + plus_minus_button.default_height
        default_width: 2 * plus_minus_button.default_width
        default_height: plus_minus_button.default_height

        minimum_value: 1
        maximum_value: root.max_axles_per_bogies
        is_max_default: false
        font_size: 8

        is_positive: false
        is_activable: true
        is_visible: root.generated && root.any

        //signal appelé lorsque le nombre d'essieux entrées change
        onValueChanged: {
            //Commence par changer la valeur dans le tableau de valeurs
            root.axles_count[root.current_bogie_index] = value

            //Ajoute/enlève autant d'éléments que nécessaires dans la liste des moteurs et de leur puissance
            while(root.motorized_axles[root.current_bogie_index].length > value){
                root.motorized_axles[root.current_bogie_index].pop()
                root.motorized_axles_powers[root.current_bogie_index].pop()
            }
            while(root.motorized_axles[root.current_bogie_index].length < value){
                root.motorized_axles[root.current_bogie_index].push(0)
                root.motorized_axles_powers[root.current_bogie_index].push(0)
            }

            //S'assure que l'index d'essieu est toujours dans la limite sinon le remet à la limite supérieure
            if(root.current_axle_index >= value) {
                root.current_axle_index = value - 1
            }

            // Change le nombre de moteurs paramétrables pour le bogie (selon le nombre d'essieux disponibles
            motorisation.model = root.motorized_axles[root.current_bogie_index].length

            //Mets à jour si l'essieu est motorisé pour tous les essieux
            for (let i = 0; i < root.motorized_axles[root.current_bogie_index].length; i++) {
                motorisation.itemAt(i).text = root.motorized_axles[root.current_bogie_index][i] ? "x" : ""
            }
        }
    }

    INI_text {
        id: axles_count_text
        objectName: "axles_count_name"

        default_x: axles_count_integerinput.default_x + axles_count_integerinput.default_width + font_size * 0.5
        default_y: axles_count_integerinput.default_y + (axles_count_integerinput.default_height - font_size) * 0.5 - 1

        text: root.axle_text
        font_size: 8

        is_dark_grey: false
        is_visible: root.generated && root.any
    }

    //Série de boutons permettant d'indiquer si l'essieu est moteur ou non. Se répète autant de fois qu'il y a d'essieux
    Repeater {
        id: motorisation
        objectName: "motorisation"

        model: 0

        INI_button {
            default_x: axles_count_integerinput.default_x + index * default_width
            default_y: axles_count_integerinput.default_y + axles_count_integerinput.default_height
            default_width: ((right_bogie_arrow_button.default_x + right_bogie_arrow_button.default_width)-plus_minus_button.default_x) / axles_count_integerinput.value
            default_height: 8

            text: ""
            font_size: 5

            is_positive: false
            is_activable: true
            is_visible: root.generated && root.any

            //signal appelé lorsque l'un des boutons est cliqué. Permet d'inverser s'il est motorisé ou non
            onClicked: {
                 //Inverse la valeur de la motorisation
                 root.motorized_axles[root.current_bogie_index][index] = !root.motorized_axles[root.current_bogie_index][index]

                 // Mets une croix ou non selon si l'essieu est maintenant motorisé ou non
                 text = root.motorized_axles[root.current_bogie_index][index] ? "x" : ""

                 // Change la valeur de la puissance moteur à 0 si la motorisation est enlevée et à la valeur par défaut
                 root.motorized_axles_powers[root.current_bogie_index][index] = root.motorized_axles[root.current_bogie_index][index] ? root.default_axle_power : 0

                // Active/désactive le valueinput de la puissance si l'index correspond
                if(index === root.current_axle_index) {
                    axle_power_floatinput.is_activable = root.motorized_axles_powers[root.current_bogie_index][index]
                    axle_power_floatinput.change_value(root.motorized_axles_powers[root.current_bogie_index][root.current_axle_index])
                }
            }
        }
    }

    //Composants permettant le paramétrage de la puissance moteur individuelles
    //button flèche permettant de naviguer à gauche dans les essieux
    INI_button {
        id: left_axle_arrow_button
        objectName: "left_axle_arrow_button"

        default_x: axles_count_integerinput.default_x
        default_y: axles_count_integerinput.default_y + axles_count_integerinput.default_height + 8
        default_height: plus_minus_button.default_height
        default_width: plus_minus_button.default_width

        image_activable: "grey_left_arrow.bmp"
        image_not_activable: "dark_grey_left_arrow.bmp"

        is_activable: root.current_axle_index > 0
        is_positive: false
        is_visible: root.generated && root.any

        //Quand cliqué enlève 1 à l'index d'essieu (is_activable évite que l'index sorte du tableau de valeurs)
        onClicked: {
            root.current_axle_index = root.current_axle_index - 1
        }
    }

    //button indiquant l'index de l'essieu actuellement paramétré
    INI_button {
        id: axle_index_button
        objectName: "axle_index_button"

        default_x: left_axle_arrow_button.default_x + left_axle_arrow_button.default_width
        default_y: left_axle_arrow_button.default_y
        default_width: left_axle_arrow_button.default_width
        default_height: left_axle_arrow_button.default_height

        text: root.current_axle_index + 1
        font_size: 8

        is_positive: false
        is_activable: false
        is_dark_grey: false
        is_visible: root.generated && root.any

        //Signal appelé lorsque le texte change (et donc que l'index d'essieu change
        onTextChanged: {
            //rend l'integerinput de la puissance moteur activable ou non selon si l'essieu est motorisé ou non et change sa valeur
            axle_power_floatinput.is_activable = root.motorized_axles[root.current_bogie_index][root.current_axle_index]
            axle_power_floatinput.change_value(root.motorized_axles_powers[root.current_bogie_index][root.current_axle_index])
        }
    }

    //button flèche permettant de naviguer à droite dans les essieux
    INI_button {
        id: right_axle_arrow_button
        objectName: "right_axle_arrow_button"

        default_x: axle_index_button.default_x + axle_index_button.default_width
        default_y: axle_index_button.default_y
        default_height: axle_index_button.default_height
        default_width: axle_index_button.default_width

        image_activable: "grey_right_arrow.bmp"
        image_not_activable: "dark_grey_right_arrow.bmp"

        is_activable: root.current_axle_index < (axles_count_integerinput.value - 1)
        is_positive: false
        is_visible: root.generated && root.any

        //Quand cliqué ajoute 1 à l'index d'essieu (is_activable évite que l'index sorte du tableau de valeurs)
        onClicked: {
            root.current_axle_index = root.current_axle_index + 1
        }
    }

    //floatinput permettant de rentrer la puissance moteur
    INI_floatinput {
        id: axle_power_floatinput
        objectName: "axle_power_floatinput"

        default_x: right_axle_arrow_button.default_x + right_axle_arrow_button.default_height
        default_y: right_axle_arrow_button.default_y
        default_width: 2 * right_axle_arrow_button.default_width
        default_height: right_axle_arrow_button.default_height

        minimum_value: is_activable ? 0.001 : 0
        maximum_value: root.max_axle_power
        is_max_default: false
        decimals: 3
        font_size: 8

        is_visible: root.generated && root.any
        is_positive: false
        is_activable: root.motorized_axles[root.current_bogie_index][root.current_axle_index]
    }

    INI_text {
        id: axles_power_text
        objectName: "axles_power_text"

        default_x: axle_power_floatinput.default_x + axle_power_floatinput.default_width + font_size * 0.5
        default_y: axle_power_floatinput.default_y + (axle_power_floatinput.default_height - font_size) * 0.5 - 1

        text: root.motor_text
        font_size: 8

        is_dark_grey: false
        is_visible: root.generated && root.any
    }

    INI_text {
        id: axle_power_unit_text
        objectName: "axle_power_unit_text"

        text: "kW"
        font_size: 4

        default_x: axle_power_floatinput.default_x + axle_power_floatinput.default_width + 2
        default_y: axle_power_floatinput.default_y + axle_power_floatinput.default_height - font_size

        is_dark_grey: true
        is_visible: root.generated && root.any
    }

    //intergerinput permettant de rentrer le nombre de roues équipées de plaquettes de freinages
    INI_integerinput {
        id: pad_brake_integerinput
        objectName: "pad_brake_integerinput"

        default_x: left_axle_arrow_button.default_x
        default_y: left_axle_arrow_button.default_y + left_axle_arrow_button.default_height
        default_width: 2 * plus_minus_button.default_width
        default_height: 12

        maximum_value: root.max_pad_per_axle * axles_count_integerinput.value
        minimum_value: 0
        is_max_default: false
        font_size: 6

        is_visible: root.generated && root.any
        is_positive: false
        is_activable: true

        //Signal permettant de mettre à jour la valeur stockée lorsque celle-ci est changée
        onValue_changed: {
            root.brakes_counts[root.current_bogie_index][0] = pad_brake_integerinput.value
        }
    }

    INI_text {
        id: pad_brake_text
        objectName: "pad_brake_text"

        default_x: pad_brake_integerinput.default_x + pad_brake_integerinput.default_width + font_size * 0.5
        default_y: pad_brake_integerinput.default_y + (pad_brake_integerinput.default_height - font_size) * 0.5 - 1

        text: root.pad_text
        font_size: 8

        is_dark_grey: false
        is_visible: root.generated && root.any
    }

    //integerinput pour indiquer le nombre de disques de freinages
    INI_integerinput {
        id: disk_brake_integerinput
        objectName: "disk_brake_integerinput"

        default_x: pad_brake_integerinput.default_x
        default_y: pad_brake_integerinput.default_y + pad_brake_integerinput.default_height
        default_width: pad_brake_integerinput.default_width
        default_height: pad_brake_integerinput.default_height

        minimum_value: 0
        maximum_value: root.max_disk_per_axle * axles_count_integerinput.value
        is_max_default: false
        font_size: 6

        is_visible: root.generated && root.any
        is_positive: false
        is_activable: true

        //Signal permettant de mettre à jour la valeur stockée lorsque celle-ci est changée
        onValue_changed: {
            root.brakes_counts[root.current_bogie_index][1] = disk_brake_integerinput.value
        }
    }

    INI_text {
        id: disk_brake_text
        objectName: "disk_brake_text"

        default_x: disk_brake_integerinput.default_x + disk_brake_integerinput.default_width + font_size * 0.5
        default_y: disk_brake_integerinput.default_y + (disk_brake_integerinput.default_height - font_size) * 0.5 - 1

        text: root.disk_text
        font_size: 8

        is_dark_grey: false
        is_visible: root.generated && root.any
    }

    //integerinput permettant
    INI_integerinput {
        id: magnetic_brake_integerinput
        objectName: "magnetic_brake_integerinput"

        default_x: disk_brake_integerinput.default_x
        default_y: disk_brake_integerinput.default_y + disk_brake_integerinput.default_height
        default_width: disk_brake_integerinput.default_width
        default_height: disk_brake_integerinput.default_height

        minimum_value: 0
        maximum_value: -foucault_brake_integerinput.value + root.max_magnetic_between_axle * (axles_count_integerinput.value - 1)
        is_max_default: false
        font_size: 6

        is_visible: root.generated && root.any
        is_positive: false
        is_activable: maximum_value != 0

        //Signal permettant de mettre à jour la valeur stockée lorsque celle-ci est changée
        onValue_changed: {
            root.brakes_counts[root.current_bogie_index][2] = magnetic_brake_integerinput.value
        }
    }

    INI_text {
        id: magnetic_brake_text
        objectName: "magnetic_brake_text"

        default_x: magnetic_brake_integerinput.default_x + magnetic_brake_integerinput.default_width + font_size * 0.5
        default_y: magnetic_brake_integerinput.default_y + (magnetic_brake_integerinput.default_height - font_size) * 0.5 - 1

        text: root.magnetic_text
        font_size: 8

        is_dark_grey: magnetic_brake_integerinput.maximum_value == 0
        is_visible: root.generated && root.any
    }

    //integerinput permettant de changer le nombre de freinages de foucault
    INI_integerinput {
        id: foucault_brake_integerinput
        objectName: "foucault_brake_integerinput"

        default_x: magnetic_brake_integerinput.default_x
        default_y: magnetic_brake_integerinput.default_y + magnetic_brake_integerinput.default_height
        default_width: magnetic_brake_integerinput.default_width
        default_height: magnetic_brake_integerinput.default_height

        minimum_value: 0
        maximum_value: -magnetic_brake_integerinput.value + root.max_magnetic_between_axle * (axles_count_integerinput.value - 1)
        is_max_default: false
        font_size: 6

        is_visible: root.generated && root.any
        is_positive: false
        is_activable: maximum_value != 0

        //Signal permettant de mettre à jour la valeur stockée lorsque celle-ci est changée
        onValue_changed: {
            root.brakes_counts[root.current_bogie_index][3] = foucault_brake_integerinput.value
        }
    }

    INI_text {
        id: foucault_brake_text
        objectName: "foucault_brake_text"

        default_x: foucault_brake_integerinput.default_x + foucault_brake_integerinput.default_width + font_size * 0.5
        default_y: foucault_brake_integerinput.default_y + (foucault_brake_integerinput.default_height - font_size) * 0.5 - 1

        text: root.foucault_text
        font_size: 8

        is_dark_grey: foucault_brake_integerinput.maximum_value == 0
        is_visible: root.generated && root.any
    }
}