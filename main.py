import logging
import os
import re
import traceback

import util
from util import logger
from github import GitHub


def generateArchiveMd(searches, topics):
    """生成归档readme
    """
    def search(item):
        return '1. [{}]({})'.format(item['title'], item['url'])

    def topic(item):
        return '1. [{}]({})\n    - {}\n    - {}'.format(item['title'], item['url'], item['detail'], item['info'])

    searchMd = '暂无数据'
    if searches:
        searchMd = '\n'.join([search(item) for item in searches])

    topicMd = '暂无数据'
    if topics:
        topicMd = '\n'.join([topic(item) for item in topics])

    readme = ''
    file = os.path.join('template','archive.md')
    with open(file) as f:
        readme = f.read()

    readme = readme.replace("{updateTime}", util.current_time())
    readme = readme.replace("{searches}", searchMd)
    readme = readme.replace("{topics}", topicMd)

    return readme


def generateReadme(searches, topics):
    """生成今日readme
    """
    def search(item):
        return '1. [{}]({})'.format(item['title'], item['url'])

    def topic(item):
        return '1. [{}]({})\n    - {}\n    - {}'.format(item['title'], item['url'], item['detail'], item['info'])

    searchMd = '暂无数据'
    if searches:
        searchMd = '\n'.join([search(item) for item in searches])

    topicMd = '暂无数据'
    if topics:
        topicMd = '\n'.join([topic(item) for item in topics])

    readme = ''
    file = os.path.join('template','README.md')
    with open(file) as f:
        readme = f.read()

    readme = readme.replace("{updateTime}", util.current_time())
    readme = readme.replace("{searches}", searchMd)
    readme = readme.replace("{topics}", topicMd)

    return readme


def handleReadme(md):
    logger.debug('today md:%s', md)
    util.write_text('README.md', md)


def handleArchiveMd(md):
    logger.debug('archive md:%s', md)
    name = '{}.md'.format(util.current_date())
    file = os.path.join('archives', name)
    util.write_text(file, md)


def saveRawContent(content: str, filePrefix: str):
    filename = '{}-{}.html'.format(filePrefix, util.current_date())
    file = os.path.join('raw', filename)
    util.write_text(file, content)


def run():
    weibo = Weibo()
    # 热搜
    searches, resp = weibo.get_hot_search()
    if resp:
        saveRawContent(resp.text,'hot-search')
    # 话题榜
    topics, resp = weibo.get_hot_topic()
    if resp:
        saveRawContent(resp.text,'hot-topic')

    # 最新数据
    readme = generateReadme(searches, topics)
    handleReadme(readme)
    # 归档
    archiveMd = generateArchiveMd(searches, topics)
    handleArchiveMd(archiveMd)


if __name__ == "__main__":
    run()
