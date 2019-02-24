from sty import fg, bg, rs, RgbFg

def print_section(message):
    """
        Function to factorise the print of each section"s message.

        Args:
        (str) message - message to print
    """

    section_message = bg.da_cyan + message + bg.rs
    print()
    print(section_message)
    print()


def print_result(message, value):
    """
        Function to factorise the print of each result"s message.

        Args:
        (str) message - message to print
        (int64) value - value calculated
    """

    result_message = bg.green + message + str(value) + bg.rs
    print(result_message)


def print_error():
    """
        Function to factorise the print of error message.

    """
    error_message = bg.red + "Unavailable answer !" + bg.rs
    print(error_message)