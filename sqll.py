import sqlite3


# Step 1: Create the database and connection

dbname = "user_settings.sqlite3"

def get_db_connection():
    conn = sqlite3.connect(dbname)
    conn.row_factory = sqlite3.Row
    return conn
    
def stop_db(conn):
    conn.commit()
    conn.close()



# Table for users
def createTables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            type TEXT,
            UNIQUE(id, type)
        )
    ''')

    # Table channels
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY,
            type TEXT,
            blc INTEGER default 0,
            UNIQUE(id, type)
        )
    ''')

    # Table for user settings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_settings (
            notifications INTEGER,
            login INTEGER,
            status INTEGER,
            compulsory_subscription TEXT
        )
    ''')
    stop_db(conn)

createTables()


# Job 1: Insert a new user if not already present
def insert_user(user_id, user_type):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO users (`id`, `type`) VALUES ('{user_id}', '{user_type}')")
    except sqlite3.IntegrityError:
        pass
    stop_db(conn)

# Job 2: Fetch the number of users in the database
def get_total_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users")
    data = cursor.fetchall()
    stop_db(conn)
    return [mms[0] for mms in data]


def get_total_bans():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users where `type` = 'blc'")
    data = cursor.fetchone()[0]
    stop_db(conn)
    return data

def get_total_mms():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users where `type` = 'mms'")
    data = cursor.fetchone()[0]
    stop_db(conn)
    return data

# Job 3: Fetch user information based on user ID
def get_user_info(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE `id` = '{user_id}'")
    data = cursor.fetchone()
    stop_db(conn)
    return data


# Job 4: Update user data based on user ID
def update_user(user_id, type):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f'''
        UPDATE users
        SET `type` = '{type}' where `id` = '{user_id}' ''')
    stop_db(conn)


def unban_uss():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f'''
        UPDATE users
        SET `type` = 'mms' ''')
    stop_db(conn)




def insert_channel(channel_id, channel_type):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO channels (`id`, `type`) VALUES ('{channel_id}', '{channel_type}')")
    except sqlite3.IntegrityError:
        pass
    stop_db(conn)

    
def delete_channel(channel_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM channels where `id` = '{channel_id}'")
    stop_db(conn)

def get_total_channels():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM channels where `blc` = '0'")
    data = cursor.fetchall()
    stop_db(conn)
    return [mms[0] for mms in data]


def get_total_ch():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM channels where `type` = 'ch' AND `blc` = '0' ")
    data = cursor.fetchone()[0]
    stop_db(conn)
    return data

def get_total_gr():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM channels where `type` = 'gr' AND `blc` = '0'")
    data = cursor.fetchone()[0]
    stop_db(conn)
    return data

# Job 3: Fetch user information based on user ID
def get_channel_info(channel_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM channels WHERE `id` = '{channel_id}'")
    data = cursor.fetchone()
    stop_db(conn)
    return data


# Job 4: Update user data based on user ID
def update_channel(channel_id, blc):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f'''
        UPDATE channels
        SET `blc` = '{blc}' where `id` = '{channel_id}' ''')
    stop_db(conn)


def unban_channels():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f'''
        UPDATE channels
        SET `blc` = '0' ''')
    stop_db(conn)


def setDefaultData():
    conn = get_db_connection()
    cursor = conn.cursor()
    if len(cursor.execute("select * from user_settings").fetchall()) == 0:
        cursor.execute("INSERT INTO user_settings VALUES('1', '1', '1', '0')")
    stop_db(conn)

setDefaultData()



# Job 4: Update user data based on user ID
def update_user_settings(notifications= None, login= None, status=None, compulsory_subscription=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if not notifications == None:
        cursor.execute(f'''
            UPDATE user_settings
            SET `notifications` = '{notifications}' ''')

    if not login == None:
        cursor.execute(f'''
            UPDATE user_settings
            SET `login` = '{login}' ''')

    if not status == None:
        cursor.execute(f'''
            UPDATE user_settings
            SET `status` = '{status}' ''')

    if not compulsory_subscription == None:
        cursor.execute(f'''
            UPDATE user_settings
            SET `compulsory_subscription` = '{compulsory_subscription}' ''')
    stop_db(conn)


# Function to display compulsory subscription value
def get_compulsory_subscription():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT compulsory_subscription FROM user_settings")
    data = cursor.fetchone()[0]
    stop_db(conn)
    return data

# Function to display notifications value
def get_notifications():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT notifications FROM user_settings")
    data = cursor.fetchone()[0]
    stop_db(conn)
    return data

# Function to display login value
def get_login():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT login FROM user_settings")
    data = cursor.fetchone()[0]
    stop_db(conn)
    return data


def get_status():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM user_settings")
    data = cursor.fetchone()[0]
    stop_db(conn)
    return data
