import pandas as pd
import numpy as np
import glob
import os
from datetime import datetime

FULL_MEMBERS = {
    'Afghanistan', 'Australia', 'Bangladesh', 'England', 'India', 
    'Ireland', 'New Zealand', 'Pakistan', 'South Africa', 
    'Sri Lanka', 'West Indies', 'Zimbabwe'
}

def analyze_wickets(format_name, total_wicket_points):
    files = glob.glob(f'data/{format_name}/*.csv')
    ball_files = [f for f in files if not f.endswith('_info.csv')]
    
    match_data = []
    
    for f in ball_files:
        try:
            df = pd.read_csv(f)
            if df.empty: continue
            
            # Filter: Since 2021, Full Members, 1st Innings
            match_date = datetime.strptime(df['start_date'].iloc[0], '%Y-%m-%d')
            if match_date < datetime(2021, 1, 1): continue
            
            teams = {df['batting_team'].iloc[0], df['bowling_team'].iloc[0]}
            if not teams.issubset(FULL_MEMBERS): continue
            
            df_1st = df[df['innings'] == 1].copy()
            if df_1st.empty: continue
            
            # Cumulative runs and wickets
            df_1st['total_runs'] = df_1st['runs_off_bat'] + df_1st['extras']
            df_1st['cum_runs'] = df_1st['total_runs'].cumsum()
            
            # Track wicket fall runs
            # player_dismissed is non-null when a wicket falls
            df_wickets = df_1st[df_1st['player_dismissed'].notnull()].reset_index()
            
            runs_at_3 = 0
            runs_at_7 = 0
            runs_at_all_out = df_1st['cum_runs'].iloc[-1]
            
            if len(df_wickets) >= 3:
                runs_at_3 = df_wickets['cum_runs'].iloc[2] # 0-indexed index 2 is 3rd wicket
            else:
                runs_at_3 = runs_at_all_out
                
            if len(df_wickets) >= 7:
                runs_at_7 = df_wickets['cum_runs'].iloc[6]
            else:
                runs_at_7 = runs_at_all_out
                
            match_data.append({
                'r3': runs_at_3,
                'r7': runs_at_7,
                'rtotal': runs_at_all_out
            })
        except Exception:
            continue

    res = pd.DataFrame(match_data)
    avg_r3 = res['r3'].mean()
    avg_r7 = res['r7'].mean()
    avg_total = res['rtotal'].mean()
    
    # Formulas provided:
    # Top Order (1-3): (RunsWhen3rdWicketFall / TotalRuns) * WicketPoints
    # Middle Order (4-7): ((RunsWhen7thWicketFall - RunsWhen3rdWicketFall) / TotalRuns) * WicketPoints
    # Lower Order (8-10): ((RunsWhenTeamGotAllOut - RunsWhen7thWicketFall) / TotalRuns) * WicketPoints
    
    w_top = (avg_r3 / avg_total) * total_wicket_points
    w_mid = ((avg_r7 - avg_r3) / avg_total) * total_wicket_points
    w_tail = ((avg_total - avg_r7) / avg_total) * total_wicket_points
    
    print(f"\n--- {format_name.upper()} Wicket Calibration ({len(match_data)} matches) ---")
    print(f"Avg Runs at W3: {avg_r3:.2f}")
    print(f"Avg Runs at W7: {avg_r7:.2f}")
    print(f"Avg Total:     {avg_total:.2f}")
    print(f"Derived Weights:")
    print(f"Top Order (1-3):   {w_top/3:.2f} pts/wicket (Total: {w_top:.2f})")
    print(f"Middle Order (4-7): {w_mid/4:.2f} pts/wicket (Total: {w_mid:.2f})")
    print(f"Tailenders (8-10):  {w_tail/3:.2f} pts/wicket (Total: {w_tail:.2f})")
    print(f"Sum: {w_top + w_mid + w_tail:.2f}")

analyze_wickets('t20', 40)
analyze_wickets('odi', 60)
