#!/usr/bin/env python3
#
#  Copyright 2022, Pygolo Project contributors
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sqlite3
import threading

import gitlab

parser = argparse.ArgumentParser(
    prog="delete-old-pipelines",
    description="Delete old Gitlab pipelines",
)

parser.add_argument("--config", type=Path, default=".delete-old-pipelines.yaml",
                    help="load configuration from path CONFIG")
parser.add_argument("--dryrun", action="store_true",
                    help="show what pipelines would be delete")
parser.add_argument("--weeks", type=int, default=6,
                    help="pipelines older than WEEKS are considered old")
parser.add_argument("--token", help="Gitlab API auth token")


def get_keep_pipelines(project):
    for issue in project.issues.list(state="opened", iterator=True):
        for label in issue.labels:
            parts = label.split("::")
            if len(parts) > 1 and parts[1] == "pipeline":
                yield int(parts[0]), issue.web_url


def delete_old_pipelines(config, project_id, weeks, token=None, dryrun=True):
    gl = gitlab.Gitlab(, private_token=token)
    project = gl.projects.get(project_id)
    now = datetime.now(timezone.utc)
    keep_pipelines = dict(get_keep_pipelines(project))

    for pipeline in project.pipelines.list(iterator=True):
        dt = datetime.fromisoformat(pipeline.created_at)
        delta = now - dt

        if pipeline.id in keep_pipelines:
            if dryrun:
                print(f"{pipeline.id} ({dt}) is {
                      delta.days} day(s) old  <---  would keep ({keep_pipelines[pipeline.id]})")
            continue

        if delta < timedelta(weeks=weeks):
            if dryrun:
                print(f"{pipeline.id} ({dt}) is {
                      delta.days} day(s) old  <---  too young")
            continue

        if dryrun:
            print(f"{pipeline.id} ({dt}) is {
                  delta.days} day(s) old  <---  would delete")
        else:
            print(f"{pipeline.id} ({dt}) is {
                  delta.days} day(s) old, deleting...")
            pipeline.delete()


def load_config(config_path):
    if config_path.exists():
        with open(config_path) as f:
            import yaml

            return yaml.safe_load(f)


def run(p):
    semaphore.acquire()
    print(f"Processing {p[1]}")
    delete_old_pipelines(config, p[0], args.weeks,
                         args.token, args.dryrun)
    conn = sqlite3.connect("../gitlab.db")
    c = conn.cursor()
    c.execute("UPDATE gitlab SET scanned = 1 WHERE id = ?", (p[0],))
    conn.commit()
    conn.close()
    semaphore.release()


if __name__ == "__main__":
    args = parser.parse_args()
    config = load_config(args.config)
    conn = sqlite3.connect("../gitlab.db")
    c = conn.cursor()
    #c.execute("UPDATE gitlab SET scanned = 0")
    c.execute("SELECT * FROM gitwClab where archived = 0 and scanned = 0")
    projects = c.fetchall()
    projects.sort()

    conn.close()
    max_threads = 200
    semaphore = threading.Semaphore(max_threads)
    threads = list()

    threads = [threading.Thread(target=run, args=(project,))
               for project in projects]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
