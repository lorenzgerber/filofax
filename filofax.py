# Programmeringsteknik webbkurs KTH Kodskelett
# Lorenz Gerber
# 22.07.2015
# Draft of classes and functions for the
# '192 Filofax' exercise
#
# - data are stored in a file using 'pickle'
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
        return

    # prints out the user menu
    def menu(self):
        return

    def read_user_selection(self):
        return

    # adds a new event
    def add_event(self, event):
        return

    # removes an event
    def remove_event(self, event):
        return

    # sets selected date
    def jump_to_date(self, date):
        return

    # sets selected date to the first day of chosen month
    def jump_to_month(self, month):
        return

    # sets selected_event to chosen event
    def jump_to_event(self, event_id):
        return

    # advances selected_day by one
    def next_day(self):
        return

    # advances selected_day to first of next month
    def next_month(self):
        return

    # advances selected_event to next in time
    def next_event(self):
        return

    # decreases selected_day by one
    def previous_day(self):
        return

    # decreases selected_day to first of previous month
    def previous_month(self):
        return

    # decreases selected_event to previous in time
    def previous_event(self):
        return

    # print events from selected_day to screen
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
        return

    # prints a sorted list of all events
    def show_events(self):
        return

    # save event_list to file
    def save(self):
        return

    # loads event list from file
    def load(self):
        return


class Event:
    """This class is the main data container

    Attributes:
        unique_id:      string     - a UUID
        date_time:      datetime   - date and time of event
        description:    string     - description of event

    methods:
    """

    def __init__(self, date, time, description):
        return


# main

FILENAME = 'event_data.pkl'
filo = Filofax(FILENAME)

# menu_select = '';
# while menu_select != '99':
#     filo.meny()
#     menu_select = filo.read_user_selection()
#     # Utför detta val.

filo.save(FILENAME)


