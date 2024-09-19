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

            # Find the main article body content
            description_div = soup.find("div", class_="c-article__body")

            # Remove unwanted elements, like <aside> and ads or video blocks
            if description_div:
                for unwanted in description_div.find_all(["aside", "div", "ul"], class_=["c-aside", "c-card--embed", "c-figure", "u-hide--smd"]):
                    unwanted.decompose()  # Remove unwanted elements completely

            # Extract the text while preserving the structure with line breaks
            article_text = ''
            if description_div:
                paragraphs = description_div.find_all(["p", "strong", "b", "i"])
                for paragraph in paragraphs:
                    # Add paragraph text with newline
                    article_text += paragraph.get_text(strip=True) + "\n"

            # Clean up unwanted text fragments or links
            clean_content = "\n".join(
                line for line in article_text.split("\n")
                if "Читайте також:" not in line
                and "Підписуйтесь на наші канали" not in line
            )

            print(f"Name: {name}")
            print(f"Published: {published}")
            print(f"Description: {clean_content}")

            defaults = {
                "name": name,
                "photo": photo,
                "published": published,
                "description": clean_content,
            }

            # Update link status and save article
            l.status = 'Done'
            l.save()

            obj, created = Articles.objects.get_or_create(url=url, defaults=defaults)
