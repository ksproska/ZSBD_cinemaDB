class ObjectWithCounter:
    counter = 1

    @classmethod
    def next(cls):
        counter_val = cls.counter
        cls.counter += 1
        return counter_val


class AddableToDatabase:
    @property
    def sql_addable(self):
        """
        example: "INSERT INTO ClassName (Atr_1, Atr_2) VALUES (%(Atr_1)s, %(Atr_2)s)"
        """
        keys = []
        values = []
        for k, v in self.__dict__.items():
            keys.append(f"{k}")
            values.append(f"{v}")
        keys_joined = ", ".join(keys)
        values_joined = ", ".join(values)
        return f'INSERT INTO {self.__class__.__name__} ({keys_joined}) VALUES ({values_joined});'

    def create_table(self):
        output = f"CREATE TABLE {self.__class__.__name__}(\n"
        for key, value in self.__dict__.items():
            output += f"\t{key} {type(value).__name__}\n"
        output += "\tPRIMARY KEY()\n"
        output += ");\n"
        return output

    def __str__(self):
        keys, values = '', ''
        if len(self.__dict__) > 0:
            keys = ', '.join(self.__dict__.keys())
            values = ', '.join([str(value) for value in self.__dict__.values()])
        return f'{self.__class__.__name__} ({keys}) : ({values})'
