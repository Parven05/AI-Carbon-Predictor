import time
import Orange

# Create a global context to store the start_time
if not hasattr(Orange.data, 'workflow_context'):
    Orange.data.workflow_context = {}

# Start the timer and store it in the context
Orange.data.workflow_context['start_time'] = time.time()

# Output the data to the next widget
out_data = in_data
