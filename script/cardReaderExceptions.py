#!/usr/bin/env python3

""" cardReaderExceptions.py
    
    Description: This contains custom exception classes for the cardReader interface 
    
                Could've combined some exceptions but I did some research and found it's
                better to not use generic exceptions, but i might be interpreting that wrong.
                
                I'll keep the docstrings out of this class cause I think its fairly simple to
                understand 
"""

class MSR605ConnectError(Exception):
    def __init__(self, arg):
        super(MSR605ConnectError, self).__init__(arg)
        
class CardReadError(Exception):
    #also stores the tracks so some card track data is provided if this error occurs
    def __init__(self, arg, tracks): 
        super(CardReadError, self).__init__(arg)
        self.tracks = tracks
        
class CardWriteError(Exception):
    def __init__(self, arg):
        super(CardWriteError, self).__init__(arg)
                
class EraseCardError(Exception):
    def __init__(self, arg):
        super(EraseCardError, self).__init__(arg)
        
class StatusError(Exception):
    #also stores the error number from the status, which is important in finding out what went wrong
    def __init__(self, arg, errorNum):
        super(StatusError, self).__init__(arg)
        self.errorNum = errorNum

class CommunicationTestError(Exception):
    def __init__(self, arg):
        super(CommunicationTestError, self).__init__(arg)
        
class SensorTestError(Exception):
    def __init__(self, arg):
        super(SensorTestError, self).__init__(arg)
        
class RamTestError(Exception):
    def __init__(self, arg):
        super(RamTestError, self).__init__(arg)

class GetDeviceModelError(Exception):
    def __init__(self, arg):
        super(GetDeviceModelError, self).__init__(arg)
        
class GetFirmwareVersionError(Exception):
    def __init__(self, arg):
        super(GetFirmwareVersionError, self).__init__(arg)
        
class SetCoercivityError(Exception):
    #also stores the coercivity, since this is a little more generic than the the other exceptions
    def __init__(self, arg, coercivity):
        super(SetCoercivityError, self).__init__(arg)
        self.coercivity = coercivity #hi or low coercivity
        
class GetCoercivityError(Exception):
    def __init__(self, arg):
        super(GetCoercivityError, self).__init__(arg)

class DecodeError(Exception):
    def __init__(self, arg):
        super(DecodeError, self).__init__(arg)