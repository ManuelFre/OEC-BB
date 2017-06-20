from Config.settings import DEBUG_PRINT


def debug_print(msg):
    """ Prints messages only if DEBUG_PRINT is set to True in the settings.
    This function is used instead of print throughout the entire app.

    Args:
        msg (str/int/obj): message to print
    """
    if DEBUG_PRINT:
        print(msg)
