class PositiveIntConverter:
    regex = r'[0]*[1-9]\d*'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value)
