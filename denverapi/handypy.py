__version__ = "2020.6.4"


def _strip_inside_white_space(line: str):
    return " ".join([x.strip() for x in line.split(" ")])


def _strip_comment(line: str):
    if line.find("#") == -1:
        return line
    else:
        return line[0 : line.index("#")]


def analise_src_imports(src: str) -> list:
    """
    Searches for all possible imports inside the src file.

    :param src: The src code required for the analysis
    :return: the list of all the imports within the module
    """
    src_code = src.split("\n")
    imports = []
    for raw_line in src_code:
        line = _strip_inside_white_space(_strip_comment(raw_line.strip()))
        if line.startswith("from "):
            line = line.split(" ", 2)
            if line[2] == "import ":
                if line[0].startswith("."):
                    imports.append(line[0])
        elif line.startswith("import "):
            if " as " not in line:
                line = line.split(" ", 1)
                i = [x.strip() for x in line[1].split(",")]
                imports.extend(i)
            else:
                line = line.split(" ", 2)
                imports.append(line[1])
    return list(set(imports))


def main():
    import os
    import sys

    src = [
        open(os.path.dirname(__file__) + "/" + x).read()
        if os.path.isfile(os.path.dirname(__file__) + "/" + x)
        else ""
        for x in os.listdir(os.path.dirname(__file__))
    ]
    a_imports = [analise_src_imports(x) for x in src]
    for k, v in zip(os.listdir(os.path.dirname(__file__)), a_imports):
        print(f"In {k}: {v}")


if __name__ == "__main__":
    main()
