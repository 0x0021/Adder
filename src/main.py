import json
import requests
# from apscheduler.schedulers.blocking import  BlockingScheduler
import time
import sched
import datetime


# 给钉钉发送群消息
def send_msg():
    # 机器人的URL
    webHook = 'https://oapi.dingtalk.com/robot/send?access_token=XXXXXXX'

    # 需要发送的内容
    content = {
        "msgtype": "text",
        "text": {
            "content": "提示：请大家准时提交SVN的内容，防止文件丢失！@所有人"
        },
        "at": {
          "isAll": True
        }
    }

    # 调用request.post发送json格式的参数
    headers = {'Content-Type': 'application/json'}
    result = requests.post(url=webHook, data=json.dumps(content), headers=headers)
    response_msg = result.json()
    if response_msg['errcode']:
        return True
    return False




# 启动时间
def circle_send_msg(scheduler):
    for i in range(3):
        time.sleep(1)
        print("hello")
        # send_msg()


    # 推测 24 小时后继续发送
    scheduler.enter(24 * 3600 - 3, 0, circle_send_msg, (scheduler,))


# 执行函数
if __name__ =="__main__":

    print("程序启动！")
    # 生成一个定时器
    s = sched.scheduler(time.time, time.sleep)
    now = datetime.datetime.now()
    format_now_time = now.strftime('%Y-%m-%d %H:%M:%S')
    if now.weekday() == 5:  # 星期6
        end_date = "%d-%d-%d 17:25:00" % (now.year, now.month, now.day + 2)
    else:
        end_date = "%d-%d-%d 17:25:00" % (now.year, now.month, now.day + 1)
    delta = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S') - \
            datetime.datetime.strptime(format_now_time, '%Y-%m-%d %H:%M:%S')
    s.enter(delta.total_seconds(), 0, circle_send_msg, (s,))
    s.run()
    # scheduler = BlockingScheduler()
    # scheduler.add_job(send_msg, 'cron', day_of_week="0-5", hour=17, minute=25)
    # scheduler.add_job(send_msg, 'cron', day_of_week="0-5", hour=17, minute=45)
    # try:
    #     scheduler.start()
    # except (KeyboardInterrupt, SystemExit):
    #     print("出现异常")
