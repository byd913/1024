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
        2  : '��������',
        15 : '��������',
        4  : 'ŷ��ԭ��',
        5  : '����ԭ��',
        21 : 'HTTP������',
        22 : '���߳���ӰԺ',
        7  : '����������',
        8  : '��ʱ��������',
        16 : '����������',
        20 : '������ѧ����',
        }
error_log = open('error.log', 'w')

class link_item:
	def __init__(self,href, content):
		self.href = href
		self.content = content

class CaoLiu:
    #fid: �������id
    #keywords: �����Ĺؼ����б�
    def __init__(self, fid, keywords):
        self.fid = fid
        self.keywords = keywords
        self.root_url = 'http://1024go.info/thread0806.php?fid=' + str(fid) + '&search=&'
        self.html_writer = open('_'.join(keywords) + '_' + fid_name_map[int(fid)] + '.html', 'w')
        self.html_writer.write('<html>\n<head>\n<title>' + ' '.join(keywords) + '</title>\n</head>')
        self.html_writer.write('<h1 align="center">' + ' '.join(keywords) + '</h1>\n')
        self.html_writer.flush()

    #url_link: ���ص�url
    #retry_times: ʧ�ܳ��ԵĴ���
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
        """���ݹؼ����������ӱ���"""
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
