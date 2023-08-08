import time
import schedule

def job():
    timeStr = time.strftime("%Y-%m-%d %H:%M:%S")
    print("WWWWWWWWWWWWWWWWWWWWWWWWWWWW Job run time:", timeStr)
    
job()

task = schedule.every(2).seconds.do(job)

while True:
    print("do do do ...")
    schedule.run_pending()