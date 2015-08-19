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
        selected_day_uuids    list         - list with (currently list indices), future, should be uuid's?
        selected_month_uuids  list         - list with (currently list indices), future, should be uuid's?
        mode                    numeric      - value 0 = event, 1 = day, 2 = month

    Methods:
        __init__:
        __str__:
        menu:
        read_user_selection:
        add_event:
        remove_event_interface:
        remove_event:
        populate_selected_event_date:
        populate_selected_date:
        populate_selected_event_day:
        populate_selected_event_month:
        populate_day_uuids:
        populate month_uuids:
        update_chain_event:
        update_chain_day:
        update_chain_month:
        jump_to_date:
        find_event_by_datetime:
        last_event:
        first_event:
        selected_event_index:
        next_unit:
        next_event:
        next_day:
        next_month:
        previous_unit:
        previous_event:
        previous_day:
        previous_month:
        show_current:
        show_event:
        show_day:
        show_month:
        show_all_events:
        sort_events:
        save:
        load:
        string_date_time_convert:
    """

    # instantiates a new filofax class object
    def __init__(self):

        self.event_list = []
        self.selected_event = None
        self.selected_date = None
        self.selected_day_uuids = []
        self.selected_month_uuids = []
        self.mode = 0  # mode 0 = event, 1 = day, 2 = month

    # prints out the number of entries in the filofax
    def __str__(self):
        return ('This Filofax contains ' + str(len(self.event_list)) + ' events.\n' +
                str(self.selected_event) + '\n' + str(self.selected_date) + '\n' +
                str(self.selected_day_uuids) + '\n' + str(self.selected_month_uuids) + '\n')

    ###################
    # User Menu related
    ###################

    # prints out the user menu
    def menu(self):
        mode = 'event'
        if self.mode == 0:
            mode = 'event'
        elif self.mode == 1:
            mode = 'day'
        elif self.mode == 2:
            mode = 'month'

        menu_text = ('\n\nYou are in ' + mode + ' view mode \n\n' +
                     'Main menu Filofax\n' +
                     '-----------------\n' +
                     '1. switch to event view \n' +
                     '2. switch to day view \n' +
                     '3. switch to month view \n' +
                     '4. show previous \n' +
                     '5. show current \n' +
                     '6. show next \n' +
                     '7. enter new event \n' +
                     '8. remove event \n' +
                     '9. jump to day/month \n' +
                     '10. show all events \n' +
                     '11. save data \n' +
                     '99. save and exit \n')
        print(menu_text)

    @staticmethod
    def read_user_selection():
        return input('make your choice \n')

    #####################
    # add / remove events
    #####################

    # add a new event
    def add_event(self, event):
        self.event_list.append(event)

    # remove event user interaction
    def remove_event_interface(self):
        print('current event is: \n')

        self.show_event()
        remove_yes_no = input('\nDo you want to remove this event? (yes/no)\n')
        if remove_yes_no == 'yes':
            self.remove_event(self.selected_event)
            print('Event removed')
            # reset selected event
            self.find_event_by_datetime(self.selected_date)

    # removes an event
    def remove_event(self, event):
        remove_event_index = self.event_list.index([x for x in self.event_list if x.unique_id == event][0])
        del self.event_list[remove_event_index]

    #####################################################################
    # populate: selected_event, selected_date, day_indices, month_indices
    #####################################################################

    # populate selected_event and selected_date for mode changes
    def populate_selected_event_date(self):
        if self.selected_event is not None:
            self.selected_date = datetime_filofax([x for x in self.event_list
                                                   if x.unique_id == self.selected_event][0].date_time)
            if self.selected_date is not None:
                try:
                    self.selected_event = [x for x in self.event_list
                                           if x.date_time >= self.selected_date][0].unique_id
                except IndexError:
                    try:
                        self.selected_event = [x for x in self.event_list
                                               if x.date_time <= self.selected_date][0].unique_id
                    except IndexError:
                        print('There are no entries in the filofax')

    # populate selected date from selected_event
    def populate_selected_date(self):
        self.sort_events()
        current_event_index = self.event_list.index([x for x in self.event_list
                                                     if x.unique_id == self.selected_event][0])
        self.selected_date = self.event_list[current_event_index].date_time

    # populate selected_event from selected_date for day jump
    # find if there is an event on the selected day else, set selected_event to None
    def populate_selected_event_day(self):
        self.sort_events()
        try:
            self.selected_event = [x for x in self.event_list
                                   if x.date_time.date() == self.selected_date.date()][0].unique_id
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
    def populate_day_uuids(self):
        try:
            day_indices = [x for x, n in enumerate(self.event_list) if n.date_time.date() == self.selected_date.date()]
            event_list_day = [self.event_list[i] for i in day_indices]
            day_uuids = [Event.unique_id for Event in event_list_day]
        except ValueError:
            day_uuids = []
            print('There are no events in day: ' + str(self.selected_date.date()))
        self.selected_day_uuids = day_uuids

    # populate the month_indices from the selected_date
    def populate_month_uuids(self):
        try:
            month_indices = (x for x, n in enumerate(self.event_list)
                             if n.date_time.month == self.selected_date.month and
                             n.date_time.year == self.selected_date.year)
            event_list_month = [self.event_list[i] for i in month_indices]
            month_uuids = [Event.unique_id for Event in event_list_month]
        except ValueError:
            month_uuids = []
            print('There are no events in month: ' + str(self.selected_date.year) + ' ' + str(self.selected_date.month))
        self.selected_month_uuids = month_uuids

    ###############
    # update chains
    ###############

    # update from selected_event: selected_date, day_indices, month_indices
    def update_chain_event(self):
        # update selected_date
        self.populate_selected_date()
        # populate day_indices
        self.populate_day_uuids()
        # populate month_indices
        self.populate_month_uuids()

    # update from selected_date for day jump: selected_event, day_indices, month_indices
    def update_chain_day(self):
        # update selected_event
        self.populate_selected_event_day()
        # update day_indices
        self.populate_day_uuids()
        # month indices
        self.populate_month_uuids()

    # update from selected_date for month jump:
    def update_chain_month(self):
        # update selected_event
        self.populate_selected_event_month()
        # update day_indices
        self.populate_day_uuids()
        # update mont_indices
        self.populate_month_uuids()

    # Jumps to date 'date_time' or date of next event after 'date_time'
    def jump_to_date(self):
        from datetime import datetime
        # find event_id and of next event equal or bigger than
        # date_time and set selected_event to it
        if self.mode == 1:
            self.selected_date = datetime.strptime(str(input('Please enter date (yymmdd):')), "%y%m%d")
        elif self.mode == 2:
            self.selected_date = datetime.strptime(str(input('Please enter month (yymm):') +
                                                       str(self.selected_date.day)), "%y%m%d")
        self.populate_day_uuids()
        self.populate_month_uuids()

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
        selected_event_index = self.event_list.index([x for x in self.event_list
                                                      if x.unique_id == self.selected_event][0])
        return selected_event_index

    ################################################################
    # methods to go back and forth by one unit, event, day and month
    ################################################################

    # select method forward move in filofax
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
        self.selected_date = self.selected_date + timedelta(days=1)
        self.populate_day_uuids()

    # next month
    def next_month(self):
        self.sort_events()
        self.selected_date = self.delta_months(self.selected_date, 1)
        self.populate_month_uuids()

    # select correct method based on self.mode
    def previous_unit(self):
        if self.mode == 0:
            self.previous_event()
        elif self.mode == 1:
            self.previous_day()
        elif self.mode == 2:
            self.previous_month()

    # previous event
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
        self.selected_date = self.selected_date - timedelta(days=1)
        self.populate_day_uuids()

    # previous month
    def previous_month(self):
        self.sort_events()
        self.selected_date = self.delta_months(self.selected_date, -1)
        self.populate_month_uuids()

    ################
    # Print commands
    ################

    # choose correct viewer according self.mode
    def show_current(self, list_object):
        if self.mode == 0:
            self.show_event(list_object)
        elif self.mode == 1:
            self.show_day(list_object)
        elif self.mode == 2:
            self.show_month(list_object)

    # print selected_event to screen
    def show_event(self, list_object):
        # output content of selected_event
        try:
            show_item = [x for x in self.event_list if x.unique_id == self.selected_event][0]
            list_object.insert(END, "{0:^15}{1:^15}{2:<30}".format(str(show_item.date_time.date()).ljust(7),
                                          str(show_item.date_time.time()).ljust(5),
                                          show_item.description.ljust(50)))
        except IndexError:
            print('\nThere is currently no event selected\n')

    # print events from selected_day to screen
    def show_day(self, list_object):
        # output content of day_indices
        print('\nSelected day is ' + str(self.selected_date.strftime('%A %d %B %Y')) + '\n')
        for iii in self.selected_day_uuids:
            self.selected_event = [x for x in self.event_list if x.unique_id == iii][0].unique_id
            self.show_event(list_object)

    # print events from month of selected_day to screen
    def show_month(self, list_object):
        print('\nSelected month is ' + str(self.selected_date.strftime('%B %Y')) + '\n')
        for iii in self.selected_month_uuids:
            self.selected_event = [x for x in self.event_list if x.unique_id == iii][0].unique_id
            self.show_event(list_object)

    # prints a sorted list of all events
    def show_all_events(self, list_object):
        self.sort_events()

        for item in self.event_list:
            list_object.insert(END, "{0:^15}{1:^15}{2:<40}".format(str(item.date_time.date()),
                                          str(item.date_time.time()),
                                          item.description))

    # additional methods / help methods
    @staticmethod
    def delta_months(source_date, months):
        import datetime
        import calendar
        month = source_date.month - 1 + months
        year = int(source_date.year + month / 12)
        month = month % 12 + 1
        day = min(source_date.day, calendar.monthrange(year, month)[1])
        return datetime.date(year, month, day)

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
        from uuid import uuid4
        self.unique_id = uuid4()
        self.date_time = date_time
        self.description = description

    @classmethod
    def user_input(cls):
        from datetime import datetime
        date_input = input("Please enter date for new event yymmdd: ")
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



from tkinter import *
from tkinter import ttk
from datetime import datetime

# main tkinter GUI class
class Application(Frame):
    def __init__(self, title, master=None):
        ttk.Frame.__init__(self, master, padding=" 3 3 3 3", relief='sunken')
        self.grid(column=0, row=0, sticky=(N, W, E, S))
        self.master.title(title)
        self.filo = Filofax()
        self.filo.load()
        # set selected_date
        self.filo.selected_date = datetime.now()
        # set format/precision to Year, Month, day, hour, minutes
        self.filo.selected_date = datetime_filofax(self.filo.selected_date)
        # set selected_event
        self.filo.find_event_by_datetime(self.filo.selected_date)

        self.main_frame()
        self.show_current()
        self.display_date.set('the next event:')





    def main_frame(self):
        # listbox with scrollbar
        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.scrollbar.grid(row=1,column=3, sticky=N+S)
        self.lb_events = Listbox(self, width=80)
        self.lb_events.config(yscrollcommand=self.scrollbar.set)
        self.lb_events.grid(column=0, row=1, rowspan=1, columnspan=3, sticky=N+E+S+W)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.scrollbar.config(command=self.lb_events.yview)

        self.display_date = StringVar()
        self.date_label = ttk.Label(self, textvariable=self.display_date, width=80)
        self.date_label.grid(column=1, row=0)

        # Next / Previous buttons
        self.next_button = ttk.Button(self, text='next', width=7, command=self.show_next)
        self.previous_button = ttk.Button(self, text='previous', width=7, command=self.show_previous)
        self.previous_button.grid(column=0,row=4, sticky=W)
        self.next_button.grid(column=1, row=4, sticky=W)



        # menu system
        # getting the toplevel window
        self.top=self.winfo_toplevel()
        self.menu_bar = Menu(self.top)
        self.top["menu"] = self.menu_bar

        # create a pulldown menu, and add it to the menu bar
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open")
        self.file_menu.add_command(label="Save")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # create more pulldown menus
        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="New Event...")
        self.edit_menu.add_command(label="Remove Event...")
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        self.mode_menu = Menu(self.menu_bar, tearoff=0)
        self.mode_menu.add_command(label="...event", command=self.mode_event)
        self.mode_menu.add_command(label="...day", command=self.mode_day)
        self.mode_menu.add_command(label="...month", command=self.mode_month)
        self.menu_bar.add_cascade(label="Display", menu=self.mode_menu)

        self.nav_menu = Menu(self.menu_bar, tearoff=0)
        self.nav_menu.add_command(label="Next", command=self.show_next)
        self.nav_menu.add_command(label="Previous", command=self.show_previous)
        self.nav_menu.add_command(label="Jump to...", command=self.call_jump_to)
        self.menu_bar.add_cascade(label="Navigate", menu=self.nav_menu)

        self.opt_menu = Menu(self.menu_bar, tearoff=0)
        self.opt_menu.add_command(label="Show all events", command=self.show_all)
        self.menu_bar.add_cascade(label="Options", menu=self.opt_menu)

        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About")
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)


    def hello():
        print("hello!")

    def call_jump_to(self):
        self.jumper = jump_to_window(mode=self.filo.mode)
        self.wait_window(self.jumper.top)



    def mode_event(self):
        self.filo.mode = 0
        self.filo.populate_selected_event_date()
        self.filo.populate_day_uuids()
        self.filo.populate_month_uuids()
        self.display_date.set('selected event')

    def mode_day(self):
        self.filo.mode = 1
        self.filo.populate_selected_event_date()
        self.filo.populate_day_uuids()
        self.filo.populate_month_uuids()
        self.display_date.set(str(self.filo.selected_date.strftime('%A %d %B %Y')))

    def mode_month(self):
        self.filo.mode = 2
        self.filo.populate_selected_event_date()
        self.filo.populate_day_uuids()
        self.filo.populate_month_uuids()
        self.display_date.set(str(self.filo.selected_date.strftime('%B %Y')))

    def show_previous(self):
        self.lb_events.delete(0,END)
        self.filo.previous_unit()
        self.filo.show_current(self.lb_events)
        if self.filo.mode==0:
            self.display_date.set('selected event')
        elif self.filo.mode==1:
            self.display_date.set(str(self.filo.selected_date.strftime('%A %d %B %Y')))
        elif self.filo.mode==2:
            self.display_date.set(str(self.filo.selected_date.strftime('%B %Y')))


    def show_current(self):
        self.lb_events.delete(0,END)
        self.filo.show_current(self.lb_events)
        if self.filo.mode==0:
            self.display_date.set('selected event')
        elif self.filo.mode==1:
            self.display_date.set(str(self.filo.selected_date.strftime('%A %d %B %Y')))
        elif self.filo.mode==2:
            self.display_date.set(str(self.filo.selected_date.strftime('%B %Y')))

    def show_next(self):
        self.lb_events.delete(0,END)
        self.filo.next_unit()
        self.filo.show_current(self.lb_events)
        if self.filo.mode==0:
            self.display_date.set('selected event')
        elif self.filo.mode==1:
            self.display_date.set(str(self.filo.selected_date.strftime('%A %d %B %Y')))
        elif self.filo.mode==2:
            self.display_date.set(str(self.filo.selected_date.strftime('%B %Y')))

    def show_all(self):
        self.filo.show_all_events(self.lb_events)
        self.display_date.set('all events in the database')

# popup window for 'jump to'
class jump_to_window(Frame):
    def __init__(self, master=None, mode=0):
        ttk.Frame.__init__(self, master)
        self.grid()
        top = self.top = Toplevel(self)
        if mode==0:
            self.label = Label(top, text='Please change to day or month mode')
            self.label.grid(row=0, column=0)
            self.button = Button(top, text='OK', command=self.top.destroy)
            self.button.grid(row=1)
        if mode==1:
            self.label = Label(top, text='Please enter day YYMMDD')
            self.label.grid(row=0, column=0)
            self.entry = Entry(top)
            self.entry.grid(row=1)
            self.button = Button(top, text='OK', command=self.top.destroy)
            self.button.grid(row=2)
        if mode==2:
            self.label = Label(top, text='Please enter month YYMM')
            self.label.grid(row=0, column=0)
            self.entry = Entry(top)
            self.entry.grid(row=1)
            self.button = Button(top, text='OK', command=self.top.destroy)
            self.button.grid(row=2)











app = Application('Filofax')
app.mainloop()
