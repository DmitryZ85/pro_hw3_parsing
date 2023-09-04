import bs4
import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import json


headers = Headers(browser='firefox', os='win')
headers_data = headers.generate()


if __name__ == "__main__":
    url = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"

    res = requests.get(url=url, headers=headers_data)
    soup = bs4.BeautifulSoup(res.text, 'lxml')

    result = []
    for item in soup.find_all(class_="vacancy-serp-item__layout"):
        item_title = item.find(class_="serp-item__title")
        title = item_title.text
        item_descr = soup.find(class_="g-user-content")
        desc = item_descr.text if item_descr is not None else ""

        if "django" in (title + desc).lower() or "flask" in (title + desc).lower():
            salary = item.find("span", class_="bloko-header-section-3")
            if salary is None:
                salary = ""
            else:
                salary = salary.text
            city = item.find(
                "div", attrs={"data-qa": "vacancy-serp__vacancy-address"}
            ).text
            company = item.find(
                "div", class_="vacancy-serp-item__meta-info-company"
            ).text

            result.append(
                {
                    "link": item_title.attrs["href"],
                    "salary": salary.replace("\u202f", ""),
                    "company": company.replace("\xa0", " "),
                    "city": re.sub("\sи.+", "", city),
                }
            )

    with open("result.json", "w", encoding="utf8") as file:
        json.dump(result, file, ensure_ascii=False, indent=2)