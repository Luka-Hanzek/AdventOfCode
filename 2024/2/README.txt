test.py:
    - Script used to test your solution on large amounts of data.
    -How to run:
        -Create file <module.py> that contains the following function:
            """
            def check_report(report: list[int]) -> bool:
                pass
            """
        - Run tests: python3 test.py --module=<module.py>

generate_examples.py:
    - Script used to generate every possible example specified with parameters:
        MAX_NUMBER_OF_ELEMENTS: int     - specifies the number of elements the largest report will have
        NUMBER_SPAN: tuple[int, int]    - specifies which numbers will be in the reports

        e.g. for parameters MAX_NUMBER_OF_ELEMENTS = 3 and NUMBER_SPAN = (1, 4) the result will be:
            [1]
            [2]
            [3]
            [1, 1]
            [1, 2]
            [1, 3]
            [2, 1]
            [2, 2]
            [2, 3]
            [3, 1]
            [3, 2]
            [3, 3]
            [1, 1, 1]
            [1, 1, 2]
            [1, 1, 3]
            [1, 2, 1]
            [1, 2, 2]
            [1, 2, 3]
            [1, 3, 1]
            [1, 3, 2]
            [1, 3, 3]
            [2, 1, 1]
            [2, 1, 2]
            [2, 1, 3]
            [2, 2, 1]
            [2, 2, 2]
            [2, 2, 3]
            [2, 3, 1]
            [2, 3, 2]
            [2, 3, 3]
            [3, 1, 1]
            [3, 1, 2]
            [3, 1, 3]
            [3, 2, 1]
            [3, 2, 2]
            [3, 2, 3]
            [3, 3, 1]
            [3, 3, 2]
            [3, 3, 3]

main.py:
    - Contains the solution.