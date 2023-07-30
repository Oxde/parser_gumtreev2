from selenium.common import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
import time
class Ad:
    def __init__(self, element: WebElement):
        self.element = element
        self.seller_rating = None
        self.item_name = None
        self.price = None
        self.publication_time = None
        self.views = None
        self.date_registered = None
        self.ad_link = None
        self.location = None
        self.id = None


    def get_info(self):
        return {
            "item_name": self.item_name,
            "price": self.price,
            "publication_time": self.publication_time,
            "ad_link": self.ad_link,
            "location": self.location,
            "id": self.id,
            "date_registered": self.date_registered
        }

    def extract_data_intital(self):  # extract data for first time ( without going into )
        self.item_name = self.element.find_element(By.CLASS_NAME, "user-ad-row-new-design__title-span").text
        try:
            self.price = self.element.find_element(By.CLASS_NAME, "user-ad-price-new-design__price").text
        except Exception: #если нет цены то нахуй скипается
                return 0
        self.publication_time = self.element.find_element(By.CLASS_NAME, "user-ad-row-new-design__age").text
        self.ad_link = self.element.get_attribute("href")
        self.location = self.element.find_element(By.CLASS_NAME, "user-ad-row-new-design__location").text
        url_parts = self.ad_link.split('/')
        # Get the last part of the URL which contains the ID
        id_part = url_parts[-1]
        # Extract the ID from the part by removing any non-digit characters
        self.id = ''.join(filter(str.isdigit, id_part))
        return 1

    def click_ad(self, driver):
        current_window = driver.current_window_handle  # Get the current window handle
        # Open the ad URL in a new tab or window
        driver.execute_script("window.open(arguments[0]);", self.ad_link)
        # Switch to the new tab or window
        for window_handle in driver.window_handles:
            if window_handle != current_window:
                driver.switch_to.window(window_handle)
                break
        try:
            try:
                self.date_registered = driver.find_element(By.CLASS_NAME, "seller-profile__member-since").text
            except NoSuchElementException:
                self.date_registered = driver.find_element(By.CLASS_NAME, "user-rating__description").text
                if self.date_registered == "Highly Rated":
                    driver.close()
                    driver.switch_to.window(current_window)
                    return 0
        except Exception as e:
            print("e", self.ad_link)
            driver.close()
            driver.switch_to.window(current_window)
            return 0

        driver.close()
        driver.switch_to.window(current_window)
        return 1

    def print_info(self):
        print("Title:", self.item_name)
        print("Price:", self.price)
        print("Location:", self.location)
        print("P_time:", self.publication_time)
        print("Link:", self.ad_link)
        print("Id:", self.id)
        print("Registred_date", self.date_registered)
        print("----------------------")
    # questions about everything

    def is_car_ad(self) -> bool:
        car_brands = ["audi", "mg", "fuso", "bmw", "mercedes", "volkswagen", "ford", "chevrolet", "toyota", "honda", "nissan",
                      "subaru", "hyundai", "kia", "mazda", "mitsubishi", "lexus", "jaguar", "land rover",
                      "harley-davidson", "yamaha", "honda", "suzuki", "kawasaki", "ducati","haval","jeep",
                      "holden", "trailer", "peugeot", "ram", "caravan","alfa","wagon","mitsubisi","hlv","takeuchi"]

        keywords = car_brands

        for keyword in keywords:
            if keyword in self.item_name.lower():
                return True
        return False

    def is_house_rental_ad(self) -> bool:
        rental_keywords = ["house", "apartment", "rent", "rental"]
        for keyword in rental_keywords:
            if keyword in self.item_name.lower():
                return True
            return False

    def is_job_offer_ad(self) -> bool:
        job_keywords = ["job", "work", "employment", "career"]
        for keyword in job_keywords:
            if keyword in self.item_name.lower():
                return True
        return False

    def is_pet_ad(self) -> bool:
        pet_keywords = ["pet", "dog", "cat", "puppy", "kitten", "bird", "parrot", "fish", "hamster", "rabbit",
                        "guinea pig", "turtle", "snake", "lizard", "reptile", "horse", "pony", "goat", "sheep",
                        "chicken", "rooster", "duck", "gecko", "ferret", "gerbil", "rat", "mouse"]
        pet_breeds = ["labrador", "golden retriever", "bulldog", "poodle", "beagle", "german shepherd", "rottweiler",
                      "siberian husky", "boxer", "maine coon", "persian", "siamese", "bengal", "ragdoll",
                      "british shorthair",
                      "abyssinian", "goldfish", "betta fish", "siamese fighting fish", "guinea pig", "dwarf rabbit",
                      "netherland dwarf rabbit", "african grey parrot", "budgerigar", "cockatiel", "aqua", "horse",
                      "pony", "domestic shorthair", "domestic longhair"]
        keywords = pet_keywords + pet_breeds

        for keyword in keywords:
            if keyword in self.item_name.lower():
                return True
        return False

    def is_ad_ok(self) -> bool:
        if not (self.is_car_ad() or self.is_pet_ad() or self.is_job_offer_ad()  or self.is_house_rental_ad()):
            if self.price != "Free":

                return True
        else:

            return False


def print_ads(ad_elements):
    for ad_element in ad_elements:
        print(ad_element.get_attribute("outerHTML"))
        print()

def cycle_one(ads,driver):
    for ad_element in ad_elements:
        try:
            ad = Ad(ad_element)
            flag = ad.extract_data_intital()
            if flag and ad.is_ad_ok():
                ads.append(ad)
                ad.print_info()
        except Exception as e:
            print(f"An error occurred while processing an ad: {str(e)}")
    for ad in ads:
        flag = ad.click_ad(driver)
        if not flag:
            ads.remove(ad)

def proxy_setup(ans):
    proxy_ip = ["45.138.156.83", "195.208.181.150"]
    proxy_port = [63818, 63182]
    proxy_username = "ibYmjwaQ"
    proxy_password = "muQmJ4gV"
    proxy_options1 = {
        'proxy': {
            'http': f'http://{proxy_username}:{proxy_password}@{proxy_ip[0]}:{proxy_port[0]}',
            'https': f'https://{proxy_username}:{proxy_password}@{proxy_ip[0]}:{proxy_port[0]}'
        },
        'executable_manager': "/Users/nikmarf/pythonProject4/chromedriver/chromedriver",
    }
    proxy_options2 = {
        'proxy': {
            'http': f'http://{proxy_username}:{proxy_password}@{proxy_ip[1]}:{proxy_port[1]}',
            'https': f'https://{proxy_username}:{proxy_password}@{proxy_ip[1]}:{proxy_port[1]}'
        },
        'executable_manager': "/Users/nikmarf/pythonProject4/chromedriver/chromedriver",
    }
    if ans == 1:
        return proxy_options1
    if ans == 2:
        return proxy_options2


chrome_options = Options()
# chrome_options.add_argument("--headless")
url = "https://www.gumtree.com.au/s-r500"
driver = webdriver.Chrome(options=chrome_options, seleniumwire_options=proxy_setup(1))
driver.get(url)
ads_finished = {} #словарь в котором по ключу ( айди) можно найти объект ad, .get_info() метод возвращает словарь со всеми полями класса

used_ads = []
'''
 # used_ads - здесь крч будут хранится id после отправки в тг соответсвенно. типо скорее всего надо энивей хранить
 данные в тексте. но я хз какую логику ты применишь в отправке в тг, так что пока так оставил
'''

while True: #бесконечный цикл
    driver.get(url)
    ad_collection_section = driver.find_element(By.CLASS_NAME, "search-results-page__user-ad-collection")
    ad_elements = ad_collection_section.find_elements(By.CLASS_NAME, "user-ad-row-new-design")
    ads = []
    cycle_one(ads, driver)
    driver.refresh()
    for ad in ads:
        if ad.id not in ads_finished.keys():
            if ad.id not in used_ads:
                ads_finished[ad.id] = ad


    time.sleep(60)


driver.quit()