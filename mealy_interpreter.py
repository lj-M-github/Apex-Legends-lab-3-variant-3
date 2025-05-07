from typing import Callable, Type, Any, List

import logging

# Configure root logger for interpreter transparency
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('MealyInterpreter')


# Decorators for input validation
def arg_type(index: int, expected_type: Type) -> Callable:

    def decorator(func: Callable) -> Callable:

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                val = args[index]
            except IndexError:
                raise IndexError(
                    f"Missing positional argument at index {index}")
            if not isinstance(val, expected_type):
                raise TypeError(
                    f"Argument {index} to {func.__name__} must be {expected_type.__name__}, got {type(val).__name__}"
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator


class Transition:
    """
    Represents a Mealy machine transition: (state, input) -> (next_state, output)
    """

    def __init__(self, current_state: str, input_symbol: str,
                 next_state: str, output_symbol: str) -> None:
        self.current_state = current_state
        self.input_symbol = input_symbol
        self.next_state = next_state
        self.output_symbol = output_symbol


class MealyMachine:

    def __init__(self, name: str = "MealyMachine") -> None:
        self.name = name
        self.states: set[str] = set()
        self.input_symbols: set[str] = set()
        self.output_symbols: set[str] = set()
        self.transitions: List[Transition] = []  # list of Transition
        self.initial_state: str | None = None

    @arg_type(1, str)
    def state(self, name: str) -> "MealyMachine":
        """Declare a state."""
        logger.debug(f"Adding state: {name}")
        self.states.add(name)
        return self

    @arg_type(1, str)
    def input_symbol(self, symbol: str) -> "MealyMachine":
        """Declare an input symbol."""
        logger.debug(f"Adding input symbol: {symbol}")
        self.input_symbols.add(symbol)
        return self

    @arg_type(1, str)
    def output_symbol(self, symbol: str) -> "MealyMachine":
        """Declare an output symbol."""
        logger.debug(f"Adding output symbol: {symbol}")
        self.output_symbols.add(symbol)
        return self

    @arg_type(1, str)
    def set_initial(self, state: str) -> "MealyMachine":
        """Set the initial state."""
        if state not in self.states:
            raise ValueError(f"Initial state '{state}' not declared")
        logger.debug(f"Setting initial state: {state}")
        self.initial_state = state
        return self

    def transition(self, current_state: str, input_symbol: str,
                   next_state: str, output_symbol: str) -> "MealyMachine":
        """Add a Mealy transition."""
        # Validate arguments
        if current_state not in self.states:
            raise ValueError(f"State '{current_state}' not declared")
        if next_state not in self.states:
            raise ValueError(f"State '{next_state}' not declared")
        if input_symbol not in self.input_symbols:
            raise ValueError(f"Input symbol '{input_symbol}' not declared")
        if output_symbol not in self.output_symbols:
            raise ValueError(f"Output symbol '{output_symbol}' not declared")
        t = Transition(current_state, input_symbol, next_state, output_symbol)
        self.transitions.append(t)
        logger.debug(
            f"Added transition: {current_state} --{input_symbol}/{output_symbol}--> {next_state}"
        )
        return self

    def process(self, inputs: List[str]) -> List[str]:
        """
        Run the Mealy machine on a sequence of inputs and return the outputs.
        """
        if self.initial_state is None:
            raise ValueError("Initial state not set")
        state = self.initial_state
        outputs = []
        logger.info(f"Starting processing in state: {state}")
        for inp in inputs:
            logger.info(f"In state {state}, processing input: {inp}")
            # find matching transition
            match = next(
                (t for t in self.transitions
                 if t.current_state == state and t.input_symbol == inp), None)
            if match is None:
                raise ValueError(
                    f"No transition from state {state} on input {inp}")
            outputs.append(match.output_symbol)
            logger.info(
                f"Transition: {state} --{inp}/{match.output_symbol}--> {match.next_state}"
            )
            state = match.next_state
        logger.info(f"Processing complete. Outputs: {outputs}")
        return outputs

    def visualize_dot(self) -> str:
        """Return GraphViz DOT representation of the machine."""
        lines = [
            "digraph Mealy {", "  rankdir=LR;", f"  label=\"{self.name}\";", ""
        ]
        # Nodes
        for s in self.states:
            shape = "doublecircle" if s == self.initial_state else "circle"
            lines.append(f"  {s} [shape={shape}];")
        # Transitions
        for t in self.transitions:
            lines.append(
                f"  {t.current_state} -> {t.next_state} [label=\"{t.input_symbol}/{t.output_symbol}\"];  "
            )
        lines.append("}")
        dot = "\n".join(lines)
        logger.debug("DOT visualization generated")
        return dot

    def visualize_table(self) -> str:
        """Return markdown table of transitions."""
        header = ["Current State", "Input", "Output", "Next State"]
        rows = [[
            t.current_state, t.input_symbol, t.output_symbol, t.next_state
        ] for t in self.transitions]
        # Build markdown
        table = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
        for row in rows:
            table.append("| " + " | ".join(row) + " |")
        md = "\n".join(table)
        logger.debug("Table visualization generated")
        return md
