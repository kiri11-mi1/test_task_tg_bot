from transitions import Machine


class StateMachine(object):


    states = ['start_state', 'food_size', 'payment_form', 'checking']


    def __init__(self, initial_state='start_state'):
        self.machine = Machine(model=self, states=StateMachine.states, initial=initial_state)
        self.machine.add_transition(trigger='start_dialog', source='start_state', dest='food_size')
        self.machine.add_transition(trigger='select_size', source='food_size', dest='payment_form')
        self.machine.add_transition(trigger='select_payment_form', source='payment_form', dest='checking')
        self.machine.add_transition(trigger='fix_order', source='checking', dest='start_state')
        self.machine.add_transition(trigger='cancel', source='*', dest='start_state')

        
