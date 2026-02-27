import math
import numpy as np
import matplotlib.pyplot as plt

"""_summary_
LTE (Long-Term Evolution) is a standard for wireless broadband communication. The LTEmodel class is designed to simulate and 
analyze the performance of LTE networks by calculating the Block Error Rate (BLER) based on the Signal-to-Interference-plus-Noise Ratio (SINR) 
and Modulation and Coding Scheme (MCS) index. The class also includes a method to plot a waterfall diagram, which visually represents the BLER as a function of SINR and MCS index.
The calculateBler method uses a sigmoid function to model the relationship between SINR, MCS index, and BLER. Higher SINR values typically result in lower BLER values, while higher MCS indices indicate more data being loaded on each wave, which can increase the BLER.
    
"""
class LTEmodel:
    def __init__(self, model_name):
        self.model_name = model_name
        self.MSC_Threshold = { }
    def calculateBler(self, sinr_db, mcs_index, steepness = 0.75): 
        """_summary_
        Args:
            sinr_db (_type_): _description_
            mcs_index (_type_): _description_

        Returns:
            _type_: _description_
        """
        # Implement the logic to calculate BLER (Block Error Rate)
        # based on the SINR (Signal-to-Interference-plus-Noise Ratio) in dB and MCS (Modulation and Coding Scheme) index
                                
        # The BLER is calculated using a sigmoid function, where higher SINR values result in lower BLER values
        
        # the value of SINR in dB ranges from -10 dB to 30 dB, and the MCS index ranges from 0 to 28
        # when the MCS is higher, that means we are loading more data on each wave
        # so it will be harder to decode the data, which will increase the BLER 
        
        #moving the threshold to the right as the MCS index increases, which means that higher MCS indices require higher SINR values to achieve the same BLER
        #with higher SINR values the bler will be lower, and with higher mcs index the bler will be higher, so we can use a sigmoid function to model this relationship
        sigmoid = 1 / (1 +  math.e ** (steepness*(sinr_db-mcs_index)))
        return sigmoid
    
    def plot_waterfall(self, data):
        # Implement the logic to plot a waterfall diagram based on the provided data
        # The waterfall diagram is a visual representation of the BLER (Block Error Rate) as a function of SINR (Signal-to-Interference-plus-Noise Ratio) and MCS (Modulation and Coding Scheme) index
        # The x-axis represents the SINR in dB, the y-axis represents the MCS index, and the color intensity represents the BLER

        plt.figure(figsize=(9, 7))

        # Waterfall diagram
        plt.subplot(2, 2, 1)
        plt.imshow(data, aspect='auto', cmap='viridis', origin='lower')
        plt.colorbar(label='BLER')
        plt.xlabel('SINR (dB)')
        plt.ylabel('MCS Index')
        plt.title('Waterfall Diagram')

        # BLER vs SINR
        plt.subplot(2, 2, 2)
        sample_mcs_indices = [0,1, 2, 5, 10, 15, 20,25, 28]  # Sample MCS indices to plot
        for mcs_index in sample_mcs_indices:
            plt.plot(np.linspace(-10, 30, data.shape[1]), data[mcs_index], label=f'MCS {mcs_index}')
        plt.xlabel('SINR (dB)')
        plt.ylabel('BLER')
        plt.title('BLER vs SINR for Different MCS Indices')
        plt.legend(fontsize=8, loc= 'lower right')
        plt.grid()

        # BLER vs MCS
        plt.subplot(2, 2, 3)
        mcs_indices = np.arange(0, 29)
        for sinr_db in np.linspace(-10, 30, 5):
            bler_values = [self.calculateBler(sinr_db, mcs_index) for mcs_index in mcs_indices]
            plt.plot(mcs_indices, bler_values, label=f'SINR {sinr_db:.1f} dB')
        plt.xlabel('MCS Index')
        plt.ylabel('BLER')
        plt.title('BLER vs MCS Index for Different SINR Values')
        plt.legend()
        plt.grid()

        plt.tight_layout()
        plt.show()


def main():
    model = LTEmodel("ExampleModel")
    
    # Example data for SINR and MCS index
    sinr_db_values = np.linspace(-10, 30, 100)  # SINR values from -10 dB to 30 dB
    mcs_indices = np.arange(0, 29)  # MCS index from 0 to 28
    
    # Create a 2D array to store BLER values for each combination of SINR and MCS index
    bler_data = np.zeros((len(mcs_indices), len(sinr_db_values)))
    
    print ("Calculating BLER data for each combination of SINR and MCS index...")
    for i, mcs_index in enumerate(mcs_indices):
        for j, sinr_db in enumerate(sinr_db_values):
            bler_data[i, j] = model.calculateBler(sinr_db, mcs_index)
    print(bler_data)

    # Plot the waterfall diagram
    model.plot_waterfall(bler_data)
    
    print("BLER data calculated and waterfall diagram plotted successfully.")
if __name__ == "__main__":
    main()