from tests.test_collection import collect_tests, test_case_files


def generate_smell_docs():
    for example_test in [list(collect_tests(file))[0] for file in test_case_files]:
        desc, symbols, before, after = example_test
        symbol = symbols[0]
        print(
            f"""### {desc} ({symbol})
{before}
Will be fixed to
{after}"""
        )


if __name__ == "__main__":
    generate_smell_docs()
