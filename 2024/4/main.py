

def parse_input(file):
    with open(file, 'r') as f:
        content = f.read()
    return [list(s) for s in content.strip().split('\n')]


def check_xmas(table, i, j):
    i_size = len(table)
    j_size = len(table[0])

    word = 'XMAS'

    occurances = 0

    can_go_right = j + len(word) - 1 < j_size
    can_go_left = j >= len(word) - 1
    can_go_up = i >= len(word) - 1
    can_go_down = i + len(word) - 1 < i_size

    # Left
    if can_go_left:
        if ''.join([table[i][j - k] for k in range(len(word))]) == word:
            occurances += 1

    # Right
    if can_go_right:
        if ''.join([table[i][j + k] for k in range(len(word))]) == word:
            occurances += 1
    # Up
    if can_go_up:
        if ''.join([table[i - k][j] for k in range(len(word))]) == word:
            occurances += 1

    # Down
    if can_go_down:
        if ''.join([table[i + k][j] for k in range(len(word))]) == word:
            occurances += 1

    # Up left
    if can_go_up and can_go_left:
        if ''.join([table[i - k][j - k] for k in range(len(word))]) == word:
            occurances += 1

    # Up right
    if can_go_up and can_go_right:
        if ''.join([table[i - k][j + k] for k in range(len(word))]) == word:
            occurances += 1

    # Down left
    if can_go_down and can_go_left:
        if ''.join([table[i + k][j - k] for k in range(len(word))]) == word:
            occurances += 1

    # Down right
    if can_go_down and can_go_right:
        if ''.join([table[i + k][j + k] for k in range(len(word))]) == word:
            occurances += 1

    return occurances

def check_x_mas(table, i, j):
    kernels = [
        [
            ['M', '.', 'S'],
            ['.', 'A', '.'],
            ['M', '.', 'S']
        ],
        [
            ['M', '.', 'M'],
            ['.', 'A', '.'],
            ['S', '.', 'S']
        ],
        [
            ['S', '.', 'M'],
            ['.', 'A', '.'],
            ['S', '.', 'M']
        ],
        [
            ['S', '.', 'S'],
            ['.', 'A', '.'],
            ['M', '.', 'M']
        ]
    ]

    def extract_matrix(i, j):
        lines = []
        for i in range(i, i + 3):
            lines.append(table[i][j:j+3])

        # Remove irreleavnt data
        lines[0][1] = '.'
        lines[1][0] = '.'
        lines[1][2] = '.'
        lines[2][1] = '.'

        return lines

    matrix = extract_matrix(i, j)
    return matrix in kernels


table = parse_input('input.txt')
sum = 0
for i in range(len(table)):
    for j in range(len(table[i])):
        sum += check_xmas(table, i=i, j=j)

print(f'xmas: {sum}')


sum = 0
i_size = len(table)
j_size = len(table[0])
for i in range(i_size - 2):
    for j in range(j_size - 2):
        sum += check_x_mas(table, i, j)

print(f'x-mas: {sum}')
