import sys
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from collections import deque

class Tree:

    def __init__(self, parent, url, degree):
        self.parent = parent
        self.url = url
        self.degree = degree

    def setSubURLs(self):
        if self.degree == max_degree:
            return
        urls = getSubURLs(self.url)
        if target_url in urls:
            answer = []
            answer.append(target_url)
            
            node = self
            while not node.parent is None:
                answer.append(node.url)
                node = node.parent
            answer.append(node.url)
            
            for i in answer[::-1][:-1]:
                sys.stdout.write(i + " => ")
            sys.stdout.write(answer[0] + '\n')    
            exit(0)
        for url in urls:
            node = Tree(self, url, self.degree + 1)
            queue.append(node)

def valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def getSubURLs(url):
    urls = set()
    
    global req_count
    req_count += 1
    if req_count > rate_limit:
        print("Достигнут лимит запросов")
        exit(5)
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            continue
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not valid_url(href):
            continue
        if href in int_url:
            continue
        if domain_name not in href:
            continue
        urls.add(href)
        int_url.add(href)
    return urls

max_degree = 5

url1 = "https://en.wikipedia.org/wiki/Six_degrees_of_separation"
url2 = "https://en.wikipedia.org/wiki/American_Broadcasting_Company"
domain_name = urlparse(url1).netloc

if urlparse(url2).netloc != domain_name:
    print("начальный и конечный URL-адреса имеют разные доменные имена")
    exit(3)

try:
	 rate_limit = 10
#  if rate_limit < 1:
 #     print("rate_limit меньше чем 1")
 #     exit(4)
except ValueError:
    print("неверный rate_limit")
    exit(4)

req_count = 0
int_url = set()
target_url = url2
tree = Tree(None, url1, 0)
queue = deque()
queue.append(tree)
while queue:
    node = queue.popleft()
    node.setSubURLs()

req_count = 0
int_url = set()
target_url = url1
tree = Tree(None, url2, 0)
queue = deque()
queue.append(tree)
while queue:
    node = queue.popleft()
    node.setSubURLs()

print("Достигнут предел ссылок")

