## hugo-leetcode-dashboard

一个 LeetCode 答题看板的生成插件， 支持一键部署到 Hugo 站点。 **完整记录刷题的心路历程 ：）**

[在线预览 Demo](http://blog.herbert.top/leetcode/)

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
       "username": "leetcode-cn@leetcode", // LeetCode-cn 账号
       "password": "leetcode", // 对应的密码
       "outputDir": "../LeetCode" // dashboard 生成路径。 注意： 这里配置为 hugo 站点的文档路径， 如：/Users/XXX/my_blogs/content
   }
   ```

4. 可以根据需求修改 `templates.py` 定义的 dashboard 模板。

5. 因为 Hugo 默认只支持 *markdown* 文档, 可以在站点，新建 `layouts/shortcodes/rawhtml.html`文件，添加以下配置即可：

   ```css
   <!-- raw html -->
   {{.Inner}}
   ```

   (*具体可以参考[这里](https://anaulin.org/blog/hugo-raw-html-shortcode/)*)

6. 最后**一键部署到 Hugo 站点**， 参考以下命令：

   ```shell
   echo "2" | python3 run.py && cp imgs/leetcode-logo.png /Users/XXX/my_blogs/static/images
   ```

## Features

1. 答题情况总览（完成的题目和整体进程）
2. LeetCode  个人答题看板， 包括展示 题号，题目，收藏标签，解答的语言， 题目通过率， 难度和题目类型
3. 直接展示 LeetCode 问题描述
4. 直接展示 LeetCode 个人的答题方案

## License

Released under the [MIT](https://github.com/olOwOlo/hugo-theme-even/blob/master/LICENSE.md) License.

## d

- [LeetCode_Helper](https://github.com/KivenCkl/LeetCode_Helper)
