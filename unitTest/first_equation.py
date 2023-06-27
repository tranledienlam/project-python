def find_x(a,b):
    if a:
        return -b/a
    elif b:
        return "NONE"
    else:
        return "ALL"


if __name__ == "__main__":
    print(find_x(10,10))