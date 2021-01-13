import logging
import os

import util
from github import GitHub, Since
from util import logger


def generateArchiveMd(daily, weekly, monthly):
    """生成归档readme
    """
    def li(item):
        href = item['href']
        url = item['url']
        description = item['description']
        language = item['language']
        stars = item['stars']
        folks = item['folks']
        recent_stars = item['recent_stars']
        title = href[1:].replace('/', ' / ')
        return '1. [{}]({})\n    - {}\n    - language: **{}** &nbsp;&nbsp; stars: **{}** &nbsp;&nbsp; folks: **{}**  &nbsp;&nbsp; `{}`\n'.format(title, url, description, language, stars, folks, recent_stars)

    dailyMd = '暂无数据'
    if daily:
        dailyMd = '\n'.join([li(item) for item in daily])

    weeklyMd = '暂无数据'
    if weekly:
        weeklyMd = '\n'.join([li(item) for item in weekly])

    monthlyMd = '暂无数据'
    if monthly:
        monthlyMd = '\n'.join([li(item) for item in monthly])

    readme = ''
    file = os.path.join('template', 'archive.md')
    with open(file) as f:
        readme = f.read()

    readme = readme.replace("{updateTime}", util.current_time())
    readme = readme.replace("{dailyTrending}", dailyMd)
    readme = readme.replace("{weeklyTrending}", weeklyMd)
    readme = readme.replace("{monthlyTrending}", monthlyMd)

    return readme


def generateReadme(daily, weekly, monthly):
    """生成今日readme
    """
    def li(item):
        href = item['href']
        url = item['url']
        description = item['description']
        language = item['language']
        stars = item['stars']
        folks = item['folks']
        recent_stars = item['recent_stars']
        title = href[1:].replace('/', ' / ')
        return '1. [{}]({})\n    - {}\n    - language: **{}** &nbsp;&nbsp; stars: **{}** &nbsp;&nbsp; folks: **{}**  &nbsp;&nbsp; `{}`\n'.format(title, url, description, language, stars, folks, recent_stars)

    dailyMd = '暂无数据'
    if daily:
        dailyMd = '\n'.join([li(item) for item in daily])

    weeklyMd = '暂无数据'
    if weekly:
        weeklyMd = '\n'.join([li(item) for item in weekly])

    monthlyMd = '暂无数据'
    if monthly:
        monthlyMd = '\n'.join([li(item) for item in monthly])

    readme = ''
    file = os.path.join('template', 'README.md')
    with open(file) as f:
        readme = f.read()

    readme = readme.replace("{updateTime}", util.current_time())
    readme = readme.replace("{dailyTrending}", dailyMd)
    readme = readme.replace("{weeklyTrending}", weeklyMd)
    readme = readme.replace("{monthlyTrending}", monthlyMd)

    return readme


def handleReadme(md):
    logger.debug('today md:%s', md)
    util.write_text('README.md', md)


def handleArchiveMd(md):
    logger.debug('archive md:%s', md)
    name = '{}.md'.format(util.current_date())
    file = os.path.join('archives', name)
    util.write_text(file, md)


def run():
    github = GitHub()
    # 今日趋势
    daily, resp = github.get_trending_repository(Since.daily)
    # 最近一周趋势
    weekly, resp = github.get_trending_repository(Since.weekly)
    # 最近一个月趋势
    monthly, resp = github.get_trending_repository(Since.monthly)

    # 最新数据
    readme = generateReadme(daily, weekly, monthly)
    handleReadme(readme)
    # 归档
    archiveMd = generateArchiveMd(daily, weekly, monthly)
    handleArchiveMd(archiveMd)


if __name__ == "__main__":
    run()
