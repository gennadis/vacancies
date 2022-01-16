from typing import Union, Callable


def predict_salary(salary_from: int, salary_to: int) -> Union[int, float, None]:
    if not (salary_from or salary_to):
        return
    if not salary_to:
        return salary_from * 1.2
    if not salary_from:
        return salary_to * 0.8
    return (salary_from + salary_to) / 2


def get_vacancies_stats(vacancies: list[dict], predict_salary_for: Callable) -> dict:
    statistics = {}

    salaries = []
    for vacancy in vacancies:
        salary: Union[int, None] = predict_salary_for(vacancy)
        if salary:
            salaries.append(salary)

    statistics["vacancies_found"] = len(vacancies)
    statistics["vacancies_processed"] = len(salaries)
    statistics["average_salary"] = int(sum(salaries) / len(salaries))

    return statistics


def prepare_table(table_headers: list, content: dict):
    table_data = [table_headers]
    for language, stats in content.items():
        row = [language]
        for param in stats.values():
            row.append(param)
        table_data.append(row)

    return table_data
