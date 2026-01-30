import csv
import sqlite3
import re

# Connect to the SQLite in-memory database
conn = sqlite3.connect(':memory:')

# A cursor object to execute SQL commands
cursor = conn.cursor()


def main():

    # users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        userId INTEGER PRIMARY KEY,
                        firstName TEXT,
                        lastName TEXT
                      )'''
                   )

    # callLogs table (with FK to users table)
    cursor.execute('''CREATE TABLE IF NOT EXISTS callLogs (
        callId INTEGER PRIMARY KEY,
        phoneNumber TEXT,
        startTime INTEGER,
        endTime INTEGER,
        direction TEXT,
        userId INTEGER,
        FOREIGN KEY (userId) REFERENCES users(userId)
    )''')

    # You will implement these methods below. They just print TO-DO messages for now.
    load_and_clean_users('../../resources/users.csv')
    load_and_clean_call_logs('../../resources/callLogs.csv')
    write_user_analytics('../../resources/userAnalytics.csv')
    write_ordered_calls('../../resources/orderedCalls.csv')

    # Helper method that prints the contents of the users and callLogs tables. Uncomment to see data.
    select_from_users_and_call_logs()

    # Close the cursor and connection. main function ends here.
    cursor.close()
    conn.close()


# TODO: Implement the following 4 functions. The functions must pass the unit tests to complete the project.

# This function will load the users.csv file into the users table, discarding any records with incomplete data
def load_and_clean_users(file_path):
    """ df = pd.read_csv(file_path, sep=None, engine="python", on_bad_lines='skip')


    df.dropna(axis=0, inplace=True)
    df = df[df['firstName'].str.strip().astype(bool)]
    df = df[df['lastName'].str.strip().astype(bool)]
    df.insert(0, 'userId', range(1, len(df) + 1))
    df = df.astype({"firstName": "str", "lastName": "str"})
    df.to_sql("users", con=conn, if_exists="replace", index=False)
    """

    data = []

    with open(file_path) as file_data:
        reader = csv.reader(file_data)
        for entry in reader:
            for item in range(len(entry)):
                #removing ending and starting spaces
                entry[item] = entry[item].strip()
            data.append(entry)

    # filter data
    filtered_data = []

    for entry in range(1, len(data)):
        isNull = False
        offColumns = False
        isNotAlpha = False
        # any null value remove
        # any entry with extra rows remove 
        # any entry without alpha characters only remove
        for item in range(len(data[entry])):
            isNull = data[entry][item] == ""
            offColumns = len(data[entry]) == len(data[0])
            isNotAlpha = data[entry][item].isalpha()
        
        if (not isNull) and (not offColumns) and (not isNotAlpha):
            filtered_data.append(data[entry])
        
    print("hello world")

    print(data)






    print("users loaded to table")


# This function will load the callLogs.csv file into the callLogs table, discarding any records with incomplete data
def load_and_clean_call_logs(file_path):
    df = pd.read_csv(file_path, names=["phoneNumber","startTime","endTime","direction","userId"], sep=None, engine="python", on_bad_lines="skip")
    df['endTime'] = pd.to_numeric(df['endTime'], errors='coerce')
    df.dropna(axis=0, inplace=True)
    df = df.astype({"userId": "int64", "phoneNumber": "str", "startTime": "int64", "endTime": "int64", "direction": "str"})
    df.insert(0, 'callId', range(1, len(df) + 1))
    df.to_sql("callLogs", con=conn, if_exists="replace", index=False)
    print("Call logs loaded to table")


# This function will write analytics data to testUserAnalytics.csv - average call time, and number of calls per user.
# You must save records consisting of each userId, avgDuration, and numCalls
# example: 1,105.0,4 - where 1 is the userId, 105.0 is the avgDuration, and 4 is the numCalls.
def write_user_analytics(csv_file_path):
    df = pd.read_sql_query("SELECT userId, AVG(endTime - startTime) AS avgDuration,COUNT(*) AS numCalls FROM callLogs GROUP BY userId", conn)
    df.to_csv(csv_file_path, index=False)

    print("Written data to user analytics csv")


# This function will write the callLogs ordered by userId, then start time.
# Then, write the ordered callLogs to orderedCalls.csv
def write_ordered_calls(csv_file_path):
    df = pd.read_sql_query("SELECT * FROM callLogs ORDER BY userId, startTime", conn)
    df.dropna(axis=0, inplace=True)
    df.to_csv(csv_file_path, index=False)

    print("Written ordered call logs to csv")



# No need to touch the functions below!------------------------------------------

# This function is for debugs/validation - uncomment the function invocation in main() to see the data in the database.
def select_from_users_and_call_logs():

    print()
    print("PRINTING DATA FROM USERS")
    print("-------------------------")

    # Select and print users data
    cursor.execute('''SELECT * FROM users''')
    for row in cursor:
        print(row)

    # new line
    print()
    print("PRINTING DATA FROM CALLLOGS")
    print("-------------------------")

    # Select and print callLogs data
    cursor.execute('''SELECT * FROM callLogs''')
    for row in cursor:
        print(row)


def return_cursor():
    return cursor


if __name__ == '__main__':
    main()
