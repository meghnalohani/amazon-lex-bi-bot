#
# Copyright 2017-2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Amazon Software License (the "License"). You may not use this file
# except in compliance with the License. A copy of the License is located at
#
# http://aws.amazon.com/asl/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS"
# BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, express or implied. See the
# License for the specific language governing permissions and limitations under the License.

import time
import logging

#
# See additional configuration parameters at bottom 
#

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# adjust dimension values as necessary prior to inserting into where clause
def pre_process_query_value(key, value):
    logger.debug('<<Jasper>> pre_process_query_value(%s, %s)', key, value)
    value = value.replace("'", "''")    # don't allow any 's in WHERE clause
    if key == 'event_month':
        value = value[0:3]
    elif key == 'venue_name':
        value = value.lower().replace('theater', 'theatre')
        value = value.lower().replace('u. s.', 'us')
        value = value.lower().replace('u.s.', 'us')
    elif key == 'venue_state':
        value = US_STATES.get(value.lower(), value)

    logger.debug('<<Jasper>> pre_process_query_value() - returning key=%s, value=%s', key, value)
       
    return value


# adjust slot values as necessary after reading from intent slots
def post_process_slot_value(key, value):
    if key == 'venue_state':
        value = US_STATES.get(value.lower(), value)
        logger.debug('<<Jasper>> post_process_slot_value() - returning key=%s, value=%s', key, value)
    return value


def post_process_dimension_output(key, value):
    logger.debug('<<Jasper>> post_process_dimension_output(%s, %s)', key, value)
    if key == 'states':
        value = get_state_name(value)
    elif key == 'months':
        value = get_month_name(value)
    logger.debug('<<Jasper>> post_process_dimension_output() - returning key=%s, value=%s', key, value)
    return value


#
# user exit functions for pre- and post-processors
#

def get_state_name(value):
    if not isinstance(value, str): return value
    state_name = REVERSE_US_STATES.get(value.upper())
    return state_name if state_name else value.title()


def get_month_name(value):
    if not isinstance(value, str): return value
    month_name = MONTH_NAMES.get(value.upper()[0:3])
    return month_name if month_name else value.title()


def post_process_venue_name(value):
    if not isinstance(value, str): return value
    value = value.title().replace('Us ', 'US ')
    return value

DIMENSION_FORMATTERS = {
    'event_name':  {'format': 'For {}',              'function': str.title},
    'event_month': {'format': 'In the month of {}',  'function': get_month_name},
    'venue_name':  {'format': 'At {}',               'function': post_process_venue_name},
    'venue_city':  {'format': 'In the city of {}',   'function': str.title},
    'venue_state': {'format': 'In the state of {}',  'function': get_state_name},
    'cat_desc':    {'format': 'For {}',              'function': str.title}
}

MONTH_NAMES = {
    "JAN": "January",
    "FEB": "February",
    "MAR": "March",
    "APR": "April",
    "MAY": "May",
    "JUN": "June",
    "JUL": "July",
    "AUG": "August",
    "SEP": "September",
    "OCT": "October",
    "NOV": "November",
    "DEC": "December"
}

US_STATES = {
    'alaska': 'AK',
    'alabama': 'AL',
    'arkansas': 'AR',
    'american samoa': 'AS',
    'arizona': 'AZ',
    'california': 'CA',
    'colorado': 'CO',
    'connecticut': 'CT',
    'district of columbia': 'DC',
    'delaware': 'DE',
    'florida': 'FL',
    'georgia': 'GA',
    'guam': 'GU',
    'hawaii': 'HI',
    'iowa': 'IA',
    'idaho': 'ID',
    'illinois': 'IL',
    'indiana': 'IN',
    'kansas': 'KS',
    'kentucky': 'KY',
    'louisiana': 'LA',
    'massachusetts': 'MA',
    'maryland': 'MD',
    'maine': 'ME',
    'michigan': 'MI',
    'minnesota': 'MN',
    'missouri': 'MO',
    'mississippi': 'MS',
    'montana': 'MT',
    'north carolina': 'NC',
    'north dakota': 'ND',
    'nebraska': 'NE',
    'new hampshire': 'NH',
    'new jersey': 'NJ',
    'new mexico': 'NM',
    'nevada': 'NV',
    'new york': 'NY',
    'ohio': 'OH',
    'oklahoma': 'OK',
    'oregon': 'OR',
    'pennsylvania': 'PA',
    'puerto rico': 'PR',
    'rhode island': 'RI',
    'south carolina': 'SC',
    'south dakota': 'SD',
    'tennessee': 'TN',
    'texas': 'TX',
    'utah': 'UT',
    'virginia': 'VA',
    'virgin islands': 'VI',
    'vermont': 'VT',
    'washington': 'WA',
    'wisconsin': 'WI',
    'west virginia': 'WV',
    'wyoming': 'WY'
}

REVERSE_US_STATES = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AS': 'American Samoa',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'GU': 'Guam',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VI': 'Virgin Islands',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}

