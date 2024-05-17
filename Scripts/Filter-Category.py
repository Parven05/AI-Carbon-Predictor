import Orange.data as orangedpc
import pandas as pd

Input_Data = orangedpc.table_to_frame(in_data)

Input_Data.columns = ["Raw Material", "Total Carbon Emission", "Gradient Boosting", "AdaBoost", "Random Forest", "Tree", "Linear Regression", "Neural Network", "KNN","SVM"]

# Group by 'Material Category' and sum the other columns
aggregated_data = Input_Data.groupby("Raw Material", as_index=False).sum()

# Print the aggregated DataFrame
print("Aggregated Data:")
print(aggregated_data)

# Convert the aggregated DataFrame back to Orange table
out_data = orangedpc.table_from_frame(aggregated_data)

# Print the output Orange table
print("Output Data:")
print(out_data)
