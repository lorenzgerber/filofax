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
        event_list              list        - here all Event
                                      class objects are stored
        selected_date           date         - the selected date
        selected_event          uuid         - the ID of the selected event
        selected_day_indices    list         - list with (currently list indices), future, should be uuid's?
        selected_month_indices  list         - list with (currently list indices), future, should be uuid's?
        mode                    numeric      - value 0 = event, 1 = day, 2 = month

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
        self.mode = 0 # mode 0 = event, 1 = day, 2 = month

    # prints out the number of entries in the filofax
    def __str__(self):
        return ('This Filofax contains ' + str(len(self.event_list)) + ' events.\n' +
                str(self.selected_event) + '\n' + str(self.selected_date) + '\n' +
                str(self.selected_day_indices) + '\n' + str(self.selected_month_indices) + '\n')



    ###################
    # User Menu related
    ###################

    # prints out the user menu
    def menu(self):
        menu_text = ('\n1. switch to event view \n' +
                     '2. switch to day view \n' +
                     '3. switch to month view \n' +
                     '4. show previous \n' +
                     '5. show current \n' +
                     '6. show next \n' +
                     '7. enter new event \n' +
                     '8. remove event \n' +
                     '9. jump to day/month \n' +
                     '99. save and exit \n ')
        print(menu_text)

    def read_user_selection(self):
        return input('make your choice \n')




    #####################
    # add / remove events
    #####################

    # add a new event
    def add_event(self, event):
        self.event_list.append(event)

    # removes an event
    def remove_event(self, event):
        remove_event_index = self.event_list.index([x for x in self.event_list if x.unique_id == event][0])
        del self.event_list[remove_event_index]






    #####################################################################
    # populate: selected_event, selected_date, day_indices, month_indices
    #####################################################################

    # populate selected_event and selected_date for mode changes
    def populate_selected_event_date(self):
        if not self.selected_event == None:
            self.selected_date = datetime_filofax([x for x in self.event_list
                                                   if x.unique_id == self.selected_event][0].date_time)
            if not self.selected_date == None:
                try:
                    self.selected_event = [x for x in self.event_list if x.date_time >= self.selected_date][0].unique_id
                except IndexError:
                    try:
                        self.selected_event = [x for x in self.event_list if x.date_time <= self.selected_date][0].unique_id
                    except IndexError:
                        print('There are no entries in the filofax')


    # populate selected date from selected_event
    def populate_selected_date(self):
        self.sort_events()
        current_event_index = self.event_list.index([x for x in self.event_list if x.unique_id == self.selected_event][0])
        self.selected_date = self.event_list[current_event_index].date_time

    # populate selected_event from selected_date for day jump
    # find if there is an event on the selected day else, set selected_event to None
    def populate_selected_event_day(self):
        self.sort_events()
        try:
            self.selected_event = [x for x in self.event_list if x.date_time.date() == self.selected_date.date()][0].unique_id
        except ValueError:
            self.selected_event = None

    # populate selected_event from selected_date for month jump
    # find if there is an event within the month of selected_date
    def populate_selected_event_month(self):
        self.sort_events()
        try:
            self.selected_event = [x for x in self.event_list if x.date_time.year == self.selected_date.year
                                   and x.date_time.month == self.selected_date.month][0].unique_id
        except ValueError:
            self.selected_event = None

    # populate the day_indices from selected_date
    def populate_day_indices(self):
        try:
            day_indices = [x for x, n in enumerate(self.event_list) if n.date_time.date() == self.selected_date.date()]
            event_list_day = [self.event_list[i] for i in day_indices]
            day_uuids = [Event.unique_id for Event in event_list_day]
        except ValueError:
            day_uuids = []
            print('There are no events in day: ' + str(self.selected_date.date()))
        self.selected_day_indices = day_uuids

    # populate the month_indices from the selected_date
    def populate_month_indices(self):
        try:
            month_indices = (x for x, n in enumerate(self.event_list) if n.date_time.month == self.selected_date.month and
                 n.date_time.year == self.selected_date.year)
            event_list_month = [self.event_list[i] for i in month_indices]
            month_uuids = [Event.unique_id for Event in event_list_month]
        except ValueError:
            month_uuids = []
            print('There are no events in month: ' + str(self.selected_date.year) + ' ' + str(self.selected_date.month))
        self.selected_month_indices = month_uuids





    ###############
    # update chains
    ###############

    # update from selected_event: selected_date, day_indices, month_indices
    def update_chain_event(self):
        # update selected_date
        self.populate_selected_date()
        # populate day_indices
        self.populate_day_indices()
        # populate month_indices
        self.populate_month_indices()

    # update from selected_date for day jump: selected_event, day_indices, month_indices
    def update_chain_day(self):
        # update selected_event
        self.populate_selected_event_day()
        # update day_indices
        self.populate_day_indices()
        # month indices
        self.populate_month_indices()


    # update from selected_date for month jump:
    def update_chain_month(self):
        # update selected_event
        self.populate_selected_event_month()
        # update day_indices
        self.populate_day_indices()
        # update mont_indices
        self.populate_month_indices()





    # Jumps to date 'date_time' or date of next event after 'date_time'
    def jump_to_date(self, date_time):
        # find event_id and of next event equal or bigger than
        # date_time and set selected_event to it
        self.find_event_by_datetime(date_time)
        # call update_chain
        self.update_chain_event()

    # sets selected date to the first day of chosen month
    # can result in empty selected event etc.
    def jump_to_month(self, date_time):
        # look up event_id of first event in month and set to selected_event
        # call update_chain
        self.update_chain_event()

    # sets selected_event to chosen event
    # should always work
    def jump_to_event(self, event_id):
        # check if there is an event with event_id
        # set selected_event to event_id
        # call update_chain
        self.update_chain_event()


    # finds the event equal or next to given datetime
    # date input as date time. Will be stripped to
    # year, month, day, hour, minute
    # This function can be used to get a valid entry for selected event
    def find_event_by_datetime(self, date_time):
        try:
            from datetime import datetime
            date_time = datetime(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute)
            self.sort_events()
            self.selected_event = [x for x in self.event_list if x.date_time >= date_time][0].unique_id
        except IndexError:
            print('There are currently no events in the filofax')
            self.selected_event = None


    ##########################
    # Check position of events
    ##########################

    # is last event
    def last_event(self):
        self.sort_events()
        if len(self.event_list) == (self.selected_event_index()+1):
            return True
        return False

    # is first event
    def first_event(self):
        self.sort_events()
        if (self.selected_event_index()+1) == 1:
            return True
        return False

    # get index of selected_event
    def selected_event_index(self):
        self.sort_events()
        selected_event_index = self.event_list.index([x for x in self.event_list if x.unique_id == self.selected_event][0])
        return selected_event_index





    ################################################################
    # methods to go back and forth by one unit, event, day and month
    ################################################################

    # to be rewritten
    def next_unit(self):
        if self.mode == 0:
            self.next_event()
        elif self.mode == 1:
            self.next_day()
        elif self.mode == 2:
            self.next_month()

    # next event
    def next_event(self):
        # look up selected_event and advance by one in time
        self.sort_events()
        if not self.last_event():
            self.selected_event = self.event_list[self.selected_event_index()+1].unique_id
        else:
            print('Current event is the last')
        # call update_chain
        self.update_chain_event()

    # next day
    def next_day(self):
        from datetime import timedelta
        self.sort_events()
        self.selected_date = self.selected_date + timedelta(days = 1)
        self.populate_day_indices()

    # next month
    def next_month(self):
        from datetime import timedelta
        self.sort_events()
        self.selected_date = self.selected_date + timedelta(months = 1)
        self.populate_month_indices()


    # select correct method based on self.mode
    def previous_unit(self):
        if self.mode == 0:
            self.previous_event()
        elif self.mode == 1:
            self.previous_day()
        elif self.mode == 2:
            self.previous_month()

    #previous event
    def previous_event(self):
        # check if there is event before selected_event
        # set selected_event to one before in time to current selected_event
        self.sort_events()
        if not self.first_event():
            self.selected_event = self.event_list[self.selected_event_index()-1].unique_id
        else:
            print('Current event is the first')
        # call update_chain
        self.update_chain_event()

    # previous day
    def previous_day(self):
        from datetime import timedelta
        self.sort_events()
        self.selected_date = self.selected_date - timedelta(days = 1)
        self.populate_day_indices()


    # previous month
    def previous_month(self):
        from datetime import timedelta
        self.sort_events()
        self.selected_date = self.selected_date - timedelta(months = 1)
        self.populate_month_indices()




    ################
    # Print commands
    ################

    # choose correct viewer according self.mode
    def show_current(self):
        if self.mode == 0:
            self.show_event()
        elif self.mode == 1:
            self.show_day()
        elif self.mode == 2:
            self.show_month()

    # print selected_event to screen
    def show_event(self):
        # output content of selected_event
        try:
            print([x for x in self.event_list if x.unique_id == self.selected_event][0])
        except IndexError:
            print('\nThere is currently no event selected\n')


    # print events from selected_day to screen
    def show_day(self):
        # output content of day_indices
        for iii in self.selected_day_indices:
            self.selected_event = [x for x in self.event_list if x.unique_id == iii][0].unique_id
            self.show_event()


    # print events from month of selected_day to screen
    def show_month(self):
        for iii in self.selected_month_indices:
            self.selected_event = [x for x in self.event_list if x.unique_id == iii][0].unique_id
            self.show_event()


    # prints a sorted list of all events
    def show_all_events(self):
        self.sort_events()

        for item in self.event_list:
            print("{}| {}| {}| {}".format(str(item.date_time.date()).ljust(7),
                                          str(item.date_time.time()).ljust(5),
                                          item.description.ljust(50),
                                          str(item.unique_id)))




    # additional methods / help methods

    # sorts all events according date and time
    def sort_events(self):
        self.event_list.sort(key=lambda e: e.date_time)

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

    # help function string date and time to datetime
    @staticmethod
    def string_date_time_convert(date, time):
        from datetime import datetime
        date = datetime.strptime(str(date), "%y%m%d").date()
        time = datetime.strptime(str(time), "%H%M").time()
        date_time = datetime.combine(date, time)
        return date_time
    
# help function ot set datetime precision to YMDHM
def datetime_filofax(datetime_in):
    from datetime import datetime
    datetime_out = datetime(datetime_in.year, datetime_in.month,
                            datetime_in.day, datetime_in.hour,
                            datetime_in.minute)
    return datetime_out




class Event:
    """This class is the main data container

    Attributes:
        unique_id:      string     - a UUID
        date_time:      datetime   - date and time of event
        description:    string     - description of event

    methods:
    """

    # date and time as date/time/datetime.date()/datetime.time() objects
    def __init__(self, date_time, description):
        from datetime import datetime
        from uuid import uuid4
        self.unique_id = uuid4()
        #time = datetime.time(time.hour, time.minute)
        #self.date_time = datetime.combine(date, time)
        self.date_time = date_time
        self.description = description

    @classmethod
    def user_input(cls):
        from datetime import datetime
        date_input = input("Please enter date for new event yyyymmdd: ")
        time_input = input("Please enter time for new event hhmm: ")
        cls.date = datetime.strptime(str(date_input), "%y%m%d").date()
        cls.time = datetime.strptime(str(time_input), "%H%M").time()
        cls.description = input("Please enter event description: ")
        cls.date_time = datetime.combine(cls.date, cls.time)
        print(cls.date)
        print(cls.time)
        return Event(cls.date_time, cls.description)

    def __str__(self):
        event_summary = ('Date: ' + str(self.date_time.date()) + '\n' +
                         'Time: ' + str(self.date_time.time()) + '\n' +
                         'Description: ' + str(self.description) + '.')
        return event_summary

# main

def main():
    from datetime import datetime

    filo = Filofax()
    filo.load()

    # set selected_date
    filo.selected_date = datetime.now()
    # set format/precision to Year, Month, day, hour, minutes
    filo.selected_date = datetime_filofax(filo.selected_date)

    #set selected_event
    filo.find_event_by_datetime(filo.selected_date)

    #show current event
    print('\nToday is the ' + str(datetime.today().date()) + '\n' +
          'The next upcoming event is : \n')
    filo.show_event()

    # user menu loop
    menu_select = ''
    while menu_select != '99':


        filo.menu()
        menu_select = filo.read_user_selection()

        # event view
        if menu_select == '1':
            filo.mode = 0
            filo.populate_selected_event_date()
            filo.populate_day_indices()
            filo.populate_month_indices()

        # day view
        if menu_select == '2':
            filo.mode = 1
            filo.populate_selected_event_date()
            filo.populate_day_indices()
            filo.populate_month_indices()

        # month view
        if menu_select == '3':
            filo.mode = 2
            filo.populate_selected_event_date()
            filo.populate_day_indices()
            filo.populate_month_indices()

        # show previous
        if menu_select == '4':
            filo.previous_unit()
            filo.show_current()

        # show current
        if menu_select == '5':
            filo.show_current()

        # show next
        if menu_select == '6':
            filo.next_unit()
            filo.show_current()

        # add event
        if menu_select == '7':
            filo.add_event(Event.user_input())

        # remove event
        if menu_select == '8':
            print('current event is: \n')
            filo.show_event()
            remove_yes_no = input('\nDo you want to remove this event? (yes/no)\n')
            if remove_yes_no  == 'yes':
                filo.remove_event(filo.selected_event)
                print('Event removed')
                # reset selected event
                filo.find_event_by_datetime(filo.selected_date)

        # jump to day/month
        if menu_select == '9':
            return

        # show all events
        if menu_select == '10':
            filo.show_all_events()

        if menu_select == '11':
            print(filo.selected_month_indices)
            print(filo.selected_day_indices)


    filo.save()
    return filo

main()

#### create some records
#from datetime import datetime
#filo = Filofax()
#filo.load()
#filo.add_event(Event(datetime(year = 2015, month = 10, day = 22, hour = 22, minute = 00), 'drink a beer with Fritz'))
#filo.add_event(Event(datetime(year = 2015, month = 10, day = 22, hour = 12, minute = 00), 'eat lunch with Paul'))
#filo.add_event(Event(datetime(year = 2015, month = 10, day = 23, hour = 14, minute = 00), 'drink a coffee with Susanne'))
#filo.save()
# set selected_date
#filo.selected_date = datetime(year = 2015, month = 10, day = 22)
# set format/precision to Year, Month, day, hour, minutes
#filo.selected_date = datetime_filofax(filo.selected_date)

#set selected_event
#filo.find_event_by_datetime(filo.selected_date)

#show current event
#print('\nToday is the ' + str(datetime.today().date()) + '\n' +
#      'The next upcoming event is : \n')

#filo.show_event()
