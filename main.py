import json
import requests
from bs4 import BeautifulSoup


def get_first_jobs():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }

    url = "https://www.work.ua/jobs-kyiv-junior+python+developer/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    job_link = soup.find_all("div", class_="job-link")

    jobs_dict = {}
    for article in job_link:
        job_link = article.find("h2").text.strip()
        article_desc = article.find("p").text.strip()
        article_url = f'https://www.work.ua{article.find("a").get("href")}'

        article_id = article_url.split("/")[4]

        jobs_dict[article_id] = {
            "job_link": job_link,
            "article_desc": article_desc,
            "article_url": article_url
        }
    with open("jobs_dict.json", "w", encoding="utf-8") as file:
        json.dump(jobs_dict, file, indent=4, ensure_ascii=False)


def check_jobs_update():
    with open("jobs_dict.json", encoding="utf-8") as file:
        jobs_dict = json.load(file)

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }

    url = "https://www.work.ua/jobs-kyiv-junior+python+developer/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    job_link = soup.find_all("div", class_="job-link")

    fresh_jobs = {}
    for article in job_link:
        article_url = f'https://www.work.ua{article.find("a").get("href")}'
        article_id = article_url.split("/")[4]

        if article_id in jobs_dict:
            continue
        else:
            job_link = article.find("h2").text.strip()
            article_desc = article.find("p").text.strip()

            jobs_dict[article_id] = {
                "job_link": job_link,
                "article_desc": article_desc,
                "article_url": article_url
            }

            fresh_jobs[article_id] = {
                "job_link": job_link,
                "article_desc": article_desc,
                "article_url": article_url
            }

    with open("jobs_dict.json", "w", encoding="utf-8") as file:
        json.dump(jobs_dict, file, indent=4, ensure_ascii=False)

    return fresh_jobs


def main():
    get_first_jobs()#Запись всех вакансий на сайте
    """print(check_jobs_update())""" #Команда на проверку нових Вакансий


if __name__ == '__main__':
    main()
