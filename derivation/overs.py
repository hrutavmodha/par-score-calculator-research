import pandas as pd
import glob
from datetime import datetime
from typing import Dict

FULL_MEMBERS = {
    'Afghanistan', 'Australia', 'Bangladesh', 'England', 'India', 
    'Ireland', 'New Zealand', 'Pakistan', 'South Africa', 
    'Sri Lanka', 'West Indies', 'Zimbabwe'
}

def get_over_weights(format_name: str, phase_map: Dict[int, int], total_over_points: int) -> Dict[int, float]:
    phases = sorted(phase_map.keys())
    files = glob.glob(f'data/{format_name}/*.csv')
    ball_files = [f for f in files if not f.endswith('_info.csv')]
    
    all_runs = []
    
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
            
            df_1st['over_val'] = df_1st['ball'].astype(int) + 1
            df_1st['runs'] = df_1st['runs_off_bat'] + df_1st['extras']
            
            all_runs.append(df_1st[['over_val', 'runs']])
        except Exception:
            continue

    if not all_runs:
        return {p: 0.0 for p in phases}

    master_df = pd.concat(all_runs)
    total_expected_runs = 0
    phase_rpos = {}
    
    prev_over = 0
    for p in phases:
        max_over = phase_map[p]
        phase_df = master_df[(master_df['over_val'] > prev_over) & (master_df['over_val'] <= max_over)]
        
        # RPO = (Total Runs / Total Balls) * 6
        rpo = (phase_df['runs'].sum() / len(phase_df)) * 6 if len(phase_df) > 0 else 0
        phase_len = max_over - prev_over
        total_expected_runs += rpo * phase_len
        phase_rpos[p] = rpo
        prev_over = max_over

    normalization_factor = total_over_points / total_expected_runs if total_expected_runs > 0 else 0
    return {p: rpo * normalization_factor for p, rpo in phase_rpos.items()}
