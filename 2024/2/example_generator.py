import main
import json


MAX_NUMBER_OF_ELEMENTS = 6
NUMBER_SPAN = (1, 10)


def check(report):
    return any(main._report_safe(report[:i] + report[i+1:], dampen=False) for i in range(len(report)))


def generate_labeled_examples():
    examples = []

    for num_elements in range(MAX_NUMBER_OF_ELEMENTS):
        old_list = [[i] for i in range(*NUMBER_SPAN)]
        for i in range(0, num_elements):
            new_list = []
            while old_list:
                l = old_list.pop(0)
                for i in range(*NUMBER_SPAN):
                    new_list.append(l + [i])

            old_list = new_list
        examples.extend(old_list)

    labeled_examples = []
    for example in examples:
        labeled_examples.append(
            {'report': example,
             'safe':   check(example),
            }
        )
    return labeled_examples




labeled_examples = generate_labeled_examples()
labeled_examples_json = json.dumps(labeled_examples, indent=3)
with open('labeled-examples.json', 'w') as f:
    f.write(labeled_examples_json)
