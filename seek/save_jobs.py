from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# 搜索关键字
KeyWord = 'DevOps'

# Chromedriver路径
chrome_driver_path = r'/Users/lxdluser01/chromedriver-mac-x64/chromedriver'
# Chrome浏览器路径
chrome_binary_path = r'/Users/lxdluser01/chrome-mac-x64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing'

# 创建Chrome浏览器选项
chrome_options = Options()
chrome_options.binary_location = chrome_binary_path
service = Service(chrome_driver_path)
chrome_options.add_argument("--headless")  # 无头模式
chrome_options.add_argument("--disable-gpu")  # 禁用GPU加速
chrome_options.add_argument("--window-size=1920x1080")  # 设置窗口大小
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")  # 设置用户代理
# 启动Chrome浏览器
driver = webdriver.Chrome(service=service, options=chrome_options)

# 定义csv文件名
CSV_FILE = KeyWord + '_' + 'jobs_inAUS' + '_' + datetime.now().strftime("%Y-%m-%d-%H-%M")+".csv"

# 从第一页开始遍历
page_num = 1
while True:
    # 拼接url
    url = 'https://www.seek.com.au/' + KeyWord + '-jobs/in-All-Australia' + '?page=' + str(page_num)
    print("Page Number: " + str(page_num))
    driver.get(url)
    driver.implicitly_wait(10)
    rendered_page_source = driver.page_source
    if "No matching search results" in rendered_page_source:
        break
    # 获取渲染后的页面内容
    rendered_page_source = driver.page_source
    soup = BeautifulSoup(rendered_page_source, 'html.parser')

    # 找出所有data-card-type为"JobCard"的元素
    job_cards = soup.find_all('article', attrs={'data-card-type': 'JobCard'})
    # 创建CSV文件
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # 如果文件不存在或为空，写入表头
        if file.tell() == 0:
            writer.writerow(["Job Title", "Company", "Location", "Salary", "Write Time", "Release Time"])

        # 遍历所有的job cards
        for job_card in job_cards:
            # 找出data-automation分别为jobTitle、jobCompany、jobLocation、jobSalary的元素
            job_title = job_card.find(attrs={'data-automation': 'jobTitle'}).text if job_card.find(attrs={'data-automation': 'jobTitle'}) else "N/A"
            job_company = job_card.find(attrs={'data-automation': 'jobCompany'}).text if job_card.find(attrs={'data-automation': 'jobCompany'}) else "N/A"
            job_location = job_card.find(attrs={'data-automation': 'jobLocation'}).text if job_card.find(attrs={'data-automation': 'jobLocation'}) else "N/A"
            job_salary = job_card.find(attrs={'data-automation': 'jobSalary'}).text if job_card.find(attrs={'data-automation': 'jobSalary'}) else "N/A"

            # 获取当前时间作为写入时间
            write_time = datetime.now().strftime("%Y/%m/%d %H:%M")

            # 获取发布时间
            job_listing_date = job_card.find(attrs={'data-automation': 'jobListingDate'})
            release_time = job_listing_date.text if job_listing_date else "Unknown"
            
            # 写入一行数据
            writer.writerow([job_title, job_company, job_location, job_salary, write_time, release_time])
    page_num += 1
    
# 关闭浏览器
driver.quit()
