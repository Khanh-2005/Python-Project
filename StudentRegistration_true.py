from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os

# Cấu hình
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://demoqa.com/automation-practice-form")
wait = WebDriverWait(driver, 5)

# 1. Nhập thông tin cá nhân
driver.find_element(By.ID, "firstName").send_keys("Khanh")
driver.find_element(By.ID, "lastName").send_keys("Ta")
driver.find_element(By.ID, "userEmail").send_keys("khanh@example.com")
time.sleep(2)

# 2. Chọn giới tính (Male)
gender_radio = driver.find_element(By.XPATH, "//label[text()='Male']")
driver.execute_script("arguments[0].click();", gender_radio)
time.sleep(2)

# 3. Nhập số điện thoại
driver.find_element(By.ID, "userNumber").send_keys("0987654321")
time.sleep(2)

# 4. Chọn ngày sinh (01 Jan 2000)
driver.execute_script("document.getElementById('dateOfBirthInput').value = '25 Sep 2003'") 
time.sleep(2)

# 5. Nhập môn học
subjects = driver.find_element(By.ID, "subjectsInput")
subjects.send_keys("Math")
subjects.send_keys(Keys.ENTER)
time.sleep(2)

# 6. Chọn sở thích (Reading, Music)
for hobby in ["Reading", "Music"]:
    hobby_element = driver.find_element(By.XPATH, f"//label[text()='{hobby}']")
    driver.execute_script("arguments[0].click();", hobby_element)
time.sleep(2)
# 7. Upload ảnh
upload_path = os.path.abspath("anh.jpg")  # Đảm bảo có ảnh tên này cùng thư mục
driver.find_element(By.ID, "uploadPicture").send_keys(upload_path)
time.sleep(2)
# 8. Nhập địa chỉ
driver.find_element(By.ID, "currentAddress").send_keys("123 Demo Street, Test City")
time.sleep(2)
# 9. Chọn State và City
# Chọn State: NCR
state_dropdown = driver.find_element(By.ID, "state")
driver.execute_script("arguments[0].scrollIntoView(true);", state_dropdown)
driver.execute_script("arguments[0].click();", state_dropdown)

ncr_option = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@id='state']//div[text()='NCR']")))
driver.execute_script("arguments[0].click();", ncr_option)

# Chọn City: Delhi
city_dropdown = driver.find_element(By.ID, "city")
driver.execute_script("arguments[0].click();", city_dropdown)

delhi_option = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@id='city']//div[text()='Delhi']")))
driver.execute_script("arguments[0].click();", delhi_option)

# 10. Submit form
submit_button = driver.find_element(By.ID, "submit")
driver.execute_script("arguments[0].click();", submit_button)

# 11. Kiểm tra kết quả
modal = wait.until(EC.visibility_of_element_located((By.ID, "example-modal-sizes-title-lg")))
if modal.text == "Thanks for submitting the form":
    print("✅ TC001 PASSED: Submit form thành công.")
else:
    print("❌ TC001 FAILED: Không tìm thấy modal xác nhận.")

# 12. Đóng modal & browser
driver.find_element(By.ID, "closeLargeModal").click()
time.sleep(2)
driver.quit()
