/**
 * Crux - Type Definitions
 */

export type MatchFormat = 'T20' | 'ODI';

export interface MatchState {
  score: number;
  wickets: number;
  overs: number;
  scheduledOvers: number;
}

export interface ParScoreResult {
  parScore: number;
  target: number;
}
