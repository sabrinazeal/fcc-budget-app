class Category:
    """Contains information about budget categories."""

    def __init__(self, name):
        """Initializes the category."""
        self.name = name
        self.ledger = []
        self.balance = 0
        self.spendings = 0

    def __str__(self):
        """Defines the category's string representation for printing."""
        total_stars = 30 - len(self.name)
        left_stars = "*" * int((total_stars / 2))
        right_stars = "*" * int(((total_stars / 2) + (total_stars % 2)))
        header = f"{left_stars}{self.name}{right_stars}\n"

        body = ""
        for operation in self.ledger:
            if len(operation["description"]) <= 23:
                body = f"{body}{operation['description']}"
                whitespace = 30 - len(operation['description']) - len(f"{operation['amount']:.2f}")
            else:
                body = f"{body}{operation['description'][0:23]}"
                whitespace = 7 - len(f"{operation['amount']:.2f}")
            whitespace *= " "
            body = f"{body}{whitespace}{operation['amount']:.2f}\n"
        body = f"{body}Total: {self.balance:.2f}"
        return f"{header}{body}"

    def deposit(self, amount, description=""):
        """Registers a deposit into the category's ledger."""
        self.balance += amount
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        """Registers a withdrawal into the category's ledger."""
        valid = self.check_funds(amount)
        if valid:
            self.balance -= amount
            self.spendings += amount
            self.ledger.append({"amount": -amount, "description": description})
        return valid

    def get_balance(self):
        """Returns the category's balance."""
        return self.balance

    def transfer(self, amount, destination):
        """Transfers funds from one category to another."""
        valid_operation = self.check_funds(amount)
        if valid_operation:
            self.withdraw(amount, f"Transfer to {destination.name}")
            destination.deposit(amount, f"Transfer from {self.name}")
        return valid_operation

    def check_funds(self, amount):
        """Checks if the provided amount is available in the category's funds."""
        if amount > self.balance:
            return False
        else:
            return True


def create_spend_chart(categories):
    """Returns a bar chart representing spendings by category."""

    # Initializes required variables
    total_spendings = 0
    spendings_by_category = []
    category_lengths = []

    # Obtains required info about the categories
    for category in categories:
        total_spendings += category.spendings
        category_lengths.append(len(category.name))
        if category.ledger:
            spendings_by_category.append({"category": category, "spending": category.spendings})
    for spending in spendings_by_category:
        spending["percent"] = spending["spending"] * 100 / total_spendings

    # Initializes strings
    line_length = 4 + (len(categories) * 3) + 1
    header = "Percentage spent by category\n"
    body = ""
    footer = (" " * 4) + ((line_length - 4) * "-") + "\n"

    # Creates chart structure
    chart = ["  0|"]
    for number in range(10, 100, 10):
        chart.append(f" {number}|")
    chart.append("100|")

    # Adds bars and flips chart
    for spending in spendings_by_category:
        marker_amount = int((spending["percent"] / 10) + 1)
        for line in chart:
            if chart.index(line) < marker_amount:
                chart[chart.index(line)] += " o "
            else:
                chart[chart.index(line)] += "   "
    chart.reverse()

    # Pads lines with whitespace as needed
    for line in chart:
        line += " " * (line_length - len(line))
        body = f"{body}{line}\n"

    # Assembles footer
    longest_name = max(category_lengths)
    for number in range(0, longest_name):
        footer += "    "
        for category in categories:
            if number < len(category.name):
                footer += f" {category.name[number]} "
            else:
                footer += "   "
        if number < longest_name - 1:
            footer += " \n"
        else:
            footer += " "

    # Puts strings together and returns the final output
    output = f"{header}{body}{footer}"
    return output
