from bs4 import BeautifulSoup
from dotenv import load_dotenv
from datetime import date
import requests
import os


class ImageInserter():
    def __init__(self) -> None:
        load_dotenv()
        self.API_KEY_PL = os.getenv('API_KEY_PL')
        self.API_URL_PL = os.getenv('API_URL_PL')
        self.API_KEY_CZ = os.getenv('API_KEY_CZ')
        self.API_URL_CZ = os.getenv('API_URL_CZ')
        self.API_KEY_EU = os.getenv('API_KEY_EU')
        self.API_URL_EU = os.getenv('API_URL_EU')
        self.API_KEY_DE = os.getenv('API_KEY_DE')
        self.API_URL_DE = os.getenv('API_URL_DE')
        self.logs = []


    def get_product_images_from_directory(self, path):
        files = os.listdir(path)
        files_dict = {}

        for file in files:
            file_name = file.split('.')[0]
            file_path = path + "\\" + file

            if file_name not in files_dict.keys():
                files_dict[file_name] = []
            if file_name in files_dict.keys():
                files_dict[file_name].append(file_path)

        return files_dict
    
    def get_product_id_by_reference(self, reference, channel):
        channel_selection = {'PL':{'url':self.API_URL_PL, 'key':self.API_KEY_PL},
                             'CZ':{'url':self.API_URL_CZ, 'key':self.API_KEY_CZ},
                             'EU':{'url':self.API_URL_EU, 'key':self.API_KEY_EU},
                             'DE':{'url':self.API_URL_DE, 'key':self.API_KEY_DE}
                             }
        try:
            response = requests.get(f"{channel_selection[channel]['url']}products?filter[reference]=[{reference}]", auth=(channel_selection[channel]['key'], ''))
        except Exception as e:
            print(f"CANNOT REACH PRODUCT: {reference}, ERROR: {e}")
            self.logs.append(f'CONNECTION ERROR,{reference}')

        if response.status_code == 200:
            try:
                response_soup = BeautifulSoup(response.text, 'xml')
                id_product = response_soup.find('product')['id']
                return id_product
            except Exception as e:
                print(f'{reference} - NO PRODUCT LIKE THAT IN SHOP')
                self.logs.append(f'NO PRODUCT,{reference}')
        return ''


    def save_logs_to_file(self):
        today_date = date.today()
        today_date_str = today_date.strftime('%d%m%Y_%H_%M_%S')
        with open(f"logs_{today_date_str}.txt", 'a') as log:
            log.write("\n".join(self.logs))


    def insert_photo_on_last_pos(self, product_id, photo_path, reference, channel):
        channel_selection = {'PL':{'url':self.API_URL_PL, 'key':self.API_KEY_PL},
                             'CZ':{'url':self.API_URL_CZ, 'key':self.API_KEY_CZ},
                             'EU':{'url':self.API_URL_EU, 'key':self.API_KEY_EU},
                             'DE':{'url':self.API_URL_DE, 'key':self.API_KEY_DE}
                             }
        print(f'ADDING PHOTO TO: {reference}')
        try:
            response = requests.post(f"{channel_selection[channel]['url']}images/products/{product_id}", files={'image': open(photo_path, 'rb')}, auth=(channel_selection[channel]['key'], ''))
            print(response.status_code)
        except Exception as e:
            print(f"ERROR: {reference}, ERROR DESC: {e}")
            self.logs.append(f'PHOTO ERROR,{reference}')
