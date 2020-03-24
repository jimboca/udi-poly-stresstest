
try:
    import polyinterface
except ImportError:
    import pgc_interface as polyinterface

from nodes import STNode1

LOGGER = polyinterface.LOGGER

class Controller(polyinterface.Controller):
    def __init__(self, polyglot):
        super(Controller, self).__init__(polyglot)
        self.name = 'Stress Test Controller'
        self.driver = {}
        self._inShortPoll = None # None until shortpoll actually runs
        #self.poly.onConfig(self.process_config)

    def start(self):
        # This grabs the server.json data and checks profile_version is up to date
        #serverdata = self.poly.get_server_data()
        #LOGGER.info('Started Stress Test NodeServer {}'.format(serverdata['version']))
        self.heartbeat(0)
        self.check_params()
        if self.getDriver('GV0') is None:
            self.setDriver('GV0',30)
        if self.getDriver('GV1') is None:
            self.setDriver('GV1',0)
        self.discover()
        #self.poly.add_custom_config_docs("<b>And this is some custom config data</b>")

    def setDriver(self,driver,value):
        self.driver[driver] = value
        super(Controller, self).setDriver(driver,value)

    def getDriver(self,driver):
        if driver in self.driver:
            return self.driver[driver]
        else:
            return None
            # WARNING: This only works on local, will not work on PGC
            #return next((dv["value"] for dv in self.drivers if dv["driver"] == driver), None)


    def shortPoll(self):
        if int(self.getDriver('GV1')) == 0:
            return
        LOGGER.debug('Controller:shortPoll')
        if self._inShortPoll is True:
            LOGGER.error('Controller:shortPoll: can not run {}'.format(self._inShortPoll))
            return
        self._inShortPoll = True
        for node in self.nodes:
            if self.nodes[node].address != self.address:
                self.nodes[node].shortPoll()
        self._inShortPoll = False

    def longPoll(self):
        LOGGER.debug('Controller:longPoll')
        self.heartbeat()

    def query(self,command=None):
        LOGGER.debug('Controller:query')
        self.check_params()
        for node in self.nodes:
            if self.nodes[node].address != self.address:
                self.nodes[node].query()
        self.reportDrivers()

    def discover(self, *args, **kwargs):
        cnt = int(self.getDriver('GV0'))
        for i in range(cnt):
            fi = '%04d' % (i + 1)
            self.addNode(STNode1(self, self.address, 'st_{}'.format(fi), 'ST Node {}'.format(fi)))

    def delete(self):
        LOGGER.info('Oh God I\'m being deleted. Nooooooooooooooooooooooooooooooooooooooooo.')

    def stop(self):
        LOGGER.debug('NodeServer stopped.')

    def process_config(self, config):
        # this seems to get called twice for every change, why?
        # What does config represent?
        LOGGER.info("process_config: Enter config={}".format(config));
        LOGGER.info("process_config: Exit");

    def heartbeat(self,init=False):
        LOGGER.debug('heartbeat: init={}'.format(init))
        if init is not False:
            self.hb = init
        LOGGER.debug('heartbeat: hb={}'.format(self.hb))
        if self.hb == 0:
            self.reportCmd("DON",2)
            self.hb = 1
        else:
            self.reportCmd("DOF",2)
            self.hb = 0

    def check_params(self):
        """
        This is an example if using custom Params for user and password and an example with a Dictionary
        """
        self.removeNoticesAll()

    def update_profile(self,command):
        LOGGER.info('update_profile:')
        st = self.poly.installprofile()
        return st

    def cmd_set_cnt(self,command):
        val = int(command.get('value'))
        LOGGER.info('cmd_set_cnt: {}'.format(val))
        self.setDriver('GV0',val)
        self.discover()

    def cmd_set_sp(self,command):
        val = int(command.get('value'))
        LOGGER.info('cmd_set_cnt: {}'.format(val))
        self.setDriver('GV1',val)

    id = 'controller'
    commands = {
        'QUERY': query,
        'DISCOVER': discover,
        'UPDATE_PROFILE': update_profile,
        'SET_CNT': cmd_set_cnt,
        'SET_SP': cmd_set_sp,
    }
    drivers = [
      {'driver': 'ST', 'value': 1, 'uom': 2},
      {'driver': 'GV0', 'value': 25, 'uom': 107},
      {'driver': 'GV1', 'value': 0, 'uom': 2}
    ]
