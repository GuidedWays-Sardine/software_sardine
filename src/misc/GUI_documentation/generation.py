# Sous librairies de tracés des images
import layouts.initialisation as ini


def main():
    """Module permettant de générer les images types documentation ETCS à partir des composants.
    Ce module est entièrement indépendant du reste du code et ne dois pas être appelé par celui-ci.
    Les images sont stockées dans {PROJECT_DIR}/results/documentation_images
    """
    ini.page_rb1()
    ini.page_rb8()


if __name__ == "__main__":
    main()
