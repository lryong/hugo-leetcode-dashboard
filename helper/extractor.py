import os
import time
import concurrent.futures
from .templates import *
from .constants import *


class Extractor:
    '''
    高速并发导出数据类
    '''
    def __init__(self, output_dir, author):
        self.output_dir = output_dir
        self.author = author

    def extractInfo(self, info, datas):
        '''导出 LeetCode README 文件'''
        # 当前时间
        cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        readme_cn_path = os.path.join(self.output_dir, 'leetcode.md')
        with open(readme_cn_path, 'w', encoding='utf-8') as f:
            f.write(
                TEMPLATE_README_CN.format(
                    user_name=info.user_name,
                    num_solved=info.num_solved,
                    num_total=info.num_total,
                    ac_easy=info.ac_easy,
                    ac_medium=info.ac_medium,
                    ac_hard=info.ac_hard,
                    time=cur_time))
            solutions = []
            for i, data in enumerate(datas):
                solutions.append('[{0}](../problemset/{1}/{1}.{2})'.format(
                    data["language"], data["title_slug"],
                    LANGS[data["lang"]]["ext"]))
                title = '[{}](../problemset/{}/readme)'.format(
                    data["title_cn"], data["title_slug"])
                # 判断同一问题是否有多个解
                if i == len(datas) - 1 or datas[i]['title_en'] != datas[
                        i + 1]['title_en']:
                    f.write(
                        TEMPLATE_README_APPEND.format(
                            frontend_id=data['frontend_id'],
                            title=title,
                            paid_only=data['paid_only'],
                            is_favor=data['is_favor'],
                            solutions='、'.join(solutions),
                            ac_rate=data['ac_rate'],
                            difficulty=DIFFICULTY_CN[data['difficulty']],
                            tags=data['tags_cn'].replace('- ', '').replace(
                                '\n', '、')))
                    solutions = []
        print(f'{os.path.abspath(readme_cn_path)} done!')
        readme_en_path = os.path.join(self.output_dir, 'leetcode_en.md')
        with open(readme_en_path, 'w', encoding='utf-8') as f:
            f.write(
                TEMPLATE_README_EN.format(
                    user_name=info.user_name,
                    num_solved=info.num_solved,
                    num_total=info.num_total,
                    ac_easy=info.ac_easy,
                    ac_medium=info.ac_medium,
                    ac_hard=info.ac_hard,
                    time=cur_time))
            solutions = []
            for i, data in enumerate(datas):
                solutions.append('[{0}](../problemset/{1}/{1}.{2})'.format(
                    data["language"], data["title_slug"],
                    LANGS[data["lang"]]["ext"]))
                title = '[{}](../problemset/{}/readme_en)'.format(
                    data["title_en"], data["title_slug"])
                if i == len(datas) - 1 or datas[i]['title_en'] != datas[
                        i + 1]['title_en']:
                    f.write(
                        TEMPLATE_README_APPEND.format(
                            frontend_id=data['frontend_id'],
                            title=title,
                            paid_only=data['paid_only'],
                            is_favor=data['is_favor'],
                            solutions=', '.join(solutions),
                            ac_rate=data['ac_rate'],
                            difficulty=DIFFICULTY_EN[data['difficulty']],
                            tags=data['tags_en'].replace('- ', '').replace(
                                '\n', ', ')))
                    solutions = []
        print(f'{os.path.abspath(readme_en_path)} done!')

    def __extractDesc(self, data):
        if data['d_stored'] == 1:
            return
        folder_path = os.path.join(self.output_dir, 'problemset',
                                   data['title_slug'])
        if not os.path.exists(folder_path):
            # 创建问题文件夹
            os.makedirs(folder_path, exist_ok=True)
        readme_cn_path = os.path.join(folder_path, 'readme.md')
        title_cn = '[{}. {}]({})'.format(
            data['frontend_id'], data['title_cn'],
            PROBLEM_FORMAT.format(data['title_slug']))
        with open(readme_cn_path, 'w', encoding='utf-8') as f:
            f.write(
                TEMPLATE_DESC_CN.format(
                    title_cn=title_cn,
                    content_cn=data['content_cn'],
                    tags_cn=data['tags_cn'],
                    similar_questions_cn=data['similar_questions_cn']))
        print(f'{os.path.abspath(readme_cn_path)} done!')

        readme_en_path = os.path.join(folder_path, 'readme_en.md')
        title_en = '[{}. {}]({})'.format(
            data['frontend_id'], data['title_en'],
            PROBLEM_FORMAT.format(data['title_slug']))
        with open(readme_en_path, 'w', encoding='utf-8') as f:
            f.write(
                TEMPLATE_DESC_EN.format(
                    title_en=title_en,
                    content_en=data['content_en'],
                    tags_en=data['tags_en'],
                    similar_questions_en=data['similar_questions_en']))
        print(f'{os.path.abspath(readme_en_path)} done!')

    def extractDesc(self, datas):
        '''导出问题描述'''
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            # futures = {executor.submit(self.__extractDesc, data): data for data in datas}
            # for future in concurrent.futures.as_completed(futures):
            #     data = futures[future]
            for _ in executor.map(self.__extractDesc, datas):
                pass

    def __extractCode(self, data):
        if data['s_stored'] == 1:
            return
        folder_path = os.path.join(self.output_dir, 'problemset',
                                   data['title_slug'])
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        code_path = os.path.join(
            folder_path, f'{data["title_slug"]}.{LANGS[data["lang"]]["ext"]}.md')
        with open(code_path, 'w', encoding='utf-8') as f:
            f.write(
                TEMPLATE_CODE.format(
                    style=LANGS[data['lang']]['style'],
                    title_cn=data['title_cn'],
                    title_en=data['title_en'],
                    author=self.author,
                    timestamp=data['timestamp'],
                    runtime=data['runtime'],
                    memory=data['memory'],
                    ext=LANGS[data['lang']]['ext'],
                    code=data['code']))
        print(f'{os.path.abspath(code_path)} done!')

    def extractCode(self, datas):
        '''导出代码'''
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            for _ in executor.map(self.__extractCode, datas):
                pass
