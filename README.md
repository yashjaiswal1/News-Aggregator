# **News Aggregator API**

## Features

- Fetches the newest blogs from [HackerNews RSS feed](https://hnrss.org/newest).
- Features API pagination with string query param for `?page=val` and `?limit=val`.
- Supports filtering via author name using query param `?author=val`.
- Supports filtering via daterange using query param `?start=val` and `?end=val`.
- Returns a JSON response in reverse chronological order.
- Baked-in support for CRON jobs to update DB isntance every 1 hour.

# Installation

Follow the given steps to run an instance of this API on your own local machine.

### Install and activate virtualenv

- Check if Python and pip is installed on your system. If you see a `command not found` error then install the respective packages from [here](https://www.python.org/downloads/) and [here](https://pip.pypa.io/en/stable/cli/pip_download/). <br>
  ```bash
  $ python3 --version
  ```
  ```bash
  $ pip3 --version
  ```
- Install virtualenv. <br>
  ```bash
  $ pip install virtualenv
  ```
- Test your installation <br>

  ```bash
  $ virtualenv --version
  ```

- Now, create a virtualenv.

  ```bash
  $ virtualenv env_name
  ```

  NOTE: Execute this command in the root dir of this project.

- Activate the virtualenv.

  ```bash
  $ source env_name/bin/activate
  ```

  Your virtualenv is now active and you should notice the env name appearing before the `$`.

  ```bash
  (env_name) $
  ```

### Install dependencies

- Install dependencies from `requirements.txt`.

  ```bash
  pip3 install -r requirements.txt
  ```

### Run flask server

- Run the `app.py` file to start the flask server.

  ```bash
  python3 app.py
  ```

- Now, you should be able to access the API endpoint at `http://127.0.0.1:5000/api`

  NOTE: You might need to run the `initDB()` method (present in `parser.py`) once to initialize your SQLite DB.

Additionally, you can run a CRON job to automatically populate your DB with HackerNews RSS feed.

```bash
# ┌───────────── minute (0 - 59)
# │ ┌───────────── hour (0 - 23)
# │ │ ┌───────────── day of the month (1 - 31)
# │ │ │ ┌───────────── month (1 - 12)
# │ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday;
# │ │ │ │ │                                   7 is also Sunday on some systems)
# │ │ │ │ │
# │ │ │ │ │
# * * * * * <command to execute>
0 * * * * source /<enter_path_here>/News-Aggregator/news_agg_env/bin/activate && python3 /<enter_path_here>/News-Aggregator/parser.py
```

This CRON job will run every hour and will update your SQLite DB with the newest RSS feed fetched from [here](https://hnrss.org/newest).
