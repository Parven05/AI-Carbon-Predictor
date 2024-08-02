import time
import Orange

# Retrieve the start time from the context
start_time = Orange.data.workflow_context.get('start_time')

if start_time is not None:
    # Stop the timer
    end_time = time.time()

    # Calculate the elapsed time
    execution_time = end_time - start_time

    # Print the execution time
    print("Execution time:", execution_time, "seconds")
else:
    print("Start time not found.")

# Output the data to the next widget if necessary
out_data = in_data
