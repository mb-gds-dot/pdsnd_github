import time
import pandas as pd
import numpy as np
from sys import exit
from tabulate import tabulate


CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington DC': 'washington.csv' }

months = ['January', 'February', 'March', 'April', 'May', 'June', 'All']

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']

bike_rows = ['      o   ', '    _/\<_ ', '___(_)/(_)']



def enter_option_number(top_value):
    """
    Asks the user to input an integer value between 1 and top_value

    A value of 9 will Exit the program

    Inputs:
    top_value - integer - must be no higher than 8 (would need a bit of adjusting to handle higher values, but that is all that is needed for this exercise)

    Returns:
    The integer value entered by the user

    If the user enters a non-integer value or a value outside of the allowed range the program will request the input value again
    """
    option_num = 0
    while option_num < 1 or option_num > top_value:
        try:
            print_table_row('', '', False, 0, 0)
            option_val = input('│  Enter Option Number:                                    │  ')
            option_num = int(option_val)
        except ValueError:
            if option_val.upper() == 'YES' or option_val.upper() == 'Y':
                option_num = 1
            elif option_val.upper() == 'NO' or option_val.upper() == 'N':
                option_num = 2
            else:
                option_num = 0
        if option_num == 9:
            reprint_previous_row('Enter Option Number:', '9. Exit - Execution Stopped')
            print_table_row('', '', False, 0, 0)
            print_table_line('bottom')
            exit("")
        if option_num < 1 or option_num > top_value:
            option_num = 0
        if option_num == 0:
            reprint_previous_row('Enter Option Number:', 'Incorrect value entered - Please enter valid number')
    return option_num



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    print_table_row('', '', False, 0, 0)
    print_table_row('Please select one city:', '', True, 1, 4)
    print_table_row('', '', True, 2, 4)
    print_table_row(' 1. Chicago', '', True, 3, 4)
    print_table_row(' 2. New York City', '', False, 0, 0)
    print_table_row(' 3. Washington DC', '', False, 0, 0)
    print_table_row(' 9. Exit', '', False, 0, 0)
    print_table_row('', '', False, 0, 0)
    print_table_line('mid')

    city_num = enter_option_number(3)
    city = list(CITY_DATA)[city_num-1]
    reprint_previous_row('Enter Option Number:', str(city_num) + '. ' + city)
    print_table_row('', '', False, 0, 0)
    print_table_line('mid')

    # get user input for month (all, january, february, ... , june)
    print_table_row('', '', False, 0, 0)
    print_table_row('Please select a month:', '', True, 1, 14)
    print_table_row('', '', True, 2, 14)
    print_table_row(' 1. January', '', True, 3, 14)
    print_table_row(' 2. February', '', False, 0, 0)
    print_table_row(' 3. March', '', False, 0, 0)
    print_table_row(' 4. April', '', False, 0, 0)
    print_table_row(' 5. May', '', False, 0, 0)
    print_table_row(' 6. June', '', False, 0, 0)
    print_table_row(' 7. All Months', '', False, 0, 0)
    print_table_row(' 9. Exit', '', False, 0, 0)
    print_table_row('', '', False, 0, 0)
    print_table_line('mid')

    month_num = enter_option_number(7)
    month = months[month_num-1]
    reprint_previous_row('Enter Option Number:', str(month_num) + '. ' + month)
    print_table_row('', '', False, 0, 0)
    print_table_line('mid')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print_table_row('', '', False, 0, 0)
    print_table_row('Please select a week day:', '', True, 1, 24)
    print_table_row('', '', True, 2, 24)
    print_table_row(' 1. Monday', '', True, 3, 24)
    print_table_row(' 2. Tuesday', '', False, 0, 0)
    print_table_row(' 3. Wednesday', '', False, 0, 0)
    print_table_row(' 4. Thursday', '', False, 0, 0)
    print_table_row(' 5. Friday', '', False, 0, 0)
    print_table_row(' 6. Saturday', '', False, 0, 0)
    print_table_row(' 7. Sunday', '', False, 0, 0)
    print_table_row(' 8. All Days', '', False, 0, 0)
    print_table_row(' 9. Exit', '', False, 0, 0)
    print_table_row('', '', False, 0, 0)
    print_table_line('mid')

    day_num = enter_option_number(8)
    day = days[day_num-1]
    reprint_previous_row('Enter Option Number:', str(day_num) + '. ' + day)

    print_table_row('', '', False, 0, 0)
    print_table_line('mid')
    print_table_row('', '', False, 0, 0)
    print_table_row('You have selected:', '', True, 1, 34)
    print_table_row('', '', True, 2, 34)
    print_table_row(' City:     ' + city, '', True, 3, 34)
    print_table_row(' Month:    ' + month, '', False, 0, 0)
    print_table_row(' Weekday:  ' + day, '', False, 0, 0)
    print_table_row('', '', False, 0, 0)
    print_table_line('mid')

    return city, month, day



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    if city in CITY_DATA:
        try:
            df = pd.read_csv(CITY_DATA[city], parse_dates=True)

            df['Start Time'] = pd.to_datetime(df['Start Time']) # Convert the Start Time value to native DateTime data types

            if month != 'All':
                df = df[df['Start Time'].dt.month == months.index(month) + 1] # This uses values 1 = January to 12 = December

            if day != 'All':
                df = df[df['Start Time'].dt.day_of_week == days.index(day)] # This uses values 0 = Monday to 6 = Sunday

            print_table_row('', '', False, 0, 0)
            print_table_row('City Data File Read Successfully', CITY_DATA[city], False, 0, 0)
            print_table_row('', '', False, 0, 0)
            print_table_row('Columns:', str(len(df.axes[1])), False, 0, 0)
            print_table_row('Rows:', str(len(df.axes[0])), False, 0, 0)
            print_table_row('Column Names:', df.columns[0] + (' ' * (20 - len(df.columns[0]))) + '(' + str(df[df.columns[0]].dtype) + ')', False, 0, 0)
            for column in df.columns[1:]:
                print_table_row('', column + (' ' * (20 - len(column))) + '(' + str(df[column].dtype) + ')', False, 0, 0) #f"{column} ({df[column].dtype})"
            print_table_row('', '', False, 0, 0)
            print_table_row('First five rows of data:', '', False, 0, 0)
            print_table_line('bottom')

            #print('')
            print(tabulate(df.head(), headers='keys', tablefmt='fancy_grid'))
        except FileNotFoundError:
            print_table_row('', '', False, 0, 0)
            print_table_row('City Data File Not Found', '', False, 0, 0)
            print_table_row('', '', False, 0, 0)
            print_table_line('bottom')
            df = None

    else:
        print_table_row('', '', False, 0, 0)
        print_table_row('City Data File Not Found', '', False, 0, 0)
        print_table_row('', '', False, 0, 0)
        print_table_line('bottom')
        df = None
    
    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print_table_line('top')
    print_table_row('', '', False, 0, 0)
    print_table_row('Calculating The Most Frequent Times of Travel...', '', False, 0, 0)
    start_time = time.time()

    # display the most common month
    df['Month'] = df['Start Time'].dt.month
    month_counts = df['Month'].value_counts()
    month_max = month_counts.idxmax()
    month_max_count = month_counts.max()

    print_table_row('', '', False, 0, 0)
    print_table_row('Most common month:', months[month_max - 1] + (' ' * (38 - len(months[month_max - 1]))) + format(month_max_count, ",d") + ' records', False, 0, 0) # month_max will return an integer from 1 to 12

    # display the most common day of week
    df['WeekDay'] = df['Start Time'].dt.day_of_week
    day_counts = df['WeekDay'].value_counts()
    day_max = day_counts.idxmax()
    day_max_count = day_counts.max()

    print_table_row('', '', False, 0, 0)
    print_table_row('Most common week day:', days[day_max] + (' ' * (38 - len(days[day_max]))) + format(day_max_count, ",d") + ' records', False, 0, 0)

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    hour_counts = df['Hour'].value_counts()
    hour_max = hour_counts.idxmax()
    hour_max_count = hour_counts.max()
    if hour_max == 0:
        hour_max_string = '12 AM'
    elif hour_max < 12:
        hour_max_string = str(hour_max) + ' AM'
    elif hour_max == 12:
        hour_max_string = '12 PM'
    elif hour_max > 12:
        hour_max_string = str(hour_max - 12) + ' PM'

    print_table_row('', '', False, 0, 0)
    print_table_row('Most common hour of the day:', hour_max_string + (' ' * (38 - len(hour_max_string))) + format(hour_max_count, ",d") + ' records', False, 0, 0)

    print_table_row('', '', False, 0, 0)
    print_table_row('Elapsed time:', str(round(time.time() - start_time, 3)) + ' seconds', False, 0, 0)
    print_table_row('', '', False, 0, 0)
    print_table_line('mid')



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print_table_row('', '', False, 0, 0)
    print_table_row('Calculating The Most Popular Stations and Trip...', '', False, 0, 0)
    start_time = time.time()

    # display most commonly used start station
    start_counts = df['Start Station'].value_counts()
    start_max = start_counts.idxmax()
    start_max_count = start_counts.max()

    print_table_row('', '', False, 0, 0)
    print_table_row('Most common start station:', start_max + (' ' * (38 - len(start_max))) + format(start_max_count, ",d") + ' records', False, 0, 0)

    # display most commonly used end station
    end_counts = df['Start Station'].value_counts()
    end_max = end_counts.idxmax()
    end_max_count = end_counts.max()

    print_table_row('', '', False, 0, 0)
    print_table_row('Most common end station:', end_max + (' ' * (38 - len(end_max))) + format(end_max_count, ",d") + ' records', False, 0, 0)

    # display most frequent combination of start station and end station trip
    df['Start and End Station'] = df['Start Station'] + '!' + df['End Station']
    start_end_counts = df['Start and End Station'].value_counts()
    start_end_max = start_end_counts.idxmax()
    start_end_max_count = start_end_counts.max()

    print_table_row('', '', False, 0, 0)
    print_table_row('Most common trip:', start_end_max.split('!')[0] + ' to', False, 0, 0)
    print_table_row('', start_end_max.split('!')[1] + (' ' * (38 - len(start_end_max.split('!')[1]))) + format(start_end_max_count, ",d") + ' records', False, 0, 0)

    print_table_row('', '', False, 0, 0)
    print_table_row('Elapsed time:', str(round(time.time() - start_time, 3)) + ' seconds', False, 0, 0)
    print_table_row('', '', False, 0, 0)
    print_table_line('mid')



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print_table_row('', '', False, 0, 0)
    print_table_row('Calculating Trip Duration...', '', False, 0, 0)
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    total_duration_string = format(int(total_duration // (3600 * 24)), ",d") + ' days, ' + str(int(total_duration %  (3600 * 24) // 3600)) + ' hours, ' + str(int((total_duration % 3600) // 60)) + ' minutes, ' + str(int(total_duration %  60)) + ' seconds'

    print_table_row('', '', False, 0, 0)
    print_table_row('Total duration of all trips:', total_duration_string, False, 0, 0)

    # display mean travel time
    mean_duration = df['Trip Duration'].mean()
    mean_duration_string = str(int(mean_duration // 3600)) + ' hours, ' + str(int((mean_duration % 3600) // 60)) + ' minutes, ' + str(int(mean_duration %  60)) + ' seconds'

    print_table_row('', '', False, 0, 0)
    print_table_row('Mean duration of all trips:', mean_duration_string, False, 0, 0)


    print_table_row('', '', False, 0, 0)
    print_table_row('Elapsed time:', str(round(time.time() - start_time, 3)) + ' seconds', False, 0, 0)
    print_table_row('', '', False, 0, 0)
    print_table_line('mid')



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print_table_row('', '', False, 0, 0)
    print_table_row('Calculating User Stats...', '', False, 0, 0)
    start_time = time.time()

    # Display counts of user types
    user_counts = df['User Type'].value_counts()
    print_table_row('', '', False, 0, 0)
    first_cycle = True
    for user_type, user_count in user_counts.items():
        if first_cycle == True:
            print_table_row('User Types:', user_type + (' ' * (38 - len(user_type))) + format(user_count, ",d") + ' records', False, 0, 0)
            first_cycle = False
        else:
            print_table_row('', user_type + (' ' * (38 - len(user_type))) + format(user_count, ",d") + ' records', False, 0, 0)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print_table_row('', '', False, 0, 0)
        first_cycle = True
        for gender_type, gender_count in gender_counts.items():
            if first_cycle == True:
                print_table_row('Genders:', gender_type + (' ' * (38 - len(gender_type))) + format(gender_count, ",d") + ' records', False, 0, 0)
                first_cycle = False
            else:
                print_table_row('', gender_type + (' ' * (38 - len(gender_type))) + format(gender_count, ",d") + ' records', False, 0, 0)
    else:
        print_table_row('', '', False, 0, 0)
        print_table_row('Genders:', 'Gender information not available in this data file', False, 0, 0)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        birth_min = df['Birth Year'].min()
        birth_max = df['Birth Year'].max()
        print_table_row('', '', False, 0, 0)
        print_table_row('Earliest Birth Year:', str(int(birth_min)), False, 0, 0)
        print_table_row('', '', False, 0, 0)
        print_table_row('Latest Birth Year:', str(int(birth_max)), False, 0, 0)

        birth_counts = df['Birth Year'].value_counts()
        birth_max = birth_counts.idxmax()
        birth_max_count = birth_counts.max()
        print_table_row('', '', False, 0, 0)
        print_table_row('Most common Birth Year:', str(int(birth_max)) + (' ' * (38 - len(str(int(birth_max))))) + format(birth_max_count, ",d") + ' records', False, 0, 0)

    else:
        print_table_row('', '', False, 0, 0)
        print_table_row('Birth Year:', 'Birth Year information not available in this data file', False, 0, 0)


    print_table_row('', '', False, 0, 0)
    print_table_row('Elapsed time:', str(round(time.time() - start_time, 3)) + ' seconds', False, 0, 0)
    print_table_row('', '', False, 0, 0)
    print_table_line('mid')



def print_table_row(left_string, right_string, show_bike, bike_row, bike_col):
    """
    Displays a line in the table format in the terminal

    Inputs:
    left_string - string to print in the left column
    right_string - string to print in the right column
    show_bike - boolean - is the bike visible in the right column in this row
    bike_row - integer with a value of 1, 2, or 3, representing the top, middle, or bottom row of the bicycle image
    bike_col - integer - what horizontal position the bike is drawn at in the right hand column
    """
    if show_bike == False:
        print('│  ' + left_string +  (' ' * (54 - len(left_string))) + '  │  ' + right_string + (' ' * (54 - len(right_string))) + '  │')
    else:
        bike_string = bike_rows[bike_row - 1]
        print('│  ' + left_string +  (' ' * (54 - len(left_string))) + '  │  ' + (' ' * bike_col) + bike_string + (' ' * (54 - 10 - bike_col)) + '  │')



def reprint_previous_row(left_string, right_string):
    """
    Reprints the previous line in the table format in the terminal

    This is useful to wrap user input in the table format used in the terminal interface

    Inputs:
    left_string - string to print in the left column
    right_string - string to print in the right column
    """
    print(f"\033[F│  " + left_string +  (" " * (54 - len(left_string))) + "  │  " + right_string + (" " * (54 - len(right_string))) + "  │")



def print_table_line(position):
    """
    Displays a horizontal dividing line in the table

    Inputs:
    position - string - either 'top', 'mid', or 'bottom'
    """
    if position == 'top':
        print('┌──────────────────────────────────────────────────────────┬──────────────────────────────────────────────────────────┐')
    elif position == 'mid':
        print('├──────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────┤')
    elif position == 'bottom':
        print('└──────────────────────────────────────────────────────────┴──────────────────────────────────────────────────────────┘')
    else:
        print('───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────')



def main():
    """
    Main program loop

    Displays introductory text and then calls the other functions to request filters, load data, and display the results of the analysis

    After completing the cycle the user is then asked if they would like to search again
    """

    print()
    print_table_line('top')
    print_table_row('', '', False, 0, 0)
    print_table_row('      Welcome to Bikeshare Explorer!', '', False, 0, 0)
    print_table_row('     =================================', '', True, 1, 4)
    print_table_row('', '', True, 2, 4)
    print_table_row('This data utility provides statistics about', '', True, 3, 4)
    print_table_row('bikeshare services in the following cities:', '', False, 0, 0)
    print_table_row(' * Chicago', '', True, 1, 14)
    print_table_row(' * New York City', '', True, 2, 14)
    print_table_row(' * Washington DC', '', True, 3, 14)
    print_table_row('', '', False, 0, 0)
    print_table_row('Data covers the period 1 January 2017 to', '', True, 1, 24)
    print_table_row('30 June 2017.', '', True, 2, 24)
    print_table_row('', '', True, 3, 24)
    print_table_row('Data can be filtered by city, month, and weekday.', '', False, 0, 0)
    print_table_row('', '', False, 0, 0)
    print_table_line('mid')

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df is not None:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

        print_table_row('', '', False, 0, 0)
        print_table_row('Would you like to search again:', '', True, 1, 44)
        print_table_row('', '', True, 2, 44)
        print_table_row(' 1. Yes', '', True, 3, 44)
        print_table_row(' 2. No', '', False, 0, 0)
        print_table_row('', '', False, 0, 0)
        print_table_line('mid')

        continue_num = enter_option_number(2)
                
        if continue_num == 1:
            reprint_previous_row('Enter Option Number:', '1. Yes')
            print_table_row('', '', False, 0, 0)
            print_table_line('mid')

        if continue_num == 2:
            reprint_previous_row('Enter Option Number:', '2. No')
            print_table_row('', '', False, 0, 0)
            print_table_row('Thank you for using Bikeshare Explorer!', '                                                   ___', False, 0, 0)
            print_table_row('', '', False, 0, 0)
            print_table_line('bottom')
            break



if __name__ == "__main__":
	main()
