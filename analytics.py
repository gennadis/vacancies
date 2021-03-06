from typing import Union, Callable

from terminaltables import SingleTable


def predict_salary(salary_from: int, salary_to: int) -> Union[int, float, None]:
    """Predict salary depending on parameters given."""
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    if not salary_to:
        return salary_from * 1.2
    if not salary_from:
        return salary_to * 0.8


def collect_vacancies_stats(
    vacancies_count: int, vacancies: list[dict], predict_salary_for: Callable
) -> dict:
    """Get vacancies and salary statistics."""
    salaries = []
    for vacancy in vacancies:
        salary: Union[int, None] = predict_salary_for(vacancy)
        if salary:
            salaries.append(salary)

    if salaries:
        statistics = {
            "vacancies_found": vacancies_count,
            "vacancies_processed": len(salaries),
            "average_salary": int(sum(salaries) / len(salaries)),
        }
        return statistics


def create_table(table_headers: list, content: dict, title: str):
    """Get nice looking job stats table."""
    table_rows = [table_headers]
    for language, stats in content.items():
        row = [language, *stats.values()]
        table_rows.append(row)

    table = SingleTable(table_rows)
    table.title = title

    return table.table
