import { CruxCalculator } from '../src/index.ts';

const calculator = new CruxCalculator();

/**
 * 1. The Hyper-Extreme Scenario from Section 5.1.1
 * Team A: 72/0 (2.0)
 * Team B: 0/0 (1.0)
 */
calculator.logSimulationResult(
  "Hyper-Extreme 2-Over Burst (Section 5.1.1)",
  "T20",
  { score: 72, wickets: 0, overs: 2, scheduledOvers: 2 },
  { score: 0, wickets: 0, overs: 1, scheduledOvers: 2 }
);

/**
 * 2. Standard T20 Rain Delay
 */
calculator.logSimulationResult(
  "Standard T20 Rain Delay",
  "T20",
  { score: 180, wickets: 5, overs: 20, scheduledOvers: 20 },
  { score: 85, wickets: 2, overs: 10, scheduledOvers: 20 }
);

/**
 * 3. ODI Late Match Interruption
 */
calculator.logSimulationResult(
  "ODI Late Match Interruption",
  "ODI",
  { score: 320, wickets: 8, overs: 50, scheduledOvers: 50 },
  { score: 240, wickets: 4, overs: 40, scheduledOvers: 50 }
);

/**
 * 4. Middle Over Collapse (Team A all out)
 */
calculator.logSimulationResult(
  "Team A All-Out vs Team B Interruption",
  "T20",
  { score: 160, wickets: 10, overs: 18.4, scheduledOvers: 20 },
  { score: 100, wickets: 6, overs: 15, scheduledOvers: 20 }
);

/**
 * 5. Fractional Overs Test
 * Team B at 15.2 overs (should be 15.3333 dec)
 */
calculator.logSimulationResult(
  "Fractional Overs Test (15.2 overs)",
  "T20",
  { score: 180, wickets: 5, overs: 20, scheduledOvers: 20 },
  { score: 100, wickets: 4, overs: 15.2, scheduledOvers: 20 }
);
