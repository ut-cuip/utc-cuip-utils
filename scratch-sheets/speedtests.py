from timeit import timeit


def step_by_step_dict():
    data = {}
    data["key1"] = 1000
    data["key2"] = "a string"
    data["key3"] = 1000
    data["key4"] = {"my_test_key": 1000}
    data["key5"] = 1000
    data["key6"] = "a string"
    data["key7"] = 1000
    data["key8"] = "another string"
    data["key9"] = 1000
    return


def brackets_dict():
    data = {
        "key1": 1000,
        "key2": "a string",
        "key3": 1000,
        "key4": {"my_test_key": 1000},
        "key5": 1000,
        "key6": "a string",
        "key7": 1000,
        "key8": "another string",
        "key9": 1000,
    }
    return

def run_timeit_tests():
    print(timeit('step_by_step_dict()', number=100000, globals=globals()))
    print(timeit('brackets_dict()', number=100000, globals=globals()))

if __name__ == '__main__':
    run_timeit_tests()