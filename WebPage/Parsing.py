import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import timedelta, datetime
import requests
from WebPage.models import CarModel





def get_deltatime(date:str):
    day_index = date.index('D')
    days = int(date[:day_index])

    hour_index = date.index('H')
    hours = int(date[day_index + 1:hour_index])

    minute_index = date.index('min')
    minutes = int(date[hour_index + 1:minute_index])

    return timedelta(days=days, hours=hours+1, minutes=minutes)


class CopartParse:
    def __init__(self, url, count_page=100):
        self.url = url
        self.count_page = count_page

    def __set_up(self):
        options = uc.ChromeOptions()
        options.add_argument('-headless')
        options.add_experimental_option(
            'prefs',
            {
                'profile.managed_default_content_settings.mixed_script': 2,
                'profile.managed_default_content_settings.media_stream': 2,
                'profile.managed_default_content_settings.stylesheets': 2,
            }
        )

        self.driver = uc.Chrome(options=options)

    def __get_url(self):
        self.driver.get(self.url)

    def __paginator(self):
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((
            By.CSS_SELECTOR, '[class="p-ripple p-element p-paginator-next p-paginator-element p-link"]')))
        while self.driver.find_elements(By.CSS_SELECTOR, '[class="p-ripple p-element p-paginator-next '
                                                         'p-paginator-element p-link"]') and self.count_page > 0:
            self.__parse_page()
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((
                By.CSS_SELECTOR, '[class="p-ripple p-element p-paginator-next p-paginator-element p-link"]')))
            self.driver.find_element(By.CSS_SELECTOR,
                                     '[class="p-ripple p-element p-paginator-next '
                                                         'p-paginator-element p-link"]').click()
            self.count_page -= 1

    def __parse_page(self):
        titles = self.driver.find_elements(By.CSS_SELECTOR, '[class="p-element p-selectable-row ng-star-inserted"]')

        urls = [title.find_element(By.CSS_SELECTOR, '[class="search_result_lot_detail_meta_data_block"]').
                find_element(By.CSS_SELECTOR, '[class="ng-star-inserted"]').get_attribute('href') for title in titles]

        for url in urls:
            if not CarModel.objects.filter(url=url):

                self.driver.get(url)
                WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((
                    By.CSS_SELECTOR, '[class="title my-0 mr-10"]')))

                lot_number = self.driver.find_element(By.ID, 'LotNumber').text

                name = self.driver.find_element(By.CSS_SELECTOR, '[class="title my-0 mr-10"]').text

                auction = self.driver.find_element(By.CSS_SELECTOR, '[class="panel-content"]').\
                    find_element(By.CSS_SELECTOR, '[class="border-top-gray pt-5 d-flex"]').\
                    find_element(By.CSS_SELECTOR, '[class="lot-details-desc"]').text

                pictures = self.driver.find_elements(By.CSS_SELECTOR,
                                                     '[class="img-responsive cursor-pointer thumbnailImg"]')
                picture_url = pictures[0].get_attribute('full-url')

                miles = self.driver.find_element(By.CSS_SELECTOR, '[class="lot-details-desc odometer-value w100"]').text

                date = self.driver.find_element(By.CSS_SELECTOR, '[data-uname="lotdetailSaleinformationtimeleftvalue"]').text

                delete_date = datetime.now() + get_deltatime(date)

                CarModel.objects.create(name=name, lot_number=lot_number, auction=auction, url=url,
                                        image=picture_url, date=delete_date)

        self.driver.get(self.url)

    def parse(self):
        self.__set_up()
        self.__get_url()
        self.__paginator()

    def quit(self):
        self.driver.quit()