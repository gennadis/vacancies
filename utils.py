from typing import Union, Callable

from terminaltables import SingleTable


def predict_salary(salary_from: int, salary_to: int) -> Union[int, float, None]:
    """Predict salary depending on parameters given."""
    if not (salary_from or salary_to):
        return
    if not salary_to:
        return salary_from * 1.2
    if not salary_from:
        return salary_to * 0.8
    return (salary_from + salary_to) / 2


def get_vacancies_stats(vacancies: list[dict], predict_salary_for: Callable) -> dict:
    """Get vacancies and salary statistics."""
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


def get_table(table_headers: list, content: dict, title: str):
    """Get nice looking job stats table."""
    table_data = [table_headers]
    for language, stats in content.items():
        row = [language]
        for param in stats.values():
            row.append(param)
        table_data.append(row)

    table = SingleTable(table_data)
    table.title = title

    return table.table
