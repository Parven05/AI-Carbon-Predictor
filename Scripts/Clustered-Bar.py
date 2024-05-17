import Orange.data as orangedpc
import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns  # This line can be removed if seaborn is not needed

# Convert Orange table to pandas DataFrame
Input_Data = orangedpc.table_to_frame(in_data)

# Ensure that the columns are correctly named
Input_Data.columns = ["Raw Material", "Total Carbon Emission", "Gradient Boosting"]

# Plotting the data
plt.figure(figsize=(10, 6))
bar_width = 0.35

# Set positions of the bars on the x-axis
r1 = range(len(Input_Data))
r2 = [x + bar_width for x in r1]

# Create bar plot
plt.bar(r1, Input_Data["Total Carbon Emission"], color='b', width=bar_width, edgecolor='grey', label='Total Carbon Emission')
plt.bar(r2, Input_Data["Gradient Boosting"], color='r', width=bar_width, edgecolor='grey', label='Gradient Boosting')

# Add labels
plt.xlabel('Raw Material', fontweight='bold', fontsize=10)
plt.ylabel('Values', fontweight='bold', fontsize=10)
plt.title('Total Carbon Emission and Gradient Boosting Values by Raw Material', fontsize=10)
plt.xticks([r + bar_width/2 for r in range(len(Input_Data))], Input_Data['Raw Material'], rotation=90, fontsize=6)

# Add legend
plt.legend()

# Show plot
plt.show()
