from src.calculator import CruxCalculator, MatchState

def run_test_case(name: str, format_name: str, team_a: MatchState, team_b: MatchState):
    calc = CruxCalculator()
    result = calc.calculate_target(format_name, team_a, team_b)
    
    print(f"--- {name} ---")
    print(f"Team A: {team_a['score']}/{team_a['wickets']} in {team_a['overs']} overs")
    print(f"Team B (at int): {team_b['score']}/{team_b['wickets']} in {team_b['overs']} overs")
    print(f"Crux Par Score: {result['parScore']:.2f}")
    print(f"Crux Target:    {result['target']} runs")
    print("-" * (len(name) + 8))
    print()

def main():
    # Case 1: 1992 WC Semi-Final (England vs SA)
    # Note: Using 42.5 in input for "42 overs and 5 balls"
    england_1992: MatchState = {
        'score': 252,
        'wickets': 6,
        'overs': 45.0,
        'scheduledOvers': 45.0
    }
    sa_1992: MatchState = {
        'score': 231,
        'wickets': 6,
        'overs': 42.5, 
        'scheduledOvers': 45.0
    }

    # Case 2: 2003 WC (Sri Lanka vs SA)
    sri_lanka_2003: MatchState = {
        'score': 268,
        'wickets': 9,
        'overs': 50.0,
        'scheduledOvers': 50.0
    }
    sa_2003: MatchState = {
        'score': 229,
        'wickets': 6,
        'overs': 45.0,
        'scheduledOvers': 50.0
    }

    run_test_case("1992 WC SF: England vs South Africa", "ODI", england_1992, sa_1992)
    run_test_case("2003 WC: Sri Lanka vs South Africa", "ODI", sri_lanka_2003, sa_2003)

if __name__ == "__main__":
    main()
