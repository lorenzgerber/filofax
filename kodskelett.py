# Programmeringsteknik webbkurs KTH Kodskelett
# Lorenz Gerber
# 04.08.2015
# Draft of classes and functions for the
# '192 Filofax' exercise
#
# - two classes: Filofax and Event
# - data will be stored as objects using module 'pickle'
# - just events, not days are are stored.
#   Hence, empty days are created on the fly for visualisation
# - each event gets a unique id at creation
# - planned to implement a tkinter GUI
# - first a version with output on the console will be
#   implemented. For the GUI version, it could become necessary
#   to separate methods for data selection and data output
#   Initially, this will be all implemented in the show_x
#   methods.


class Filofax:
    """ This class is the data container for all
    Event class objects. It has some attributes to
    store user navigation parameters

    Attributes:
        event_list       list        - here all Event
                                      class objects are stored
        selected_date   date         - the selected date
        selected_event  uuid         - the ID of the selected event

    Methods:
        __init__:
        menu:
        read_user_selection:
        add_event:
        remove_event:
        jump_to_day:
        jump_to_month:
        jump_to_event:
        next_day:
        next_month:
        next_event:
        previous_day:
        previous_month:
        previous_event:
        show_day:
        show_month:
        sort_events:
        show_all_events:
        save:
        load:
    """

    # creates a new filofax class object
    def __init__(self, filename):
        import datetime

        self.event_list = []
        self.selected_date = datetime.date.today()
        return 'Filofax object created'

    # prints out the number of entries in the filofax
    def __str__(self):
        return 'This Filofax contains ' + str(len(self.event_list)) + ' events.'

    # prints out the user menu
    def menu(self):
        return

    def read_user_selection(self):
        return

    # adds a new event
    def add_event(self, event):
        self.event_list.append(event)
        return 'event added'

    # removes an event
    def remove_event(self, event):
        return

    # sets selected_date
    def jump_to_date(self, date):
        return

    # sets selected_date to the first day of chosen month
    def jump_to_month(self, month):
        return

    # sets selected_event to chosen event
    def jump_to_event(self, event_id):
        return

    # advances selected_date by one
    def next_day(self):
        return

    # advances selected_date to first of next month
    def next_month(self):
        return

    # advances selected_event to next in time
    def next_event(self):
        return

    # decreases selected_date by one
    def previous_day(self):
        return

    # decreases selected_date to first of previous month
    def previous_month(self):
        return

    # decreases selected_event to previous in time
    def previous_event(self):
        return

    # print events from selected_date to screen
    def show_day(self):
        return

    # print events from month of selected_day to screen
    def show_month(self):
        return

    # print selected_event to screen
    def show_event(self):
        return

    # sorts all events according date and time
    def sort_events(self):
        self.event_list.sort(key=lambda e: e.datetime)
        return 'all events sorted'

    # prints a sorted list of all events
    def show_events(self):
        self.sort_events()

        for item in self.event_list:
            print("{}| {}| {}".format(str(item.datetime.date()).ljust(7),
                                      str(item.datetime.time()).ljust(5),
                                      item.description))

    # save event_list to file
    def save(self):
        import pickle
        with open('filofaxdata.pkl', 'wb') as output:
            pickle.dump(self.event_list, output, pickle.HIGHEST_PROTOCOL)

    # loads event list from file
    def load(self):
        import pickle
        with open('filofaxdata.pkl', 'rb') as get_data:
            self.event_list = pickle.load(get_data)


class Event:
    """This class is the main data container

    Attributes:
        unique_id:      string     - a UUID
        date_time:      datetime   - date and time of event
        description:    string     - description of event

    methods:
    """

    # creates a new event object
    def __init__(self, date, time, description):
        from datetime import datetime
        date = datetime.strptime(str(date), "%y%m%d").date()
        time = datetime.strptime(str(time), "%H%M").time()
        self.datetime = datetime.combine(date, time)
        self.description = description

    @classmethod
    def user_input(cls):
        date_input = input("Please enter date for new event yymmdd: ")
        time_input = input("Please enter time for new event hhmm: ")
        cls.description = input("Please enter event description: ")
        return Event(date_input, time_input, cls.description)

    def __str__(self):
        event_summary = ('Date: ' + str(self.datetime.date()) + '\n' +
                         'Time: ' + str(self.datetime.time()) + '\n' +
                         'Description: ' + str(self.description) + '.')
        return event_summary


# main

FILENAME = 'event_data.pkl'
filo = Filofax(FILENAME)

menu_select = ''
while menu_select != '99':
    filo.meny()
    menu_select = filo.read_user_selection()

filo.save(FILENAME)


