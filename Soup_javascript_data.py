# In this website the data is loaded using javascrpit , check how that data is captured using a data key
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

movie_IMDB_IDs = [
    "tt15398776",  #oppenheimer
    "tt1517268"    #barbie 
]

num_reviews_needed = 1000

def scrape_reviews(imdb_id, reviews_needed):
    headers = {"User-Agent": "Mozilla/5.0"}
    base_url = f"https://www.imdb.com/title/{imdb_id}/reviews?ref_=tt_ql_3"
    reviews = []
    current_page = base_url

    while len(reviews) < reviews_needed:
        response = requests.get(current_page, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        review_elements = soup.find_all("div", class_="text show-more__control")
        for review in review_elements:
            if len(reviews) < reviews_needed:
                reviews.append(review.get_text())
            else:
                break

        load_more_button = soup.find('div', class_='load-more-data')
        if load_more_button:
            key = load_more_button.get('data-key')
            if key:
                next_page_url = f"https://www.imdb.com/title/{imdb_id}/reviews/_ajax?ref_=undefined&paginationKey={key}"
                current_page = next_page_url
                time.sleep(1)  
            else:
                break
        else:
            break

    return reviews

all_reviews = []
for imdb_id in movie_IMDB_IDs:
    reviews = scrape_reviews(imdb_id, num_reviews_needed - len(all_reviews))
    all_reviews.extend(reviews)
    if len(all_reviews) >= num_reviews_needed:
        break

df = pd.DataFrame(all_reviews, columns=["Review"])
df.to_csv("imdb_movie_reviews.csv", index=False)

print(f"Scraped {len(all_reviews)} reviews and saved to imdb_movie_reviews.csv")