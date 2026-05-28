from derivation.overs import get_over_weights
from derivation.wickets import get_wicket_weights

# Configuration for Derivation
T20_CONFIG = {
    'phase_map': {1: 6, 2: 15, 3: 20},
    'over_target': 160,
    'wicket_target': 40
}

ODI_CONFIG = {
    'phase_map': {1: 10, 2: 40, 3: 50},
    'over_target': 140,
    'wicket_target': 60
}

# Dynamic Derivation (Run once at module import)
# This performs the 'data ops' and stores result in variables
T20_OVER_VALS = get_over_weights('t20', T20_CONFIG['phase_map'], T20_CONFIG['over_target'])
T20_WKT_VALS = get_wicket_weights('t20', T20_CONFIG['wicket_target'])

ODI_OVER_VALS = get_over_weights('odi', ODI_CONFIG['phase_map'], ODI_CONFIG['over_target'])
ODI_WKT_VALS = get_wicket_weights('odi', ODI_CONFIG['wicket_target'])

T20_WEIGHTS = {
    'overs': T20_OVER_VALS,
    'wickets': T20_WKT_VALS,
    'phase_map': T20_CONFIG['phase_map'],
    'over_target': T20_CONFIG['over_target'],
    'wicket_target': T20_CONFIG['wicket_target']
}

ODI_WEIGHTS = {
    'overs': ODI_OVER_VALS,
    'wickets': ODI_WKT_VALS,
    'phase_map': ODI_CONFIG['phase_map'],
    'over_target': ODI_CONFIG['over_target'],
    'wicket_target': ODI_CONFIG['wicket_target']
}
