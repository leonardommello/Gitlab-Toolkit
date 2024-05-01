import sqlite3


def CreateDB(cursor: sqlite3.Cursor):
    cursor.execute('CREATE TABLE projects ('
                   'id INTEGER PRIMARY KEY,'
                   'name TEXT,'
                   'path TEXT,'
                   'url TEXT,'
                   'repo_empty BOOLEAN,'
                   'only_readme BOOLEAN,'
                   'archived BOOLEAN,'
                   'created_at TEXT,'
                   'last_activity_at TEXT'
                   ')'
                   )
    conn.commit()
    cursor.execute('CREATE TABLE users ('
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
    cursor.commit()


def insert_project(cursor: sqlite3.Cursor, project):
    if git.archived:
        archived = True
    else:
        archived = False

    cursor.execute('INSERT INTO projects ('
                   'id,'
                   'name,'
                   'path,'
                   'url,'
                   'repo_empty,'
                   'only_readme,'
                   'archived,'
                   'created_at,'
                   'last_activity_at'
                   ')'
                   'VALUES (?,?,?,?,?,?,?,?,?)',
                   (
                       project.id,
                       project.name,
                       project.path_with_namespace,
                       project.web_url,
                       False,
                       False,
                       archived,
                       project.created_at,
                       project.last_activity_at
                   )
                   )
    cursor.commit()


def update_project(cursor: sqlite3.Cursor, project):
    if project.archived:
        archived = True
    else:
        archived = False

    cursor.execute('UPDATE projects SET '
                   'name=?,'
                   'path=?,'
                   'url=?,'
                   'repo_empty=?,'
                   'only_readme=?,'
                   'archived=?,'
                   'created_at=?,'
                   'last_activity_at=? '
                   'WHERE id=?',
                   (
                       project.name,
                       project.path_with_namespace,
                       project.web_url,
                       False,
                       False,
                       archived,
                       project.created_at,
                       project.last_activity_at,
                       project.id
                   )
                   )
    cursor.commit()


def insert_user(cursor: sqlite3.Cursor, user):
    cursor.execute('INSERT INTO users ('
                   'id,'
                   'username,'
                   'email,'
                   'url,'
                   'is_admin,'
                   'state,'
                   'last_activity_on,'
                   'last_sign_in_at,'
                   'confirmed_at'
                   ')'
                   'VALUES (?,?,?,?,?,?,?,?,?)',
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
    cursor.commit()


def update_user(cursor: sqlite3.Cursor, user):
    cursor.execute('UPDATE users SET '
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
    cursor.commit()
