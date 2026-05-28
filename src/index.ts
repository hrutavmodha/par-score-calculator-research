import type { MatchFormat, MatchState, ParScoreResult } from '../types/index.ts';

/**
 * Crux - Cross-Resource Utilization Index Method
 * A deterministic model for calculating revised targets in limited-overs cricket.
 */
export class CruxCalculator {
  readonly #P_TOTAL = 200;

  /**
   * Calculates the total resource footprint consumed by a team.
   */
  public calculateResourceFootprint(format: MatchFormat, state: MatchState): number {
    const overs = this.#toDecimalOvers(state.overs);
    const scheduledOvers = this.#toDecimalOvers(state.scheduledOvers);
    const { wickets } = state;
    
    const overPointsUsed = this.#calculateOverPoints(format, overs);
    const totalOverCapacity = this.#calculateOverPoints(format, scheduledOvers);
    const wicketPointsUsed = this.#calculateWicketPoints(format, wickets);
    const totalWicketCapacity = format === 'T20' ? 40 : 60;

    // Forfeited Over Capacity (Wicket-Driven)
    const forfeitedOvers = (wickets / 10) * (totalOverCapacity - overPointsUsed);

    // Forfeited Wicket Survival (Over-Driven)
    const forfeitedWickets = (overs / scheduledOvers) * (totalWicketCapacity - wicketPointsUsed);

    return overPointsUsed + wicketPointsUsed + forfeitedOvers + forfeitedWickets;
  }

  /**
   * Calculates the Dynamic Stabilizer D.
   */
  public calculateStabilizer(rUsed1: number): number {
    return Math.ceil((this.#P_TOTAL - rUsed1) / 4);
  }

  /**
   * Calculates the Par Score and Target.
   */
  public calculateTarget(
    format: MatchFormat,
    teamA: MatchState,
    teamBAtInterruption: MatchState
  ): ParScoreResult {
    const rUsed1 = this.calculateResourceFootprint(format, teamA);
    const rUsed2 = this.calculateResourceFootprint(format, teamBAtInterruption);
    const stabilizerD = this.calculateStabilizer(rUsed1);

    const parScore = teamA.score * ((rUsed2 + stabilizerD) / (rUsed1 + stabilizerD));
    const target = Math.floor(parScore) + 1;

    return { parScore, target };
  }

  /**
   * Logs a detailed simulation result to the console.
   */
  public logSimulationResult(
    name: string,
    format: MatchFormat,
    teamA: MatchState,
    teamB: MatchState
  ): void {
    const rUsed1 = this.calculateResourceFootprint(format, teamA);
    const rUsed2 = this.calculateResourceFootprint(format, teamB);
    const stabilizerD = this.calculateStabilizer(rUsed1);
    const { parScore, target } = this.calculateTarget(format, teamA, teamB);

    console.log(`==================================================`);
    console.log(`SCENARIO: ${name}`);
    console.log(`FORMAT:   ${format}`);
    console.log(`--------------------------------------------------`);
    console.log(`Team A: ${teamA.score}/${teamA.wickets} (${teamA.overs.toFixed(1)})`);
    console.log(`Team B: ${teamB.score}/${teamB.wickets} (${teamB.overs.toFixed(1)}) [At Interruption]`);
    console.log(`Scheduled: ${teamA.scheduledOvers.toFixed(1)} overs`);
    console.log(`--------------------------------------------------`);
    console.log(`[Resources]`);
    console.log(`R_used,1 (Team A): ${rUsed1.toFixed(4)} pts`);
    console.log(`R_used,2 (Team B): ${rUsed2.toFixed(4)} pts`);
    console.log(`Stabilizer (D):   ${stabilizerD} pts`);
    console.log(`--------------------------------------------------`);
    console.log(`[Result]`);
    console.log(`Par Score:        ${parScore.toFixed(2)}`);
    console.log(`Target:           ${target} runs`);
    console.log(`==================================================\n`);
  }

  /**
   * Converts cricket-style overs (e.g. 18.4) to 10-base decimals (e.g. 18.6667).
   */
  #toDecimalOvers(overs: number): number {
    const fullOvers = Math.floor(overs);
    const balls = Math.round((overs - fullOvers) * 10);
    
    if (balls >= 6) {
      throw new Error(`Invalid overs format: ${overs}. Balls component cannot be 6 or more.`);
    }
    
    return fullOvers + balls / 6;
  }

  /**
   * Piecewise Step Function for Over Points O(u).
   */
  #calculateOverPoints(format: MatchFormat, overs: number): number {
    if (format === 'T20') {
      // Empirically derived (Full Members, 1st Innings, Since 2021): 7.47, 7.65, 9.27
      if (overs <= 6) return overs * 7.47;
      if (overs <= 15) return 44.82 + (overs - 6) * 7.65;
      return 113.67 + (overs - 15) * 9.27;
    } 
    
    // ODI: Empirically derived (Full Members, 1st Innings, Since 2021): 2.40, 2.60, 3.80
    if (overs <= 10) return overs * 2.40;
    if (overs <= 40) return 24.0 + (overs - 10) * 2.60;
    return 102.0 + (overs - 40) * 3.80;
  }

  /**
   * Piecewise Step Function for Wicket Points W(w).
   */
  #calculateWicketPoints(format: MatchFormat, wickets: number): number {
    if (format === 'T20') {
      // Empirically derived (Full Members, 1st Innings, Since 2021): 7.24, 4.07, 0.67
      if (wickets <= 3) return wickets * 7.24;
      if (wickets <= 7) return 21.72 + (wickets - 3) * 4.07;
      return 37.99 + (wickets - 7) * 0.67;
    } 
    
    // ODI: Empirically derived (Full Members, 1st Innings, Since 2021): 9.37, 6.53, 1.92
    if (wickets <= 3) return wickets * 9.37;
    if (wickets <= 7) return 28.12 + (wickets - 3) * 6.53;
    return 54.24 + (wickets - 7) * 1.92;
  }
}
