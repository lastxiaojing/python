# -*- coding:utf-8 -*-
#import urllib
#import re
import urllib2
from lxml import etree
#################################
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class MSCHINA:

    __url = ''
    __user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:50.0) Gecko/20100101 Firefox/50.0"
    __headers = {'user-agent' : __user_agent}

    # 根据url获取可供xpath解析的源代码
    def getCodeByBaseUrl(self, url):
        self.__url = url
        try:
            # 获取网页源代码
            request = urllib2.Request(self.__url, headers = self.__headers)
            response = urllib2.urlopen(request)
            content = response.read()
            html = etree.HTML(content);
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
        return html

    # 根据xpath表达式和源代码获取解析结果，返回数组
    def getResByXpathExpr(self, html, expr):
        try:
            result = html.xpath(expr)
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
        return result

#######################################################################
# 获取美食天下新秀菜谱 一周热门 最受欢迎的家常菜里边的所有url
def getFirUrl(url):
    mschina = MSCHINA()
    html = mschina.getCodeByBaseUrl(url)
    # 新秀菜谱
    first_xpath = 'body/div[3]/div/div[4]/div[2]/ul[1]//li/a[1]/@href'
    first_part = mschina.getResByXpathExpr(html, first_xpath);
    # 一周热门
    second_xpath = 'body/div[3]/div/div[4]/div[2]/ul[2]//li/a[1]/@href'
    second_part = mschina.getResByXpathExpr(html, second_xpath);
    # 最受欢迎的家常菜 第一层url
    third_xpath = 'body/div[3]/div/div[4]/div[2]/ul[3]//li/a[1]/@href'
    third_part = mschina.getResByXpathExpr(html, third_xpath)
    # 最受欢迎的家常菜第二层url
    third_part_url = []
    for url_1 in third_part:
        html_1 = mschina.getCodeByBaseUrl(url_1)

        xpath = 'body/div[3]/div[3]//ul/li/div/a/@href'
        href = mschina.getResByXpathExpr(html_1, xpath)
        third_part_url += href

        xpath = 'body/div[3]/div[5]//ul/li/div/a/@href'
        href = mschina.getResByXpathExpr(html_1, xpath)
        third_part_url += href

    # 返回所有url
    return first_part + second_part + third_part_url

# 根据url获取菜谱的制作方法和内容
def getContentByUrl(url):
    mschina = MSCHINA()
    html = mschina.getCodeByBaseUrl(url)
    # title = "食材明细"
    # 获取食材标签数量
    xpath = 'body/div[5]/div/div[1]/div[2]/div/div[3]/ul//li'
    lis = mschina.getResByXpathExpr(html, xpath)
    names = []
    qual = []
    _len = len(lis)
    for ind in range(0, _len):
        # 每种食材名称
        index = '%d' %(ind + 1)
        xpath = 'body/div[5]/div/div[1]/div[2]/div/div[3]/ul//li[' + index + ']/span[1]/b/text()'
        name = mschina.getResByXpathExpr(html, xpath)
        if(len(name) == 0):
            xpath = 'body/div[5]/div/div[1]/div[2]/div/div[3]/ul//li[' + index + ']/span[1]/a/b/text()'
            name = mschina.getResByXpathExpr(html, xpath)
        names.append(name[0])
        # 每种食材用量
        xpath = 'body/div[5]/div/div[1]/div[2]/div/div[3]/ul//li[' + index + ']/span[2]/text()'
        q = mschina.getResByXpathExpr(html, xpath)
        if(len(q) == 0):
            q = ['适量']
        qual.append(q[0])
    # 制作步骤
    xpath = 'body/div[5]/div/div[1]/div[2]/div/div[6]/ul//li/div[2]/text()'
    step = mschina.getResByXpathExpr(html, xpath)
    #
    res = ''
    _len = len(names)
    for ind in range(0, _len):
        single = ''
        single += names[ind]
        single += '\t'
        single += qual[ind]
        single += '\n'
        res += single
    res += ('-' * 25)
    res += '\n'
    for s in step:
        res += s
        res += '\n'
    res += ('+' * 100)
    return res

# 获取所有菜的制作步骤
def getAllStep(urls):
    result = []
    for url in urls:
        single = getContentByUrl(url)
        result.append(single)
        result.append("\n\n")
    return result

#######################################################################

if __name__ == "__main__":
     url = 'http://www.meishichina.com/'
     urls = getFirUrl(url)

     result = getAllStep(urls)
     for res in result:
         print res
