# This is the bikeshare python. You can open it in terminal and ask cool statistic questions about bikeshare data!
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


MONTHS = ['january','february','march','april','may','june','all']

DAYS_OF_WEEK = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']

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
    try:
        city = input('For which city you would like to see data from? Available cities: Chicago, New York, Washington: ').lower()
        while city not in CITY_DATA:
            print('Seems like there is a typo in the name of the city. Please note that only the above mentioned cities are supported!')
            city = input('For which city you would like to see data from? Available cities: Chicago, New York, Washington: ').lower()

        print('You selected city: ', city)


        # get user input for month (all, january, february, ... , june)
        month = input('For which month you would like to analyze data? Date range: January - June Or would you simply analyze all these monts? Type in "all".: ').lower()
        while month not in MONTHS:
            print('Seems like there is a typo in the name of the month. Please note that only the above months are supported.')
            month = input('For which month you would like to analyze data? Date range: January - June Or would you simply analyze all these monts? Type in "all".: ').lower()

        print('You selected month: ', month)


    # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input('For which day you would like to analyze data? Or would you simply analyze all weekdays? Type in "all in this case."').lower()
        while day not in DAYS_OF_WEEK:
            print('Seems like there is a typo in your name. Please type in a valid weekday :-)')
            day = input('For which day you would like to analyze data? Or would you simply analyze all weekdays? Type in "all in this case."').lower()

        print('You selected weekday: ', day)

        return city, month, day
    except Exception as error:
        print('There was an error with your input data: {}'.format(error))
    print('-'*40)




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
    try:
        df = pd.read_csv(CITY_DATA[city])

        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['End Time'] = pd.to_datetime(df['End Time'])
        df['month'] = df['Start Time'].dt.month
        #df['day_of_week'] = df['Start Time'].dt.weekday_name
        df['day_of_week'] = df['Start Time'].dt.day_name()
        df['hour'] = df['Start Time'].dt.hour

        # filter by month if applicable
        if month != 'all':
        # use the index of the months list to get the corresponding int
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            month = MONTHS.index(month) + 1

            # filter by month to create the new dataframe
            df = df[df['month'] == month]

    # filter by day of week if applicable
        if day != 'all':
            # filter by day of week to create the new dataframe
            df = df[df['day_of_week'] == day.title()]
        return df
    except Exception as error:
        print('There was an error with your input data: {}'.format(error))

def time_stats(df, city):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    try:
        popular_month_num = df['Start Time'].dt.month.mode()[0]
        popular_month = MONTHS[popular_month_num-1].title()
        print('The most popular month in', city, 'is:', popular_month)
    except Exception as error:
        print('There was an error with your data: {}'.format(error))

    # display the most common day of week
    try:
        popular_day_of_week = df['day_of_week'].mode()[0]
        print('The most popular weekday in', city, 'is:',popular_day_of_week)
    except Exception as error:
        print('There was an error with your data: {}'.format(error))


    # display the most common start hour
    try:
        popular_start_hour = df['hour'].mode()[0]
        print('The most popular starting hour in', city, 'is:',popular_start_hour)
    except Exception as error:
        print('There was an error with your data: {}'.format(error))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df, city):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    try:
        popular_start_station = df['Start Station'].mode()[0]
        popular_start_station_amount = df['Start Station'].value_counts()[0]
        print('The most popular start station in', city, 'is:',popular_start_station, 'and was used', popular_start_station_amount, 'times.')
    except Exception as error:
        print('There was an error with your data: {}'.format(error))
    #display most commonly used end station
    try:
        popular_end_station = df['End Station'].mode()[0]
        popular_end_station_amount = df['End Station'].value_counts()[0]
        print('The most popular end station in', city, 'is:',popular_end_station, 'and was used', popular_end_station_amount, 'times.')
    except Exception as error:
        print('There was an error with your data: {}'.format(error))

    # display most frequent combination of start station and end station trip
    try:
        #old (wrong) code:
        #popular_trip = df.loc[:, 'Start Station':'End Station'].mode()[0:]
        #popular_trip_amt = df.groupby(["Start Station", "End Station"]).size().max()
        #new code:
        df['Start End'] = df['Start Station'].map(str) + '&' + df['End Station']
        popular_start_end = df['Start End'].value_counts().idxmax()
        print('the most popular trip is: ', popular_start_end)
    except Exception as error:
        print('There was an error with your data: {}'.format(error))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, city):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    try:
        df['Time Delta'] = df['End Time'] - df['Start Time']
        total_time_delta = df['Time Delta'].sum()
        print('the total travel time was:', total_time_delta)
    except Exeption as error:
        print('There was an error with your data: {}'.format(error))
    # display mean travel time
    try:
        total_mean = df['Time Delta'].mean()
        print('the average travel time was:', total_mean)
    except Exception as error:
        print('There was an error with your data: {}'.format(error))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
        print('The amount and type of users in', city, 'are this:', df['User Type'].value_counts())
    except Execption as error:
        print('There was an error with your data: {}'.format(error))
    # Display counts of gender
    try:
        print('The amount and gender of users in', city, 'are this:',df['Gender'].value_counts())
    except Exception as error:
        print('There was an error with your data: {}'.format(error))
     # Display earliest, most recent, and most common year of birth
    try:
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()
        print('The demographic structure (age/gender) in', city, 'is' 'oldest customer was born in:', int(earliest_year),'\n' 'youngest customer was born in:', int(most_recent_year),'\n' 'most of the customers are born in:', int(most_common_year))
    except Exception as error:
        print('There was an error with your data: {}'.format(error))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#raw data output
def output_raw_data(df):
    """Displays raw data on user request.
    """
    print(df.head())
    next_line = 0
    while True:
        raw_data = input('Would you like to see next five rows of raw data? ***PLEASE NOTE TO MAKE A WIDE SCREEN OF YOUR TERMINAL IN ORDER TO SEE ALL COLUMNS :) Enter yes or no.')
        if raw_data.lower() != 'yes':
            return
        next_line = next_line + 5
        print(df.iloc[next_line:next_line+5])

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, city)
        station_stats(df, city)
        trip_duration_stats(df, city)
        user_stats(df,city)
        while True:
            raw_data = input('Would you like to see five rows of raw data? ***PLEASE NOTE TO MAKE A WIDE SCREEN OF YOUR TERMINAL IN ORDER TO SEE ALL COLUMNS :) Enter yes or no.')
            if raw_data.lower() != 'yes':
                break
            output_raw_data(df)
            break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
