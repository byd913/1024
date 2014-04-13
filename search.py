#encoding=gbk
import socket
import urllib
import urllib2
import cookielib
import re
keywords = []
START_PAGE = 1
END_PAGE = 50
SOCKET_TIMEOUT = 60
root_urls = []
link_list = []

fid_name_map = { 
        2  : '亚洲有码',
        15 : '亚洲无码',
        4  : '欧美原创',
        5  : '动漫原创',
        21 : 'HTTP下载区',
        22 : '在线成人影院',
        7  : '技术讨论区',
        8  : '新时代的我们',
        16 : '草榴自拍区',
        20 : '成人文学交流',
        }
error_log = open('error.log', 'w')

class link_item:
	def __init__(self,href, content):
		self.href = href
		self.content = content

class CaoLiu:
    #fid: 草榴板块的id
    #keywords: 搜索的关键词列表
    def __init__(self, fid, keywords):
        self.fid = fid
        self.keywords = keywords
        self.root_url = 'http://1024go.info/thread0806.php?fid=' + str(fid) + '&search=&'
        self.html_writer = open('_'.join(keywords) + '_' + fid_name_map[int(fid)] + '.html', 'w')
        self.html_writer.write('<html>\n<head>\n<title>' + ' '.join(keywords) + '</title>\n</head>')
        self.html_writer.write('<h1 align="center">' + ' '.join(keywords) + '</h1>\n')
        self.html_writer.flush()

    #url_link: 下载的url
    #retry_times: 失败尝试的次数
    def download_link(self, url_link, retry_times):
        content = None
        cur_retry_times = 0
        while cur_retry_times <= retry_times:
            try:
                content = urllib2.urlopen(url_link).read()
                break
            except Exception :
                cur_retry_times += 1
                print 'cur_retry_times:' + str(cur_retry_times)
                continue
        if (cur_retry_times > retry_times):
            error_log.write('download ' + url_link + ' failed!\n')
            error_log.flush()
        return content
    def search(self):
        """根据关键字搜索帖子标题"""
        for page in xrange(START_PAGE, END_PAGE):
            page_url = self.root_url + 'page=' + str(page)
            content = self.download_link(page_url, 3)
            if content == None:
                continue

            item_groups = content.split('<h3><a href="htm_data')
            for item in item_groups:
                lines = item.split('\n')
                m = re.search(u'[^"]+', lines[0])
                href = ''
                if m != None:
                    href = 'http://1024go.info/htm_data' + m.group(0)
                content = re.sub('<[^>]*>', '',lines[0])
                content = re.sub('^[^>]*>', '',content)
                has_keyword = False
                for word in keywords:
                    if content.upper().find(word.upper()) != -1:
                        has_keyword = True
                        break
                if has_keyword == True:
                    self.html_writer.write('<a href="' + href + '">' + content + '</a><br>\n')
                    self.html_writer.flush()	
        self.html_writer.write('</html>\n')
        self.html_writer.flush()
        self.html_writer.close()


def load_keyword():
		for line in open('keyword.txt'):
			word = line.replace('\n', '')
			keywords.append(word)

socket.setdefaulttimeout(SOCKET_TIMEOUT)
load_keyword()
obj = CaoLiu(2, keywords)
obj.search()
