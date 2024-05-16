from phi.tools import Toolkit

import threading as th
import time as t
import sched as s
import datetime as d


class Scheduler(Toolkit):
    def __init__(self):
        self.current_time = t.time()
        self.scheduler = s.scheduler(t.time, t.sleep)
        self.scheduler.enter(t.time()+1, 1, self._run)
        self.scheduler.run()

    def _run(self):
        self.current_time = t.time()
        self.scheduler.enter(t.time()+1, 1, self._run)

    def call_at(self, 
                func, 
                arguments, 
                prio = 10, 
                microsecond = d.datetime.microsecond(), 
                second = d.datetime.second()+1, 
                minute = d.datetime.minute()+1, 
                hour = d.datetime.hour(), 
                day = d.datetime.day(), 
                month = d.datetime.month(), 
                year = d.datetime.year()
                ):
        """call_at is a tool that allows you to call a method at a later time. This can be used to make periotic API calls
        
        Args
            func (method): (required) This is the method to call when the time has elapsed.
            arguments (args): (optional) The arguments for the method to call when the time has elapsed.
            prio (integer): (optional) The priority of the method to call when the time has elapsed. Default: 10
            microsecond (integer): (optional) number of microseconds of the time.
            second (integer): (optional) number of seconds of the time.
            minute (integer): (optional) number of minutes of the time.
            hour (integer): (optional) number of hours of the time.
            day (integer): (optional) number of day of the time.
            month (integer): (optional) number of month of the time.
            year (integer): (optional) number of year of the time."""
        time = d.datetime(year, month, day, hour, minute, second, microsecond)
        self.scheduler.enterabs(time, prio, func, arguments)

    def call_in(self,
                func, 
                arguments,  
                seconds, 
                prio = 10
                ):
        """call_in is a tool that allows you to call a method in a number of seconds. This can be used to make periotic API calls"""
        self.scheduler.enter(t.time()+seconds, prio, func, arguments)

    
        
