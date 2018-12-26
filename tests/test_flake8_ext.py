from good_smell import GoodSmellFlake8


def test_leading_digit_str():
    for num in range(1, 5):
        for digits in range(1, 10 ** num):
            assert len(GoodSmellFlake8.leading_digit_str(num, digits)) == digits
