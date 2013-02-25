import re

class State(object):
    """Represent a state in a finite state machine.

    A state reads a single character for input by default.
    @token = a regex to match on the input stream, '' for epsilon
    @enter = list of callbacks when this state is entered in an Automaton
    @exit = list of callbacks when this state is exited in an Automaton
    """

    def __init__(self, token='.'):
        self.token = token
        self.enter_hooks = []
        self.exit_hooks = []
        self.final_hooks = []

    def on(self, event, callback):
        """Add a callback for this state.

        Available callback events: 'enter', 'exit', 'final'
        """
        if event == 'enter':
            self.enter_hooks.append(callback)
        elif event == 'exit':
            self.exit_hooks.append(callback)
        elif event == 'final':
            self.final_hooks.append(callback)

    def off(self, event, callback):
        """Remove a callback for this state.

        Available callback events: 'enter', 'exit', 'final'
        """
        if event == 'enter':
            self.enter_hooks.remove(callback)
        elif event == 'exit':
            self.exit_hooks.remove(callback)
        elif event == 'final':
            self.final_hooks.remove(callback)


class Transition(object):
    """Represent a transition between two states.

    @start_state = the state this transition leaves from
    @end_state = the state this transition ends in
    @condition = function(token) that determines if this transition activates
    @callbacks = callback when this transition is traversed
    """

    def __init__(self, start_state, end_state, condition):
        self.start_state = start_state
        self.end_state = end_state
        self.condition = condition
        self.callbacks = []

    def on(self, callback):
        """Add a callback for this transition.
        """
        self.callbacks.append(callback)

    def off(self, callback):
        """Remove a callback for this transition.
        """
        self.callbacks.remove(callback)


class Automaton(object):
    """Create an automaton from a list of states and transitions.

    @states = maps State's to maps from @end_state to Transition
    """

    def __init__(self, states, transitions, start_state):
        if start_state not in states:
            raise RuntimeError('Invalid start_state')
        self.states = dict((s, {}) for s in states)
        self.start_state = start_state
        self.current_state = start_state
        self.current_input = '' 
        for t in transitions:
            if t.start_state not in self.states \
                    or t.end_state not in self.states \
                    or not callable(t.condition):
                        raise RuntimeError('Invalid transition', t)
            self.states[t.start_state][t.end_state] = t

        self.reject_hooks = []

    def on(self, event, callback):
        """Add a callback for this automaton.

        Available callback events: 'reject'
        """
        if event == 'reject':
            self.reject_hooks.append(callback)

    def off(self, event, callback):
        """Remove a callback for this automaton.

        Available callback events: 'reject'
        """
        if event == 'reject':
            self.reject_hooks.remove(callback)

    def stream(self, string):
        """Add to the automaton input stream.
        """
        self.current_input += string

    def lex(self):
        """Determine the next state based on the current state and input stream.

        Returns a (token, next_state) tuple
        """
        if self.current_state is None:
            return (None, None)
        token = re.match(self.current_state.token, self.current_input)
        if token is None:
            return (None, None)

        neighbors = self.states[self.current_state]
        candidates = [] # list of candidates for next state
        for s in neighbors:
            if neighbors[s].condition(token.group()):
                candidates.append(s)

        if len(candidates) > 1:
            raise RuntimeError('Automaton must be deterministic')

        next_state = None if not candidates else candidates[0]
        return (token, next_state)

    def step(self, string=''):
        """Advance the automaton one state.

        Returns False if no valid @next_state was found.
        """
        self.stream(string)
        (token, next_state) = self.lex()
        if next_state is None:
            return False

        self.current_input = self.current_input[token.end():]
        # Run exit hooks for current_state
        for hook in self.current_state.exit_hooks:
            if not callable(hook):
                raise TypeError('Hook is not callable', hook)
            hook()
        # Run transition hooks
        transition = self.states[self.current_state][next_state]
        for hook in transition.callbacks:
            if not callable(hook):
                raise TypeError('Hook is not callable', hook)
            hook()

        self.current_state = next_state
        # Run enter hooks for next_state
        for hook in self.current_state.enter_hooks:
            if not callable(hook):
                raise TypeError('Hook is not callable', hook)
            hook()

        return True

    def run(self, string='', streamed=False):
        """Step to the end of the input stream, or until no match is found.

        Returns False if no match is found.
        If the end of the input stream is reached, the automaton is reset and
        the @final_hooks of the @end_state will run.
        Setting @streamed to True disables this.
        """
        self.stream(string)
        while self.current_state and self.current_input:
            if not self.step():
                break
        if len(self.current_input) == 0:
            if not streamed:
                for hook in self.current_state.final_hooks:
                    if not callable(hook):
                        raise TypeError('Hook is not callable', hook)
                    hook()
                self.reset()
            return True
        else:
            if not streamed:
                for hook in self.reject_hooks:
                    if not callable(hook):
                        raise TypeError('Hook is not callable', hook)
                    hook()
                self.reset()
            return False

    def reset(self):
        """Return the automaton to the start state. Flush the input stream.
        """
        self.current_state = self.start_state
        self.current_input = '' 


def main():
    def move():
        print 'Transitioning...'
    def reject():
        print 'Rejected'
    def accept():
        print 'Accepted'

    A = State()
    B = State()
    A.on('final', accept)
    B.on('final', reject)

    ab = Transition(A, B, lambda x: x == 'a')
    ba = Transition(B, A, lambda x: x == 'a')

    ab.on(move)
    ba.on(move)

    a = Automaton([A, B], [ab, ba], A)
    a.on('reject', reject)

    a.run('aa')
    a.run('aa')
    a.run('ab')
    a.run('a')

if __name__ == '__main__':
    main()
