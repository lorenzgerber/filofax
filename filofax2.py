# Programmeringsteknik webbkurs KTH Kodskelett
# Lorenz Gerber
# 22.07.2015
# Draft of classes and functions for the
# '192 Filofax' exercise
#
# - data are stored in a text file
# - per event one line
# - empty days are created on the fly for
#   visualisation but not as event objects without
#   description


class Filofax:
    """ This class will be a data container for all
    Event class objects.

    Attributes:
        event_list       list        - here all Event
                                      class objects are stored
        selected_date   date         - the currently selected date

    Methods:
        saveDB:
        loadDB:
        next_day:
        next_event:
        showDay:
        showMonth:
        showAllEvents:
        addEvent:
        removeEvent:
    """
    def __init__(self):
        import datetime

        self.event_list = []
        self.selected_date = datetime.date.today()

    def add_event(self, event):
        self.event_list.append(self, event)

class Event(self):
    """This class is the main data container

    Attributes:
        date:           date       - date of event
        time:           time       - time of event
        description:    string     - description of event

    methods:
    """
    def __init__(self, date, time, description):
        self.date = date
        self.time = time
        self.description = description

    def __init__(self):
        self.date = input('Please enter date for new event yymmdd: ')
        self.time = input('Please enter time for new event hhmm: ')
        self.description = input('Please enter event description: ')


    def __str__(self):
        event_summary = ('Date: ' + str(self.date) + '\n' +
                         'Time: ' + str(self.time) + '\n' +
                         'Description: ' + str(self.description) + '.')
        return event_summary






def main():
    filo = Filofax()
    



