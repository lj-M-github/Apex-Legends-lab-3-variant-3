# Apex-Legends - lab 3 - variant 3

This project implements an embedded Domain-Specific
Language (eDSL) for defining Mealy machines, including state
transitions, input/output handling, and visualization capabilities.

## Project Structure

- `mealy_interpreter.py`
   - `MealyMachine` class for state machine definition
   - State/input/output symbol management
   - Transition rules configuration
   - Execution engine with logging
   - GraphViz DOT and Markdown visualization

- `test_mealy_interpreter.py`  
   - State transition logic
   - Error handling (undefined states/symbols)
   - Input validation
   - Visualization outputs

- `complex_traffic_light_example.py`  
   - Traffic light controller state machine
   - Timer-based state transitions
   - Visualization generation

## Mealy Machine Definition

- `state(name)` - Declare states
- `input_symbol(symbol)` - Define valid input symbols
- `output_symbol(symbol)` - Define output symbols
- `set_initial(state)` - Set initial state
- `transition(current_state, input, next_state, output)`
- Create state transition rules

## Execution & Validation

- `process(inputs)` - Execute input sequence and generate outputs
- Type checking via `@arg_type` decorators
- Runtime validation of:
   - Undefined states
   - Missing transitions
   - Invalid symbols

### Visualization

- `visualize_dot()` - Generate GraphViz DOT state diagrams
- `visualize_table()` - Create Markdown transition tables
- Example visualization outputs:

  ```dot
  digraph Mealy {
    rankdir=LR;
    label="TrafficLight";
    Green [shape=doublecircle];
    Green -> Yellow [label="timer/caution"];
    Yellow -> Red [label="timer/stop"];
    Red -> Green [label="timer/go"];
  }

## Contribution

- LI Yichen (<1806015345@qq.com>)
- MOU Lingjie (<553571948@qq.com>)

## Changelog

- 07.05.2025 - 0
   - pass mypy strict type checking.
- 06.05.2025 - 2
   - Add test coverage.
   - Update README.
- 06.05.2025 - 1
   - Add formal sections.
- 20.04.2025 - 0
   - Initial
