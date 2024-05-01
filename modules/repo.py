import os
import sqlite3
import gitlab

# Gitlab API URL
GITLAB_URL = os.environ.get('GITLAB_URL')
GITLAB_TOKEN = os.environ.get('GITLAB_PRIVATE_TOKEN')

git = gitlab.Gitlab(
    GITLAB_URL, private_token=GITLAB_TOKEN, api_version=4)  # type: ignore
git.auth()

# Connect to the database
connection = sqlite3.connect('gitlab.db')
cursor = connection.cursor()


def create_table():



if os.path.exists('gitlab.db'):
    if cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="gitlab"').fetchone():
        print('Table exists')
    else:
        cursor.execute(
            'CREATE TABLE gitlab ('
            'id INTEGER PRIMARY KEY,'
            'name TEXT,'
            'path TEXT,'
            'url TEXT,'
            'ci_variables BOOLEAN,'
            'pipeline_yml BOOLEAN,'
            'have_jobcommons BOOLEAN,'
            'repo_empty BOOLEAN,'
            'only_readme BOOLEAN,'
            'archived BOOLEAN,'
            'created_at TEXT,'
            'last_activity_at TEXT'
            ')'
        )
        print('Table created')
        connection.commit()

for project in git.projects.list(all=True):
    # Check if the project exists in the database
    
        print(f'Project {project.name} already exists')
        print('Updating project...')
        if project.archived:
            cursor.execute(
                'UPDATE gitlab SET '
                'name=?,'
                'path=?,'
                'url=?,'
                'ci_variables=?,'
                'pipeline_yml=?,'
                'have_jobcommons=?,'
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
                    False,
                    False,
                    False,
                    True,
                    project.created_at,
                    project.last_activity_at,
                    project.id
                )
            )
            continue
        else:
            cursor.execute(
                'UPDATE gitlab SET '
                'name=?,'
                'path=?,'
                'url=?,'
                'ci_variables=?,'
                'pipeline_yml=?,'
                'have_jobcommons=?,'
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
                    False,
                    False,
                    False,
                    project.archived,
                    project.created_at,
                    project.last_activity_at,
                    project.id
                )
            )
            continue
    else:
        print(f'Project {project.name} does not exist')
        print('Inserting project...')
        if project.archived:
            cursor.execute(
                'INSERT into gitlab ('
                'id,'
                'name,'
                'path,'
                'url,'
                'ci_variables,'
                'pipeline_yml,'
                'have_jobcommons,'
                'repo_empty,'
                'only_readme,'
                'archived,'
                'created_at,'
                'last_activity_at) '
                'VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
                (
                    project.id,
                    project.name,
                    project.path_with_namespace,
                    project.web_url,
                    False,
                    False,
                    False,
                    False,
                    False,
                    True,
                    project.created_at,
                    project.last_activity_at
                )
            )
        else:
            cursor.execute(
                'INSERT into gitlab ('
                'id,'
                'name,'
                'path,'
                'url,'
                'ci_variables,'
                'pipeline_yml,'
                'have_jobcommons,'
                'repo_empty,'
                'only_readme,'
                'archived,'
                'created_at,'
                'last_activity_at) '
                'VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
                (
                    project.id,
                    project.name,
                    project.path_with_namespace,
                    project.web_url,
                    False,
                    False,
                    False,
                    False,
                    False,
                    False,
                    project.created_at,
                    project.last_activity_at
                )
            )
    connection.commit()

connection.close()