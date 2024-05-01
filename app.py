import argparse
import os
import sqlite3
import modules.db
import gitlab


cmdargs = argparse.ArgumentParser(
    prog="Gitlab Automation Tool",
    description="Gitlab Automation Tool to create, management project and users in GitLab.",
    add_help=False
)

#
# Required Arguments
reqgroup = cmdargs.add_argument_group('Required Arguments')
# Action is the main argument to specify the action to perform
reqgroup.add_argument('--action', '-a', required=True,
                      help='Action to perform. Possible values: update, delete, list ')
# Type is the type of the object to perform the action on
reqgroup.add_argument('--gitlab-token', required=True,
                      help='GitLab Token. See https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html to create a token')
# GitLab URL is the URL of the GitLab server
reqgroup.add_argument('--gitlab-url', required=True,
                      help='URL of the GitLab server')
#
# Optional Arguments
optgroup = cmdargs.add_argument_group('Optional Arguments')
optgroup.add_argument('--help', '-h', action='help', default=argparse.SUPPRESS,
                      help='Show this help message with all the available options')
# NoDB is a flag to skip the database creation and usage
optgroup.add_argument('--no-db', action='store_true',
                      help='Do not use local database to store list of projects (consequently more slow for the other executions)')
# All is a flag to get all projects or users
optgroup.add_argument('--all', action='store_true',
                      help='Get all projects, applicable for Group or All GitLab (Projects or Users)')
#
# Project Group
pgroup = cmdargs.add_argument_group('Projects')
# Project ID is of project to perform the action
pgroup.add_argument('--project-id', '-pid',
                    required=False, help='ID of the project')
# Project Name of project to perform the action
pgroup.add_argument('--project-name', '-pname',
                    required=False, help='Name of the project')
# Project Namespace is the group of the project
pgroup.add_argument('--project-namespace', '-pnamespace',
                    required=False, help='Group of the project')
#
# User Group
ugroup = cmdargs.add_argument_group('Users')
# Username is the name of the user to perform the action
ugroup.add_argument('--username', '-u', required=False,
                    help='Name of the user')
# User Email is the email of the user to perform the action
ugroup.add_argument('--user-email', '-email', required=False,
                    help='Email of the user')
args = cmdargs.parse_args()

GITLAB_URL = args.gitlab_url
GITLAB_TOKEN = args.gitlab_token
GITLAB_ACTION = args.action

GITLAB_PROJECT_ID = args.project_id
GITLAB_PROJECT_NAME = args.project_name
GITLAB_PROJECT_NAMESPACE = args.project_namespace

GITLAB_USERNAME = args.username
GITLAB_USER_EMAIL = args.user_email

if args.no_db:
    SKIP_DB = True
else:
    SKIP_DB = None
    if not os.path.exists('gitlab_data.db'):
        connnection = sqlite3.connect('gitlab_data.db')
        cursor = connnection.cursor()
        modules.db.CreateDB(cursor)

GITLAB_GET_ALL = args.all


git = gitlab.Gitlab(
    GITLAB_URL, private_token=GITLAB_TOKEN, api_version=4)  # type: ignore
git.auth()

