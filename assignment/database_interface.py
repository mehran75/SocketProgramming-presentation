import sqlite3
from sqlite3 import Error
from datetime import datetime


class User:

    def __init__(self, user_id, username, messages=None):
        self.messages = list(messages)
        self.username = username
        self.user_id = user_id

    def remove_message(self, message):
        self.messages.remove(message)

    def __repr__(self):
        s = str(self.user_id) + '-' + str(self.username) + ':\n'

        for message in self.messages:
            s += '\t' + str(message) + '\n'

        return s


class Message:

    def __init__(self, message_id, text):
        self.message_id = message_id
        self.text = text

    def __repr__(self):
        return str(self.message_id) + '-' + str(self.text)

    def __eq__(self, other):
        return self.message_id == other.message_id


def create_connection(db_file):
    """
    description: create a database connection to the SQLite database
        specified by the db_file

    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def add_notification(connection, message):
    """
    description: add new push notification message to database

    :param  connection : current connection to database
    :param  message    : message of type string object
    :return ID          : inserted ID
    """

    bindings = (message, str(datetime.now()))
    sql = '''Insert into Messages(messagetext, "date") values (?,?)'''

    cursor = connection.cursor()
    cursor.execute(sql, bindings)

    return cursor.lastrowid


def add_new_user(connection, username):
    """ add new push notification message to database
        :param  connection : current connection to database
        :param  username    : username of type string object
        :return ID          : inserted ID
        """

    bindings = (username, str(datetime.now()))
    sql = '''Insert into User(Username, JoinDate) values (?,?)'''

    cursor = connection.cursor()
    cursor.execute(sql, bindings)

    return cursor.lastrowid


def print_all_database_content(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """

    cur = conn.cursor()
    print("-----------------------Messages----------------------------")
    cur.execute("SELECT * FROM Messages")

    rows = cur.fetchall()

    for row in rows:
        print(row)

    print("-----------------------Users----------------------------")
    cur.execute("SELECT * FROM User")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def update_visited_notification(connection, username, message_id):
    """
    description: after sending each message to its client you this method help you to update your database

    :param  connection  : current connection to database
    :param  username    : username of type string object
    :param  message_id  : type integer
    :return ID          : inserted ID
    """

    bindings = (message_id, username, str(datetime.now()))
    sql = '''Insert into visited_notifications(messageid, userid, notifieddate) values (?,?,?)'''

    cursor = connection.cursor()
    cursor.execute(sql, bindings)

    return cursor.lastrowid


def find_user(users, user_id):
    for user in users:
        if user.user_id == user_id:
            return user


def find_message(user, message_id):
    for message in user.messages:
        if message_id == message.message_id:
            return message


def get_unvisited_notifications(connection):
    """
    description: determines which user should see what messages based on last chenges in database

    :param connection: sqlite connection
    :return: list that contains Users object
    """

    sql = "select * from Messages"
    cursor = connection.cursor()
    cursor.execute(sql)

    rows = cursor.fetchall()
    all_messages = []
    for row in rows:
        all_messages.append(Message(row[0], row[1]))

    sql = "select * from USER"
    cursor = connection.cursor()
    cursor.execute(sql)

    rows = cursor.fetchall()
    users = []
    for row in rows:
        users.append(User(row[0], row[1]))

    sql = "select * from visited_notifications"
    cursor = connection.cursor()
    cursor.execute(sql)

    visited_messages = cursor.fetchall()

    dic = dict()

    for row in visited_messages:
        for user in users:
            for message in user.messages:
                if user.user_id == row[2] and message.message_id == row[1]:
                    dic[user.user_id] = message.message_id

    for user_id, message_id in dic.items():
        user = find_user(users, user_id)
        message = find_message(user, message_id)
        user.remove_message(message)

    return users


def check_user_validation(connection, username, password):
    """
    check if user subscribed to our push notification service

    :param connection: sqlite connection
    :param username: the given username in sign-up form (from interface)
    :param password: the given password in sign-up form (from interface)
    :return: userId if user is valid otherwise method returns -1
    """

    bindings = (username, password)
    sql = "select UserID from User where Username = ? AND Password = ?"
    cursor = connection.cursor()
    cursor.execute(sql,bindings)

    rows = cursor.fetchall()

    if len(rows) == 0:
        return -1

    return rows[0][0]


def main():
    database = "db.sqlite"

    # create a database connection
    conn = create_connection(database)

    with conn:
        while True:
            print('database connected\n')
            command = input("command instructions\n\n"
                            "'add-notification' : for adding a new push notification\n"
                            "'add-user'         : to add new user\n"
                            "'query'            : to print all messages and users in database\n"
                            "'exit'             : exit\n")

            if command == 'exit':
                return
            elif command == 'add-notification':
                print('Notification ID:',
                      add_notification(conn, input("insert new push notification message and hit enter:\n")))
            elif command == 'add-user':
                print('User ID:', add_new_user(conn, input("insert a username and hit enter:\n")))
            elif command == 'query':
                print_all_database_content(conn)


if __name__ == '__main__':
    main()
