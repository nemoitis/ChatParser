---
ChatParser
---

Easier, faster, and more efficient way to extract text from Chat Screenshot.

## Installation

Create a virtual environment with Python 3.10. Two `requirements` files are provided. One (`requirements.light.txt`) with a small number of packages for API only usages, another (`requirements.txt`) is with more packages and a GUI support using Gradio. Install either one as per your necessity.

```bash
pip install -r requirements.txt
```

## Running

### API Mode

To run the app in API only mode simply execute `./run.sh` from your terminal.

#### Endpoints

__GET `/api/v1/extract`__

| Param           | Type | Default | Description                  |
| --------------- | ---- | ------- | ---------------------------- |
| url (required)  | str  | None    | URL of an image file         |
| list (optional) | bool | False   | Determines the output format |

### GUI Mode

To run as the GUI run `python ui.py` from your terminal. You'll see the private and public URL in the terminal output. Hit the URL and it will open the user interface.

> [!IMPORTANT]
> Full dependencies should be installed using `requirement.txt`

## Deployment

You should use a process control system like `supervisor` to run the app in production mode. We recommend to use `gunicorn` – which is included in requirements – [to run the app](https://fastapi.tiangolo.com/deployment/server-workers/). Here's an example of the supervisor configuration.

```ini
[program:chatparser]
directory=path/to/chatparser
command=path/to/venv/gunicorn -c gunicorn.conf.py wsgi:app
process_name=%(program_name)s_%(process_num)02d
autostart=true
autorestart=true
user=<user-of-your-system>
numprocs=1
startsecs=1
redirect_stderr=true
stdout_logfile=/path/to/log/file.log
stdout_logfile_maxbytes=5MB
stdout_logfile_backups=3
stopwaitsecs=60
stopsignal=SIGTERM
stopasgroup=true
killasgroup=true
```

> [!NOTE]
> By default in `gunicorn.conf.py` file we set the `port` to __5023__ and `workers` to __4__. Adjust these values as per your system resources.
