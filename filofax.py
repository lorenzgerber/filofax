# Programmeringsteknik webbkurs KTH Kodskelett
# Lorenz Gerber
# 22.07.2015
# Draft of classes and functions for the
# '192 Filofax' exercise
#
# - data are stored in a file using 'pickle'
# - each event one line
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
        find_event_by_date:
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

    # instantiates a new filofax class object
    def __init__(self):

        self.event_list = []
        self.selected_event = None
        self.selected_date = None
        self.selected_day_indices = []
        self.selected_month_indices = []

    # prints out the number of entries in the filofax
    def __str__(self):
        return 'This Filofax contains ' + str(len(self.event_list)) + ' events.'

    # prints out the user menu
    def menu(self):
        menu_text = ('\n1. show current event \n' +
                     '2. show next event event \n' +
                     '3. show previous event \n' +
                     '4. enter new event \n' +
                     '5. remove event \n' +
                     '6. show all events \n' +
                     '7. show current day \n' +
                     '8. show next day \n' +
                     '9. show previous day \n' +
                     '10. show current month \n' +
                     '11. show next month \n' +
                     '12. show previous month\n' +
                     '99. save and exit \n ')
        print(menu_text)

    def read_user_selection(self):
        return input('make your choice \n')

    # adds a new event
    def add_event(self, event):
        self.event_list.append(event)

    # removes an event
    def remove_event(self, event):
        remove_event_index = self.event_list.index([x for x in self.event_list if x.unique_id == event][0])
        del self.event_list[remove_event_index]

    # populate the day_indices from selected_date
    def populate_day_indices(self):
        try:
            day_indices = self.event_list.index(
                [x for x in self.event_list if x.datetime.date() == self.selected_date]
            )
        except ValueError:
            day_indices = []
        self.selected_day_indices = day_indices

    # populate the month_indices from the selected_date

    # sets selected date
    def jump_to_date(self, date):
        # check if there is an event on date
        # find event_id and set selected_event
        self.find_event_by_datetime(date, time=0000)
        # call update_chain
        return

    # sets selected date to the first day of chosen month
    def jump_to_month(self, month):
        # check if there is an event in the month
        # look up event_id of first event in month and set to selected_event
        # call update_chain
        return

    # sets selected_event to chosen event
    def jump_to_event(self, event_id):
        # check if there is an event with event_id
        # set selected_event to event_id
        # call update_chain
        return

    # update from event_id, date, day_indices, month_indices
    def update_chain(self):
        # check date of selected_event
        # update selected_date
        # populate day_indices
        # populate month_indices
        return

    # finds the event equal or next to given datetime
    def find_event_by_datetime(self, date, time):
        from datetime import datetime
        date = datetime.strptime(str(date), "%y%m%d").date()
        time = datetime.strptime(str(time), "%H%M").time()
        search_for = datetime.combine(date, time)
        self.sort_events()
        self.selected_event = [x for x in self.event_list if x.datetime >= search_for][0].unique_id
        self.selected_date = date

    # advances selected_day by one
    def next_day(self):
        return

    # advances selected_day to first of next month
    def next_month(self):
        # check if there is an event in the next month
        # set selected_event to first event in next month
        # call update_chain
        return

    # advances selected_event to next in time
    def next_event(self):
        # look up selected_event and advance by one in time
        current_event_index = self.event_list.index([x for x in self.event_list if x.unique_id == self.selected_event][0])
        self.selected_event = self.event_list[current_event_index+1].unique_id
        # call update_chain


    # decreases selected_day by one
    def previous_day(self):
        # check if there is an event day before selected_date
        # find first event on day before selected_date and set selected_event
        # call update_chain
        return

    # decreases selected_day to first of previous month
    def previous_month(self):
        # check if there is event one month before selected_date
        # find first event in month before selected_date and set selected_event
        # call update_chain
        return

    # decreases selected_event to previous in time
    def previous_event(self):
        # check if there is event before selected_event
        # set selected_event to one before in time to current selected_event
        self.sort_events()
        current_event_index = self.event_list.index([x for x in self.event_list if x.unique_id == self.selected_event][0])
        self.selected_event = self.event_list[current_event_index-1].unique_id
        # update chain

    # print events from selected_day to screen
    def show_day(self):
        # output content of day_indices
        return

    # print events from month of selected_day to screen
    def show_month(self):
        # output content of month_indices
        return

    # print selected_event to screen
    def show_event(self):
        # output content of selected_event
        print([x for x in self.event_list if x.unique_id == self.selected_event][0])

    # sorts all events according date and time
    def sort_events(self):
        self.event_list.sort(key=lambda e: e.datetime)

    # prints a sorted list of all events
    def show_all_events(self):
        self.sort_events()

        for item in self.event_list:
            print("{}| {}| {}| {}".format(str(item.datetime.date()).ljust(7),
                                          str(item.datetime.time()).ljust(5),
                                          item.description.ljust(50),
                                          str(item.unique_id)))

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
        unique_id:      string     - a UUID
        date_time:      datetime   - date and time of event
        description:    string     - description of event

    methods:
    """

    def __init__(self, date, time, description):
        from datetime import datetime
        from uuid import uuid4
        date = datetime.strptime(str(date), "%y%m%d").date()
        time = datetime.strptime(str(time), "%H%M").time()
        self.unique_id = uuid4()
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

def main():
    from datetime import datetime

    filo = Filofax()
    filo.load()

    # set selected_date
    filo.selected_date = datetime.today().date()

    #set selected_event
    filo.find_event_by_datetime(filo.selected_date.strftime("%y%m%d"), datetime.now().strftime("%H%M"))

    #show current event
    print('\nToday is the ' + str(datetime.today().date()) + '\n' +
          'The next upcoming event is : \n')
    filo.show_event()

    # user menu loop
    menu_select = ''
    while menu_select != '99':




        filo.menu()
        menu_select = filo.read_user_selection()

        # show current event
        if menu_select == '1':
            filo.show_event()

        # next event
        if menu_select == '2':
            filo.next_event()
            filo.show_event()

        # previous event
        if menu_select == '3':
            filo.previous_event()
            filo.show_event()

        # add event
        if menu_select == '4':
            filo.add_event(Event.user_input())

        # remove event
        if menu_select == '5':
            print('current event is: \n')
            filo.show_event()
            remove_yes_no = input('\nDo you want to remove this event? (yes/no)\n')
            if remove_yes_no  == 'yes':
                filo.remove_event(filo.selected_event)
                print('Event removed')
                # reset selected event
                filo.find_event_by_datetime(filo.selected_date.strftime("%y%m%d"), datetime.now().strftime("%H%M"))


        # show all events
        if menu_select == '6':
            filo.show_all_events()

        # show current day
        if menu_select == '7':
            filo.populate_day_event_indices()


    filo.save()
    return filo

main()

#### create some records
#filo = Filofax()
#filo.load()
#filo.add_event(Event(151022,2200, 'drink a beer with Fritz'))
#filo.add_event(Event(151022,1200, 'eat lunch with Paul'))
#filo.add_event(Event(151023,1400, 'drink a coffee with Susanne'))
#filo.save()
