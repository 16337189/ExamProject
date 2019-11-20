## 毕业设计 ##
选题阶段
***
### 作品推荐网站 ###
#### 功能 ####
为作品建立帖子进行介绍和评价，对作品就某一问题发起讨论，帮助用户找到合适的作品。
#### 原因 ####
随着越来越多作品（小说，电视剧，电影，游戏等等）的出现，人们搜索作品能得到的结果也越来越庞大。
但人们找到自己喜欢的作品得难度也随之增大。
我想搭建一个网站，通过增加人们之间的互动（如作者和读者都可以添加和点赞的标签系统，就作品某一问题相互讨论的系统，通过描述寻找合适作品的提问系统），使人们更容易找到合适心意的作品。
#### 项目模块 ####
* **用户模块**：进入网站的人，可以随意看作品和讨论的问题。但要注册登录后，用户才能写新的作品推荐，发表删除对作品的评论，评分，贴标签，发起问题讨论，收藏查看喜爱的作品，重新编辑自己的作品介绍。
* **作品模块**：作品的介绍包括名称，载体，制作时间，制作地区，语言，标签，评分，作者对作品的看法，作者对作品德展示（图片）。
* **评论模块**：每一篇作品介绍下面是评论部分，作者可以发表感想之类的，进一步推荐作品，读者也可以发表自己的感想或者发出一些对作品的提问。
* **分数模块**：每一篇作品都会有一个总评分和一些项目评分，作者和读者都可以对作品进行评分，还可以选择评分的方式（平均数，中位数，众数）。总评分是必定存在，而项目评分是作者设置的，因为不同载体的作品评分项目会有不同。
* **标签模块**：作者和读者都可以贴上标签和给已存在的标签点赞，可以通过标签来筛选和搜索作品。标签会定期清除，排除那些低赞且创造时间久远的标签，这样更容易分类正确。另外，标签可以进行相似推荐，如用点赞数前五的标签，进行相似度比较，选差距最小的几部作品。
* **搜索模块**：用户可以搜索名称查找作品，按载体，制作时间，制作地区，语言，标签等分类搜索作品，也可以按总评分，评论数排序。
* **讨论模块**：用户可以就某一作品以某一问题发起讨论，这些讨论会以随机出现在首页，让人们通过问题来找到新的感兴趣的作品。
* **收藏模块**：用户可以收藏某一作品，当有人发起关于该作品的讨论时会有通知，让用户参与讨论。
* **提问模块**：用户可以对想要找的作品进行描述，由其他用户帮忙回答。
#### 进度安排 ####
* 12月：网站基本框架，用户模块，作品模块，评论模块
* 1月：分数模块，标签模块，搜索模块
* 2月：讨论模块，收藏模块，提问模块
* 3月：写论文