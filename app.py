from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import time


def page_to_df(driver):
    models = driver.find_elements_by_class_name("feeditem")
    model_data = {'Model': [], 'Hand': [], 'Year': [], 'Price': [], 'Engine': [], 'Kilometers': [], 'EngineType': [],
                  'GearBox': [], 'Color': []}
    time.sleep(5)
    for index, model in enumerate(models):
        try:
            driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/main/div/div[5]/div/button').click()
        except Exception as ex:
            pass
        model.find_elements_by_class_name("merchant")[0].click()
        print(f"opened model {index}")
        time.sleep(2)

    for model in models:
        model_name = model.find_element_by_class_name("title").get_attribute('innerHTML')
        extradata = model.find_elements_by_class_name("data")
        if len(extradata) == 3:
            model_data['Model'].append(model_name.replace('\n', '').replace('  ', ''))
            model_data['Price'].append(
                model.find_element_by_class_name("price").get_attribute('innerHTML').replace('\n', '').replace(' ', ''))
            model_data['Year'].append(extradata[0].find_element_by_class_name("val").get_attribute('innerHTML'))
            model_data['Hand'].append(extradata[1].find_element_by_class_name("val").get_attribute('innerHTML'))
            model_data['Engine'].append(extradata[2].find_element_by_class_name("val").get_attribute('innerHTML'))

            kilometers = None
            engineType = None
            gearBox = None
            color = None

            try:
                kilometers = model.find_element_by_id("more_details_kilometers").find_element_by_tag_name(
                    "span").get_attribute(
                    "innerHTML").replace('\n', '').replace(' ', '')
            except Exception:
                pass

            try:
                engineType = model.find_element_by_id("more_details_engineType").find_element_by_tag_name(
                    "span").get_attribute(
                    "innerHTML").replace('\n', '').replace(' ', '')
            except Exception:
                pass

            try:
                gearBox = model.find_element_by_id("more_details_gearBox").find_element_by_tag_name(
                    "span").get_attribute(
                    "innerHTML").replace('\n', '').replace(' ', '')
            except Exception:
                pass

            try:
                color = model.find_element_by_id("more_details_color").find_element_by_tag_name("span").get_attribute(
                    "innerHTML").replace('\n', '').replace(' ', '')
            except Exception:
                pass

            model_data['EngineType'].append(engineType)
            model_data['GearBox'].append(gearBox)
            model_data['Color'].append(color)
            model_data['Kilometers'].append(kilometers)
    df = pd.DataFrame(data=model_data,
                      columns=['Model', 'Hand', 'Year', 'Price', 'Engine', 'Kilometers', 'EngineType', 'GearBox',
                               'Color'])
    return df


# פתיחת האתר המבוקש ע"י ה driver
PATH = "chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')

driver = webdriver.Chrome(PATH, chrome_options=chrome_options)
driver.maximize_window()
frames = []

for i in range(1, 2):
    driver.get(f"https://www.yad2.co.il/vehicles/private-cars?year=2007--1&page={i}")
    time.sleep(15)

    frames.append(page_to_df(driver))

results = pd.concat(frames)
results.to_csv('outfinal1.csv', index=False)
driver.quit()
