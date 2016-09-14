# finglonger

![Finglonger](futurama_finglonger.jpg)

Finglonger is a small tool that turns an intention log into shell commands that are run by a robot on a server. This means you can use git and code review to poke servers instead of rooters logging in.

# setup

You need a repo to hold the log. Make this.

* Clone finglonger into /opt/git/finglonger (or wherever)
* `virtualenv /opt/git/finglonger/venv`
* `/opt/git/finglonger/venv/bin/pip install pyyaml`
* Clone the log repo into /opt/git/finglonger-tasks/
* Create /var/run/finglonger.lock and /var/log/finglonger.log such that the user running finglonger can write to them
* (optional) setup logrotate on the finglonger log file
* Set some kind of a cron job to run ``git pull`` and ``finglonger.py`` in the log git repo periodically. It will automatically run things from the log.

# cron configuration


```shell
*/5 * * * * cd /opt/git/finglonger-tasks && git pull && flock -n /var/run/finglonger.lock /opt/git/finglonger/venv/bin/python /opt/git/finglonger/finglonger.py >> /var/log/finglonger.log 2>&1
```

The above crontab would cause finglonger to run once every five minutes and log to `/var/log/finglonger.log`:

## finglonger-tasks repo

You need a finglonger tasks repo. Start out with:

```
envs/default/tasks.yaml
files/
scripts/
```

See https://github.com/nibalizer/finglonger-tasks as an example
Tasks will only be run in the environment they are set in.


## tasks file format

Start your tasks file (tasks.yaml) out looking like this:


```yaml
---
- task:
    name: job
    shell: echo test +
- task:
    name: job
    shell: echo test +

```


Add one task object per commit or things are gonna break for you.


## Config file

Finglonger is controlled by `~/.config/finglonger/config.yaml`

```
---
environment: myenv
```

Environments allow different servers to be controlled by different tasks files.

# Note

Finglonger is super beta, it will probably set your computer on fire. Try it, break it, and lets make it better together.

# Hey this looks like ansible

Yup. Two big goals here:

1) Don't depend on ansible

2) Don't rewrite ansible

It is more important to accomplish the first than the second.


# Examples

## Echo some hello world


```yaml
- task:
    name: Hello world job
    shell: echo 'Hello, World!'
```


## Copy a file to a host

(Add config.js to the files directory in your finglonger-tasks)

```yaml
- task:
    name: Copy config.js to /var/www/html/myapp on app-server1.example.com
    shell: scp files/config.js root@app-server1.example.com:/var/www/html/myapp/config.js
```

## Restart some service on a host


```yaml
- task:
    name: Restart nova-api on compute1
    shell: ssh root@compute1.example.com 'service nova-api restart'
```


## Use more than one line

```yaml
- task:
    name: Some task that takes a while
    shell:  |
      echo "starting the big script woo"
      dd if=/dev/zero of=/tmp/bigfile bs=1k count=1000
```

## Log output

```yaml
- task:
    name: Something we care about the status of
    shell:  |
      echo "starting the big rsync woo"
      rsync -PHaze ssh my_dir remotehost:/home/nibz/my_dir | tee /var/www/html/finglonger/rsync_log1.txt
```
