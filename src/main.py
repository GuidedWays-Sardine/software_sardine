import logging
import log.log as log


def main():
    log.initialise('../log/', '1.0.1', logging.INFO)
    logging.info("Simulateur Sardine")


if __name__ == "__main__":
    main()
