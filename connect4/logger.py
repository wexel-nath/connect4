from datetime import datetime

LEVEL_DEBUG = 10
LEVEL_INFO = 20
LEVEL_WARN = 30
LEVEL_ERROR = 40
levels = {
    LEVEL_DEBUG: "DEBUG",
    LEVEL_INFO: "INFO",
    LEVEL_WARN: "WARN",
    LEVEL_ERROR: "ERROR",
}

LOG_LEVEL = LEVEL_INFO


def log(level: int, format: str, *args):
    if level < LOG_LEVEL:
        return
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    print(("{} [{}] " + format).format(
        now,
        levels[level],
        *args,
    ))


def debug(format: str, *args):
    log(LEVEL_DEBUG, format, *args)


def info(format: str, *args):
    log(LEVEL_INFO, format, *args)


def warn(format: str, *args):
    log(LEVEL_WARN, format, *args)


def error(format: str, *args):
    log(LEVEL_ERROR, format, *args)
