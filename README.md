## hugo-leetcode-dashboard

✨ 一个 LeetCode 答题看板的生成插件， 支持一键部署到 Hugo 站点。 **完整记录刷题心路历程** ✨

[在线预览 Demo](https://blog.herbert.top/leetcode/)

## Screenshots

![leetcode-dashboard](https://raw.githubusercontent.com/lryong/hugo-leetcode-dashboard/master/imgs/leetcode_dashboard.png)

## Installation

1. 下载 Repo 到本地：

   ```shell
   git  clone https://github.com/lryong/hugo-leetcode-dashboard
   ```

2. 安装依赖： 本项目需要用到 `requests` 和 `aiohttp` 包， 通过 pip 安装即可。

3. 更新仓库根目录下的 `config.json`文件：

   ```json
   {
     "username": "leetcode-cn@leetcode",
     "password": "leetcode",
     "outputDir": "../LeetCode"
   }
   ```

   username 是 LeetCode-cn 账号， password 是对应密码。
   outputDir 为 dashboard 生成路径。 (注： 这里配置为 hugo 站点的文档路径， 如：/Users/XXX/my_blogs/content)

4. 因为 Hugo 默认只支持 _markdown_ 文档, 在个人网站根目录下新建 `layouts/shortcodes/rawhtml.html`文件，以支持原生 HTML：

   ```css
   <!-- raw html -->
   {{.Inner}}
   ```

   (_具体参考[这里](https://anaulin.org/blog/hugo-raw-html-shortcode/)_)

5. 最后**一键部署到 Hugo 站点**， 参考以下命令：

   ```shell
   echo "2" | python3 run.py && cp imgs/leetcode-logo.png /Users/XXX/my_blogs/static/images
   ```

## Directory Structure

通过 `hugo-leetcode-dashboard` 生成的文件目录如下：

```shell
.
├── leetcode.md # 中文看板入口
├── leetcode_en.md #英文看板入口
├── problemset # 答题集
│   ├── 3sum #题目
│   │   ├── 3sum.go #题解原文件
│   │   ├── 3sum.go.md # 题解
│   │   ├── readme.md # 中文题目描述
│   │   └── readme_en.md # 英文题目描述
```

把以上文件放到 hugo 文章根目录即可

## Features

1. 答题情况总览（完成的题目和整体进程）
2. LeetCode 个人答题看板， 包括展示 题号，题目，收藏标签，解答的语言， 题目通过率， 难度和题目类型
3. 展示 LeetCode 问题描述
4. 展示 LeetCode 个人的解题方案

## License

Released under the [MIT](https://github.com/lryong/hugo-leetcode-dashboard/blob/master/LICENSE) License.

## Acknowledgements

- [LeetCode_Helper](https://github.com/KivenCkl/LeetCode_Helper)
