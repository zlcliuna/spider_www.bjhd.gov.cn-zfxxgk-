import time

class SearchView:
    zyk_url = 'http://www.bjhd.gov.cn/zfxxgk/'
    wzk_url = 'http://www.bjhd.gov.cn/'

    def __init__(self,form):
        self.siteName = form.siteName.data
        self.department = form.department.data
        self.column = form.column.data
        self.keyword = form.keyword.data
        self.startTime = self.__returnStamp(form.startTime.data)
        self.endTime = self.__returnStamp(form.endTime.data)
        self.domainUrl = self.__returnDomainUrl(form.siteName.data)

    # 字符类型的时间格式：'2019-10-10'
    @staticmethod
    def __returnStamp(str):
        if(str):
            timeArray = time.strptime(str,'%Y-%m-%d')
            return int(time.mktime(timeArray))


    def __returnDomainUrl(self,siteName):
        if (siteName == '海淀区信息公开大厅'):
            return self.zyk_url
        if (siteName == '海淀区政府'):
            return self.wzk_url