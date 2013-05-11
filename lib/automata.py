import re
from event import EventHook

class State(object):
    """Represent a state in a finite state machine.

    A state reads a single character for input by default.
    @token = a regex to match on the input stream, '' for epsilon
    """

    def __init__(self, token='.*'):
        self.token = token
        self.on_enter = EventHook()
        self.on_exit = EventHook()
        self.on_end = EventHook()


class Transition(object):
    """Represent a transition between two states.

    @start_state = the state this transition leaves from
    @end_state = the state this transition ends in
    @condition = function(token) that determines if this transition activates
    """

    def __init__(self, start_state, end_state, condition=None):
        self.start_state = start_state
        self.end_state = end_state
        self.condition = condition
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
        self.current_input = '' 
        for t in transitions:
            if t.start_state not in self.states or t.end_state not in self.states:
                raise RuntimeError('Invalid transition', t)
            self.states[t.start_state].append(t)

        self.on_reject = EventHook()

        self.begin = True

    def stream(self, string):
        """Add to the automaton input stream.
        """
        self.current_input = string

    def lex(self):
        """Determine the next state based on the current state and input stream.

        Returns a (token, next_state) tuple
        """
        if self.current_state is None:
            return (None, None)
        token = re.match(self.current_state.token, self.current_input)


        if token is None:
            return (None, None)

        transitions = self.states[self.current_state]
        candidates = [] # list of candidates for next state
        defaults = []
        for t in transitions:
            if t.condition is not None:
                # maybe change from token.string to token.group
                if t.condition(token.string):
                    candidates.append(t)
            else:
                defaults.append(t)
    

        if len(candidates) > 1:
            raise RuntimeError('Automaton must be deterministic (more than one transition on input)')
        elif candidates:
            trans = candidates[0]


        if not candidates and not defaults:
            trans = None
        elif not candidates and len(defaults) > 1:
            raise RuntimeError('Automaton must be deterministic (more than one default transistion)')
        elif not candidates:
            trans = defaults[0]
        else:
            pass

        return (token, trans)

    def step(self, string=''):
        """Advance the automaton one state.

        Returns False if no valid @next_state was found.
        """

        if self.begin:
            self.current_state.on_enter.fire()
            self.begin = False


        self.stream(string)
        (token, trans) = self.lex()
        if trans is None:
            return False

        #self.current_input = self.current_input[token.end():]

        # Run exit hooks for current_state
        self.current_state.on_exit.fire()
        # Run transition hooks with matched token groups
        trans.on_enter.fire(token.groups())

        self.current_state = trans.end_state
        # Run enter hooks for next_state
        self.current_state.on_enter.fire()
        return True

#    def run(self, string='', streamed=False):
#        """Step to the end of the input stream, or until no match is found.
#
#        Returns False if no match is found.
#        If the end of the input stream is reached, the automaton is reset.
#        Setting @streamed to True disables this.
#        """
#        self.stream(string)
#        while self.current_state and self.current_input:
#            if not self.step():
#                break
#        if len(self.current_input) == 0:
#            if not streamed:
#                self.current_state.on_end.fire()
#                self.reset()
#            return True
#        else:
#            if not streamed:
#                self.on_reject.fire()
#                self.reset()
#            return False

#    def reset(self):
#        """Return the automaton to the start state. Flush the input stream.
#        """
#        self.current_state = self.start_state
#        self.current_input = ''
#        self.begin = True



def main():
    def move():
        print 'Transitioning...'
    def reject():
        print 'Rejected'
    def accept():
        print 'Accepted'

    A = State()
    B = State()
    A.on_end += accept
    B.on_end += reject

    ab = Transition(A, B, lambda x: x == 'a')
    ba = Transition(B, A, lambda x: x == 'a')

    ab.on_enter += move
    ba.on_enter += move

    a = Automaton([A, B], [ab, ba], A)
    a.on_reject += reject

    a.run('aa')
    a.run('aa')
    a.run('ab')
    a.run('a')

if __name__ == '__main__':
    main()
