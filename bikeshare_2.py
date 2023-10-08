import time
import pandas as pd
import sys 
#import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). 
    while True:
        print("Enter City's name : Chicago, New York City, or Washington")
        city = input("city:").lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        elif city == '':
            print("You did not Enter any city's name") 
        else:
            print('You enetered a wrong city\'s name')

    # get user input for month (all, january, february, ... , june)
    print('Do you want to filter by month?')
    while True:
        month_filter = input("Enter yes or no:").lower()
        if month_filter == "no":
            month = "all"
            break
        elif month_filter == "yes":
            months = ["january", "february", "march", "april", "may", "june"]
            while True:
                print('Enter month January, February, March, April, May, or June')
                month = input("Month:").lower()
                if month in months:
                    break
                elif month == '':
                    print('You did not enter any value, enter any value to proceed')
                else:
                    print('You entered a wrong input')
            break
        else:
            print('You entered a wrong input')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('Would you want to filter by day?')
    while True:
        answer = input('Enter yes or no:').lower()
        if answer == "no":
            day = 'all'
            break
        elif answer == 'yes':
            days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            while True:
                print('Enter any of the weekdays Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday')
                day = input('Weekday:').lower()
                if day in days:
                    break
                elif day == '':
                    print('You did not enter any day')
                else:
                    print('You entered an invalid value')
            break
        else:
            print('You entered a wrong input')

    print('-'*40)
    return city, month, day

#Load the data
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
    df = pd.read_csv('./{}'.format(CITY_DATA[city]))
    #Convert the start time colume to the datetime object
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #create a new month column by extracting the month name from the date time object
    df['month'] = df['Start Time'].dt.month_name()
    #create the day colume by extracting the day name from the datetime object
    df['day'] = df['Start Time'].dt.day_name()
    #create the start hour column by extracting the start hour from datetime
    df['Start Hour'] = df['Start Time'].dt.hour

    #if there is no filter, return the full dataframe
    if month == 'all' and day == 'all':
        df = df
    #if only the date is filtered, filter only the day column
    elif month == 'all' and day != 'all':
        df = df[df['day'] == day.title()]
    #if only the month is filterd, filter only the month columm
    elif month != 'all' and day == 'all':
        df = df[df['month'] == month.title()]
    #if both the month and the day is filtered, filter both the month and day columns
    else:
        df = df[(df['month'] == month.title()) & (df['day'] == day.title())]
    #return the dataframe
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    try:
        print('\nCalculating The Most Frequent Times of Travel...\n')
        start_time = time.time()

        # display the most common month
        print("The most common month is:", df['month'].mode()[0])

        # display the most common day of week
        print('The most common day of the week is:', df['day'].mode()[0])

        # display the most common start hour
        print('The most common Start Hour is:', df['Start Hour'].mode()[0])

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except (ValueError, KeyError, IndexError):
        print('No available data for the filter selected')
        sys.exit()

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    try:
        print('\nCalculating The Most Popular Stations and Trip...\n')
        start_time = time.time()

        # display most commonly used start station
        print("The most commonly used Start Station is:", df['Start Station'].mode()[0])

        # display most commonly used end station
        print("The most commonly used end station:", df['End Station'].mode()[0])

        # display most frequent combination of start station and end station trip
        start_end_station = pd.DataFrame()
        start_end_station['combined'] = df['Start Station'] + ' ' + 'and' + ' ' + df['End Station']
        print("The most frequent combination of start station and end station are:", start_end_station['combined'].mode()[0])

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except (ValueError, KeyError, IndexError):
        print('No data for the selected filters')
        sys.exit()


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    try:
        print('\nCalculating Trip Duration...\n')
        start_time = time.time()

        # display total travel time
        print('The total travel time is:', df['Trip Duration'].sum())

        # display mean travel time
        print('the mean travel time is:', df['Trip Duration'].mean())

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except (ValueError, KeyError, IndexError):
        print(' No data available for the selected filters')
        sys.exit()


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The count of user types:\n', df['User Type'].value_counts())

    print()

    # Display counts of gender
    try:
        print('The counts of Gender are:\n', df['Gender'].value_counts())
    except KeyError:
        print('There is no Gender information for the selected city')

    print()
        
    # Display earliest, most recent, and most common year of birth
    try:
        print('The earliest, most recent, and the most common year of birth are:', df['Birth Year'].min(), ',', df['Birth Year'].max(), 'and',  df['Birth Year'].mode()[0], 'respectively')
    except KeyError:
        print('There is no birth year information for the selected city')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#show raw data in chuncks of 5 rows at a time
def view_raw_data(df):
    print('Would you like to see the raw data in 5 rows at a time?')
    see_raw_data = input('Enter yes or no:').lower()
    if see_raw_data == 'yes':
        start_of_chunck, end_of_chunck = 0, 5
        while True:
            chunck = df.iloc[start_of_chunck : end_of_chunck, :]
            print(chunck)
            start_of_chunck += 5 
            end_of_chunck += 5
            print()

            #check if we are at the end of the raw data
            if(end_of_chunck - 5 > df.tail(1).index):
                print('This is the end of the raw data')
                break

            #check if the user wants to keep viewing
            print('Enter yes to continue viewing, no to stop viewing ')
            answer = input('yes/no:').lower()
            if answer == 'no':
                break

def main():
    try:
        while True:
            city, month, day = get_filters()
            df = load_data(city, month, day)

            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            view_raw_data(df)

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
    except KeyboardInterrupt:
        print('exiting..... Done')
        sys.exit()

if __name__ == "__main__":
	main()
