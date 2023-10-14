class INTEGER:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "NULL" if self.value is None else f"{self.value}"


class NUMBER:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.value}"


class BOOLEAN:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.value}"


class CHAR:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"\"{self.value}\""


class DATE:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.value}"


class TIMESTAMP:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"timestamp '{self.value}'"


class FLOAT:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.value}"
