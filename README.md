# Crux - Par Score Calculator

A deterministic, resource-based model for calculating revised targets in limited-overs cricket (ODI and T20).

## Overview

This repository implements the **Crux (Cross-Resource Utilization Index) Method**, an alternative to the Duckworth-Lewis-Stern (DLS) system for target revision in rain-affected cricket matches. 

Unlike DLS, which relies on statistical probability curves and historical averages, Crux is a **deterministic physical container model**. It treats a cricket innings as a finite vessel of potential energy, mapping the discrete resources of overs and wickets into a fixed 200-point capacity matrix ($P_{total} = 200$).

### Key Features
- **Deterministic Modeling**: Replaces statistical regression with a fixed resource matrix.
- **Cross-Coupled Forfeiture**: Accounts for the physical entanglement of overs and wickets—where consuming time exposes wickets to risk, and losing wickets destroys future time-utility.
- **Dynamic Stabilizer ($D$)**: A mathematical offset that ensures stability and fairness by solving the "Small Denominator Problem" in short matches.
- **Mutable-N Design**: Dynamically tracks the current scheduled maximum overs ($N$) across multiple interruptions to eliminate "Phantom Resources."

## Methodology

The core of the Crux method is the calculation of the **Resource Footprint** ($R_{used}$), which is the sum of four components:

1.  **Over Points ($O(u)$)**: Active consumption of time via format-specific piecewise step functions (80% of T20 points, 70% of ODI points).
2.  **Wicket Points ($W(w)$)**: Active consumption of survival capacity via tier-based weights (20% of T20 points, 30% of ODI points).
3.  **Forfeited Over Capacity ($F_u$)**: Passive destruction of time-utility driven by wicket loss: $F_u = \frac{w}{10} \cdot [O(N) - O(u)]$.
4.  **Forfeited Wicket Survival ($F_w$)**: Passive destruction of survival-utility driven by over consumption: $F_w = \frac{u}{N} \cdot [W_{total} - W(w)]$.

### The Master Formula
The Par Score is calculated as:
$$Par = Score_A \times \left( \frac{R_{used,2} + D}{R_{used,1} + D} \right)$$

Where $D$ is the dynamic stabilizer ($k=4$):
$$D = \lceil (200 - R_{used,1}) / 4 \rceil$$

## Project Structure

- `src/index.ts`: The core `CruxCalculator` implementation.
- `types/index.ts`: TypeScript type definitions for match states and results.
- `docs/research-paper.tex`: The formal academic specification (LaTeX).
- `compile.sh`: Shell script to compile the LaTeX research paper into a PDF.

## Installation

```bash
npm install
```

## Usage

```typescript
import { CruxCalculator } from './src/index';
import { MatchState } from './types/index';

const calculator = new CruxCalculator();

// State of Team A at the end of their innings
const teamA: MatchState = {
  score: 280,
  wickets: 8,
  overs: 50,
  scheduledOvers: 50
};

// State of Team B at the moment of interruption
const teamBAtInterruption: MatchState = {
  score: 150,
  wickets: 3,
  overs: 25.4,
  scheduledOvers: 50
};

const result = calculator.calculateTarget('ODI', teamA, teamBAtInterruption);

console.log(`Par Score: ${result.parScore.toFixed(2)}`);
console.log(`Target: ${result.target}`);
```

## Development

### Building the Project
The build process compiles the TypeScript source code and the LaTeX research paper simultaneously.

```bash
npm run build
```

The output will be located in the `dist/` directory:
- Compiled JavaScript: `dist/src/`
- Research Paper PDF: `dist/docs/research-paper.pdf`

### Requirements
- **Node.js**: For the calculator implementation.
- **pdflatex**: For compiling the research paper (TeX Live or MiKTeX).

## License

This project is licensed under the MIT License - see the `package.json` file for details.

## Author

**Hrutav Modha**
