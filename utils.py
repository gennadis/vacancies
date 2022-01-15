from typing import Union


def predict_salary(salary_from: int, salary_to: int) -> Union[int, float, None]:
    if not (salary_from or salary_to):
        return
    if not salary_to:
        return salary_from * 1.2
    if not salary_from:
        return salary_to * 0.8
    return (salary_from + salary_to) / 2


def main():
    pass


if __name__ == "__main__":
    main()
