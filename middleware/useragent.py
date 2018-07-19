from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class UserAgentMiddleware(MiddlewareMixin):
    '''
    判断请求是否为正常浏览器（反爬虫措施）
    '''
    def __init__(self, get_response):
        super(UserAgentMiddleware, self).__init__(get_response)

    def process_request(self,request):
        print(request.META)
        user_agent = request.META.get("HTTP_USER_AGENT")
        if user_agent.strip() == '':
            return HttpResponse('<p>爬虫太low</p>')