import pytest
from mealy_interpreter import MealyMachine


def test_turnstile_behavior():
    # Build a simple turnstile machine
    m = MealyMachine('Turnstile')
    m.state('Locked').state('Unlocked')
    m.input_symbol('coin').input_symbol('push')
    m.output_symbol('unlock').output_symbol('alarm').output_symbol('lock')
    m.set_initial('Locked')
    # Define transitions
    m.transition('Locked', 'coin', 'Unlocked', 'unlock')
    m.transition('Locked', 'push', 'Locked', 'alarm')
    m.transition('Unlocked', 'push', 'Locked', 'lock')

    # Valid sequence
    inputs = ['coin', 'push', 'push']
    expected = ['unlock', 'lock', 'alarm']
    assert m.process(inputs) == expected


def test_missing_initial_state_raises():
    m = MealyMachine('NoInit')
    m.state('A').input_symbol('x').output_symbol('y')
    # No initial state set
    with pytest.raises(ValueError) as ei:
        m.process(['x'])
    assert "Initial state not set" in str(ei.value)


def test_undefined_transition_raises():
    m = MealyMachine('Broken')
    m.state('S')
    m.input_symbol('a')
    m.output_symbol('o')
    m.set_initial('S')
    # No transition declared for input 'a'
    with pytest.raises(ValueError) as ei:
        m.process(['a'])
    assert "No transition from state S on input a" in str(ei.value)


def test_invalid_state_declaration_type():
    m = MealyMachine()
    # Passing non-str to state() should TypeError
    with pytest.raises(TypeError):
        m.state(123)


def test_transition_with_undeclared_state_or_symbol():
    m = MealyMachine('BadTrans')
    m.state('A')
    m.input_symbol('i')
    m.output_symbol('o')
    m.set_initial('A')
    # Next state 'B' not declared
    with pytest.raises(ValueError):
        m.transition('A', 'i', 'B', 'o')
    # Input symbol 'x' not declared
    m.state('B')
    with pytest.raises(ValueError):
        m.transition('A', 'x', 'B', 'o')
    # Output symbol 'z' not declared
    m.input_symbol('x')
    with pytest.raises(ValueError):
        m.transition('A', 'x', 'B', 'z')


def test_visualizations():
    m = MealyMachine('Visual')
    m.state('Start').state('End')
    m.input_symbol('go')
    m.output_symbol('ok')
    m.set_initial('Start')
    m.transition('Start', 'go', 'End', 'ok')

    dot = m.visualize_dot()
    assert 'digraph Mealy' in dot
    assert 'Start' in dot and 'End' in dot

    table = m.visualize_table()
    # Check header and a row
    assert '| Current State | Input | Output | Next State |' in table
    assert '| Start | go | ok | End |' in table
