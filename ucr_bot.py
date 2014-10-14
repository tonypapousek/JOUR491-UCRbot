#! /usr/bin/env python

# ucr_bot.py
# Copyright © 2014 Tony Papousek <tony@papousek.org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the LICENSE file for more details.

import csv, string, datetime

def state_total(list_name, state_name, crime_selector, population_selector):
    # Initialize counters
    crime_counter = 0
    population_counter = 0
    city_counter = 0

    for current_city in list_name:
        selected_state = current_city[0]
        if state_name == selected_state and current_city[crime_selector]:
        #    print "%s, %s" % (current_city[2], state_name)
            crime_counter += int(current_city[crime_selector])
            population_counter += int(current_city[population_selector])
            city_counter += 1
    return [city_counter, crime_counter, population_counter]
# Open csv file
ucr_reader = csv.reader(open("UCRdata.csv", "rU"), dialect=csv.excel)

# Skip header line
ucr_reader.next()

# Create empty list
city_list = []

# Throw all of csv in memory
for row in ucr_reader:
    city_list.append(row)

# Read state_names.csv and put it in it's own list
state_reader = csv.reader(open("state_names.csv", "rU"))
state_reader.next()

state_list = []

for row in state_reader:
    state_list.append(row)


for state in state_list:
    selected_state = state[0]
    print "================"
    print selected_state
    print "----------------"
    state_stats_2012 = state_total(city_list, selected_state, 6, 3)
    if state_stats_2012[1] == 0:
        print "There are no forcible rape statistics available for %s." % (selected_state)

    elif state_stats_2012[1] != 0:
        crime_rate_2012 = (float(state_stats_2012[1] / float(state_stats_2012[2]))) * 100000
        state_stats_2011 = state_total(city_list, selected_state, 17, 14)
        state_stats_2010 = state_total(city_list, selected_state, 27, 24)
        state_stats_2009 = state_total(city_list, selected_state, 37, 34)
        crime_rate_2011 = (float(state_stats_2011[1] / float(state_stats_2011[2]))) * 100000
        crime_rate_2010 = (float(state_stats_2010[1] / float(state_stats_2010[2]))) * 100000
        crime_rate_2009 = (float(state_stats_2009[1] / float(state_stats_2009[2]))) * 100000
        crime_rate_change = (crime_rate_2012 - crime_rate_2011) / abs(crime_rate_2011) * 100
        print "In 2012, there were %.2f counts of forcible rapes per 100,000 people in %s." % (crime_rate_2012, selected_state)
        if crime_rate_change > 0:
            print "This is a %.2f percent increase from the rate of %.2f per 100,000 in 2011." % (abs(crime_rate_change),crime_rate_2011)
        elif crime_rate_change < 0:
            print "This is a %.2f percent decrease from the rate of %.2f per 100,000 in 2011." % (abs(crime_rate_change),crime_rate_2011)
        else:
            print "The 2011 rate is the same."
    else:
        print "Huh? Program error.\n You done messed up A-A-Ron!"
