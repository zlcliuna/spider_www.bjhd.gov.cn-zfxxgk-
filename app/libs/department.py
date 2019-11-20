import re
import time
import requests
from bs4 import BeautifulSoup

class Department:
    zyk_url = 'http://www.bjhd.gov.cn/zfxxgk/'
    wzk_url = 'http://www.bjhd.gov.cn/'

    def __init__(self,searchView):
        self.departList = self.__get_department(searchView)
        self.columns = self.__get_column(searchView)
        self.pageList = self.__get_pageList()
        self.itemsList = self.__get__items(searchView)
        self.itemsList = self.__filter_keyword(searchView)
        self.itemsList = self.__filter_date(searchView)

    # 获取html
    @staticmethod
    def __get_html(url):
        r = requests.get(url)
        if(r.status_code==200):
            r.encoding = 'utf-8'
            return r.text
        return False

    # 获取分页链接
    @staticmethod
    def __get_pageLink(url,num):
        pageLink = []
        for i in range(num):
            if(i == 0):
                pageLink.append(url)
            else:
                pageLink.append(url.replace('.shtml',('_' + str(i) + '.shtml')))
        return pageLink

    # 获取单位名称和链接
    def __get_department(self,searchView):
        departList = {}
        htmlDoc = self.__get_html(searchView.domainUrl)
        if(htmlDoc):
            soup = BeautifulSoup(htmlDoc,'html.parser')
            if(searchView.department):
                for a in soup.select('.zdlyList li a'):
                    if(a.get_text()==searchView.department):
                        departList[a.get_text()] = a.attrs['href'].replace('./',self.zyk_url)
            else:
                for a in soup.select('.zdlyList li a'):
                    departList[a.get_text()] = a.attrs['href'].replace('./',self.zyk_url)
        return departList

    # 获取栏目名称和链接
    def __get_column(self,searchView):
        columns = {}
        for key,val in self.departList.items():
            column = []
            htmlDoc = self.__get_html(val)
            if(htmlDoc):
                soup = BeautifulSoup(htmlDoc,'html.parser')

                for script in soup.select('.mlList script'):
                    pattern = re.compile(r'<a href="(.*?)</a>')
                    patternHref = re.compile(r'<a href="(.*?)"')
                    patternTitle = re.compile(r'target="DataList">(.*?)</a>')
                    txt_a = re.search(pattern, script.get_text()).group()
                    temp = {}
                    temp['link'] = re.search(patternHref,txt_a).group(1).replace('./',val)
                    temp['title'] = re.sub(r'<(.*?)>','',re.search(patternTitle,txt_a).group(1))
                    if (searchView.column != '' and temp['title']==searchView.column):
                        column = []
                        column.append(temp)
                        break
                    else:
                        column.append(temp)
                if (len(column)):
                    columns[key] = column
        return columns

    # 获取列表页的链接
    def __get_pageList(self):
        pageList = []

        for key, val in self.columns.items():
            for column in val:
                tempDict = {}
                tempDict['depart'] = key
                htmlDoc = self.__get_html(column['link'])
                if (htmlDoc):
                    soup = BeautifulSoup(htmlDoc,'html.parser')
                    pattern = re.compile(r'var countPage = (.*?)//共多少页')
                    total_page = int(re.search(pattern,soup.select('.page')[0].get_text()).group(1))
                    pageLink = self.__get_pageLink(column['link'],total_page)
                    tempDict['link'] = pageLink
                    tempDict['column'] = column['title']
                    pageList.append(tempDict)
        return pageList

    # 获取文章的标题、链接、发布日期
    def __get__items(self,searchView):

        pageItems = []

        for page in self.pageList:
            tempItem = {}
            tempItem['location'] = {}
            tempItem['list'] = []
            tempItem['location']['depart'] = page['depart']
            tempItem['location']['column'] = page['column']
            tempItem['location']['colLink'] = page['link'][0].replace('index_bm.shtml','')

            for link in page['link']:
                htmlDoc = self.__get_html(link)
                if(htmlDoc):
                    soup = BeautifulSoup(htmlDoc, 'html.parser')
                    pattern_wl = re.compile("var strLink = '(.*?)'")
                    pattern_href = re.compile('<a href="./(.*?)"')
                    pattern_title = re.compile('target="_blank">(.*?)</a>')
                    pattern_date = re.compile('<td class="rq"><span>(.*?)</span></td>')
                    for tr in soup.select('.listTab tr'):
                        tempDict = {}
                        if(re.search(pattern_wl,tr.get_text()) == None or re.search(pattern_href, tr.get_text())==None):
                            continue
                        if(re.search(pattern_wl,tr.get_text()).group(1) == ''):
                            tempDict['link'] = re.search(pattern_href, tr.get_text()).group(1)
                        else:
                            tempDict['link'] = re.search(pattern_wl,tr.get_text()).group(1)
                        tempDict['title'] = re.search(pattern_title, tr.get_text()).group(1)

                        if(len(tr.select('td[class="rq"]')) and tr.select('td[class="rq"]')[0].get_text()):
                            tempDict['date'] = tr.select('td[class="rq"]')[0].get_text()
                        else:
                            tempDict['date'] = time.strftime("%Y-%m-%d", time.localtime())
                        tempItem['list'].append(tempDict)
            if(len(tempItem['list'])):
                pageItems.append(tempItem)
                tempItem['location']['total'] = len(tempItem['list'])
        return pageItems

    # 关键字过滤
    def __filter_keyword(self, searchView):
        if(searchView.keyword):
            tempList = self.itemsList
            for depart in tempList[::-1]:
                for item in depart['list'][::-1]:
                    if(searchView.keyword in item['title']):
                        item['link'] = depart['location']['colLink'] + item['link']
                        continue
                    else:
                        depart['list'].remove(item)
                        depart['location']['total'] = depart['location']['total']-1
                if(len(depart['list'])<=0):
                    tempList.remove(depart)
            return tempList
        else:
            for depart in self.itemsList:
                for item in depart['list']:
                    item['link'] = depart['location']['colLink'] + item['link']
            return self.itemsList


    # 日期过滤
    def __filter_date(self,searchView):
        if(searchView.startTime and searchView.endTime):
            tempList = self.itemsList
            for depart in tempList[::-1]:
                for item in depart['list'][::-1]:
                    timeArray = time.strptime(item['date'], '%Y-%m-%d')
                    itemStamp = int(time.mktime(timeArray))
                    if(itemStamp < searchView.startTime or itemStamp > searchView.endTime):
                        depart['list'].remove(item)
                        depart['location']['total'] = depart['location']['total'] - 1
                if(len(depart['list'])<=0):
                    tempList.remove(depart)
            return tempList
        return self.itemsList



