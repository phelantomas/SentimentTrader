from apscheduler.schedulers.blocking import BlockingScheduler
import collect_tweets, collect_prices

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=10)
def timed_job():
    print('This job is run every 10 seconds.')

@sched.scheduled_job('interval', minute=1)
def timed_job():
    print('This job is run every 10 seconds.')

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=10)
def scheduled_job():
    print('This job is run every weekday at 10am.')

#sched.configure(options_from_ini_file)
sched.start()