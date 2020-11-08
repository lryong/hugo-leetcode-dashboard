'''
@Author: KivenChen
@Date: 2019-04-22
@LastEditTime: 2019-05-23
'''

# LeetCode 相关链接
LEETCODE = "https://leetcode-cn.com"
GRAPHQL = LEETCODE + "/graphql"
LOGIN = LEETCODE + "/accounts/login/"
PROBLEMS = LEETCODE + "/api/problems/all/"
SUBMISSIONS_FORMAT = LEETCODE + "/api/submissions/?offset={}&limit=20"
CODE_FORMAT = LEETCODE + "/submissions/latest/?qid={}&lang={}"
TAG_FORMAT = LEETCODE + "/tag/{}"
PROBLEM_FORMAT = LEETCODE + "/problems/{}/"

HEADERS = {
    'Origin':
    LEETCODE,
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
}

DIFFICULTY_CN = ['', '简单', '中等', '困难']
DIFFICULTY_EN = ['', 'easy', 'medium', 'hard']

LANGS = {
    'bash': {
        'lang': 'Shell',
        'ext': 'sh',
        'style': '#'
    },
    'c': {
        'lang': 'C',
        'ext': 'c',
        'style': '//'
    },
    'cpp': {
        'lang': 'C++',
        'ext': 'cpp',
        'style': '//'
    },
    'csharp': {
        'lang': 'C#',
        'ext': 'cs',
        'style': '//'
    },
    'golang': {
        'lang': 'Go',
        'ext': 'go',
        'style': '//'
    },
    'java': {
        'lang': 'Java',
        'ext': 'java',
        'style': '//'
    },
    'javascript': {
        'lang': 'JavaScript',
        'ext': 'js',
        'style': '//'
    },
    'kotlin': {
        'lang': 'Kotlin',
        'ext': 'kt',
        'style': '//'
    },
    'mysql': {
        'lang': 'SQL',
        'ext': 'sql',
        'style': '--'
    },
    'python': {
        'lang': 'Python',
        'ext': 'py',
        'style': '#'
    },
    'python3': {
        'lang': 'Python3',
        'ext': 'py',
        'style': '#'
    },
    'ruby': {
        'lang': 'Ruby',
        'ext': 'rb',
        'style': '#'
    },
    'rust': {
        'lang': 'Rust',
        'ext': 'rs',
        'style': '//'
    },
    'scala': {
        'lang': 'Scala',
        'ext': 'scala',
        'style': '//'
    },
    'swift': {
        'lang': 'Swift',
        'ext': 'swift',
        'style': '//'
    }
}
