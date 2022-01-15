import requests
from pprint import pprint

HH_BASE_API = "https://api.hh.ru"
PROG_LANGUAGES = ["JavaScript", "Python", "Go", "Java", "Kotlin", "C++", "PHP", "Swift"]


def get_vacacnies(
    base_url: str, endpoint: str, role_id: int, area_id: int, period: int, text: str
):

    url = f"{base_url}{endpoint}"
    params = {
        "professional_role": role_id,
        "area": area_id,
        "period": period,
        "text": text,
    }

    response = requests.get(url, params)
    response.raise_for_status()

    return response.json()


def main():
    python_jobs = get_vacacnies(HH_BASE_API, "/vacancies", 96, 1, 30, "ptyhon")["items"]
    for job in python_jobs:
        print(job["salary"])


if __name__ == "__main__":
    main()
