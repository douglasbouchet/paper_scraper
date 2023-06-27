from bs4 import BeautifulSoup
import requests

trigger_words = [
    word.lower()
    for word in [
        "transformers",
        "Language Models",
        "BERT",
        "GPT",
        "GPT-2",
        "GPT2",
        "GPT-3",
        "GPT3",
        "T5",
        "Generative Adversarial Networks",
        "GAN",
        "lora",
        "lomo",
    ]
]


def get_seen_articles():
    with open("already_seen.txt", "r") as f:
        articles = f.readlines()
    return [article.strip().lower() for article in articles]


def clean_new_articles():
    with open("new_articles.txt", "w") as f:
        f.write("")


def scrap_journal_of_ml():
    clean_new_articles()
    url = "https://www.jmlr.org/"
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to get the content of the url")
        exit(1)
    s = BeautifulSoup(response.text, "html.parser")
    unparsed_title = s.find_all("dt")
    print("number of article: ", len(unparsed_title))
    matching_articles = []
    for title in unparsed_title:
        title = title.get_text().lower().strip()
        # splited = title.split(" ")
        if any([word in title for word in trigger_words]):
            matching_articles.append(title)
    print("number of articles matched: ", len(matching_articles))
    seen_articles = get_seen_articles()
    new_articles = [article for article in matching_articles if article not in seen_articles]
    if len(new_articles) == 0:
        print("No new articles")
        return

    # save the articles in a file
    with open("new_articles.txt", "w") as f:
        for title in new_articles:
            f.write(title + "\n")
    # add new articles at the beginning of the already seen articles
    with open("already_seen.txt", "w") as f:
        for title in new_articles:
            f.write(title + "\n")
        for title in seen_articles:
            f.write(title + "\n")


if __name__ == "__main__":
    scrap_journal_of_ml()
