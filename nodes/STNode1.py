
import time

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
        LOGGER.debug('%s:shortPoll: ',self.address)
        self.update_time()
        if int(self.getDriver('ST')) == 0:
            self.setOn(None)
            ckval = 1
        else:
            self.setOff(None)
            ckval = 0
        dv = 'ST'
        val = self.getDriver(dv)
        if val is None:
            LOGGER.error('%s:shortPoll: %s expected %d, got %d',self.address,dv,ckval,val)
        else:
            val=int(val)
            if val != ckval:
                LOGGER.error('%s:shortPoll: %s expected %d, got %d',self.address,dv,ckval,val)
        dv = 'Gv1'
        val = self.getDriver(dv)
        if val is None:
            LOGGER.error('%s:shortPoll: %s expected %d, got %d',self.address,dv,ckval,val)
        else:
            val=int(val)
            if val != ckval:
                LOGGER.error('%s:shortPoll: %s expected %d, got %d',self.address,dv,ckval,val)

    def update_time(self):
        self.setDriver('GV0',int(time.time()))

    def longPoll(self):
        LOGGER.debug('{}:longPoll'.format(self.address))

    def setOn(self, command):
        LOGGER.debug('%s:setOn: ',self.address)
        self.setDriver('ST', 1)
        self.setDriver('GV1', 1)

    def setOff(self, command):
        LOGGER.debug('%s:setOff: ',self.address)
        self.setDriver('ST', 0)
        self.setDriver('GV1', 0)

    def query(self,command=None):
        LOGGER.debug('{}:query'.format(self.address))
        self.update_time()
        self.reportDrivers()

    "Hints See: https://github.com/UniversalDevicesInc/hints"
    hint = [1,2,3,4]
    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2},
        {'driver': 'GV0', 'value': 0, 'uom': 110},
        {'driver': 'GV1', 'value': 0, 'uom': 2},
    ]
    id = 'stnode1'
    commands = {
                    'DON': setOn, 'DOF': setOff
                }
