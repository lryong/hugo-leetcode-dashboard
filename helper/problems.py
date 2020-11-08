'''
@Author: KivenChen
@Date: 2019-04-23
@LastEditTime: 2019-05-23
'''
import os
import sqlite3
import requests
import asyncio
import aiohttp
from .config import config
from .login import Login
from .extractor import Extractor
from .utils import handle_tasks
from .node import InfoNode, ProblemInfoNode, ProblemDescNode, SubmissionNode
from .constants import PROBLEMS, HEADERS, GRAPHQL, CODE_FORMAT


class Problems:
    '''核心逻辑'''
    def __init__(self):
        self.login = Login(config.username, config.password)
        self.__db_dir = os.path.abspath(os.path.join(__file__, "../..", "db"))
        if not os.path.exists(self.__db_dir):
            os.makedirs(self.__db_dir)
        self.db_path = os.path.join(self.__db_dir, "leetcode.db")
        self.__cookies = self.login.cookies
        self.problems_json = self.__getProblemsJson()

    def __getProblemsJson(self):
        resp = requests.get(PROBLEMS, headers=HEADERS, cookies=self.__cookies)
        if resp.status_code == 200:
            return resp.json()

    @property
    def info(self):
        '''获取用户基本信息'''
        return InfoNode(self.problems_json)

    def __dict_factory(self, cursor, row):
        '''修改 SQLite 数据呈现方式'''
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def updateProblemsInfo(self):
        '''更新问题基本信息'''
        problems_list = self.problems_json.get('stat_status_pairs')
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS problem (
                id INTEGER,
                frontend_id TEXT,
                title_en TEXT,
                title_slug TEXT,
                difficulty INTEGER,
                paid_only INTEGER,
                is_favor INTEGER,
                status TEXT,
                total_acs INTEGER,
                total_submitted INTEGER,
                ac_rate TEXT,
                PRIMARY KEY(id)
            )
            ''')
        c.execute('DELETE FROM problem')
        for problem in problems_list:
            p = ProblemInfoNode(problem)
            c.execute(
                '''
                INSERT INTO problem (
                    id, frontend_id, title_en, title_slug, difficulty, paid_only, is_favor, status, total_acs, total_submitted, ac_rate
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
                ''', (p.id, p.frontend_id, p.title_en, p.title_slug,
                      p.difficulty, p.paid_only, p.is_favor, p.status,
                      p.total_acs, p.total_submitted, p.ac_rate))
        conn.commit()
        conn.close()

    async def __getProblemDesc(self, title_slug):
        payload = {
            'query': '''
            query questionData($titleSlug: String!) {
                question(titleSlug: $titleSlug) {
                    questionId
                    content
                    translatedTitle
                    translatedContent
                    similarQuestions
                    topicTags {
                        name
                        slug
                        translatedName
                    }
                    hints
                }
            }
            ''',
            'operationName': 'questionData',
            'variables': {
                'titleSlug': title_slug
            }
        }
        async with aiohttp.ClientSession(cookies=self.__cookies) as session:
            async with session.post(GRAPHQL, json=payload,
                                    headers=HEADERS) as resp:
                return await resp.json()

    async def storeProblemsDesc(self):
        '''存储 AC 问题描述信息'''
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT title_slug FROM problem WHERE status == 'ac'")
        res = c.fetchall()
        if not res:
            return
        loop = asyncio.get_event_loop()
        problems_list = await handle_tasks(
            loop, self.__getProblemDesc, [dict(title_slug=t[0]) for t in res])
        c.execute('''
            CREATE TABLE IF NOT EXISTS description (
                id INTEGER,
                content_en TEXT,
                title_cn TEXT,
                content_cn TEXT,
                similar_questions_cn TEXT,
                similar_questions_en TEXT,
                tags_cn TEXT,
                tags_en TEXT,
                d_stored INTEGER DEFAULT 0,
                PRIMARY KEY(id)
            )
            ''')
        for problem in problems_list:
            p = ProblemDescNode(problem)
            c.execute(
                '''
                INSERT OR IGNORE INTO description (
                    id, content_en, title_cn, content_cn, similar_questions_cn, similar_questions_en, tags_cn, tags_en
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?
                )
                ''', (p.id, p.content_en, p.title_cn, p.content_cn,
                      p.similar_questions_cn, p.similar_questions_en,
                      p.tags_cn, p.tags_en))
        conn.commit()
        conn.close()

    def updateProblemsDesc(self):
        '''更新处理后的 description 数据库'''
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('UPDATE description SET d_stored=1')
        conn.commit()
        conn.close()

    async def __getSubmissions(self, title_slug, offset=0, limit=500):
        payload = {
            'query': '''
            query submissions($offset: Int!, $limit: Int!, $lastKey: String, $questionSlug: String!) {
                submissionList(offset: $offset, limit: $limit, lastKey: $lastKey, questionSlug: $questionSlug) {
                    lastKey
                    hasNext
                    submissions {
                        id
                        statusDisplay
                        lang
                        runtime
                        timestamp
                        url
                        isPending
                        memory
                        __typename
                    }
                __typename
                }
            }
            ''',
            'operationName': 'submissions',
            'variables': {
                'limit': limit,
                'offset': offset,
                'questionSlug': title_slug
            }
        }
        async with aiohttp.ClientSession(cookies=self.__cookies) as session:
            async with session.post(GRAPHQL, json=payload,
                                    headers=HEADERS) as resp:
                return await resp.json(), title_slug

    async def __getCode(self, qid, lang):
        url = CODE_FORMAT.format(qid, lang)
        async with aiohttp.ClientSession(cookies=self.__cookies) as session:
            async with session.get(url, headers=HEADERS) as resp:
                return await resp.json(), qid, lang

    async def storeSubmissions(self):
        '''存储提交的代码信息'''
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT title_slug FROM problem WHERE status == 'ac'")
        res = c.fetchall()
        if not res:
            return
        loop = asyncio.get_event_loop()
        submissions_list = await handle_tasks(
            loop, self.__getSubmissions, [dict(title_slug=t[0]) for t in res])
        data = []
        for submissions, title_slug in submissions_list:
            dic = set()
            for submission in submissions['data']['submissionList'][
                    'submissions']:
                status = submission['statusDisplay']
                key = submission['lang']
                if status == 'Accepted' and key not in dic:
                    data.append(submission)
                    data[-1]['title_slug'] = title_slug
                    dic.add(key)
        c.execute('''
            CREATE TABLE IF NOT EXISTS submission (
                submission_id INTEGER,
                lang TEXT,
                language TEXT,
                memory TEXT,
                runtime TEXT,
                timestamp TEXT,
                title_slug TEXT,
                s_stored INTEGER DEFAULT 0,
                PRIMARY KEY(submission_id)
            )
            ''')
        for submission in data:
            s = SubmissionNode(submission)
            c.execute(
                '''
                INSERT OR IGNORE INTO submission (
                    submission_id, lang, language, memory, runtime, timestamp, title_slug
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?
                )
                ''', (s.submission_id, s.lang, s.language, s.memory, s.runtime,
                      s.timestamp, s.title_slug))
        conn.commit()
        conn.close()

    async def storeCodes(self):
        '''存储提交的代码'''
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            "SELECT p.id, lang FROM submission s LEFT JOIN problem p ON s.title_slug=p.title_slug"
        )
        res = c.fetchall()
        if not res:
            return
        loop = asyncio.get_event_loop()
        codes_list = await handle_tasks(
            loop, self.__getCode, [dict(qid=t[0], lang=t[1]) for t in res])
        try:
            c.execute("ALTER TABLE submission ADD COLUMN code TEXT")
        except sqlite3.OperationalError:
            pass
        for code, qid, lang in codes_list:
            c.execute(
                """
                UPDATE submission SET code = ?
                WHERE title_slug=(SELECT title_slug
                                FROM problem
                                WHERE id=?)
                AND lang=?""", (code.get("code", ""), qid, lang))
        conn.commit()
        conn.close()

    def updateSubmissions(self):
        '''更新处理后的 submission 数据库'''
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('UPDATE submission SET s_stored=1')
        conn.commit()
        conn.close()

    async def update(self):
        '''增量式更新数据'''
        output_dir = config.outputDir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        extractor = Extractor(output_dir, config.username)
        self.updateProblemsInfo()
        await self.storeProblemsDesc()
        await self.storeSubmissions()
        await self.storeCodes()
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = self.__dict_factory
        c = conn.cursor()
        # 获取新的数据
        c.execute('''
            SELECT *
            FROM description d
            JOIN problem p
            ON p.id=d.id
            JOIN submission s
            ON p.title_slug=s.title_slug
            WHERE (d.d_stored=0 OR s.s_stored=0)
            ORDER BY p.id DESC
            ''')
        datas = c.fetchall()
        if datas:
            extractor.extractDesc(datas)
            self.updateProblemsDesc()
            extractor.extractCode(datas)
            self.updateSubmissions()
            await self.storeCodes()
        c.execute('''
            SELECT *
            FROM description d
            JOIN problem p
            ON p.id=d.id
            JOIN submission s
            ON p.title_slug=s.title_slug
            ORDER BY p.id DESC
            ''')
        datas = c.fetchall()
        extractor.extractInfo(self.info, datas)
        print('数据已更新！')
        conn.close()

    def clearDB(self):
        '''重建数据'''
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            SELECT name
            FROM sqlite_master
            WHERE type="table" AND name="problem"
            ''')
        if c.fetchone():
            # 删除 problem 表
            c.execute('DROP TABLE problem')
        c.execute('''
            SELECT name
            FROM sqlite_master
            WHERE type="table" AND name="description"
            ''')
        if c.fetchone():
            # 删除 description 表
            c.execute('DROP TABLE description')
        c.execute('''
            SELECT name
            FROM sqlite_master
            WHERE type="table" AND name="submission"
            ''')
        if c.fetchone():
            # 删除 submission 表
            c.execute('DROP TABLE submission')
        conn.commit()
        conn.close()
