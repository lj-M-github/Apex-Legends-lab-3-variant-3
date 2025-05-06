# complex_traffic_light_example.py
"""
Example: Traffic Light Controller as a Mealy machine.
States cycle on a timer input, emitting the appropriate signal:
  Green --timer--> Yellow (caution)
  Yellow --timer--> Red (stop)
  Red --timer--> Green (go)
"""
from mealy_interpreter import MealyMachine

# Instantiate machine
m = MealyMachine('TrafficLight')

# Define states
m.state('Green')
m.state('Yellow')
m.state('Red')

# Define input and output symbols
m.input_symbol('timer')

m.output_symbol('go')       # green light means “go”
m.output_symbol('caution')  # yellow means “caution”
m.output_symbol('stop')     # red means “stop”

# Set initial state
m.set_initial('Green')

# Define transitions
m.transition('Green', 'timer', 'Yellow', 'caution')
m.transition('Yellow', 'timer', 'Red', 'stop')
m.transition('Red', 'timer', 'Green', 'go')

# Simulate a series of timer events
sequence = ['timer'] * 6
outputs = m.process(sequence)
print("Inputs:   ", sequence)
print("Outputs:  ", outputs)

# Show visualizations
dot = m.visualize_dot()
table = m.visualize_table()

print("\nDOT representation:")
print(dot)

print("\nMarkdown transition table:")
print(table)
