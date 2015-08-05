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
        selected_event  string       - the ID of the selected event

    Methods:
        save_db:
        load_db:
        next_day:
        next_event:
        previous_day:
        previous_event:
        show_day:
        show_month:
        show_all_events:
        add_event:
        remove_event:
        sort_events:
    """

    # instantiates a new filofax class object
    def __init__(self):
        import datetime

        self.event_list = []
        self.selected_date = datetime.date.today()

    # prints out the number of entries in the filofax
    def __str__(self):
        return 'This Filofax contains ' + str(len(self.event_list)) + ' events.'

    # prints out the user menu
    def menu(self):
        return

    # adds a new event
    def add_event(self, event):
        self.event_list.append(event)

    # sorts all events according date and time
    def sort_events(self):
        self.event_list.sort(key=lambda e: e.datetime)

    # prints a sorted list of all events
    def show_events(self):
        self.sort_events()

        for item in self.event_list:
            print("{}| {}| {}".format(str(item.datetime.date()).ljust(7),
                                      str(item.datetime.time()).ljust(5),
                                      item.description))

    # save event list to file
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
        date_time:       datetime   - date and time of event
        description:    string     - description of event

    methods:
    """

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


def main():
    filo = Filofax()
    print(filo)
    print('Load Data...\n')
    filo.load()
    print(filo)
    print("""
    1. new entry
    2. exit)
    return filo

main()
