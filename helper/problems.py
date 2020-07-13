# -*- coding: utf-8 -*-
import os
import time
import sqlite3
import requests
import asyncio
import aiohttp
from .config import Config
from .login import Login
from .extractor import Extractor
from .utils import handle_tasks
from .node import InfoNode, ProblemInfoNode, ProblemDescNode, SubmissionNode
from .constants import PROBLEMS, HEADERS, GRAPHQL, SUBMISSIONS_FORMAT


class Problems:
    '''核心逻辑'''

    def __init__(self):
        self.config = Config()
        self.login = Login(self.config.username, self.config.password)
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
            'query':
            '''
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
            'operationName':
            'questionData',
            'variables': {
                'titleSlug': title_slug
            }
        }
        async with aiohttp.ClientSession(cookies=self.__cookies) as session:
            async with session.post(
                    GRAPHQL, json=payload, headers=HEADERS) as resp:
                return await resp.json()

    def storeProblemsDesc(self):
        '''存储 AC 问题描述信息'''
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT title_slug FROM problem WHERE status == 'ac'")
        res = c.fetchall()
        if not res:
            return
        loop = asyncio.get_event_loop()
        problems_list = handle_tasks(loop, self.__getProblemDesc,
                                     [t[0] for t in res])
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

    def __getSubmissions(self):
        result = []
        offset = 0
        while True:
            resp = requests.get(
                SUBMISSIONS_FORMAT.format(offset),
                headers=HEADERS,
                cookies=self.__cookies)
            content = resp.json()
            if "submissions_dump" not in content:
                time.sleep(2)
                continue
            result.extend(content['submissions_dump'])
            # 判断是否还有下一页
            if not content['has_next']:
                return result
            offset += 20
            time.sleep(1)

    def storeSubmissions(self):
        '''存储提交的代码信息'''
        submissions_list = self.__getSubmissions()
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS submission (
                submission_id INTEGER,
                code TEXT,
                lang TEXT,
                language TEXT,
                memory TEXT,
                runtime TEXT,
                timestamp TEXT,
                title_cn TEXT,
                s_stored INTEGER DEFAULT 0,
                PRIMARY KEY(submission_id)
            )
            ''')
        for submission in submissions_list:
            s = SubmissionNode(submission)
            if s.status_display == 'Accepted':
                c.execute(
                    '''
                    INSERT OR IGNORE INTO submission (
                        submission_id, code, lang, language, memory, runtime, timestamp, title_cn
                    )
                    VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?
                    )
                    ''', (s.submission_id, s.code, s.lang, s.language,
                          s.memory, s.runtime, s.timestamp, s.title_cn))
        conn.commit()
        conn.close()

    def updateSubmissions(self):
        '''更新处理后的 submission 数据库'''
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('UPDATE submission SET s_stored=1')
        conn.commit()
        conn.close()

    def update(self):
        '''增量式更新数据'''
        output_dir = self.config.outputDir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        extractor = Extractor(output_dir, self.config.username)
        self.updateProblemsInfo()
        self.storeProblemsDesc()
        self.storeSubmissions()
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
            ON d.title_cn=s.title_cn
            WHERE (d.d_stored=0 OR s.s_stored=0) AND s.submission_id IN (
                SELECT MAX(submission_id)
                FROM submission
                GROUP BY title_cn, language
            )
            ORDER BY p.id DESC
            ''')
        datas = c.fetchall()
        if datas:
            extractor.extractDesc(datas)
            self.updateProblemsDesc()
            extractor.extractCode(datas)
            self.updateSubmissions()
        c.execute('''
            SELECT *
            FROM description d
            JOIN problem p
            ON p.id=d.id
            JOIN submission s
            ON d.title_cn=s.title_cn
            WHERE s.submission_id IN (
                SELECT MAX(submission_id)
                FROM submission
                GROUP BY title_cn, language
            )
            ORDER BY p.id DESC
            ''')
        datas = c.fetchall()
        extractor.extractInfo(self.info, datas)
        print('数据已更新！')
        conn.close()

    def rebuild(self):
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
        self.update()
