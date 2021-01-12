import contextlib
import json
import traceback
from enum import Enum

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from util import logger

TRENDING_REPOSITORY_URL = "https://github.com/trending"
TRENDING_DEVELOPER_URL = "https://github.com/trending/developers"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
}

RETRIES = Retry(total=3,
                backoff_factor=1,
                status_forcelist=[k for k in range(400, 600)])


@contextlib.contextmanager
def request_session():
    s = requests.session()
    try:
        s.headers.update(HEADERS)
        s.mount("http://", HTTPAdapter(max_retries=RETRIES))
        s.mount("https://", HTTPAdapter(max_retries=RETRIES))
        yield s
    finally:
        s.close()


class Since(Enum):
    daily = 'daily'
    weekly = 'weekly'
    monthly = 'monthly'


class GitHub:

    def get_trending_repository(self, since: Since = Since.daily):
        """热门仓库
        """
        items = []
        resp = None
        try:
            with request_session() as s:
                resp = s.get(TRENDING_REPOSITORY_URL)
                soup = BeautifulSoup(resp.text, features='html.parser')
                articles = soup.select('main article.Box-row')
                logger.info('articles:%s', len(articles))
                for article in articles:
                    href = article.select_one('h1.h3 > a')['href']
                    desc = article.select_one('p').text.strip()
                    div = article.select_one('div.f6')
                    spans = div.select('span')
                    # TODO 并非每个仓库都有语言标签
                    language = spans[0].text.strip()
                    since_stars = spans[2].text.strip()
                    all_stars = div.select_one('a').text.strip()
                    logger.info('repo:%s %s', href,desc)
                    logger.info('lan:%s stars:%s allStars:%s',
                                language, since_stars, all_stars)
        except:
            logger.warning(traceback.format_exc())
        return (items, resp)

    def get_trending_developer(self):
        """热门话题
        """
        items = []
        resp = None
        try:
            with request_session() as s:
                resp = s.get(TRENDING_DEVELOPER_URL)
                html = resp.text
                soup = BeautifulSoup(html)
                ul = soup.select('section.list > ul.list_b > li')
                if ul:
                    for li in ul:
                        a = li.find('a')
                        if a:
                            url = 'https://s.weibo.com{}'.format(a['href'])
                            title = a.select_one('article > h2').text
                            detail = a.select_one('article > p').text
                            if not detail:
                                detail = '暂无数据'
                            info = a.select_one('article > span').text
                            if not info:
                                info = '暂无数据'
                            items.append({'title': title, 'url': url,
                                          'detail': detail, 'info': info})
        except:
            logger.warning(traceback.format_exc())
        return (items, resp)


if __name__ == "__main__":
    github = GitHub()
    repositories, resp = github.get_trending_repository(Since.daily)
    # logger.info('%s', repositories[0])
