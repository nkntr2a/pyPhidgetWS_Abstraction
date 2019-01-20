class HoldGripper():
    def __init__(self):
        self.hold_object = False

    def get_hold_state(self):
        return self.hold_object

    def set_hold_state(self, val):
        self.hold_object = val
        return