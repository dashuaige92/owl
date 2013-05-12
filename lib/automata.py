import re
from event import EventHook

class State(object):
    """Represent a state in a finite state machine.

    A state reads a single character for input by default.
    @token = a regex to match on the input stream, '' for epsilon
    """

    def __init__(self):
        self.on_enter = EventHook()
        self.on_exit = EventHook()
        self.on_end = EventHook()

class Transition(object):
    """Represent a transition between two states.

    @start_state = the state this transition leaves from
    @end_state = the state this transition ends in
    @match = regex that activates this transition, or default if None
    """

    def __init__(self, start_state, end_state, match=None):
        self.start_state = start_state
        self.end_state = end_state
        self.match = match
        self.on_enter = EventHook()

class Automaton(object):
    """Create an automaton from a list of states and transitions.

    @states = maps State's to maps from @end_state to Transition
    """

    def __init__(self, states, transitions, start_state):
        if start_state not in states:
            raise RuntimeError('Invalid start_state')
        self.states = dict((s, []) for s in states)
        self.start_state = start_state
        self.current_state = start_state
        for t in transitions:
            if t.start_state not in self.states or t.end_state not in self.states:
                raise RuntimeError('Invalid transition', t)
            self.states[t.start_state].append(t)

    def step(self, string=''):
        """Advance the automaton one state.

        Raises a runtime error if no valid @next_state was found.
        """

        transitions = self.states[self.current_state]
        candidates = {} # Maps candidates to its re.match
        defaults = []
        transition = None
        for t in transitions:
            if t.match is not None:
                match = re.match(t.match, string)
                if match:
                    transition = t
                    candidates[t] = match
            else:
                defaults += [t]

        if len(candidates) == 1:
            transition = candidates.keys()[0]
            match = candidates[transition]
        elif len(candidates) > 1 or len(defaults) > 1:
            raise RuntimeError('Automaton must be deterministic (more than one transition on input)')
        elif len(candidates) == 0 and len(defaults) == 1:
            transition = defaults[0]
            match = re.match('', '')
        else:
            raise RuntimeError('No matching transition found!')

        # Run exit hooks for current_state
        self.current_state.on_exit.fire()

        # Run transition hooks with matched token groups
        transition.on_enter.fire(match.groups())

        self.current_state = transition.end_state
        # Run enter hooks for next_state
        self.current_state.on_enter.fire()
        return True
