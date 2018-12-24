'''

** ONLY change methods with (**) sign
** fill free to add method as much as you need

you need to complete this file by creating a multi-threaded socket server

1. create a socket server using TCP protocol
2. server should create a thread per each client
3. server only has two types of requests
    3-1. handshake                      -- which is socket.accept() method
    3-2. get all push notifications     -- server should respond this request by getting all unvisited messages in database for this user

4. after sending push notification to each user you need to call 'update_visited_notification'
5. error handling: server must be able to handle wrong requests coming from clients
'''

import socket
import database_interface as db_interface


host = ''
port = 2019


# (**)
def run_server(host, port):
    '''
    this method run socket server
    :param host: host name
    :param port:
    :return: None
    '''

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))

    print(server)  # to see what is IP and Port

    server.listen(10)

    # now implement your code


# stater point
if __name__ == '__main__':
    database = "db.sqlite"
    connection = db_interface.create_connection(database)


def update_visited_notification(username, message_id):
    db_interface.update_visited_notification(connection, username, message_id)


def check_database_for_new_push_messages():
    '''
    :return: user object see User class in database_interface
    '''
    return db_interface.get_unvisited_notifications(connection)
