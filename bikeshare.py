import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
CITIES = ['chicago', 'new york city', 'washington']
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def is_valid(input_option: str, valid_options: list, allow_all: bool = True):
    """ Determines if input is in a list of valid options.

    Args:
        input_option (str): User entered string
        valid_options (list): Either cities, months, or days
        allow_all (bool, optional): Allow user to input 'all' to reference all elements of valid options. Defaults to True.

    Returns:
        bool: Whether input is valid
    """
    return (input_option.lower() in valid_options) or (allow_all and input_option == 'All')
    

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
    invalid_city_input = True
    while invalid_city_input:
        city = input('Enter a city (Chicago, New York City, Washington) to view data:').title()
        
        if is_valid(city, CITIES, allow_all=False):
            invalid_city_input = False
        else:
            print(f'{city} is not a valid option. Please try again.')
    
    # get user input for month (all, january, february, ... , june)
    invalid_month_input = True
    while invalid_month_input:
        month = input(f'Enter a month to view data for {city}. (to view all, type ''all''):').title()

        if is_valid(month, MONTHS):
            invalid_month_input = False
            
        else:
            print(f'{month} is not a valid option. Please try again.')
    print(f'{month} is a valid option. enjoy your data')
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
#     query_day = []
    invalid_day_input = True
    while invalid_day_input:
        day = input(f'Enter a day of the week to view data for {month} in {city}:').title()
        
        print(day)
        if is_valid(day, DAYS):
            invalid_day_input = False
        else:
            print(f'{day} is not an option. Please try again.')
    print(f'{day} is a valid option. ENJOY!')


    print('-'*40)
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

    # loaded data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # converted the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extracted month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        if month not in months:
            print(f'No data exists for {month}. Try again.')
            get_filters()
        month = months.index(month) + 1

        # filtered by month to create the new dataframe
        df = df[df['month'] == month]

    # filtered by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

             
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name()
    df['day'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    
    # display the most common month
    common_month = df['month'].mode()[0]
    print(f'The most common month of travel is {common_month}')
    # display the most common day of week
    common_day = df['day'].mode()[0]
    print(f'The most common day of travel is {common_day}')
 
    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print(f'The most common hour is {common_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return df

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
   
    
    # display most commonly used start station
    common_ss = df['Start Station'].mode()[0]
    print(f'The most commonly used start station is {common_ss}')

    # display most commonly used end station
    common_es = df['End Station'].mode()[0]
    print(f'The most commonly used start station is {common_ss}')

    # display most frequent combination of start station and end station trip

    df['freq_comb'] = df['Start Station'] + df['End Station']
    frequent_ss_es = df['freq_comb'].mode()[0]
    print(f'The most frequent combibation of start station and end station trip is {frequent_ss_es}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    tt1 = total_travel / 24
    tt2 = tt1 / 365
    print(f'The total travel duration is {tt2} years.')

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print(f'The mean travel time is {mean_travel} hours.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f'The type and amount of customers are as follows: \n{user_types}')
    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print(f'The amount of each gender is \n{gender}.')
    

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest = df['Birth Year'].min()
        print(f'The earliest birth year is {earliest}')
        most_recent = df['Birth Year'].max()
        print(f'The most recent birth year is {most_recent}')
        most_common = df['Birth Year'].mode()[0]
        print(f'The most common birth year is {most_common}')
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def data_viewer(df):
    counter = 0
    view_next = True
    while view_next:
        if counter == 0:
            response = input('Would you like to see five rows of data? Yes or no:').title()
        else:
            response = input('Would you like to view five more rows? Yes or no:').title()
        if response == 'No':
            return
        counter += 5
        print(df.iloc[counter-5:counter, :])


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        data_viewer(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
