import sys

from . import logger


def main() -> None:
    try:
        logger.init_logger(True)

        logger.get_logger().debug("test log message")
        logger.get_logger().info("test log message")
        logger.get_logger().warn("test log message")
        logger.get_logger().error("test log message")

        raise Exception("test exception")
    except Exception as exception:
        logger.get_logger().error(exception)
        sys.exit(1)
    except KeyboardInterrupt:
        print("")  # output a line break after the ^C symbol in a terminal
        sys.exit(1)
