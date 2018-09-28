## 利用selenium爬取qq空间并生成词云
#### 主要模块 `selenium`,`lxml`,`wordcloud`,`matplotlib`
#### 步骤如下：
- 先用slenium模拟登陆qq空间（注意：iframe标签内的内容不能直接提取，需要switch_to.frame()先切入进去）
- selenium模拟下拉到底的动作，获取第一个网页的page_source
- selenium模拟不断点击下一页的操作，当到最后一页，源码上找不到我们需要的标签id,退出循环
- 利用wordcloud,matplolib生成词云并保存为图片即可。

