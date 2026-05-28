import json
import os
from derivation.overs import get_over_weights
from derivation.wickets import get_wicket_weights

CACHE_FILE = "data/weights_cache.json"

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

class WeightManager:
    def __init__(self):
        self._weights = self._load_from_cache()

    def _load_from_cache(self):
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, 'r') as f:
                    data = json.load(f)
                    # Convert string keys back to int for phase_map and overs
                    for fmt in ['T20', 'ODI']:
                        if fmt in data:
                            data[fmt]['phase_map'] = {int(k): v for k, v in data[fmt]['phase_map'].items()}
                            data[fmt]['overs'] = {int(k): v for k, v in data[fmt]['overs'].items()}
                    return data
            except (json.JSONDecodeError, KeyError, ValueError):
                # Fallback to update if cache is corrupted
                return self.update()
        return self.update()

    def update(self):
        """Explicitly recalculates weights and saves to disk."""
        t20_over = get_over_weights('t20', T20_CONFIG['phase_map'], T20_CONFIG['over_target'])
        t20_wkt = get_wicket_weights('t20', T20_CONFIG['wicket_target'])
        
        odi_over = get_over_weights('odi', ODI_CONFIG['phase_map'], ODI_CONFIG['over_target'])
        odi_wkt = get_wicket_weights('odi', ODI_CONFIG['wicket_target'])

        self._weights = {
            'T20': {
                'overs': t20_over, 
                'wickets': t20_wkt, 
                'phase_map': T20_CONFIG['phase_map'],
                'over_target': T20_CONFIG['over_target'],
                'wicket_target': T20_CONFIG['wicket_target']
            },
            'ODI': {
                'overs': odi_over, 
                'wickets': odi_wkt, 
                'phase_map': ODI_CONFIG['phase_map'],
                'over_target': ODI_CONFIG['over_target'],
                'wicket_target': ODI_CONFIG['wicket_target']
            }
        }
        
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, 'w') as f:
            json.dump(self._weights, f, indent=2)
            
        return self._weights

    def get_weights(self, format_name):
        if format_name not in self._weights:
             raise ValueError(f"Invalid format name '{format_name}'")
        return self._weights[format_name]

# Singleton instance for the calculator to use
weights_manager = WeightManager()

# Export for backward compatibility or direct access if needed
T20_WEIGHTS = weights_manager.get_weights('T20')
ODI_WEIGHTS = weights_manager.get_weights('ODI')
