# 根目录下的 README 英文模板
TEMPLATE_README_EN = '''
---
title: "LeetCode_en"
layout: "leetcode_en"
url: "/leetcode_en/"
author: "Herbert Lu"
---

| English | [简体中文](../leetcode) |

![leetcode-logo](/images/leetcode-logo.png)

{{{{< rawhtml >}}}}
<p align="center">
    <img src="https://img.shields.io/badge/User-{user_name}-blue.svg?" alt="">
    <img src="https://img.shields.io/badge/Solved-{num_solved}/{num_total}-blue.svg?" alt="">
    <img src="https://img.shields.io/badge/Easy-{ac_easy}-green.svg?" alt="">
    <img src="https://img.shields.io/badge/Medium-{ac_medium}-orange.svg?" alt="">
    <img src="https://img.shields.io/badge/Hard-{ac_hard}-red.svg?" alt="">
</p>
<h1 align="center">My LeetCode Solutions</h1>

<p align="center">
    <br>
    <b>Last updated: {time}</b>
    <br>
</p>
{{{{< /rawhtml >}}}}

| # | Title | Solutions | Acceptance | Difficulty | Tags |
|:--:|:-----|:---------:|:----:|:----:|:----|
'''

# 根目录下的 README 中文模板
TEMPLATE_README_CN = '''
---
title: "LeetCode"
layout: "leetcode"
url: "/leetcode/"
menu: "main"
author: "Herbert Lu"
---

| [English](../leetcode_en) | 简体中文 |

![leetcode-logo](/images/leetcode-logo.png)
{{{{< rawhtml >}}}}
<p align="center">
    <img src="https://img.shields.io/badge/用户-{user_name}-blue.svg?" alt="">
    <img src="https://img.shields.io/badge/已解决-{num_solved}/{num_total}-blue.svg?" alt="">
    <img src="https://img.shields.io/badge/简单-{ac_easy}-green.svg?" alt="">
    <img src="https://img.shields.io/badge/中等-{ac_medium}-orange.svg?" alt="">
    <img src="https://img.shields.io/badge/困难-{ac_hard}-red.svg?" alt="">
</p>
<h1 align="center">LeetCode 的解答</h1>

<p align="center">
    <br>
    <b>最近一次更新: {time}</b>
    <br>
</p>
{{{{< /rawhtml >}}}}

| # | 题名 | 解答 | 通过率 | 难度 | 标签 |
|:--:|:-----|:---------:|:----:|:----:|:----|
'''

# 根目录下 README 中的题目概要信息
TEMPLATE_README_APPEND = '|{frontend_id}|{title}{paid_only}{is_favor}|{solutions}|{ac_rate}|{difficulty}|{tags}|\n'

# 题目描述 README 英文模板
TEMPLATE_DESC_EN = '''
---
title: "{title_en}"
categories: ["leetcode_en"]
draft: false
---

| English | [简体中文](../readme) |

# {title_en}

## Description

{{{{< rawhtml >}}}}
{content_en}
{{{{< /rawhtml >}}}}

## Related Topics

{tags_en}

## Similar Questions

{similar_questions_en}
'''

# 题目描述 README 中文模板
TEMPLATE_DESC_CN = '''
---
title: "{title_cn}"
categories: ["leetcode_cn"]
draft: false
---

| [English](../readme_en) | 简体中文 |

# {title_cn}

## 题目描述

{{{{< rawhtml >}}}}
{content_cn}
{{{{< /rawhtml >}}}}

## 相关话题

{tags_cn}

## 相似题目

{similar_questions_cn}
'''

# 题目代码模板
TEMPLATE_CODE = '''
---
title: "{title_cn} ({title_en})"
draft: false
---
```{ext}
{style} @Title: {title_cn} ({title_en})
{style} @Author: {author}
{style} @Date: {timestamp}
{style} @Runtime: {runtime}
{style} @Memory: {memory}
{code}
```
'''
