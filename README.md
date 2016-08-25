# finglonger

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


# log format

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


# Note

Finglonger is super beta, it will probably set your computer on fire. Try it, break it, and lets make it better together
