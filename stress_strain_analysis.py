import numpy as np
import matplotlib.pyplot as plt

# Sample tensile test data
# Note: Replace these values with actual test data
stress = np.array([0, 50, 100, 150, 200, 250, 300])  # in MPa
strain = np.array([0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06])  # Dimensionless

# Function to plot stress-strain curve

def plot_stress_strain(stress, strain):
    plt.figure(figsize=(8, 6))
    plt.plot(strain, stress, marker='o')
    plt.title('Stress-Strain Curve')
    plt.xlabel('Strain (dimensionless)')
    plt.ylabel('Stress (MPa)')
    plt.grid(True)
    plt.axhline(0, color='black', lw=1)  # Add horizontal line at y=0
    plt.axvline(0, color='black', lw=1)  # Add vertical line at x=0
    plt.xlim(0, max(strain) * 1.1)  # Leave some space on the right
    plt.ylim(0, max(stress) * 1.1)  # Leave some space at the top
    plt.show()

# Main function to execute the analysis
if __name__ == '__main__':
    plot_stress_strain(stress, strain)