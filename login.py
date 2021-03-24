from selenium.webdriver import Chrome
import captchaocr
import time


def get_login_cookies():
    id = input("yourID:")
    pd = input("yourPassword:")

    driver = Chrome("./chromedriver")
    login_page = "https://cart.books.com.tw/member/login"
    driver.get(login_page)
    driver.maximize_window()

    try_times = 2
    for i in range(try_times):
        driver.find_element_by_id("login_id").send_keys(id)
        driver.find_element_by_id("login_pswd").send_keys(pd)
        capta_img = driver.find_element_by_id("captcha_img").find_element_by_tag_name("img")
        driver.save_screenshot('captcha/test.png')
        # * 2 是由於surface預設螢幕放大2倍
        left = capta_img.location['x'] * 2
        top = capta_img.location['y'] * 2
        right = left + capta_img.size['width'] * 2
        bottom = top + capta_img.size['height'] * 2

        crop = (left, top, right, bottom)

        captch = captchaocr.captchocr(crop)
        print(captch)
        driver.find_element_by_id("captcha").send_keys(captch[0:4])
        driver.find_element_by_id("books_login").click()
        time.sleep(10)
        if driver.current_url != login_page:
            print("登入成功")
            time.sleep(5)
            break
        else:
            print("登入失敗")
            if i == try_times - 1:
                driver.close()
            else:
                driver.refresh()
                time.sleep(5)

    cookies_list = driver.get_cookies()
    print(cookies_list)

    # 取得登入用cookie
    login_cookies = {}
    for c in cookies_list:
        if c["name"] in ["cid", "pd", "lpk", "bday", "gud"]:
            login_cookies[c["name"]] = c["value"]
    driver.close()

    return login_cookies