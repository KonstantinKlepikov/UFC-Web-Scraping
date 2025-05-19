import pandas as pd

from scraper.constants import (
    EVENT_COLUMNS,
    EVENT_DATA_PATH,
    FIGHT_COLUMNS,
    FIGHT_DATA_PATH,
    FIGHTER_COLUMNS,
    FIGHTER_DATA_PATH,
    FIGHTSTATS_COLUMNS,
    FIGHTSTATS_DATA_PATH,
)


def add_primary_keys(
    ufc_events: pd.DataFrame,
    ufc_fights: pd.DataFrame,
    ufc_fight_stats: pd.DataFrame,
    ufc_fighters: pd.DataFrame,
) -> None:
    """Create primary keys"""

    # Creates unique keys for each row in table
    event_id = [num for num in range(1, len(ufc_events) + 1)]
    fight_id = [num for num in range(1, len(ufc_fights) + 1)]
    fight_stat_id = [num for num in range(1, len(ufc_fight_stats) + 1)]
    fighter_id = [num for num in range(1, len(ufc_fighters) + 1)]

    # Check if primary key is already present in table
    # If not present, adds primary key to each table
    # (reversed so that new data will retain same primary key order)
    if 'event_id' not in ufc_events.columns:
        ufc_events['event_id'] = event_id[::-1]

    if 'fight_id' not in ufc_fights.columns:
        ufc_fights['fight_id'] = fight_id[::-1]

    if 'fight_stat_id' not in ufc_fight_stats.columns:
        ufc_fight_stats['fight_stat_id'] = fight_stat_id[::-1]

    if 'fighter_id' not in ufc_fighters.columns:
        ufc_fighters['fighter_id'] = fighter_id[::-1]


def add_foreign_key(  # noqa: C901
    ufc_events: pd.DataFrame,
    ufc_fights: pd.DataFrame,
    ufc_fight_stats: pd.DataFrame,
    ufc_fighters: pd.DataFrame,
) -> None:
    """
    Create dictionaries of primary keys and column in primary
    table to match with foreign table
    """

    # Add fighter name column to ufc_fighters match with fighter names
    # in ufc_fights/ufc_fight_stats
    ufc_fighters['fighter_name'] = (
        ufc_fighters['fighter_f_name'] + ' ' + ufc_fighters['fighter_l_name']
    )

    # Dictionary of all event names and their corresponding ID
    event_id_dict = {}
    for num in range(len(ufc_events)):
        event_id_dict[ufc_events.loc[num, 'event_name']] = ufc_events.loc[
            num, 'event_id'
        ]

    # Dictionary of all fight urls and their corresponding ID
    fight_url_dict = {}
    for num in range(len(ufc_fights)):
        fight_url_dict[ufc_fights.loc[num, 'fight_url']] = ufc_fights.loc[
            num, 'fight_id'
        ]

    # Dictionary of all fighter names and their corresponding ID
    fighter_id_dict = {}
    for num in range(len(ufc_fighters)):
        fighter_id_dict[ufc_fighters.loc[num, 'fighter_name']] = ufc_fighters.loc[
            num, 'fighter_id'
        ]

    # Add event_id to ufc_fights if not already present
    if 'event_id' not in ufc_fights.columns:
        ufc_fights['event_id'] = ufc_events['event_name'].map(event_id_dict)

    # Replace fighter names in ufc_fights with their fighter_id if not already changed
    try:
        if isinstance(ufc_fights['f_1'][0], str):
            ufc_fights['f_1'] = ufc_fights['f_1'].map(fighter_id_dict)
    except KeyError:
        print(f'KeyError: "f_1", {ufc_fights.keys()}')

    try:
        if isinstance(ufc_fights['f_2'][0], str):
            ufc_fights['f_2'] = ufc_fights['f_2'].map(fighter_id_dict)
    except KeyError:
        print(f'KeyError: "f_2", {ufc_fights.keys()}')

    try:
        if isinstance(ufc_fights['winner'][0], str):
            ufc_fights['winner'] = ufc_fights['winner'].map(fighter_id_dict)
    except KeyError:
        print(f'KeyError: "winner", {ufc_fights.keys()}')

    # Replace fighter names in ufc_fight_stats with their fighter_id
    try:
        if isinstance(ufc_fight_stats['fighter_id'], str):
            ufc_fight_stats['fighter_id'] = ufc_fight_stats['fighter_id'].map(
                fighter_id_dict
            )
    except KeyError:
        print(f'KeyError: "fighter_id", {ufc_fights.keys()}')

    # Add fight_id to ufc_fight_stats
    try:
        if 'fight_id' not in ufc_fight_stats.columns:
            ufc_fight_stats['fight_id'] = ufc_fight_stats['fight_url'].map(
                fight_url_dict
            )
    except KeyError:
        print(f'KeyError: "fight_id", {ufc_fights.keys()}')


def save_to_file(
    ufc_events: pd.DataFrame,
    ufc_fights: pd.DataFrame,
    ufc_fight_stats: pd.DataFrame,
    ufc_fighters: pd.DataFrame,
) -> None:
    """Save to files"""

    # Set columns for final output
    ufc_events = ufc_events[EVENT_COLUMNS]
    ufc_fights = ufc_fights[FIGHT_COLUMNS]
    ufc_fight_stats = ufc_fight_stats[FIGHTSTATS_COLUMNS]
    ufc_fighters = ufc_fighters[FIGHTER_COLUMNS]

    # Set primary key as index
    ufc_events.set_index('event_id', inplace=True)
    ufc_fights.set_index('fight_id', inplace=True)
    ufc_fight_stats.set_index('fight_stat_id', inplace=True)
    ufc_fighters.set_index('fighter_id', inplace=True)

    ufc_events.to_csv(EVENT_DATA_PATH)
    ufc_fights.to_csv(FIGHT_DATA_PATH)
    ufc_fight_stats.to_csv(FIGHTSTATS_DATA_PATH)
    ufc_fighters.to_csv(FIGHTER_DATA_PATH)


def normalise_tables():

    ufc_events = pd.read_csv(EVENT_DATA_PATH)
    ufc_fights = pd.read_csv(FIGHT_DATA_PATH)
    ufc_fight_stats = pd.read_csv(FIGHTSTATS_DATA_PATH)
    ufc_fighters = pd.read_csv(FIGHTER_DATA_PATH)

    print('Adding primary keys')
    add_primary_keys(ufc_events, ufc_fights, ufc_fight_stats, ufc_fighters)

    print('Adding foreign keys')
    add_foreign_key(ufc_events, ufc_fights, ufc_fight_stats, ufc_fighters)

    save_to_file(ufc_events, ufc_fights, ufc_fight_stats, ufc_fighters)
    print('Tables normalised')
