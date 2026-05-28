from src.calculator import CruxCalculator, MatchState

def main():
    calc = CruxCalculator()
    
    # Sample Scenario: T20
    # Team A: 180/5 in 20.0 overs
    # Team B: 85/2 in 10.0 overs
    team_a: MatchState = {
        'score': 180,
        'wickets': 5,
        'overs': 20.0,
        'scheduledOvers': 20.0
    }
    
    team_b: MatchState = {
        'score': 85,
        'wickets': 2,
        'overs': 10.0,
        'scheduledOvers': 20.0
    }
    
    print("Calibrating weights and calculating target...")
    result = calc.calculate_target('T20', team_a, team_b)
    
    print(f"\nScenario: Standard T20 Rain Delay")
    print(f"Par Score: {result['parScore']:.2f}")
    print(f"Target:    {result['target']} runs")

if __name__ == "__main__":
    main()
