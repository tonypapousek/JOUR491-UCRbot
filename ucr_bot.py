#! /usr/bin/env python

# ucr_bot.py
# Copyright (c) 2014 Tony Papousek <tony@papousek.org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the LICENSE file for more details.

import csv, string, datetime

def percent_change(old_value, new_value):
    return ((new_value - old_value) / abs(old_value)) * 100

def crime_rate(crime_count, population_count):
    return (float(crime_count) / float(population_count)) * 100000

def state_total(list_name, state_name, crime_selector, population_selector):
    # Initialize counters
    crime_counter = 0
    population_counter = 0
    city_counter = 0

    for current_city in list_name:
        selected_state = current_city[0]
        if state_name == selected_state and current_city[crime_selector]:
            crime_counter += int(current_city[crime_selector])
            population_counter += int(current_city[population_selector])
            city_counter += 1
    return [city_counter, crime_counter, population_counter]

def print_cities(list_name, state_name, number_of_cities, state_crime_rate):
    for current_city in list_name:
        selected_state = current_city[0]
        if state_name == selected_state and current_city[6]:
            city_rate_2012 = crime_rate(current_city[6], current_city[3])
            city_rate_2011 = crime_rate(current_city[17], current_city[14])
            city_rate_change = percent_change(city_rate_2011, city_rate_2012)

            # Print current year stats
            print "In 2012, there were %.2f counts of forcible rapes per 100,000 people in %s, %s." % (city_rate_2012, current_city[2], selected_state)

            # Comparison to last year
            if city_rate_change > 0:
                print "This is a %.2f percent increase from the rate of %.2f per 100,000 in 2011.\n" % (abs(city_rate_change),city_rate_2011)
            elif city_rate_change < 0:
                print "This is a %.2f percent decrease from the rate of %.2f per 100,000 in 2011.\n" % (abs(city_rate_change),city_rate_2011)
            else:
                print "The 2011 rate is the same.\n"

            # Comparison to state
            if number_of_cities == 1:
                print "%s is the primary source of rape statistics for %s\n" % (current_city[2], selected_state)

            # End Comparison
          #  print city_rate_2012

    return

# Read UCRdata.csv and put it in its own list
ucr_reader = csv.reader(open("UCRdata.csv", "rU"), dialect=csv.excel)
ucr_reader.next()
city_list = []
for row in ucr_reader:
    city_list.append(row)

# Read state_names.csv and put it in its own list
state_reader = csv.reader(open("state_names.csv", "rU"))
state_reader.next()
state_list = []
for row in state_reader:
    state_list.append(row)

# Loop through all states in list
for state in state_list:
    selected_state = state[0]
    print "================"
    print selected_state
    print "----------------"
    state_stats_2012 = state_total(city_list, selected_state, 6, 3)
    if state_stats_2012[1] == 0:
        print "There are no forcible rape statistics available for %s.\n" % (selected_state)

    elif state_stats_2012[1] != 0:
        # grab state_stats for 2011
        state_stats_2011 = state_total(city_list, selected_state, 17, 14)

        # calculate crime_rate for 2011 - 2012
        crime_rate_2012 = crime_rate(state_stats_2012[1], state_stats_2012[2])
        crime_rate_2011 = crime_rate(state_stats_2011[1], state_stats_2011[2])

        # calculate change is crime rate between 2012 and 2011
        crime_rate_change = percent_change(crime_rate_2011, crime_rate_2012)

        print "In 2012, there were %.2f counts of forcible rapes per 100,000 people in %s." % (crime_rate_2012, selected_state)

        # Determine rise, fall, or no change in crime
        if crime_rate_change > 0:
            print "This is a %.2f percent increase from the rate of %.2f per 100,000 in 2011.\n" % (abs(crime_rate_change),crime_rate_2011)
        elif crime_rate_change < 0:
            print "This is a %.2f percent decrease from the rate of %.2f per 100,000 in 2011.\n" % (abs(crime_rate_change),crime_rate_2011)
        else:
            print "The 2011 rate is the same.\n"

        print ("----------------\nCrime by city:\n----------------\n" )
        print_cities(city_list, selected_state, state_stats_2012[0], crime_rate_2012)

    else:
        print "Huh? Program error.\n You done messed up A-A-Ron!"
