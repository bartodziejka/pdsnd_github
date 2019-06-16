import time
import pandas as pd
import numpy as np

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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    while True:
        city = input('Data from which city would you like to see? Chicago, New York City or Washington?\n').lower()
        if city not in ('chicago', 'new york city', 'washington'):
            print('Incorrect city. Please try again!\n')
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('For which month (from January to June)?\n'
                      'To see all data, type \'all\'.\n').lower()
        if month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print('Incorrect month. Please try again!\n')
            if month == 'all':
                months = ['january', 'february', 'march', 'april', 'may', 'june']
            continue
        else:
            break


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_of_week = input('For which day of week?\n'
                            'To see all data, type \'all\'.\n').lower()
        if day_of_week not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
            print('Incorrect day. Please try again!\n')
            if day_of_week == 'all':
                days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            continue
        else:
            break

    print('-'*60)
    print('You are about to see data for:\n'
          'city: {},\n'
          'month: {},\n'
          'day of week: {}.'.format(city.title(), month.title(), day_of_week.title()))
    return city, month, day_of_week


def load_data(city, month, day_of_week):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print("The most popular month is:", popular_month)

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print("The most popular day of week is:", popular_day_of_week)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print("The most popular hour is:", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("The most commonly used Start Station is:", popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("The most commonly used End Station is:", popular_end_station)

    # display most frequent combination of start station and end station trip
    df['Start End'] = df['Start Station'].map(str) + ' AND ' + df['End Station']
    popular_start_end = df['Start End'].value_counts().idxmax()
    print("The most frequent combination of Start Station and End Station is:", popular_start_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    total_time_hours = round(total_time/3600, 2)
    print("The total travel time is: {} (s) => {} (h).".format(total_time, total_time_hours))


    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    mean_time_minutes = round(mean_time/60, 2)
    print("The mean travel time is: {} (min).".format(mean_time_minutes))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("The users' types are:\n", user_types)
    print("\n")

    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print("The users' genders are:\n", gender)
        print("\n")
    else:
        print('Gender data is not available for this city.')
        print("\n")
    
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print("Statistics about year of birth:\n"
              "The earliest year is: {}\n"
              "The most recent year is: {}\n"
              "The most common year is: {}".format(earliest_year, most_recent_year, most_common_year))
    else:
        print('Birth year data is not available for this city.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def display_raw_data(df):
    raw_data = input('\nWould you like to see 5 rows of raw data?\nPlease enter \'yes\' or \'no\'.\n').lower()
    if raw_data in ('yes'):
        i = 0
        while True:
            print(df.iloc[i:i+5])
            i += 5
            more_data = input('Would you like to see more data?\nPlease enter \'yes\' or \'no\'.\n').lower()
            if more_data not in ('yes'):
                break

def main():
    while True:
        city, month, day_of_week = get_filters()
        df = load_data(city, month, day_of_week)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
    
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()





