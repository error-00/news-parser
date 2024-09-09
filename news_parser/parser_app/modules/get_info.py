from email.policy import default
import requests

from bs4 import BeautifulSoup
from parser_app.models import Links, Articles


class News:
    def __init__(self) -> None:
        self.base_url = "https://tsn.ua/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def get_links(self, keyword=""):
        # Fetch the page content
        url = self.base_url
        if keyword:
            url += f"search?keyword={keyword}"
        else:
            url += "news"

        print(f"[+] Opening website {url}")

        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, "lxml")

        # Find the news links
        news_links = soup.find_all("a", class_="c-card__link")

        if news_links:
            print(f"[+] Found {len(news_links)} links")
            for j, link in enumerate(news_links, start=1):
                news_link = link.get("href")
                news_name = link.text.strip()

                # Save the link to the database
                obj, created = Links.objects.get_or_create(
                    link=news_link, name=news_name
                )
        else:
            print("[ERR] News not found")
        print()

    def get_data(self):
        # Iterate over 'New' links in the database
        for l in Links.objects.filter(status="New"):
            url = l.link
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.content, "lxml")

            print()
            print("########################################################")
            print("URL:", url)

            # Extract news details
            name = soup.find("h1", class_="c-card__title")
            name = name.text.strip() if name else None

            photo = soup.find("img", class_="c-card__embed__img")
            photo = photo.get("src") if photo else None

            published = soup.find("time")
            published = published.text.strip() if published else None

            description_lst = soup.find("div", class_="c-article__body").find_all("p")
            description = "\n".join(
                p.text.strip()
                for p in description_lst
                if "Читайте також:" not in p.text
                and "Підписуйтесь на наші канали" not in p.text
            )

            print(f"Name: {name}")
            print(f"Published: {published}")
            print(f"Description: {description}")

            defaults = {
                "name": name,
                "photo": photo,
                "published": published,
                "description": description,
            }

            # Update link status and save article
            l.status = 'Done'
            l.save()

            obj, created = Articles.objects.get_or_create(url=url, defaults=defaults)
