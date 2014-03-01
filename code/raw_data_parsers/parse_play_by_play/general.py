#!/usr/bin/env python3

from data_helpers.team_list import pfr_codes_to_code


def row_type(row):
    """Takes a row of plain text and returns the type.

    args:
        row: A row from BrautifulSoup, filtered with soup.find_all("tr") and
        parsed with get_text(' ', strip=True)

    returns:
        An integer indicating the type of row:
            -1: Header
            0: Normal Row
            1: 1st Quarter
            2: 2nd Quarter
            3: 3rd Quarter
            4: 4th Quarter
            5: New Overtime
            6: End of Game/Overtime
    """
    if "Quarter Time Down" in row:
        return -1
    elif "1st Quarter" in row:
        return 1
    elif "2nd Quarter" in row:
        return 2
    elif "3rd Quarter" in row:
        return 3
    elif "4th Quarter" in row:
        return 4
    elif "End" in row:
        return 6
    elif "Overtime" in row:
        return 5
    else:
        return 0


def get_kicking_team(kick_text):
    """Takes a field position and returns the kicking team on kickoff.

    args:
        kick_text: A string giving the field position.

    returns:
        A string of the kicking team's code.

    raises:
        KeyError if the team codes don't exist.
    """
    split_cols = kick_text.split()
    return pfr_codes_to_code[split_cols[0]]