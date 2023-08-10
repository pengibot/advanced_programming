import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# Load the data
data = pd.read_csv('TESTING1.csv')

# Select the columns of interest
columns_of_interest = ["Freq.", "Block", "Serv Label1", "Serv Label2", "Serv Label3", "Serv Label4", "Serv Label10"]
data_subset = data[columns_of_interest]

# Drop the rows with missing values
data_subset_clean = data_subset.dropna()

# Calculate the correlation matrix
corr_matrix = data_subset_clean.corr()

# Create a new figure for the plot
fig, ax = plt.subplots(figsize=(10, 8))

# Create a colormap
cmap = mpl.colormaps['coolwarm']

# Create a mask for the diagonal (where variables are compared with themselves)
mask = np.eye(corr_matrix.shape[0], dtype=bool)

# Apply the mask to the correlation matrix
masked_corr_matrix = np.ma.array(corr_matrix, mask=mask)

# Create a matrix plot
cax = ax.matshow(masked_corr_matrix, cmap=cmap)

# Create colorbar
fig.colorbar(cax, label='Correlation coefficient')

# Show the plot with labels
plt.xticks(np.arange(len(corr_matrix.columns)), corr_matrix.columns, rotation=90)
plt.yticks(np.arange(len(corr_matrix.columns)), corr_matrix.columns)

# Add text to each cell
for (i, j), z in np.ndenumerate(masked_corr_matrix):
    if ~np.ma.getmask(masked_corr_matrix)[i, j]:  # Only add text to cells that are not masked
        ax.text(j, i, '{:0.2f}'.format(z), ha='center', va='center')

# Set title
plt.title('Correlation Matrix of Selected Variables', pad=90)

# Show the plot
plt.show()
