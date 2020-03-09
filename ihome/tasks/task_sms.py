from celery import Celery
from ihome.libs.yuntongxun.sms import CCP

celery_app = Celery("ihome", broker="redis://10.1.1.128:6379/1")

@celery_app.task
def send_sms(to, datas, temp_id=1):
    """发送短信的异步任务"""
    ccp = CCP()
    ccp.send_template_sms(to, datas, temp_id)

# celery命令
# celery -A ihome.tasks.task_sms worker -l info