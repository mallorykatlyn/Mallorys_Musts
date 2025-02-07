import requests
from bs4 import BeautifulSoup
import openai
import json
import os

#Amazon Affiliate ID
AFFILIATE_ID = "mallorymusts-20"

# OpenAI API Key (Stored in Github actions)
openai.api_key = os.getenv("OPENAI_API_KEY")

BEST_SELLERS_URL = "https;//www.amazon.com/Best-Sellers/zgbs"

def get_best_sellers():
    headers = {"User-Agent": "Mozill/5.0"}
    response = requests.get(BEST_SELLERS_URL, headers=heder)

    if response.status_code != 200:
        return[]

    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    for item in soup.select(".zg-item-immersion"):
        title = item.select_one(".p13n-sc-truncte").text.strip()
        base_link = "https://www.amazon.com" + item.select_one("a")["href"]
        affilite_link = f"{base_link}?tag={AFFILIATE_ID}"
        img = item.select_one("img")["src"]

        products.append({"title": title, "link": affiliate_link, "image": img})


    return products

def generte_review(product_name):
    prompt = f"Write a compelling product review for {product_name}. Highlight features, pros and cons, and why its a good buy."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["choices"[0]["message"]["content"]]

def save_data():
    products = get_best_sellers()

    for product in products[:10]: #top 10 best sellers
    product["review"] = generate_review(product["title"])

    with open("data.json", "w") as f:
        json.dump(products, f, indent=4)

    print("Data Saved Successfully")

if __name__ == "__main__":
    save_data()
