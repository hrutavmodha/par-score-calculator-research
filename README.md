# Par Score Calculator

A deterministic, resource-based framework for calculating revised targets in rain-interrupted limited-overs cricket matches (ODI and T20).

## Overview

This repository implements a **deterministic physical container model** for cricket par scores. It treats a cricket innings as a finite vessel of potential energy, mapping the discrete resources of overs and wickets into a fixed 200-point capacity matrix ($P_{total} = 200$).

### Key Features
- **Deterministic Modeling**: Replaces statistical regression with a fixed resource matrix.
- **Persistent Weight Management**: Weights are derived once from modern international data (Cricsheet) and cached locally to ensure efficiency and consistency.
- **Cross-Coupled Forfeiture**: Accounts for the physical entanglement of overs and wickets—where consuming time exposes wickets to risk, and losing wickets destroys future time-utility.
- **Dynamic Stabilizer ($D$)**: A mathematical offset that ensures stability and fairness by solving the "Small Denominator Problem" in short matches.
- **Mutable-N Design**: Dynamically tracks the current scheduled maximum overs ($N$) across multiple interruptions.

## Methodology

The core of the framework is the calculation of the **Resource Footprint** ($R_{used}$), which is the sum of four components:

1.  **Over Points ($O(u)$)**: Active consumption of time via format-specific piecewise step functions.
2.  **Wicket Points ($W(w)$)**: Active consumption of survival capacity via tier-based weights.
3.  **Forfeited Over Capacity ($F_u$)**: Passive destruction of time-utility driven by wicket loss.
4.  **Forfeited Wicket Survival ($F_w$)**: Passive destruction of survival-utility driven by over consumption.

### The Master Formula
The Par Score is calculated as:
$$Par = Score_A \times \left( \frac{R_{used,2} + D}{R_{used,1} + D} \right)$$

Where $D$ is the dynamic stabilizer ($k=4$):
$$D = \lceil (200 - R_{used,1}) / 4 \rceil$$

## Project Structure

- `src/calculator.py`: The core calculator implementation.
- `src/weights.py`: Manages the derivation and caching of empirical weights.
- `data/weights_cache.json`: Local cache for derived weights (generated on first run).
- `derivation/`: Scripts to derive weights from raw ball-by-ball data.
- `docs/research-paper.tex`: The formal academic specification (LaTeX).
- `compile.sh`: Shell script to compile the research paper into the `build/` directory.
- `main.py`: Entry point for running sample scenarios and test cases.

## Installation

Ensure you have Python 3.x installed. It is recommended to use the provided virtual environment.

```bash
# The project expects dependencies (like pandas) in .venv
# To run directly using the established environment:
./.venv/bin/python3 main.py
```

## Usage

```python
from src.calculator import CruxCalculator, MatchState

calc = CruxCalculator()

# State of Team A at the end of their innings
team_a: MatchState = {
    'score': 280,
    'wickets': 8,
    'overs': 50.0,
    'scheduledOvers': 50.0
}

# State of Team B at the moment of interruption
team_b: MatchState = {
    'score': 150,
    'wickets': 3,
    'overs': 25.4,
    'scheduledOvers': 50.0
}

result = calc.calculate_target('ODI', team_a, team_b)

print(f"Par Score: {result['parScore']:.2f}")
print(f"Target: {result['target']}")

# To manually refresh weights from raw data:
# calc.update_weights()
```

## Research Paper

The formal mathematical foundation of this model is documented in `docs/research-paper.tex`.

To compile the paper:
```bash
bash compile.sh
```
The compiled PDF and auxiliary files will be located in the `build/` directory.

## Empirical Validation

The repository includes a `controversial_matches.md` file documenting historically significant rain-affected matches (e.g., the 1992 and 2003 World Cup incidents) and how this model interprets them. You can run these cases via `main.py`.

## License

This project is licensed under the MIT License.

## Author

**Hrutav Modha**
