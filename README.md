# finglonger

![Finglonger](futurama_finglonger.jpg)

Finglonger is a small tool that turns an intention log into shell commands that are run by a robot on a server. This means you can use git and code review to poke servers instead of rooters logging in.

# setup

You need a repo to hold the log. Make this.

* Clone finglonger into /opt/git/finglonger (or wherever)
* `virtualenv /opt/git/finglonger/venv`
* `/opt/git/finglonger/venv/bin/pip install pyyaml`
* Clone the log repo into /opt/git/finglonger-tasks/
* Symlink in the finglonger hook: `ln -s /opt/git/finglonger/finglonger-hook /opt/git/finglonger-tasks/.git/hooks/post-merge`
* Create /var/run/finglonger.lock and /var/log/finglonger.log such that the user running finglonger can write to them
* (optional) setup logrotate on the finglonger log file
* Set some kind of a cron job to run 'git pull' in the log git repo periodically. It will automatically run things from the log.
  * For example, adding the following to the appropriate user's crontab would cause finglonger to run once every five minutes and log to `/var/log/finglonger.log`:

        ```shell
        */5 * * * * cd /opt/git/finglonger-tasks && flock -n /var/run/finglonger.lock git pull >> /var/log/finglonger.log 2>&1
        ```

## finglonger-tasks repo

You need a finglonger tasks repo. Start out with:

```
envs/default/tasks.yaml
files
scripts
```

See https://github.com/nibalizer/finglonger-tasks as an example
Tasks will only be run in the environment they are set in.



## log format

Start your log(tasks.yaml) out looking like this:


```yaml
---
task:
  name: job
  shell: echo test +
task:
  name: job
  shell: echo test +

```


Add one task object per commit or things are gonna break for you.


## Config file

Finglonger is controlled by `~/.config/finglonger/finglongerrc`

```
environment=myenv
```

The default environment is 'default'. If you don't have a finglongerrc, 'default' will be used.
Tasks will only be run in the environment they are set in.

# Note

Finglonger is super beta, it will probably set your computer on fire. Try it, break it, and lets make it better together


# Examples

## Echo some hello world


```yaml
task:
  name: Hello world job
  shell: echo Hello World!
```


## Copy a file to a host

(Add config.js to the files directory in your finglonger-tasks)

```yaml
task:
  name: Copy config.js to /var/www/html/myapp on app-server1.example.com
  shell: scp files/config.js root@app-server1.example.com:/var/www/html/myapp/config.js
```

## Restart some service on a host


```yaml
task:
  name: Restart nova-api on compute1
  shell: ssh root@compute1.example.com 'service nova-api restart'
```

