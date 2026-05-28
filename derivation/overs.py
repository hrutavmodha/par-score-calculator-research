import pandas as pd
import numpy as np
import glob
from datetime import datetime

FULL_MEMBERS = {
    'Afghanistan', 'Australia', 'Bangladesh', 'England', 'India', 
    'Ireland', 'New Zealand', 'Pakistan', 'South Africa', 
    'Sri Lanka', 'West Indies', 'Zimbabwe'
}

def analyze_overs(format_name, phase_map, total_over_points):
    phases = sorted(phase_map.keys())
    files = glob.glob(f'data/{format_name}/*.csv')
    ball_files = [f for f in files if not f.endswith('_info.csv')]
    
    all_runs = []
    
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
            
            df_1st['over_val'] = df_1st['ball'].astype(int) + 1
            df_1st['runs'] = df_1st['runs_off_bat'] + df_1st['extras']
            
            all_runs.append(df_1st[['over_val', 'runs']])
        except Exception:
            continue

    master_df = pd.concat(all_runs)
    
    phase_stats = []
    total_expected_runs = 0
    
    prev_over = 0
    for p in phases:
        max_over = phase_map[p]
        # Filter rows in this phase
        phase_df = master_df[(master_df['over_val'] > prev_over) & (master_df['over_val'] <= max_over)]
        
        # RPO = (Total Runs / Total Balls) * 6
        rpo = (phase_df['runs'].sum() / len(phase_df)) * 6
        phase_len = max_over - prev_over
        total_expected_runs += rpo * phase_len
        
        phase_stats.append({
            'phase': p,
            'rpo': rpo,
            'len': phase_len
        })
        prev_over = max_over

    normalization_factor = total_over_points / total_expected_runs
    
    print(f"\n--- {format_name.upper()} Over Calibration ({len(all_runs)} matches) ---")
    print(f"Total Expected Runs (1st Innings): {total_expected_runs:.2f}")
    print(f"Derived Weights:")
    for s in phase_stats:
        weight = s['rpo'] * normalization_factor
        print(f"Phase {s['phase']} (Over {phase_map[s['phase']]}): {weight:.2f} pts/over (RPO: {s['rpo']:.2f})")

# T20 Phases (Target 160 points for overs)
t20_phases = {1: 6, 2: 15, 3: 20}
analyze_overs('t20', t20_phases, 160)

# ODI Phases (Target 140 points for overs)
odi_phases = {1: 10, 2: 40, 3: 50}
analyze_overs('odi', odi_phases, 140)
