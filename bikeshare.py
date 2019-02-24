import time
import json
from typing import List, Dict
import pandas as pd
from sty import fg, bg, rs, RgbFg

CITY_DATA: Dict[str, str] = {"chicago": "chicago.csv",
                             "new york": "new_york_city.csv",
                             "washington": "washington.csv"}

CITIES_LIST: List[str] = ["chicago",
                          "new york",
                          "washington"]

MONTHS_LIST: List[str] = ["january",
                          "february",
                          "march",
                          "april",
                          "may",
                          "june"]

DAYS_LIST: List[str] = ["sunday",
                        "monday",
                        "tuesday",
                        "wednesday",
                        "thursday",
                        "friday",
                        "saturday"]

fg.set_style("orange", RgbFg(255, 150, 50))


def print_section(message):
    """
        Function to factorise the print of each section"s message.

        Args:
        (str) message - message to print
    """

    section_message = bg.da_cyan + message + bg.rs
    print()
    print(section_message)
    print()


def print_result(message, value):
    """
        Function to factorise the print of each result"s message.

        Args:
        (str) message - message to print
        (int64) value - value calculated
    """

    result_message = bg.green + message + str(value) + bg.rs
    print(result_message)


def print_error():
    """
        Function to factorise the print of error message.

    """
    error_message = bg.red + "Unavailable answer !" + bg.rs
    print(error_message)


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    hello = fg.orange + "Hello! Let\s explore some US bikeshare data!" + fg.rs
    print(hello)
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city_message = bg.green + "Which city do you want to explore between : Chicago, New York or Washington?" + bg.rs
        print(city_message)
        city = get_input_value(">>> ", CITIES_LIST).lower()
        if city in CITIES_LIST:
            break

    # get user input for month (all, january, february, ... , june)
    month_message = bg.green + "Do you want to explore the whole dataset (all) or a specific month  :" + bg.rs
    print(month_message)
    month_example = bg.da_magenta + "=> january || february || march || april || may || june " + bg.rs
    print(month_example)
    month = get_input_value(">>> ", MONTHS_LIST)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_message = bg.green + "Do you want to explore the whole month (all) or a specific day of the week ?" + bg.rs
    print(day_message)
    day = get_input_value(">>> ", DAYS_LIST)

    print('-' * 40)
    print()
    return city, month, day


def get_input_value(msg, available_list):
    """
    Used to obtain user input value
    Args:
        (str) msg - a message to go with the request
        (str) available_list - list of possibilities
    Returns:
        (str) data - requested data
    """

    while True:
        data = input(msg).lower()
        if data in available_list:
            break
        elif data == "all":
            break
        else:
            print_error()

    return data


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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # extract month and day of week and hour by adding new columns
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.weekday_name
    df["hour"] = df["Start Time"].dt.hour

    # filter by month if asked
    if month != "all":
        month = MONTHS_LIST.index(month) + 1
        df = df[df["month"] == month]

    # filter by day of week if asked
    if day != "all":
        df = df[df["day_of_week"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print_section("Calculating The Most Frequent Times of Travel...")
    start_time = time.time()

    # display the most common month
    common_month = df["month"].value_counts().idxmax()
    print_result("Most common month -> ", common_month)

    # display the most common day of week
    day_of_week = df["day_of_week"].value_counts().idxmax()
    print_result("Most common day of week -> ", day_of_week)

    # display the most common start hour
    start_hour = df["hour"].value_counts().idxmax()
    print_result("Most common start hour is -> ", start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print_section("Calculating The Most Popular Stations and Trip...")
    start_time = time.time()

    # display most commonly used start station
    start_station = df["Start Station"].value_counts().idxmax()
    # station_message =
    print_result("Most commonly used start station -> ", start_station)

    # display most commonly used end station
    most_common_end_station = df["End Station"].value_counts().idxmax()
    print_result("Most commonly used end station -> ", most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_common_start_end_station = df[["Start Station", "End Station"]].mode().loc[0]
    print_result("Most commonly used start station is ", most_common_start_end_station[0])
    print_result("And the most commonly used end station is  ", most_common_start_end_station[1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print_section("Calculating Trip Duration...")
    start_time = time.time()

    # display total travel time
    total_travel = df["Trip Duration"].sum()
    print_result("Total travel time -> ", total_travel)

    # display mean travel time
    mean_travel = df["Trip Duration"].mean()
    print_result("Mean travel time -> ", mean_travel)

    # display max travel time
    max_travel = df["Trip Duration"].max()
    print_result("Max travel time -> ", max_travel)

    # display the total trip duration for each user type
    print_section("Travel time for each user type:")
    total_trip_duration = df.groupby(["User Type"]).sum()["Trip Duration"]
    for index, user_trip in enumerate(total_trip_duration):
        temp = "  - " + total_trip_duration.index[index] + " : "
        print_result(temp, user_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print_section("Calculating User Stats...")
    start_time = time.time()

    # Display counts of user types
    print_section("Counts of user types :")
    value_counts = df["User Type"].value_counts()

    # print out the total numbers of each user types
    for index, user_count in enumerate(value_counts):
        temp = "  - " + value_counts.index[index] + " : "
        print_result(temp, user_count)

    if "Gender" in df.columns:
        gender_stats(df)

    if "Birth Year" in df.columns:
        birth_stats(df)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
    print('-' * 40)


def gender_stats(df):
    """Displays statistics of analysis based on the gender of bikeshare users."""

    # Display counts of gender
    print_section("Counts of gender :")
    gender_counts = df["Gender"].value_counts()

    # print out the total of each genders
    for index, gender_count in enumerate(gender_counts):
        temp = "  - " + gender_counts.index[index] + " : "
        print_result(temp, gender_count)


def birth_stats(df):
    """Displays statistics of analysis based on the birth years of bikeshare users."""

    print_section("Birthday stats :")

    # Display earliest, most recent, and most common year of birth
    birth_year = df["Birth Year"]

    # the most common birth year
    most_common_year = birth_year.value_counts().idxmax()
    print_result("The most common birth year -> ", most_common_year)

    # the most recent birth year
    most_recent = birth_year.max()
    print_result("The most recent birth year -> ", most_recent)

    # the most earliest birth year
    earliest_year = birth_year.min()
    print_result("The most earliest birth year -> ", earliest_year)


def show_raw_data(df):
    """Show raw bikeshare data."""

    row_length = df.shape[0]

    for i in range(0, row_length, 5):

        print_section("Would you want to examine the dataset in a JSON style 5 by 5 objects?")
        answer = input(">>> ")
        if answer.lower() == "no":
            break
        elif answer.lower() == "yes":
            row_data = df.iloc[i: i + 5].to_json(orient="records", lines=True).split("\n")
            for row in row_data:
                # print JSON style each row
                parsed_row = json.loads(row)
                json_row = json.dumps(parsed_row, indent=2)
                print(json_row)
        else:
            print_error()


def main():
    while True:
        city, month, day = get_filters()
        loading = bg.yellow + "Loading data..." + bg.rs
        print(loading)
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() == "no":
            break
        else:
            print()
            print('-' * 40)
            print('-' * 40)
            print()


if __name__ == "__main__":
    main()
