import math
import numpy as np
import matplotlib.pyplot as plt

"""
LTE (Long-Term Evolution) Link Adaptation Simulator - Day 1
A visual analysis of the relationship between SINR, BLER, and Throughput.
Comments are in English for professional Git documentation.
"""

class LTEmodel:
    def __init__(self, model_name):
        self.model_name = model_name
        
    def calculateBler(self, sinr_db, mcs_index, steepness=0.75): 
        # Calculate BLER using a sigmoid function shifted by MCS index
        exponent = steepness * (sinr_db - mcs_index)
        exponent = np.clip(exponent, -50, 50)
        bler = 1 / (1 + np.exp(exponent))
        return bler

    def max_rate(self, mcs_index, amplification_factor=2.5):
        # Peak rate in Mbps for a given MCS
        return mcs_index * amplification_factor

    def calc_throughput(self, mcs_index, sinr_db):
        # Net Throughput = Max Rate * Success Probability (1 - BLER)
        bler = self.calculateBler(sinr_db, mcs_index)
        return self.max_rate(mcs_index) * (1 - bler)
    
    def plot_full_analysis(self, bler_data, sinr_range, mcs_indices):
        plt.style.use('seaborn-v0_8-muted')
        fig, axs = plt.subplots(2, 2, figsize=(15, 11))
        
        # 1. Waterfall Diagram (Heatmap)
        im = axs[0, 0].imshow(bler_data, aspect='auto', cmap='viridis', 
                             origin='lower', extent=[sinr_range[0], sinr_range[-1], mcs_indices[0], mcs_indices[-1]])
        fig.colorbar(im, ax=axs[0, 0], label='BLER (Error Rate)')
        axs[0, 0].set_title('1. Waterfall Diagram (BLER Heatmap)', fontweight='bold')
        axs[0, 0].set_xlabel('SINR (dB)')
        axs[0, 0].set_ylabel('MCS Index')

        # 2. BLER vs SINR
        sample_mcs = [2, 10, 18, 26]
        for mcs in sample_mcs:
            bler_values = [self.calculateBler(s, mcs) for s in sinr_range]
            axs[0, 1].plot(sinr_range, bler_values, label=f'MCS {mcs}', linewidth=2)
        
        axs[0, 1].axhline(y=0.1, color='red', linestyle='--', alpha=0.6, label='10% Target')
        axs[0, 1].set_title('2. BLER Waterfall Curves', fontweight='bold')
        axs[0, 1].set_xlabel('SINR (dB)')
        axs[0, 1].set_ylabel('BLER')
        axs[0, 1].legend(fontsize=8)
        axs[0, 1].grid(True, alpha=0.3)

        # 3. BLER vs MCS
        sample_sinrs = [-2, 5, 15, 25]
        for s in sample_sinrs:
            bler_v_mcs = [self.calculateBler(s, m) for m in mcs_indices]
            axs[1, 0].plot(mcs_indices, bler_v_mcs, label=f'SINR {s} dB', marker='o', markersize=3)
        
        axs[1, 0].set_title('3. BLER vs MCS (Fixed Signal Quality)', fontweight='bold')
        axs[1, 0].set_xlabel('MCS Index')
        axs[1, 0].set_ylabel('BLER')
        axs[1, 0].legend(fontsize=8)
        axs[1, 0].grid(True, alpha=0.3)
        
        # 4. THROUGHPUT vs SINR (The "Money" Graph)
        for mcs in sample_mcs:
            tp_values = [self.calc_throughput(mcs, s) for s in sinr_range]
            axs[1, 1].plot(sinr_range, tp_values, label=f'MCS {mcs}', linewidth=2)
        
        # Using Axis Coordinates (0 to 1) for text to ensure it stays inside the plot   

        axs[1, 1].set_title('4. Actual Throughput (Mbps) vs SINR', fontweight='bold')
        axs[1, 1].set_xlabel('SINR (dB)')
        axs[1, 1].set_ylabel('Throughput (Mbps)')
        axs[1, 1].legend(fontsize=8, loc='upper left')
        axs[1, 1].grid(True, alpha=0.3)
        
        # Tight layout with extra padding to prevent clipping
        plt.tight_layout(pad=3.0)
        plt.show()

def main():
    model = LTEmodel("LTE_PHY_Sim_Day1")
    sinr_range = np.linspace(-10, 35, 200) # Extended range for better visualization
    mcs_indices = np.arange(0, 30)
    
    # Calculate heatmap data
    bler_data = np.array([[model.calculateBler(s, m) for s in sinr_range] for m in mcs_indices])

    print("Day 1 Simulation Complete. Opening Dashboard...")
    model.plot_full_analysis(bler_data, sinr_range, mcs_indices)

if __name__ == "__main__":
    main()