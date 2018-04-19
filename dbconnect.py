import pymysql

"""Function to open the database connection
"""
def open_db_connection():
    host_name = 'localhost'
    port_number = 3306
    user_name = 'rideshareusr'
    password = 'test'
    database_name = 'RideSharing'
    connection_object = pymysql.connect(host=host_name, port=port_number,
                                        user=user_name, passwd=password, db=database_name)
    return connection_object

"""Function to close the database connection
"""
def close_db_connection(connection_object):
    if connection_object is  not None:
        connection_object.commit()
    connection_object.close()