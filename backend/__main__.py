import logging

from backend.app import create_app

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.DEBUG)
    logger.info('start app')

    app.run(
        port=config.server.port,
        host=config.server.host,
        debug=False
    )
    return app


if __name__ == "__main__":
    main()
