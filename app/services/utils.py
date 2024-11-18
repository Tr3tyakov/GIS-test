import re


def get_snake_case(class_name: str) -> str:
    repl = r"\1_\2"
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", repl, class_name)
    return re.sub(r"([a-z\d])([A-Z])", repl, name).lower()
