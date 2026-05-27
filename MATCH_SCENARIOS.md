# Taxonomy of Rain-Interrupted Match Scenarios

This document classifies the various permutations of match interruptions in limited-overs cricket. These scenarios provide the structural framework for applying the Deterministic Mathematical Framework (Modha Method).

## Category A: Completed First Innings
In these scenarios, Team A has utilized their full scheduled resource capacity (either by playing all overs or getting all out).

### 1. Post-Innings Truncation
*   **Description:** Team A completes their full innings. Rain occurs during the break. Team B’s chase is reduced in length before the first ball of the second innings.
*   **Example:** 
    *   Team A: 320/5 (50.0)
    *   Interruption: Heavy rain during lunch.
    *   Team B: Revised target for 20.0 overs.

### 2. Mid-Chase Truncation (Dynamic Reduction)
*   **Description:** Team A completes their full innings. Team B starts their chase, but rain interrupts play and reduces the remaining overs available to Team B.
*   **Example:** 
    *   Team A: 280/8 (50.0)
    *   Team B: 120/2 (25.0)
    *   Interruption: Rain at the 25-over mark. Chase reduced to 40.0 overs total.

### 3. Retrospective Termination (The Snapshot Finish)
*   **Description:** Team A completes their full innings. Team B starts their chase, but rain stops play and no further cricket is possible. The result is determined by the state of the match at the moment of the final ball bowled.
*   **Example:** 
    *   Team A: 190/10 (20.0)
    *   Team B: 110/3 (12.4)
    *   Interruption: Match abandoned. Result decided by Par Score at 12.4 overs.

---

## Category B: Truncated First Innings
In these scenarios, Team A is prevented from utilizing their original scheduled resource capacity.

### 4. Premature Termination (Innings 1)
*   **Description:** Team A is batting when rain stops play permanently for their innings. Team B is then set a target for a match of equal or further reduced length.
*   **Example:** 
    *   Team A: 145/4 (32.0/50.0)
    *   Interruption: Rain ends Innings 1.
    *   Team B: Set a target for a 32-over (or shorter) chase.

### 5. Mid-Play Reduction (The "Accordion" Innings)
*   **Description:** Team A is batting when rain stops play. Play resumes, but Team A's overs are reduced mid-innings. Team A finishes their reduced innings, and Team B then chases the same (or a further reduced) number of overs.
*   **Example:** 
    *   Team A: 100/2 (20.0/50.0)
    *   Interruption: Rain reduces match to 35 overs per side.
    *   Team A Resumes: Finishes 210/6 (35.0).
    *   Team B: Chases in 35.0 overs.

---

## Category C: Null Scenarios

### 6. Sub-Threshold Abandonment (No Result)
*   **Description:** The match is abandoned before the minimum number of overs required for a legal result (e.g., 20 overs in ODI, 5 overs in T20) has been completed in the second innings.
*   **Example:** 
    *   Team A: 300/5 (50.0)
    *   Team B: 40/0 (4.0)
    *   Interruption: Match abandoned. 
    *   **Result:** No Result (NR).
