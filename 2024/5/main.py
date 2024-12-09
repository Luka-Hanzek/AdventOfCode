from typing import List, Set
from collections import defaultdict


class Rules:
    def __init__(self, rules: str):
        self._pages_after = defaultdict(set)
        rules_lines = rules.split("\n")
        for rule in rules_lines:
            page, page_after = (int(x) for x in rule.split("|"))
            self._pages_after[page].add(page_after)

    def has_rule_for_page(self, page: int) -> bool:
        return page in self._pages_after

    def get_pages_after_page(self, page: int) -> Set[int]:
        """For a given page, get pages which need to occur after the given page."""
        assert self.has_rule_for_page(page)

        return self._pages_after[page]


with open("input.txt", "r") as f:
    content = f.read()

rules_str, updates_str = (x.strip() for x in content.split("\n\n"))
rules = Rules(rules_str)
updates = [[int(x) for x in y.split(",")] for y in updates_str.split("\n")]


# Algorithm:
#   We prepared a data stucture which enables us to check if page violates the single necessary rule.
#   That is, for each page we check all of its successor pages and for each pair (page, successor_page)
#   we check whether that pair violates a rule. If no rule violation is found for the given page and
#   all of its successors then that page is at a valid position in the update.
#   Complexity: O(n^2), n := number of pages in the update
valid_updates = []
invalid_updates = []
for update in updates:
    invalid = False
    for i, page in enumerate(update):
        if not rules.has_rule_for_page(page):
            continue

        pages_after = rules.get_pages_after_page(page)
        if any(p in pages_after for p in update[:i]):
            invalid = True
            break

    if not invalid:
        valid_updates.append(update)
    else:
        invalid_updates.append(update)

sum = 0
for update in valid_updates:
    middle = (len(update) - 1) // 2
    sum += update[middle]

print(f"Sum of middle elements: {sum}")


# Algorithm:
#   We use the same data structure as above.
#   For each page we check all of its successor pages. For each pair (page, succesor_page) we check
#   whether page is required to be the succesor of successor_page. If it does then we change the positions of
#   page and sucessor_page.
#   This could cause the successor_page to be placed at any position before so we need to check the same indices again.
#   The page is determined to be on the valid place only if checks for all the sucessor_pages of a given page
#   finished without swapping.
#
#   !! This algorithm requires update to be fixable i.e. the algorithm could get stzck in a loop.
#
#   Complexity (worst case): O(n^3)
fixed_updates = []
for update in invalid_updates:
    i = 0
    while i != len(update) - 1:
        pages_swapped = False
        page = update[i]
        for successor_page_idx, successor_page in enumerate(update[i+1:], start=i+1):
            pages_after_successor_page = rules.get_pages_after_page(successor_page)
            if page in pages_after_successor_page:
                update[i], update[successor_page_idx] = update[successor_page_idx], update[i]
                pages_swapped = True
                break
        if not pages_swapped:
            # We are sure i-th page is at the right place.
            i += 1
    fixed_updates.append(update)

sum = 0
for update in fixed_updates:
    middle = (len(update) - 1) // 2
    sum += update[middle]

print(f"Sum of middle elements of fixed pages: {sum}")
