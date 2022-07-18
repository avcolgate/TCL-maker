
# True for int, float any sign
def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        return False