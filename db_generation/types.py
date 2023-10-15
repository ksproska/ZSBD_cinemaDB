class OracleType:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.value}"


class INTEGER(OracleType):
    def __str__(self):
        return "NULL" if self.value is None else f"{self.value}"


class NUMBER(OracleType):
    pass


class BOOLEAN(OracleType):
    def __str__(self):
        return "'Y'" if self.value else "'N'"


class CHAR(OracleType):
    def __init__(self, value):
        super().__init__(value.replace("'", ""))

    def __str__(self):
        return f"'{self.value}'"


class DATE(OracleType):
    pass


class TIMESTAMP(OracleType):
    def __str__(self):
        return f"timestamp '{self.value}'"


class FLOAT(OracleType):
    pass
