#!/usr/bin/env python3

from data_helpers.team_list import pfr_codes_to_code, pfr_codes


def split_turnovers(col):
    """Takes a string describing the play, and splits it into a list of the
    turnovers.

    args:
        col: A string describing the play.

    returns:
        A list of strings.
    """
    # Either the turnover is alone, or is set off in its own sentence, so we
    # split on '.'
    final_list = []
    for item in col.split('.'):
        if "fumble" in item.lower() or "intercepted" in item.lower():
            final_list.append(item.strip())

    return final_list


def get_turnover_type(turnover_string):
    """Takes a string describing the play, and returns the type of turnover.

    args:
        turnover_string: A string about the turnover, as returned by
            split_turnovers.

    returns:
        A string indicating the type, or None if it can't be figured out
    """
    if "fumble" in turnover_string.lower():
        return "fumble"
    elif "intercept" in turnover_string.lower():
        return "interception"
    else:
        out = "Unknown turnover type: '" + turnover_string + "'"
        print(out)
        return None


def get_turnover_recoverer(turnover_string):
    """Takes a string describing the play, and returns the player that
    recovered the turnover.

    args:
        turnover_string: A string about the turnover, as returned by
            split_turnovers.

    returns:
        A string indicating the player's name.
    """
    # Use the type to set the string to split on
    to_type = get_turnover_type(turnover_string)
    if to_type == "fumble":
        split_string = "recovered by"
    elif to_type == "interception":
        split_string = "intercepted by"
    else:  # Unknown case, we can't do anything
        return None
    # Now split the string
    r_string = turnover_string.split(split_string)[1].strip()
    l_string = r_string.split(" at ")[0].strip()
    return l_string


def get_turnover_committer(turnover_string):
    """Takes a string describing the play, and returns the player that
    committed the turnover.

    args:
        turnover_string: A string about the turnover, as returned by
            split_turnovers.

    returns:
        A string indicating the player's name.
    """
    # Use the type to set the string to split on
    to_type = get_turnover_type(turnover_string)
    if to_type == "fumble":
        split_string = "fumbles"
    elif to_type == "interception":
        split_string = "pass incomplete"
    else:  # Unknown case, we can't do anything
        return None
    # Now split the string
    l_string = turnover_string.split(split_string)[0].strip()
    return l_string


def get_turnover_teams(turnover_string, home_players, away_players):
    """Takes a string describing the play, and returns the teams that lost and
    recovered the turnover.

    args:
        turnover_string: A string about the turnover, as returned by
            split_turnovers.
        home_players, away_players: Iterables that support 'in' containing a
            list of all players on the home and away team, respectively.

    returns:
        A tuple of (committing_team, recovering_team) with values "home",
            "away"
    """
    com = get_turnover_committer(turnover_string)
    rec = get_turnover_recoverer(turnover_string)
    com_uniq_home = (com in home_players and com not in away_players)
    com_uniq_away = (com in away_players and com not in home_players)
    rec_uniq_home = (rec in home_players and rec not in away_players)
    rec_uniq_away = (rec in away_players and rec not in home_players)
    # With an interception, we only need to get one team, because we know the
    # other by the fact that an interception only happens when possession
    # changes.
    if get_turnover_type(turnover_string) == "interception":
        if com_uniq_home or rec_uniq_away:
            return ("home", "away")
        elif com_uniq_away or rec_uniq_home:
            return ("away", "home")
    # Fumbles can be recovered by the same team, so we need both
    else:
        error_text = ""

        com_team = None
        if com_uniq_home:
            com_team = "home"
        elif com_uniq_away:
            com_team = "away"
        else:
            error_text += "\tTurnover committing player '" + com + "' not recognized!"

        rec_team = None
        if rec_uniq_home:
            rec_team = "home"
        elif rec_uniq_away:
            rec_team = "away"
        else:
            error_text += "\tTurnover recovering player '" + pre + "' not recognized!"

        if error_text:
            print(error_text)

        return (com_team, rec_team)