import sqlite3

# Step 1: Create the database and tables
conn = sqlite3.connect('user_settings.sqlite3', check_same_thread=False)
cursor = conn.cursor()

# Table for users
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
        compulsory_subscription TEXT
    )
''')


# Job 1: Insert a new user if not already present
def insert_user(user_id, user_type):
    try:
        cursor.execute(f"INSERT INTO users (`id`, `type`) VALUES ('{user_id}', '{user_type}')")
        conn.commit()
    except sqlite3.IntegrityError:
        # User already exists, do nothing
        pass

# Job 2: Fetch the number of users in the database
def get_total_users():
    cursor.execute("SELECT id FROM users")
    return [mms[0] for mms in cursor.fetchall()]


def get_total_bans():
    cursor.execute("SELECT COUNT(*) FROM users where `type` = 'blc'")
    return cursor.fetchone()[0]

def get_total_mms():
    cursor.execute("SELECT COUNT(*) FROM users where `type` = 'mms'")
    return cursor.fetchone()[0]

# Job 3: Fetch user information based on user ID
def get_user_info(user_id):
    cursor.execute(f"SELECT * FROM users WHERE `id` = '{user_id}'")
    return cursor.fetchone()


# Job 4: Update user data based on user ID
def update_user(user_id, type):
    cursor.execute(f'''
        UPDATE users
        SET `type` = '{type}' where `id` = '{user_id}' ''')
    conn.commit()

def unban_uss():
    cursor.execute(f'''
        UPDATE users
        SET `type` = 'mms' ''')
    conn.commit()



def insert_channel(channel_id, channel_type):
    try:
        cursor.execute(f"INSERT INTO channels (`id`, `type`) VALUES ('{channel_id}', '{channel_type}')")
        conn.commit()
    except sqlite3.IntegrityError:
        # User already exists, do nothing
        pass

    
def delete_channel(channel_id):
        cursor.execute(f"DELETE FROM channels where `id` = '{channel_id}'")
        conn.commit()

def get_total_channels():
    cursor.execute("SELECT id FROM channels where `blc` = '0'")
    return [mms[0] for mms in cursor.fetchall()]


def get_total_ch():
    cursor.execute("SELECT COUNT(*) FROM channels where `type` = 'ch' AND `blc` = '0' ")
    return cursor.fetchone()[0]

def get_total_gr():
    cursor.execute("SELECT COUNT(*) FROM channels where `type` = 'gr' AND `blc` = '0'")
    return cursor.fetchone()[0]

# Job 3: Fetch user information based on user ID
def get_channel_info(channel_id):
    cursor.execute(f"SELECT * FROM channels WHERE `id` = '{channel_id}'")
    return cursor.fetchone()


# Job 4: Update user data based on user ID
def update_channel(channel_id, blc):
    cursor.execute(f'''
        UPDATE channels
        SET `blc` = '{blc}' where `id` = '{channel_id}' ''')
    conn.commit()


def unban_channels():
    cursor.execute(f'''
        UPDATE channels
        SET `blc` = '0' ''')
    conn.commit()



if len(cursor.execute("select * from user_settings").fetchall()) == 0:
    cursor.execute("INSERT INTO user_settings VALUES('1', '1', '0')")
    conn.commit()



# Job 4: Update user data based on user ID
def update_user_settings(notifications= None, login= None, compulsory_subscription=None):
    if not notifications == None:
        cursor.execute(f'''
            UPDATE user_settings
            SET `notifications` = '{notifications}' ''')
        conn.commit()

    if not login == None:
        cursor.execute(f'''
            UPDATE user_settings
            SET `login` = '{login}' ''')
        conn.commit()

    if not compulsory_subscription == None:
        cursor.execute(f'''
            UPDATE user_settings
            SET `compulsory_subscription` = '{compulsory_subscription}' ''')
        conn.commit()



# Function to display compulsory subscription value
def get_compulsory_subscription():
    cursor.execute("SELECT compulsory_subscription FROM user_settings")
    return cursor.fetchone()[0]

# Function to display notifications value
def get_notifications():
    cursor.execute("SELECT notifications FROM user_settings")
    return cursor.fetchone()[0]

# Function to display login value
def get_login():
    cursor.execute("SELECT login FROM user_settings")
    return cursor.fetchone()[0]
