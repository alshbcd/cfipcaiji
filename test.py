from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import os

# 目标URL
urls = ['https://ipdb.030101.xyz/bestcfv4/']
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

# 初始化浏览器（需安装 Chrome 浏览器）
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

if os.path.exists('ip.txt'):
    os.remove('ip.txt')

with open('ip.txt', 'w') as file:
    for url in urls:
        driver.get(url)  # 加载页面并执行JS
        # 等待动态内容加载（根据实际情况调整等待时间）
        driver.implicitly_wait(10)  # 隐式等待10秒
        # 获取加载后的页面源码
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # 查找所有tr标签（此时包含动态生成的内容）
        elements = soup.find_all('tr')
        print(f"找到 {len(elements)} 个tr标签")  # 验证是否获取到
        
        # 提取IP
        for element in elements:
            element_text = element.get_text()
            ip_matches = re.findall(ip_pattern, element_text)
            for ip in ip_matches:
                # 简单验证IP有效性
                if all(0 <= int(part) <= 255 for part in ip.split('.')):
                    file.write(ip + '\n')

driver.quit()  # 关闭浏览器
print('IP地址已保存到ip.txt文件中。')
