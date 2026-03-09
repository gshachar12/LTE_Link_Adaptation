import numpy as np
import matplotlib.pyplot as plt
from LTEmodel import LTEmodel
class Simulation: 
    def __init__(self):
        pass
    def generate_mobility_path(self, seconds, sampling_rate, max_val=25, min_val=5, mean=0, std=2):
        num_samples = int(seconds * sampling_rate)
        white_noise = np.random.normal(loc=mean, scale=std, size=num_samples)
        return np.linspace(max_val, min_val, num_samples) + white_noise

    def run_simulation(self, seconds, sampling_rate):
        LTE = LTEmodel("Example LTE Model")
        seconds_range = np.arange(0, seconds, 1/sampling_rate)
        sinr_path = self.generate_mobility_path(seconds, sampling_rate)
        
        optimal_mcs_values = []
        # Analyze and print optimal MCS for each time step
        for t, sinr in zip(seconds_range, sinr_path):
            optimal_mcs = LTE.get_optimal_mcs(sinr)
            optimal_mcs_values.append(optimal_mcs)
        
        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Plotting SINR path on the left y-axis
        ax1.set_xlabel('Time (seconds)')
        ax1.set_ylabel('SINR (dB)', color='blue', fontweight='bold')
        ax1.plot(seconds_range, sinr_path, color='blue', alpha=0.5, label='SINR Path')
        ax1.tick_params(axis='y', labelcolor='blue')

        # Plotting optimal MCS on the right y-axis  
        
        ax2 = ax1.twinx() 
        ax2.set_ylabel('Optimal MCS', color='orange', fontweight='bold')
        ax2.step(seconds_range, optimal_mcs_values, color='orange', where='post', label='Selected MCS')
        ax2.tick_params(axis='y', labelcolor='orange')

        plt.title('Link Adaptation: MCS Tracking SINR Changes', fontweight='bold')
        fig.tight_layout()
        plt.grid(True, alpha=0.3)
        plt.show()
        
        print( "Simulation Complete. Optimal MCS values have been plotted against the SINR path."   )
        print("Mean Throughput:", np.mean([LTE.calc_throughput(mcs, sinr) for mcs, sinr in zip(optimal_mcs_values, sinr_path)]), "Mbps")

if __name__ == "__main__":
    sim = Simulation()
    
    # Simulation parameters
    seconds = 10
    sampling_rate = 100  # samples per second
    sim.run_simulation(seconds, sampling_rate)