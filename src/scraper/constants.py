import os
from pathlib import Path

DIST_PATH = Path(os.getcwd()).parent / 'dist'
SCRAPED_FILES_PATH = DIST_PATH / 'scraped_files'
URL_PATH = DIST_PATH / 'urls'
EVENT_TABLE_ROWS = [
    'event_name',
    'event_date',
    'event_city',
    'event_state',
    'event_country',
    'event_url',
]
EVENT_FIELD = 'event_url'
EVENT_DATA_PATH = SCRAPED_FILES_PATH / 'ufc_event_data.csv'
EVENT_URLS = URL_PATH / 'event_urls.csv'
FIGHTER_TABLE_ROWS = [
    'fighter_f_name',
    'fighter_l_name',
    'fighter_nickname',
    'fighter_height_cm',
    'fighter_weight_lbs',
    'fighter_reach_cm',
    'fighter_stance',
    'fighter_dob',
    'fighter_w',
    'fighter_l',
    'fighter_d',
    'fighter_nc_dq',
    'fighter_url',
]
FIGHTER_FIELD = 'fighter_url'
FIGHTER_DATA_PATH = SCRAPED_FILES_PATH / 'ufc_fighter_data.csv'
FIGHTER_URLS = URL_PATH / 'fighter_urls.csv'
FIGHT_TABLE_ROWS = [
    'event_name',
    'referee',
    'f_1',
    'f_2',
    'winner',
    'num_rounds',
    'title_fight',
    'weight_class',
    'gender',
    'result',
    'result_details',
    'finish_round',
    'finish_time',
    'fight_url',
]
FIGHT_FIELD = 'fight_url'
FIGHT_DATA_PATH = SCRAPED_FILES_PATH / 'ufc_fight_data.csv'
FIGHT_URLS = URL_PATH / 'fight_urls.csv'
FIGHTSTATS_TABLE_ROWS = [
    'fighter_id',
    'knockdowns',
    'total_strikes_att',
    'total_strikes_succ',
    'sig_strikes_att',
    'sig_strikes_succ',
    'takedown_att',
    'takedown_succ',
    'submission_att',
    'reversals',
    'ctrl_time',
    'fight_url',
]
FIGHTSTATS_FIELD = 'fightstats_url'
FIGHTSTATS_DATA_PATH = SCRAPED_FILES_PATH / 'ufc_fight_stat_data.csv'
FIGHTSTATS_URLS = URL_PATH / 'fight_urls.csv'

# Define columns for final output
EVENT_COLUMNS = [
    'event_id',
    'event_name',
    'event_date',
    'event_city',
    'event_state',
    'event_country',
    'event_url',
]
FIGHT_COLUMNS = [
    'fight_id',
    'event_id',
    'referee',
    'f_1',
    'f_2',
    'winner',
    'num_rounds',
    'title_fight',
    'weight_class',
    'gender',
    'result',
    'result_details',
    'finish_round',
    'finish_time',
    'fight_url',
]
FIGHTSTATS_COLUMNS = [
    'fight_stat_id',
    'fight_id',
    'fighter_id',
    'knockdowns',
    'total_strikes_att',
    'total_strikes_succ',
    'sig_strikes_att',
    'sig_strikes_succ',
    'takedown_att',
    'takedown_succ',
    'submission_att',
    'reversals',
    'ctrl_time',
    'fight_url',
]
FIGHTER_COLUMNS = [
    'fighter_id',
    'fighter_f_name',
    'fighter_l_name',
    'fighter_nickname',
    'fighter_height_cm',
    'fighter_weight_lbs',
    'fighter_reach_cm',
    'fighter_stance',
    'fighter_dob',
    'fighter_w',
    'fighter_l',
    'fighter_d',
    'fighter_nc_dq',
    'fighter_url',
]

USER_AGENT_HEADERS = (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
    ' Chrome/135.0.0.0 Safari/537.36'
)
CONNECTION_LOST_TRYING = 3
CONNECTION_LOST_TIMOUT = 60
TO_MANY_REQUESTS_TRYING = 1
TO_MANY_REQUESTS_TIMOUT = 30
