import seleniumwire.undetected_chromedriver as uc
import undetected_chromedriver as uc2
from selenium.webdriver.remote.webdriver import By
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import random
import string


class Scraper:

    def __init__(self, headless: bool = True) -> None:
        """
        Scraper uses undetected_chromedriver to browse homeworkify and scrape solution. Gets around seleniumwire
        cloudfare issue by managing two chromedrivers

        :param headless: undetected_chromedriver headless mode
        """
        options = uc.ChromeOptions()
        options2 = uc2.ChromeOptions()
        if headless:
            options.headless = True
            options.add_argument('--headless')

            options2.headless = True
            options2.add_argument('--headless')

        self.driver = uc.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, timeout=10)

        self.driver2 = uc2.Chrome(options=options2)
        self.wait2 = WebDriverWait(self.driver2, timeout=10)

    def open_homeworkify(self, proxy: str, link: str) -> None:
        """
        Open homeworkify, input link, and press submit
        :param proxy: proxy to use with request
        :param link: chegg link
        :return:
        """
        # open new tab with proxy
        self.driver.proxy = {
            'https': proxy
        }
        self.driver.switch_to.new_window()
        self.driver.get("https://homeworkify.net/")

        # input link and press submit
        email_input = self.wait.until(EC.presence_of_element_located((By.ID, "hw-header-input")))
        email_input.send_keys(link)
        submit = self.driver.find_element(By.XPATH, '//*[@id="hw-header-searchbox"]/button/span/span/span')
        submit.click()

    def get_captcha(self, email: str) -> str:
        """
        Input email and save captcha image at img_path (e.g. tmp/captcha_123.png)
        :param email: used to fill email field
        :return: img_path
        """
        # click on captcha
        captcha_button = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "captcha-loader")))
        captcha_button.click()

        # input email
        email_input = self.wait.until(EC.presence_of_element_located((By.ID, "user_email")))
        email_input.send_keys(email)

        # get captcha image
        locator = (By.ID, "captcha_challenge_img")
        captcha_element = self.wait.until(EC.presence_of_element_located(locator))
        self.wait.until(EC.staleness_of(captcha_element))
        captcha_element = self.driver.find_element(*locator)

        # generate filename and save captcha image
        img_path = 'tmp/captcha_' + ''.join(random.choice(string.digits) for _ in range(3)) + '.png'
        captcha_element.screenshot(img_path)
        return img_path

    def retry_get_captcha(self) -> str:
        # locate captcha element
        captcha_element = self.wait.until(EC.presence_of_element_located((By.ID, "captcha_challenge_img")))

        # generate filename and save captcha image
        img_path = 'tmp/captcha_' + ''.join(random.choice(string.digits) for _ in range(3)) + '.png'
        captcha_element.screenshot(img_path)
        return img_path

    def captcha_has_failed(self) -> bool:
        # get presence of flash message
        captcha_msg = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "captcha_msg")))
        # check failure state
        if captcha_msg.text == "Please try again!":
            print("fail")
            fail = True
        else:
            print("no fail")
            fail = False
        return fail

    def submit_captcha(self, result: str) -> None:
        # find result field and send answer
        result_field = self.driver.find_element(By.ID, "cp-user-input")
        result_field.send_keys(result)

        # submit button
        submit_button = self.driver.find_element(By.ID, "verify-captcha")
        submit_button.click()

    def open_answer_link(self, link: str) -> None:
        # moving cookies from driver 1 to driver 2
        cookies = self.driver.get_cookies()
        self.driver2.switch_to.new_window()  # new tab
        self.driver2.get(link)
        for cookie in cookies:
            self.driver2.add_cookie(cookie)

        # finally open link answer
        self.driver2.get(link)

    def get_full_screenshot(self) -> str:
        """
        Take full screenshot of webpage. Works in headless mode.

        :return: image path
        """
        # set image size for full page screenshot
        size = lambda x: self.driver.execute_script('return document.body.parentNode.scroll' + x)
        self.driver2.set_window_size(size('Width'), size('Height'))
        # generate img_path
        img_path = 'tmp/result_' + ''.join(random.choice(string.digits) for _ in range(3)) + '.png'

        # wait until page loads
        self.wait2.until(EC.presence_of_element_located((By.CLASS_NAME, "more-sol")))
        # take screenshot
        self.driver2.find_element(By.TAG_NAME, 'body').screenshot(img_path)
        # close window
        self.driver2.close()
        return img_path
