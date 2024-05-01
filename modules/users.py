import os
import sqlite3
import gitlab

git = gitlab.Gitlab(
    GITLAB_URL, private_token=GITLAB_TOKEN, api_version=4)  # type: ignore
git.auth()


# Connect to the database
connection = sqlite3.connect('../gitlab.db')
cursor = connection.cursor()

if os.path.exists('../gitlab.db'):
    if cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="gitlab_users"').fetchone():
        print('Table exists')
    else:
        cursor.execute(
            'CREATE TABLE gitlab_users ('
            'id INTEGER PRIMARY KEY,'
            'username TEXT,'
            'email TEXT,'
            'url TEXT,'
            'is_admin BOOLEAN,'
            'state TEXT,'
            'last_activity_on TEXT,'
            'last_sign_in_at TEXT,'
            'confirmed_at TEXT'
            ')'
        )
        print('Table created')
        connection.commit()

for user in git.users.list(all=True):
    # Check if the user exists in the database
    if cursor.execute('SELECT id FROM gitlab_users WHERE id=?', (user.id,)).fetchone():
        print(f'User {user.username} already exists')
        print('Updating user...')
        cursor.execute(
            'UPDATE gitlab_users SET '
            'username=?,'
            'email=?,'
            'url=?,'
            'is_admin=?,'
            'state=?,'
            'last_activity_on=?,'
            'last_sign_in_at=?,'
            'confirmed_at=? '
            'WHERE id=?',
            (
                user.username,
                user.email,
                user.web_url,
                user.is_admin,
                user.state,
                user.last_activity_on,
                user.last_sign_in_at,
                user.confirmed_at,
                user.id
            )
        )
        connection.commit()
        print('User updated')
    else:
        print(f'Adding user {user.username}')
        cursor.execute(
            'INSERT INTO gitlab_users (id, username, email, url, is_admin, state, last_activity_on, last_sign_in_at, confirmed_at) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (
                user.id,
                user.username,
                user.email,
                user.web_url,
                user.is_admin,
                user.state,
                user.last_activity_on,
                user.last_sign_in_at,
                user.confirmed_at
            )
        )
        connection.commit()


connection.close()
