#!/usr/bin/env python
# E. Londero, July 2018 
# contact elisa.londero@inaf.it

import sys
import os
import PyTango
import pdb


# 2- secondo blocco con definizione di comandi e attributi
class txtImporterClass(PyTango.DeviceClass):

    cmd_list = { 'On' : [ [ PyTango.ArgType.DevVoid, "none" ],
                          [ PyTango.ArgType.DevVoid, "none" ] ],
                 'Off' : [ [ PyTango.ArgType.DevVoid, "none" ],
                           [ PyTango.ArgType.DevVoid, "none"] ],
                 'ResetCounter' : [ [ PyTango.ArgType.DevVoid, "none" ],
                                    [ PyTango.ArgType.DevVoid, "none"] ],
    }
    attr_list = { 'FailedFileCounter' : [ [ PyTango.ArgType.DevLong,
                                            PyTango.AttrDataFormat.SCALAR,
                                            PyTango.AttrWriteType.READ ],
                                            { 'Unit' : "", } ],
            'WarningFileCounter' : [ [ PyTango.ArgType.DevLong,
                                       PyTango.AttrDataFormat.SCALAR,
                                       PyTango.AttrWriteType.READ ],
                                       { 'Unit' : "", } ],
            'RegularFileCounter' : [ [ PyTango.ArgType.DevLong ,
                                       PyTango.AttrDataFormat.SCALAR ,
                                       PyTango.AttrWriteType.READ],
                                       { 'Unit' : "", } ]
    }


# 3- terzo blocco, implementa metodi eseguiti da comandi e attributi
class txtImporter(PyTango.Device_4Impl):

    def __init__(self,cl,name):
        PyTango.Device_4Impl.__init__(self, cl, name)
        self.info_stream('In txtImporter.__init__')
        txtImporter.init_device(self)

    def init_device(self):
        self.info_stream('In Python init_device method')
        self.set_state(PyTango.DevState.ON)
        self.attr_regular = 3
        self.attr_warning = 3 
        self.attr_failed = 3 

    #------------------------------------------------------------------

    def delete_device(self):
        self.info_stream('txtImporter.delete_device')

    #------------------------------------------------------------------
    # COMMANDS
    #------------------------------------------------------------------

    def is_On_allowed(self):
        return self.get_state() == PyTango.DevState.OFF

    def On(self):
        self.info_stream('On')
        self.set_state(PyTango.DevState.ON)

    #------------------------------------------------------------------

    def is_Off_allowed(self):
        return self.get_state() == PyTango.DevState.ON

    def Off(self):
        self.info_stream('Off')
        self.set_state(PyTango.DevState.OFF)

    #------------------------------------------------------------------

    def is_ResetCounter_allowed(self):
        return self.get_state() == PyTango.DevState.ON

    def ResetCounter(self):
        self.info_stream('ResetCounter')
        self.attr_regular = 0
        self.attr_warning = 0
        self.attr_failed = 0

    #------------------------------------------------------------------
    # ATTRIBUTES
    #------------------------------------------------------------------

    def read_attr_hardware(self, data):
        self.info_stream('In read_attr_hardware')

    def read_RegularFileCounter(self, the_att):
        self.info_stream("read_RegularFileCounter")
        the_att.set_value(self.attr_regular)

    def is_RegularFileCounter_allowed(self, req_type):
        return self.get_state() in (PyTango.DevState.ON,)

    def read_WarningFileCounter(self, the_att):
        self.info_stream("read_WarningFileCounter")
        the_att.set_value(self.attr_warning)

    def is_WarningFileCounter_allowed(self, req_type):
        return self.get_state() in (PyTango.DevState.ON,)

    def read_FailedFileCounter(self, the_att):
        self.info_stream("read_FailedFileCounter")
        the_att.set_value(self.attr_failed)

    def is_FailedFileCounter_allowed(self, req_type):
        return self.get_state() in (PyTango.DevState.ON,)


# 1- blocco di partenza di un device Tango
if __name__ == '__main__':
    util = PyTango.Util(sys.argv)
    util.add_class(txtImporterClass, txtImporter)

    U = PyTango.Util.instance()
    U.server_init()
    U.server_run()
