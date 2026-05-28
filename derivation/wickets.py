import pandas as pd
import glob
from datetime import datetime
from typing import Dict, Tuple
from derivation.full_members import FULL_MEMBERS

def get_wicket_weights(format_name: str, total_wicket_points: int) -> Tuple[float, float, float]:
    files = glob.glob(f'data/{format_name}/*.csv')
    ball_files = [f for f in files if not f.endswith('_info.csv')]
    
    match_data = []
    
    for f in ball_files:
        try:
            df = pd.read_csv(f)
            if df.empty: continue
            
            match_date = datetime.strptime(df['start_date'].iloc[0], '%Y-%m-%d')
            if match_date < datetime(2021, 1, 1): continue
            
            teams = {df['batting_team'].iloc[0], df['bowling_team'].iloc[0]}
            if not teams.issubset(FULL_MEMBERS): continue
            
            df_1st = df[df['innings'] == 1].copy()
            if df_1st.empty: continue
            
            df_1st['total_runs'] = df_1st['runs_off_bat'] + df_1st['extras']
            df_1st['cum_runs'] = df_1st['total_runs'].cumsum()
            
            df_wickets = df_1st[df_1st['player_dismissed'].notnull()].reset_index()
            
            runs_at_all_out = df_1st['cum_runs'].iloc[-1]
            runs_at_3 = df_wickets['cum_runs'].iloc[2] if len(df_wickets) >= 3 else runs_at_all_out
            runs_at_7 = df_wickets['cum_runs'].iloc[6] if len(df_wickets) >= 7 else runs_at_all_out
                
            match_data.append({'r3': runs_at_3, 'r7': runs_at_7, 'rtotal': runs_at_all_out})
        except Exception:
            continue

    if not match_data:
        return (0.0, 0.0, 0.0)

    res = pd.DataFrame(match_data)
    avg_r3 = res['r3'].mean()
    avg_r7 = res['r7'].mean()
    avg_total = res['rtotal'].mean()
    
    w_top = (avg_r3 / avg_total) * total_wicket_points
    w_mid = ((avg_r7 - avg_r3) / avg_total) * total_wicket_points
    w_tail = ((avg_total - avg_r7) / avg_total) * total_wicket_points
    
    # Return average points per wicket in each tier
    return (w_top/3, w_mid/4, w_tail/3)
