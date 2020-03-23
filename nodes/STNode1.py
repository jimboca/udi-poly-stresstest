
try:
    import polyinterface
except ImportError:
    import pgc_interface as polyinterface

LOGGER = polyinterface.LOGGER

class STNode1(polyinterface.Node):
    def __init__(self, controller, primary, address, name):
        super(STNode1, self).__init__(controller, primary, address, name)
        self.driver = {}

    def start(self):
        self.setDriver('ST', 0)
        pass

    def setDriver(self,driver,value):
        self.driver[driver] = value
        super(STNode1, self).setDriver(driver,value)

    def getDriver(self,driver):
        if driver in self.driver:
            return self.driver[driver]
        else:
            return super(STNode1, self).getDriver(driver)

    def shortPoll(self):
        LOGGER.debug('{}:shortPoll'.format(self.address))
        if int(self.getDriver('ST')) == 0:
            self.setOn(None)
        else:
            self.setOff(None)

    def longPoll(self):
        LOGGER.debug('{}:longPoll'.format(self.address))

    def setOn(self, command):
        self.setDriver('ST', 1)
        self.setDriver('GV0', 1)
        self.setDriver('GV1', 1)

    def setOff(self, command):
        self.setDriver('ST', 0)
        self.setDriver('GV0', 0)
        self.setDriver('GV1', 0)

    def query(self,command=None):
        LOGGER.debug('{}:query'.format(self.address))
        self.reportDrivers()

    "Hints See: https://github.com/UniversalDevicesInc/hints"
    hint = [1,2,3,4]
    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2},
        {'driver': 'GV0', 'value': 0, 'uom': 2},
        {'driver': 'GV1', 'value': 0, 'uom': 2},
    ]
    id = 'stnode1'
    commands = {
                    'DON': setOn, 'DOF': setOff
                }
