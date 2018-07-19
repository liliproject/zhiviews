from datetime import datetime
import time
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
import redis

# 全局黑名单
BLACK_MEMBER = {}

class IpCountMiddleware(MiddlewareMixin):
    '''
    同一个ip访问次数（反爬虫措施）
    '''
    def __init__(self, get_response):
        super(IpCountMiddleware, self).__init__(get_response)
        self.db = redis.Redis(host='127.0.0.1',
                              port=6379,
                              db=1,
                              decode_responses=True)

    def process_request(self,request):
        user_ip = request.META.get('REMOTE_ADDR')
        # 判断user_ip 是否在黑名单中
        if user_ip in BLACK_MEMBER.keys():
            if time.time()-BLACK_MEMBER[user_ip] < 24*3600:
                return HttpResponse('<p>您的请求过于频繁，请休息一下先</p>')
            else:
                BLACK_MEMBER.pop(user_ip)
        self.db.rpush(user_ip,time.time())
        # 获取同一个ip的登陆次数
        fw_count = self.db.llen(user_ip)
        if fw_count >=5:
            fw_times = self.db.lrange(user_ip,0,-1)  # 返回当前ip登录的所有时间点
            # 判断第五次请求和第一次请求的时间间隔是否大于1s
            if fw_times[4]-fw_times[0] < 1:
                # 属于非正常请求，加入黑名单
                self.add_black(user_ip)
            # 清楚记录
            self.db.delete(user_ip)


    @staticmethod
    def add_black(user_ip):
        BLACK_MEMBER[user_ip] = time.time()