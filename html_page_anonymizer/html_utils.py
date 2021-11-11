from bs4 import BeautifulSoup as bs
import requests


class HTMLHandler:
    def __init__(self, link: str, output_file_name: str = "dumped_result.html"):
        self.output_file_name = output_file_name
        req = requests.get(link)
        self.soup = bs(req.content, "html.parser")

    def dump(self):
        with open(self.output_file_name, "w", encoding='utf-8') as file:
            file.write(str(self.soup))