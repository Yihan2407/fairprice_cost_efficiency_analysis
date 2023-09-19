def parse_string_for_query(
        string: str
):
    """
    Parses a string for a query to be used in a URL.
    :param string: String to be parsed.
    :return: Parsed string.
    """
    string = string.lower()
    if len(string.split()) > 1:
        string = string.replace(" ", "%20")
    return string