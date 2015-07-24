# Programmeringsteknik webbkurs KTH Kodskelett
# Lorenz Gerber
# 22.07.2015
# Draft of classes and functions for the
# '192 Filofax' exercise

# This file contains the code draft for '192 Filofax' project
# The planned design uses classes.
#
# Thoughts about different ways to implement:
#
# Dynamic implementation
# An unsorted heap of event objects that have
# attributes date and time. They are selected dynamically by
# filtering when needed, i.e. to show one day, one month etc.
#
# Months and days could be implemented as transient objects that
# are created on request, i.e. the constructor would filter the
# main data table
#
# Flat implementation
# The main data table is a list of event objects that is kept
# sorted. Sort first day, then time. Data access is implemented
# as methods on the main data table object
#
# For using a GUI, probably selecting a time period and showing
# it on the screen has to be separated
#
# Deep implementation
# Year, month and day are all object types. Day has a list container
# for data. In a more extreme case even hours could be objects living
# in day objects. As there would be a chain of inheritance, one could
# then easily work on event objects, with the selecting methods inherited
# from the parent classes.


class EventDB:
    """ This class will be a data container for all
    Event class objects.

    Attributes:
        EventList       list        - here all Event
                                      class objects are stored
        selected_Date   date        - the currently selected date

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

class Event:
    """This class is the main data container

    Attributes:
        date:           date       - date of event
        time:           time       - time of event
        description:    string     - description of event

    methods:
    """
