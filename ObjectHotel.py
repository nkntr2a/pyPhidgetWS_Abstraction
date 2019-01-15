import logging

log = logging.getLogger(__name__)


class Concierge:
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state


class ObjectHotel(Concierge):
    def __init__(self):
        Concierge.__init__(self)
        try:
            self.storage
        except AttributeError:
            self.storage = {}
            log.info("Object Hotel Instantiated")

    def checkIn(self, device, val):
        self.storage[device] = val
        log.info("Checked the handler for " + device + " into the ObjectHotel")

    def visit(self, device):
        return self.storage[device]

    def check(self, device):
        if device in self.storage:
            exists = True
        else:
            exists = False
        return exists

    def checkOut(self, device):
        log.info("Deleting " + device + " from the Object hotel")
        if device in self.storage:
            guest = self.storage.pop(device, None)
        else:
            print(device + " was not found in the ObjectHotel so could not delete")
            log.warning(device + " was not found in the ObjectHotel so could not delete")
        return guest