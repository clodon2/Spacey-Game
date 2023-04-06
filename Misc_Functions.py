import Globals
from PIL import ImageOps


def get_turn_multiplier(speed):
    return speed / (Globals.PLAYER_MAX_SPEED / 1.5)


def screen_scale(num, axis="other"):
    return_num = num
    if axis.lower() == "other":
        return_num = num * Globals.SCREEN_PERCENT
    elif axis.lower() == "x":
        return_num = num * Globals.SCREEN_PERCENTS[0]
    elif axis.lower() == "y":
        return_num = num * Globals.SCREEN_PERCENTS[1]

    return return_num


def tint_image(src, color="#FFFFFF"):
    src.load()
    r, g, b, alpha = src.split()
    gray = ImageOps.grayscale(src)
    result = ImageOps.colorize(gray, (0, 0, 0, 0), color)
    result.putalpha(alpha)
    return result


def parent_to(parent, child):
    parent.children.append(child)
    child.parent = parent
