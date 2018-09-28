from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from lxml import etree
import time
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def login():
    try:
        driver = webdriver.Chrome()
        driver.get("https://qzone.qq.com/")
        driver.refresh()
        #设置隐性等待
        driver.implicitly_wait(5)
        #注意，frame标签会影响定位，需要切进该标签。
        driver.switch_to.frame("login_frame")
        driver.find_element_by_xpath("//a[@id='switcher_plogin']").click()
        #以下几行模拟qqd登陆
        driver.find_element_by_id("u").clear()
        driver.find_element_by_id("u").send_keys("qq号码")
        driver.find_element_by_id("p").clear()
        driver.find_element_by_id("p").send_keys("qq密码")
        driver.find_element_by_id("login_button").click()
        time.sleep(5)
        #开始切入到frame标签内，现在需要切回主文档
        driver.switch_to.default_content()
        driver.get("https://user.qzone.qq.com/好友的qq号/311")
        get_data(driver)
    except TimeoutException:
        login()

def get_data(driver):
    num = 0
    while True:
        print("正在爬取第"+str(num+1)+"页")
        #selenium模拟下拉到底
        js = "var q=document.documentElement.scrollTop=100000"
        driver.execute_script(js)
        time.sleep(4)
        driver.switch_to.frame("app_canvas_frame")
        try:
            #获取所有说说
            tree = etree.HTML(driver.page_source)
            li_list = tree.xpath("//ol[@id='msgList']/li")
            for li in li_list:
                content = li.xpath(".//div[@class='bd']/pre/text()")[0]
                # print(content)
                #存入txt文件中
                with open("test.txt","a") as file:
                    file.write(content+"\n")
        except:
            print("error")
        #如果找不到该id,返回-1，终止循环
        if driver.page_source.find("pager_next_"+str(num)) == -1:
            break
        #模拟点击下一页
        driver.find_element_by_id("pager_next_"+str(num)).click()
        num += 1
        driver.switch_to.parent_frame()
    print("所有均以爬取完！")
    driver.close()

def create_word_cloud():
    #打开存储说说的文件
    text = open("test.txt","r").read()
    #设置背景图片
    color_mask = plt.imread("huge.jpg")
    cloud = WordCloud(
        background_color="white",
        max_words=2000,
        mask=color_mask,
        #设置字体
        font_path="STXINGKA.TTF",
        height=1200,
        width=2000,
        max_font_size=100,
        random_state=30,
    )
    #生成词云
    word_cloud = cloud.generate(text)
    word_cloud.to_file('huge.png')
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.show()

if __name__ == '__main__':
    login()
    create_word_cloud()




