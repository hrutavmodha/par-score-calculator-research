import math
from typing import TypedDict, Literal, Optional
from src.weights import weights_manager

MatchFormat = Literal['T20', 'ODI']

class MatchState(TypedDict):
    score: int
    wickets: int
    overs: float
    scheduledOvers: float

class ParScoreResult(TypedDict):
    parScore: float
    target: int

class CruxCalculator:
    def __init__(self):
        pass

    def update_weights(self):
        """Manually trigger a recalculation of the weights."""
        return weights_manager.update()

    def _get_weights(self, format_name: MatchFormat):
        try:
            return weights_manager.get_weights(format_name)
        except ValueError as e:
            raise Exception(str(e))

    def get_total_capacity(self, format_name: MatchFormat, scheduled_overs: float) -> float:
        weights = self._get_weights(format_name)
        scheduled_dec = self._to_decimal_overs(scheduled_overs)
        total_over_cap = self._calculate_over_points(format_name, scheduled_dec, weights)
        total_wicket_cap = weights['wicket_target']
        return total_over_cap + total_wicket_cap

    def calculate_resource_footprint(self, format_name: MatchFormat, state: MatchState) -> float:
        weights = self._get_weights(format_name)
        
        overs_dec = self._to_decimal_overs(state['overs'])
        scheduled_dec = self._to_decimal_overs(state['scheduledOvers'])
        wickets = state['wickets']

        over_pts_used = self._calculate_over_points(format_name, overs_dec, weights)
        total_over_cap = self._calculate_over_points(format_name, scheduled_dec, weights)
        wicket_pts_used = self._calculate_wicket_points(format_name, wickets, weights)
        total_wicket_cap = weights['wicket_target']

        # Forfeited Over Capacity (Wicket-Driven)
        forfeited_overs = (wickets / 10.0) * (total_over_cap - over_pts_used)

        # Forfeited Wicket Survival (Over-Driven)
        forfeited_wickets = (overs_dec / scheduled_dec) * (total_wicket_cap - wicket_pts_used)

        return over_pts_used + wicket_pts_used + forfeited_overs + forfeited_wickets

    def calculate_stabilizer(self, r_used1: float, capacity1: float) -> int:
        return math.ceil((capacity1 - r_used1) / 4.0)

    def calculate_target(self, format_name: MatchFormat, team_a: MatchState, team_b_at_int: MatchState) -> ParScoreResult:
        r_used1 = self.calculate_resource_footprint(format_name, team_a)
        r_used2 = self.calculate_resource_footprint(format_name, team_b_at_int)
        
        # Stance B: Use specifically scheduled capacity as the reference baseline
        ref_cap1 = self.get_total_capacity(format_name, team_a['scheduledOvers'])
        stabilizer_d = self.calculate_stabilizer(r_used1, ref_cap1)

        par_score = team_a['score'] * ((r_used2 + stabilizer_d) / (r_used1 + stabilizer_d))
        target = math.floor(par_score) + 1

        return {'parScore': par_score, 'target': target}

    def _to_decimal_overs(self, overs: float) -> float:
        full_overs = math.floor(overs)
        balls = round((overs - full_overs) * 10)
        if balls >= 6:
            raise ValueError(f"Invalid overs format: {overs}. Balls component cannot be 6 or more.")
        return full_overs + balls / 6.0

    def _calculate_over_points(self, format_name: MatchFormat, overs: float, weights: dict) -> float:
        w = weights['overs']
        pm = weights['phase_map']
        
        if format_name == 'T20':
            if overs <= pm[1]: return overs * w[1]
            if overs <= pm[2]: return (pm[1] * w[1]) + (overs - pm[1]) * w[2]
            return (pm[1] * w[1]) + (pm[2] - pm[1]) * w[2] + (overs - pm[2]) * w[3]
        elif format_name == 'ODI':
            if overs <= pm[1]: return overs * w[1]
            if overs <= pm[2]: return (pm[1] * w[1]) + (overs - pm[1]) * w[2]
            return (pm[1] * w[1]) + (pm[2] - pm[1]) * w[2] + (overs - pm[2]) * w[3]
        else:
            raise Exception(f"Invalid format: '{format_name}'")
    def _calculate_wicket_points(self, format_name: MatchFormat, wickets: int, weights: dict) -> float:
        w = weights['wickets'] # (top, mid, tail) average per wicket
        if wickets <= 3:
            return wickets * w[0]
        if wickets <= 7:
            return (3 * w[0]) + (wickets - 3) * w[1]
        return (3 * w[0]) + (4 * w[1]) + (min(wickets, 10) - 7) * w[2]
