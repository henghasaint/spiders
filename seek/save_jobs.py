from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

# Chromedriver路径
chrome_driver_path = r'/Users/lxdluser01/chromedriver-mac-x64/chromedriver'
# Chrome浏览器路径
# chrome_binary_path = r'/Users/lxdluser01/chrome-mac-x64/Google Chrome for Testing.app'
chrome_binary_path = r'/Users/lxdluser01/chrome-mac-x64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing'
# chrome_binary_path = r'/Users/lxdluser01/chrome-mac-x64/Google\ Chrome\ for\ Testing.app/Contents/MacOS/'

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

# 打开页面
driver.get('https://www.seek.com.au/DevOps-jobs/in-All-Australia')

# 等待页面加载
driver.implicitly_wait(10)

# 获取渲染后的页面内容
rendered_page_source = driver.page_source
#分割线
print("########################1")
# 将渲染后的页面内容写入到txt文件中
with open('rendered_page.txt', 'w', encoding='utf-8') as file:
    file.write(rendered_page_source)
# 打印渲染后的页面内容
print(rendered_page_source)

#分割线
print("########################2")

# 找出所有包含所需信息的职位列表项
# job_listings = driver.find_elements(By.CSS_SELECTOR, '[data-card-type="JobCard"]')
job_listings = driver.find_elements(By.NAME, 'JobCard')


# 打印job_listings列表
print("########################22")
print(job_listings)

# 创建空的列表来保存职位信息
job_data = []


# 遍历每个职位列表项并提取所需信息
for job_listing in job_listings:
    job_title = job_listing.find_element(By.NAME, 'jobTitle').text.strip()
    job_company = job_listing.find_element(By.NAME, 'jobCompany').text.strip()
    job_location = job_listing.find_element(By.NAME, 'jobLocation').text.strip()
    job_salary = job_listing.find_element(By.NAME, 'jobSalary').text.strip()
    print('jobTitle: ', job_title, ", jobCompany: ", job_company, ", jobLocation: ", job_location ,", jobSalary: ", job_salary)
    # 将职位信息添加到列表中
    job_data.append([job_title, job_company, job_location, job_salary])
    
# 打印job_data列表
print("########################3")
print(job_data)

# 创建DataFrame对象
df = pd.DataFrame(job_data, columns=["Job Title", "Company", "Location", "Salary"])

# 将数据保存到CSV文件
df.to_csv("job_data.csv", index=False)

# 关闭浏览器
driver.quit()
