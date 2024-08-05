class Policy:
    def __init__(self, policy_type: str, coverage_amount: float, premium: float, start_date: str, end_date: str) -> None:
        self.policy_type = policy_type
        self.coverage_amount = coverage_amount
        self.premium = premium
        self.start_date = start_date
        self.end_date = end_date

    def __str__(self):
        return f"Typ pojištění: {self.policy_type}, Výše krytí: {self.coverage_amount}, Pojistné: {self.premium}, Platnost od: {self.start_date} do: {self.end_date}"