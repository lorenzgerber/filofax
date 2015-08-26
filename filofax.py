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
    FiloEvent class objects.

    Attributes:
        event_list              list        - here all FiloEvent
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

    #####################
    # add / remove events
    #####################

    # add a new event
    def add_event(self, event):
        self.event_list.append(event)

    # remove event user interaction
    # def remove_event_interface(self):
    #    print('current event is: \n')

    #    self.show_event()
    #    remove_yes_no = input('\nDo you want to remove this event? (yes/no)\n')
    #    if remove_yes_no == 'yes':
    #        self.remove_event(self.selected_event)
    #        print('Event removed')
    #        # reset selected event
    #        self.find_event_by_datetime(self.selected_date)

    # removes an event, event is a uuid
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
            day_uuids = [FiloEvent.unique_id for FiloEvent in event_list_day]
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
            month_uuids = [FiloEvent.unique_id for FiloEvent in event_list_month]
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
    def jump_to_date(self, date_input):
        from datetime import datetime
        from tkinter import messagebox
        # find event_id and of next event equal or bigger than
        # date_time and set selected_event to it
        if self.mode == 1:
            try:
                self.selected_date = datetime.strptime(date_input, "%y%m%d")
            except ValueError:
                messagebox.showwarning('user entry error', 'your provided date value does not '
                                                           'confirm with the required format')
        elif self.mode == 2:
            try:
                self.selected_date = datetime.strptime(str(date_input + str(self.selected_date.day)), "%y%m%d")
            except ValueError:
                messagebox.showwarning('user entry error', 'your provided date value does not '
                                                           'confirm with the required format')
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
        if len(self.event_list) == (self.selected_event_index() + 1):
            return True
        return False

    # is first event
    def first_event(self):
        self.sort_events()
        if (self.selected_event_index() + 1) == 1:
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
        from tkinter import messagebox
        # look up selected_event and advance by one in time
        self.sort_events()
        if not self.last_event():
            self.selected_event = self.event_list[self.selected_event_index() + 1].unique_id
        else:
            print('Current event is the last')
            messagebox.showinfo('last', 'current event is the last')
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
        from tkinter import messagebox
        # check if there is event before selected_event
        # set selected_event to one before in time to current selected_event
        self.sort_events()
        if not self.first_event():
            self.selected_event = self.event_list[self.selected_event_index() - 1].unique_id
        else:
            print('Current event is the first')
            messagebox.showinfo('First', 'Current event is the first')
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
    # listbox_object is lb_events
    def show_current(self, listbox_object):
        if self.mode == 0:
            self.show_event(listbox_object)
        elif self.mode == 1:
            self.show_day(listbox_object)
        elif self.mode == 2:
            self.show_month(listbox_object)

    # print selected_event to screen
    def show_event(self, listbox_object):
        # output content of selected_event
        try:
            show_item = [x for x in self.event_list if x.unique_id == self.selected_event][0]
            listbox_object.insert(END, "{0:^15}{1:^15}{2:<30}".format(str(show_item.date_time.date()).ljust(7),
                                                                   str(show_item.date_time.time()).ljust(5),
                                                                   show_item.description.ljust(50)))
        except IndexError:
            print('\nThere is currently no event selected\n')

    # print events from selected_day to screen
    def show_day(self, listbox_object):
        # output content of day_indices
        print('\nSelected day is ' + str(self.selected_date.strftime('%A %d %B %Y')) + '\n')
        for iii in self.selected_day_uuids:
            self.selected_event = [x for x in self.event_list if x.unique_id == iii][0].unique_id
            self.show_event(listbox_object)

    # print events from month of selected_day to screen
    def show_month(self, listbox_object):
        print('\nSelected month is ' + str(self.selected_date.strftime('%B %Y')) + '\n')
        for iii in self.selected_month_uuids:
            self.selected_event = [x for x in self.event_list if x.unique_id == iii][0].unique_id
            self.show_event(listbox_object)

    # prints a sorted list of all events
    def show_all_events(self, listbox_object):
        self.sort_events()

        for item in self.event_list:
            listbox_object.insert(END, "{0:^15}{1:^15}{2:<40}".format(str(item.date_time.date()),
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
        from tkinter import messagebox
        try:
            date = datetime.strptime(str(date), "%y%m%d").date()
            time = datetime.strptime(str(time), "%H%M").time()
            date_time = datetime.combine(date, time)
        except ValueError:
            messagebox.showwarning('wrong date input', 'The provided date and/or time value(s)'
                                                    ' did not confirm with the required format')
        return date_time


# help function ot set datetime precision to YMDHM
def datetime_filofax(datetime_in):
    from datetime import datetime
    datetime_out = datetime(datetime_in.year, datetime_in.month,
                            datetime_in.day, datetime_in.hour,
                            datetime_in.minute)
    return datetime_out


class FiloEvent:
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
        return FiloEvent(cls.date_time, cls.description)

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
        self.scrollbar.grid(row=1, column=3, sticky=N + S)
        self.lb_events = Listbox(self, width=80)
        self.lb_events.config(yscrollcommand=self.scrollbar.set)
        self.lb_events.grid(column=0, row=1, rowspan=1, columnspan=3, sticky=N + E + S + W)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.scrollbar.config(command=self.lb_events.yview)

        self.display_date = StringVar()
        self.date_label = ttk.Label(self, textvariable=self.display_date, width=80)
        self.date_label.grid(column=1, row=0)

        # Next / Previous buttons
        self.next_button = ttk.Button(self, text='next', width=7, command=self.show_next)
        self.previous_button = ttk.Button(self, text='previous', width=7, command=self.show_previous)
        self.previous_button.grid(column=0, row=4, sticky=W)
        self.next_button.grid(column=1, row=4, sticky=W)

        # menu system
        # getting the toplevel window
        self.top = self.winfo_toplevel()
        self.menu_bar = Menu(self.top)
        self.top["menu"] = self.menu_bar

        # create a pulldown menu, and add it to the menu bar
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open", command=self.filo.load)
        self.file_menu.add_command(label="Save", command=self.filo.save)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.save_quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # create more pulldown menus
        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="New Event...", command=self.call_enter_new_event)
        self.edit_menu.add_command(label="Remove Event...", command=self.gui_remove_event)
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

    # gui method for removing events
    def gui_remove_event(self):
        from tkinter import messagebox
        # store the current selection of self.lb_events in a variable
        item = list(map(int, self.lb_events.curselection()))

        # if elif construct for different modes
        # mode 0 is event mode
        if self.filo.mode == 0:
            # get unique_id of current event. There is always a current event.
            show_item = [x for x in self.filo.event_list if x.unique_id == self.filo.selected_event][0]
            # messagebox, ask if the respective event shall be deleted
            if messagebox.askokcancel("Remove Events", "Shall the event:\n" + str(show_item.date_time) +
                                      " " + show_item.description + "\nbe removed?"):
                self.filo.remove_event(self.filo.selected_event)
                self.filo.find_event_by_datetime(self.filo.selected_date)
                self.show_current()
        # day mode
        elif self.filo.mode == 1:
            if len(item) > 0:
                print('day mode: remove current event')
                day_uuid = self.filo.selected_day_uuids[item[0]]
                show_item = [x for x in self.filo.event_list if x.unique_id == day_uuid][0]
                if messagebox.askokcancel("Remove Events", "Shall the event:\n" + str(show_item.date_time) +
                                      " " + show_item.description + "\nbe removed?"):
                    self.filo.remove_event(self.filo.selected_day_uuids[item[0]])
                    self.filo.populate_day_uuids()
                    self.show_current()
            else:
                messagebox.showinfo('no event selected', 'you need to select an event first')

        # month mode
        elif self.filo.mode == 2:
            if len(item) > 0:
                print('month mode: remove current event')
                month_uuid = self.filo.selected_month_uuids[item[0]]
                show_item = [x for x in self.filo.event_list if x.unique_id == month_uuid][0]
                if messagebox.askokcancel("Remove Events", "Shall the event:\n" + str(show_item.date_time) +
                                      " " + show_item.description + "\nbe removed?"):
                    self.filo.remove_event(self.filo.selected_month_uuids[item[0]])
                    self.filo.populate_month_uuids()
                    self.show_current()
            else:
                messagebox.showinfo('no event selected', 'you need to select an event first')
        else:
            print('no event removed')

    # method to call JumpTo popup window
    # JumpTo popup can not be called direct from
    # menu as in menu no args can be passed
    def call_jump_to(self):
        jumper = JumpToWindow(mode=self.filo.mode)
        self.wait_window(jumper.top)
        if jumper.data is not False:
            self.filo.jump_to_date(jumper.data)
            self.show_current()

    # method to call EnterNewEvent popup window
    # EnterNewEvent popup can not be called direct from
    # menu as in menu no args can be passed
    def call_enter_new_event(self):
        new_event = EnterNewEvent()
        self.wait_window(new_event.top)
        if new_event.entry_date is not False:
            from datetime import datetime
            assemble_date = self.filo.string_date_time_convert(new_event.date_data, new_event.time_data)
            assemble_date = datetime_filofax(assemble_date)
            self.filo.add_event(FiloEvent(assemble_date, new_event.event_data))
            self.mode_day()
            self.filo.jump_to_date(assemble_date.strftime("%y%m%d"))
            self.show_current()
            print('event added')

    # GUI method to be called for switching to event mode
    def mode_event(self):
        self.filo.mode = 0
        self.filo.populate_selected_event_date()
        self.filo.populate_day_uuids()
        self.filo.populate_month_uuids()
        self.display_date.set('selected event')
        self.show_current()

    # GUI method to be called for switching to day mode
    def mode_day(self):
        self.filo.mode = 1
        self.filo.populate_selected_event_date()
        self.filo.populate_day_uuids()
        self.filo.populate_month_uuids()
        self.display_date.set(str(self.filo.selected_date.strftime('%A %d %B %Y')))
        self.show_current()
    # GUI method to be called for switching to month mode
    def mode_month(self):
        self.filo.mode = 2
        self.filo.populate_selected_event_date()
        self.filo.populate_day_uuids()
        self.filo.populate_month_uuids()
        self.display_date.set(str(self.filo.selected_date.strftime('%B %Y')))
        self.show_current()

    # GUI method to be called for showing previous entry (event/day/month)
    def show_previous(self):
        self.lb_events.delete(0, END)
        self.filo.previous_unit()
        self.filo.show_current(self.lb_events)
        if self.filo.mode == 0:
            self.display_date.set('selected event')
        elif self.filo.mode == 1:
            self.display_date.set(str(self.filo.selected_date.strftime('%A %d %B %Y')))
        elif self.filo.mode == 2:
            self.display_date.set(str(self.filo.selected_date.strftime('%B %Y')))

    # GUI method to be called for showing current entry (event/day/month)
    def show_current(self):
        self.lb_events.delete(0, END)
        self.filo.show_current(self.lb_events)
        if self.filo.mode == 0:
            self.display_date.set('selected event')
        elif self.filo.mode == 1:
            self.display_date.set(str(self.filo.selected_date.strftime('%A %d %B %Y')))
        elif self.filo.mode == 2:
            self.display_date.set(str(self.filo.selected_date.strftime('%B %Y')))

    # GUI method to be called for showing next entry (event/day/month)
    def show_next(self):
        self.lb_events.delete(0, END)
        self.filo.next_unit()
        self.filo.show_current(self.lb_events)
        if self.filo.mode == 0:
            self.display_date.set('selected event')
        elif self.filo.mode == 1:
            self.display_date.set(str(self.filo.selected_date.strftime('%A %d %B %Y')))
        elif self.filo.mode == 2:
            self.display_date.set(str(self.filo.selected_date.strftime('%B %Y')))

    # GUI method to be called for showing all events
    def show_all(self):
        self.filo.show_all_events(self.lb_events)
        self.display_date.set('all events in the database')

    # GUI method to be called for save and quit filofax application
    def save_quit(self):
        self.filo.save()
        self.quit()

# popup window for 'jump to'
class JumpToWindow(Frame):
    def __init__(self, master=None, mode=0):
        ttk.Frame.__init__(self, master).grid()
        top = self.top = Toplevel(self)
        # event mode
        if mode == 0:
            self.label = Label(top, text='Please change to day or month mode').grid(row=0, column=0)
            self.data = False
            self.button = Button(top, text='OK', command=self.top.destroy).grid(row=1)
        # day mode
        if mode == 1:
            self.label = Label(top, text='Please enter day YYMMDD').grid(row=0, column=0)
            self.entry = Entry(top).grid(row=1)
            self.button = Button(top, text='OK', command=self.on_button).grid(row=2)
        # month mode
        if mode == 2:
            self.label = Label(top, text='Please enter month YYMM')
            self.label.grid(row=0, column=0)
            self.entry = Entry(top).grid(row=1)
            self.button = Button(top, text='OK', command=self.on_button).grid(row=2)

    # evaluating entry on button press event (JumpToWindow)
    def on_button(self):
        self.data = self.entry.get()
        self.top.destroy()


# Pop-up window for entering a new event
class EnterNewEvent(Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.grid()
        top = self.top = Toplevel(self)
        self.label_main = Label(top, text='please enter a new event').grid(column=0, row=0)
        self.label_event = Label(top, text='Event').grid(column=0, row=1)
        self.label_time = Label(top, text='Time (hhmm)').grid(column=0, row=2)
        self.label_date = Label(top, text='Date (yymmdd)').grid(column=0, row=3)
        self.entry_event = Entry(top).grid(column=2, row=1)
        self.entry_time = Entry(top).grid(column=2, row=2)
        self.entry_date = Entry(top).grid(column=2, row=3)
        self.button_ok = ttk.Button(top, text='OK', command=self.on_ok_button).grid(column=1, row=4)
        self.button_cancel = ttk.Button(top, text='Cancel', command=self.on_cancel_button).grid(column=2, row=4)

    # evaluating on_cancel button press event
    def on_cancel_button(self):
        self.date = False
        self.top.destroy()

    # evaluating ok_button press event in EnterNewEvent popup
    def on_ok_button(self):
        self.event_data = self.entry_event.get()
        self.time_data = self.entry_time.get()
        self.date_data = self.entry_date.get()
        self.top.destroy()


# Popup window to ask if selected event shall be deleted
app = Application('Filofax')
app.mainloop()
