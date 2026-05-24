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
    const { overs, wickets, scheduledOvers } = state;
    
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
   * Piecewise Step Function for Over Points O(u).
   */
  #calculateOverPoints(format: MatchFormat, overs: number): number {
    if (format === 'T20') {
      // 9-4-14 ratio for 160 total points
      if (overs <= 6) return overs * 9;
      if (overs <= 15) return 54 + (overs - 6) * 4;
      return 90 + (overs - 15) * 14;
    } 
    
    // ODI: 3-2-5 ratio for 140 total points
    if (overs <= 10) return overs * 3;
    if (overs <= 40) return 30 + (overs - 10) * 2;
    return 90 + (overs - 40) * 5;
  }

  /**
   * Piecewise Step Function for Wicket Points W(w).
   */
  #calculateWicketPoints(format: MatchFormat, wickets: number): number {
    if (format === 'T20') {
      // 6-4-2 ratio for 40 total points
      if (wickets <= 3) return wickets * 6;
      if (wickets <= 7) return 18 + (wickets - 3) * 4;
      return 34 + (wickets - 7) * 2;
    } 
    
    // ODI: 9-6-3 ratio for 60 total points
    if (wickets <= 3) return wickets * 9;
    if (wickets <= 7) return 27 + (wickets - 3) * 6;
    return 51 + (wickets - 7) * 3;
  }
}
