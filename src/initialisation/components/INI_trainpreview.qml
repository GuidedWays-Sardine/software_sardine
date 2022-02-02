import QtQuick 2.15
import QtQuick.Controls 2.15


//https://doc.qt.io/qt-5/qtqml-documents-definetypes.html
//Comment créer un élément personalisé


Item {
    id: root

    //Propriétés sur la position et la taille du trainpreview
    property double default_x: 0
    property double default_y: 0
    property double default_width: 640
    property double default_height: 40
    anchors.fill: parent

    //Propriétés reliés au nombre d'éléments maximum visible dans chacune des divisions
    property int visible_count: 10
    onVisible_countChanged: {
        //S'assure que le nombre de voitures visible est supérieur à 1
        if(visible_count < 1){
            visible_count = 1
        }

        //S'assure aussi que la page actuellement visible contient toujours l'index
        if(root.current_index >= (root.current_page + 1) * root.visible_count || root.current_index < root.current_page * root.visible_count) {
            root.current_page = ((root.current_index - root.current_index) % root.visible_count) / root.visible_count
        }
        // Les signaux associés seront appelés dans la fonction onCurrent_pageChanged si la page a été changée
    }

    //Propriété sur la liste des voitures
    property var type_list: []      // Liste contenant le type de chacune des voitures (fret, passager, ...)
    readonly property var prime_list: [2, 3, 5, 7, 11, 13, 17]      //permettant de varier les icones visibles en bas
    property var position_list: []  // Liste contenant la position de chacune des voitures (avant, arrière, milieu)

    //propriétés relié à la visibilité et la présentation de la barre
    property bool is_visible: true
    property bool is_activable: true
    property bool is_positive: false

    //Propriétés permettant de connaitre la taille du train (et donc l'index maximal) et le nombre de pages possibles
    readonly property int train_length: type_list.length > position_list.length ? position_list.length : type_list.length     //La longueur du train se base toujours sur la liste la plus courte
    readonly property int pages_count: (((root.train_length % root.visible_count) != 0) + (root.train_length - root.train_length % root.visible_count) / root.visible_count)
    onTrain_lengthChanged: {
        //S'assure que l'index montre bien une page contenant des voitures
        if(root.current_index >= root.train_length){
            root.current_index = root.train_length - 1
        }
        // S'occupe de mettre à jour la page et d'appeler les différents signaux dans onCurrent_indexChanged
    }


    //Propriété sur l'index de train à montrer
    property int current_page: 0
    onCurrent_pageChanged: {
        //S'assure que la page est bien dans la bonne zone de valeurs
        if(root.current_page >= root.pages_count || root.current_page < 0){
            root.current_page = root.current_page < 0 ? 0 : root.pages_count - 1
        }
        // Appelle le signal associé au changement de page
        page_changed()

        //S'assure que l'index montre bien un train de cette page
        if(root.current_index >= (root.current_page + 1) * root.visible_count || root.current_index < root.current_page * root.visible_count) {
            root.current_index = (root.current_index < (root.current_page * root.visible_count)) ? (root.current_page * root.visible_count) : ((root.current_page + 1) * root.visible_count - 1)
        }
        // Le signal sera appelé dans onCurrent_indexChanged si la valeur a été changée
    }

    // Propriété sur l'élément sélectionné
    property int current_index: 0
    onCurrent_indexChanged: {
        //S'assure que l'index est bien dans la bonne zone de valeurs
        if(root.current_index >= root.train_length || root.current_index < 0){
            root.current_index = root.current_index < 0 ? 0 : root.train_length - 1
        }
        //Appelle le signal pour dire que l'index a été changé
        index_changed()

        //S'assure que la l'index montre bien un train qui se situe dans la page actuelle
        if(root.current_index >= (root.current_page + 1) * root.visible_count || root.current_index < root.current_page * root.visible_count) {
            root.current_page = (root.current_index - (root.current_index % root.visible_count)) / root.visible_count
        }
        //Le signal sera appelé dans onCurrent_page_Changed si la valeur a été changée
    }


    // Les signaux (permettant de détecter le changement d'index et le changement de page)
    signal index_changed()
    signal page_changed()


    //Bouton pour passer à la liste de gauche
    INI_button{
        id: left_list_button
        objectName: "left_list_button"

        default_x: root.default_x
        default_y: root.default_y
        default_width: root.default_height
        default_height: root.default_height

        image_activable: "Navigation/grey_left_arrow.bmp"
        image_not_activable: "Navigation/dark_grey_left_arrow.bmp"

        is_positive: root.is_positive
        is_activable: root.current_page > 0 && root.is_activable
        is_visible: root.is_visible

        onClicked: {
            root.current_page = root.current_page - 1
        }
    }

    //Bouton pour passer à la liste de droite
    INI_button{
        id: right_list_button
        objectName: "right_list_button"

        default_x: root.default_x + root.default_width - root.default_height
        default_y: root.default_y
        default_width: root.default_height
        default_height: root.default_height

        image_activable: "Navigation/grey_right_arrow.bmp"
        image_not_activable: "Navigation/dark_grey_right_arrow.bmp"

        is_positive: root.is_positive
        is_activable: root.current_page < root.pages_count - 1 && root.is_activable
        is_visible: root.is_visible

        onClicked: {
            root.current_page = root.current_page + 1
        }
    }

    // ... permettant d'indiquer qu'il y a plus de trains sur le côté gauche
    INI_button{
        id: left_dots_button
        objectName: "left_dots_button"

        default_x: root.default_x + root.default_height
        default_y: root.default_y
        default_width: (root.default_width - 2 * root.default_height) / (root.visible_count + 2.0)
        default_height: root.default_height * 0.5

        text: root.current_page > 0 ? "..." : ""

        is_positive: root.is_positive
        is_activable: false
        is_dark_grey: false
        is_visible: root.is_visible
    }


    // ... permettant d'indiquer qu'il y a plus de trains sur le côté droit
    INI_button{
        id: right_dots_button
        objectName: "right_dots_button"

        default_x: root.default_x + root.default_height + right_dots_button.default_width * (root.visible_count + 1)
        default_y: root.default_y
        default_width: (root.default_width - 2 * root.default_height) / (root.visible_count + 2)
        default_height: root.default_height * 0.5

        text: root.current_page < root.pages_count - 1 ? "..." : ""

        is_positive: root.is_positive
        is_dark_grey: false
        is_activable: false
        is_visible: root.is_visible
    }

    //Liste de boutons permettant de montrer les icones de chacune des voitures visibles
    Repeater{
        id: trains_showing
        objectName: trains_showing

        anchors.fill: parent
        model: root.visible_count

        INI_button {
            property int button_index: root.current_page * root.visible_count + index

            default_x: root.default_x + root.default_height + right_dots_button.default_width * (index + 1)
            default_y: root.default_y
            default_width: (root.default_width - 2 * root.default_height) / (root.visible_count + 2)
            default_height: root.default_height * 0.5

            image_activable: "Train_icons/" + root.type_list[button_index] + (root.prime_list.includes(button_index % (root.visible_count + 3)) ? "/empty/" : "/full/") + (is_dark_grey ? "dark_" : "") + "grey_" + root.position_list[button_index] + ".png"
            image_not_activable: ""
            text: is_activable ? (button_index + 1).toString() : ""
            font_size: 8

            is_positive: root.is_positive
            is_activable: button_index < root.train_length
            is_dark_grey: button_index != root.current_index
            is_visible: root.is_visible

            //Fonction qui change l'index lorsque l'une des icones en bas est cliquée
            onClicked: {
                root.current_index = root.current_page * root.visible_count + index
            }
        }
    }

    // Bouton permettant d'afficher le numéro de la page ainsi que l'index de la voiture sélectionnée
    INI_button{
        id: index_button
        objectName: "index_button"

        default_x: root.default_x + root.default_height
        default_y: root.default_y + root.default_height / 2
        default_width: (root.default_width - 2 * root.default_height)
        default_height: root.default_height/2

        text: `${root.current_index + (root.train_length != 0)}/${root.train_length}    ${root.current_page + (root.pages_count != 0)}/${root.pages_count}`

        is_positive: root.is_positive
        is_activable: false
        is_dark_grey: false
        is_visible: root.is_visible
    }
}