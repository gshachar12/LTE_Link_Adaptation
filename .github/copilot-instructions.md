# LTE Link Adaptation Simulator - AI Coding Agent Instructions

## Project Overview
This is a wireless communication simulation project focused on LTE (Long-Term Evolution) link adaptation. The core purpose is to model and visualize Block Error Rate (BLER) performance based on Signal-to-Interference-plus-Noise Ratio (SINR) and Modulation and Coding Scheme (MCS) parameters.

## Architecture & Key Components

### Core Class: `LTEmodel`
- **Single-file architecture**: All logic in [LTEmodel.py](../LTEmodel.py)
- **Purpose**: Simulate LTE network performance by calculating BLER and generating visualization
- **Key attributes**: 
  - `model_name`: Identifier for the model instance
  - `MSC_Threshold`: Dictionary for storing MCS thresholds (currently unused but intended for future expansion)

### Critical Domain Knowledge
- **SINR Range**: -10 dB to 30 dB (signal quality metric)
- **MCS Index Range**: 0 to 28 (modulation/coding scheme complexity)
- **BLER Relationship**: Higher MCS = more data per wave = harder decoding = higher BLER
- **Sigmoid Function**: Used to model BLER decay with increasing SINR

## Key Methods & Algorithms

### `calculateBler(sinr_db, mcs_index)`
Current formula: `1 / (1 + mcs_index * e^(-sinr_db/10))`
- Higher SINR → lower BLER (better signal quality)
- Higher MCS → higher BLER (more complex encoding)
- **Note**: This is a simplified model; real-world LTE BLER curves use lookup tables from 3GPP standards

### `plot_waterfall(data)`
Generates 3-subplot visualization:
1. **Waterfall diagram**: 2D heatmap (SINR × MCS → BLER)
2. **BLER vs SINR**: Line plots for each MCS index
3. **BLER vs MCS**: Line plots for sampled SINR values

## Development Workflow

### Running the Simulation
```bash
python LTEmodel.py
```
- Generates 100 SINR samples × 29 MCS values = 2,900 BLER calculations
- Displays matplotlib figure with three subplots
- Console output shows calculated BLER matrix

### Dependencies
- `numpy`: Numerical operations and array handling
- `matplotlib`: Visualization (3-subplot layout)
- `math`: Exponential calculations in sigmoid function

## Code Conventions

### Visualization Style
- Use `viridis` colormap for heatmaps (perceptually uniform)
- 2×2 subplot layout (with subplot(2,2,4) empty)
- `tight_layout()` to prevent label overlap
- Legend font size: 8pt for multi-line plots

### Naming Patterns
- Snake_case for variables: `sinr_db`, `mcs_index`, `bler_data`
- CamelCase for classes: `LTEmodel`
- Descriptive parameter names matching wireless domain: `sinr_db` not `snr`

### Data Structures
- 2D NumPy arrays: `[mcs_index, sinr_value]` indexing convention
- SINR sampling: Use `np.linspace()` for continuous range
- MCS iteration: Use `np.arange()` for discrete indices

## Future Extensions (Inferred from Code Structure)

### `MSC_Threshold` Dictionary
Currently empty but intended for storing:
- MCS-specific SINR thresholds for adaptive link selection
- Potential use: Dynamic MCS selection based on channel conditions

### Potential Improvements
- Replace sigmoid with 3GPP-compliant BLER tables
- Add adaptive MCS selection logic using `MSC_Threshold`
- Implement time-domain simulations (currently static analysis)
- Add throughput calculations based on BLER and MCS data rates

## Testing & Validation
No formal tests exist. When modifying `calculateBler()`:
1. Verify BLER ∈ [0, 1] for all valid inputs
2. Check that BLER decreases monotonically with increasing SINR
3. Validate that higher MCS yields higher BLER at same SINR
4. Run main() to visually inspect waterfall diagram consistency
