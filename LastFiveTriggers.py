import time


class LastFiveEvents:
    def __init__(self):
        self.last_five_events = []

    def add_event(self, trigger_value):
        if len(self.last_five_events) >= 5:
            self.last_five_events.pop(0)
        tstamp = time.gmtime()
        dictval = {"trigger_value": trigger_value, "timestamp": tstamp}
        self.last_five_events.append(dictval)

    def get_last_true(self):
        if len(self.last_five_events) == 0:
            return 0
        last_true = 0
        for i in self.last_five_events:
            if i["trigger_value"] == 1:
                if last_true < i["timestamp"]:
                    last_true = i["timestamp"]
        return last_true

    def get_last_false(self):
        if len(self.last_five_events) == 0:
            return 0
        last_false = 0
        for i in self.last_five_events:
            if i["trigger_value"] == 0:
                if last_false < i["timestamp"]:
                    last_false = i["timestamp"]
        return last_false

    def get_event_array(self):
        return self.last_five_events