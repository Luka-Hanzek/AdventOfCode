from typing import List, Tuple


def parse_reports_file() -> Tuple[List, List]:
    reports = []
    with open('input.txt', 'r') as f:
        while line := f.readline():
            line = line.strip()

            report =  [int(x) for x in line.split(' ')]

            reports.append(report)

    return reports


# O(n)
def calculate_deltas(values):
    return [v2 - v1 for v1, v2 in zip(values, values[1:])]


def sign(v):
    if v > 0: return 1
    if v < 0: return -1
    if v == 0: return 0


# O(n)
def _report_safe(report, dampen: bool):
    deltas = calculate_deltas(report)
    # Check sufficient condition.
    if (all(v > 0 for v in deltas) or all(v < 0 for v in deltas)) and all(abs(v) <= 3 for v in deltas):
        return True

    if not dampen:
        return False

    # These are indices which will be used to try check if report is valid after respective element is removed.
    # Only one element is removed for one check i.e. we perorm `len(indices_to_remove)` checks where each check checks report with one element missing.
    indices_to_remove = []
    for i in range(len(report)):        # Maximum complexity of O(n) * O(m) = O(n*m). We do at most n iterations and 2 * O(n) report checks in total
        # Check places where delta is zero.
        if not indices_to_remove and i < len(deltas) and deltas[i] == 0:
            # We need to remove one of the elements. It doesn't matter which one since they are the same.
            if _report_safe(report[:i] + report[i + 1:], dampen=False):
                return True
            else:
                # The report is not valid after removing duplicate element. There's nothing we can do -> it's not safe.
                return False
        # We are at element `report[i]` and we are looking at next 3 points.
        if not indices_to_remove and len(report) - i >= 4:
            # This is "zig-zag" pattern.
            if sign(deltas[i]) != sign(deltas[i+1]) and sign(deltas[i]) == sign(deltas[i+2]):
                if sign(deltas[i] > 0):
                    #    o   o
                    #   / \ /
                    # -i---o-----------
                    if report[i + 1] >= report[i + 3]:
                        #      x
                        #     / \   o
                        #    /   \ /
                        #   /     o
                        # -i--------------
                        indices_to_remove = [i + 1]     # Only way to solve this is to remove `x`.
                    elif report[i + 1] < report[i + 3] and report[i + 1] > report[i]:
                        #           o
                        #     x    /
                        #    /  \ /
                        #   /    x
                        # -i--------------
                        indices_to_remove = [i + 1, i + 2]     # Two potential ways to solve this.
                    elif report[i + 2] < report[i]:
                        #            o
                        #           /
                        #    o     /
                        #   / \   /
                        # -i---\-/--------
                        #       x
                        indices_to_remove = [i + 2]     # Only way to solve this is to remove `x`.
                    else:
                        # If this happens, it means there are duplicate elements in the pattern thus when removing one element 2 adjacent elements will be the same.
                        # This will still yield unsafe report. So we don't try to do anything.
                        pass
                else:
                    # -i---o----------
                    #   \ / \
                    #    o   o
                    if report[i + 1] <= report[i + 3]:
                        # -i--------------
                        #   \     o
                        #    \   / \
                        #     \ /   o
                        #      x
                        indices_to_remove = [i + 1]     # Only way to solve this is to remove `x`.
                    elif report[i + 1] > report[i + 3] and report[i + 1] < report[i]:
                        # -i--------------
                        #   \    x
                        #    \  / \
                        #     x    \
                        #           o
                        indices_to_remove = [i + 1, i + 2]     # Two potential ways to solve this.
                    elif report[i + 2] > report[i]:
                        #       x
                        # -i---/-\--------
                        #   \ /   \
                        #    o     \
                        #           \
                        #            o
                        indices_to_remove = [i + 2]     # Only way to solve this is to remove `x`.
                    else:
                        # If this happens, it means there are duplicate elements in the pattern thus when removing one element 2 adjacent elements will be the same.
                        # This will still yield unsafe report. So we don't try to do anything.
                        pass
            # This is "knee" pattern.
            elif (sign(deltas[i]) == sign(deltas[i + 1]) and sign(deltas[i + 1]) != sign(deltas[i + 2])):
                if sign(deltas[i] > 0):
                    #      o
                    #     / \
                    #    o   o
                    #   /
                    # -i-------------
                    if report[i + 3] > report[i + 1]:
                        #       x
                        #      / \
                        #     /   x
                        #    o
                        #   /
                        # -i-------------
                        indices_to_remove = [i + 2, i + 3]      # Two potential ways to solve this.
                    else:
                        #       o
                        #      / \
                        #     /   \
                        #    o     \
                        #   /       x
                        # -i-------------
                        indices_to_remove = [i + 3]     # Only way to solve this is to remove `x`.
                else:
                    # -i-------------
                    #   \
                    #    o   o
                    #     \ /
                    #      o
                    if report[i + 3] < report[i + 1]:
                        # -i-------------
                        #   \
                        #    o
                        #     \   x
                        #      \ /
                        #       x
                        indices_to_remove = [i + 2, i + 3]      # Two potential ways to solve this.

                    else:
                        # -i-------------
                        #   \       x
                        #    o     /
                        #     \   /
                        #      \ /
                        #       o
                        indices_to_remove = [i + 3]     # Only way to solve this is to remove `x`.
            # This is other "knee" pattern.
            elif sign(deltas[i]) != sign(deltas[i + 1]) and sign(deltas[i + 1]) == sign(deltas[i + 2]):
                if sign(deltas[i] > 0):
                    #      o
                    #     / \
                    #----i---o----
                    #         \
                    #          o
                    if report[i] < report[i + 2]:
                        #      o
                        #     / \
                        #----/---o----
                        #   i     \
                        #          o
                        indices_to_remove = [i]     # Only way to solve this is to remove `i`.
                    else:
                        #      x
                        #     / \
                        #    i   \
                        #---------o----
                        #          \
                        #           o
                        indices_to_remove = [i, i + 1]      # Two potential ways to solve this. Remove `i` or `x`.
                else:
                    # -i-------o-----
                    #   \     /
                    #    \   o
                    #     \ /
                    #      o
                    if report[i] > report[i + 2]:
                        # ---------o-----
                        #   i     /
                        #    \   o
                        #     \ /
                        #      o
                        indices_to_remove = [i]     # Only way to solve this is to remove `i`.
                    else:
                        # -----------o-----
                        #           /
                        #          o
                        #     i   /
                        #      \ /
                        #       x
                        indices_to_remove = [i, i + 1]      # Two potential ways to solve this. Remove `i` or `x`.
        # We are at element `report[i]` and we are looking at next 2 points.
        # This should only occur if we only have 2 points left.
        elif not indices_to_remove and len(report) - i >= 3:
            if sign(deltas[i]) != sign(deltas[i + 1]):
                #    x
                #   / \
                # -i---o---------
                assert i == len(report) - 3

                indices_to_remove = [i, i + 2]
        # Check places where `abs(delta) > 3`.
        # We do this last because if we did it first it could shadow a possible pattern which needs to be resolved regardledd of delta magnitude.
        if not indices_to_remove and i < len(deltas) and abs(deltas[i]) > 3:
            if i == len(report) - 2:
                # [..., x, i, x]
                if abs(report[i + 1] - report[i - 1]) < abs(report[i] - report[i - 1]):
                    indices_to_remove = [i]
                else:
                    indices_to_remove = [i + 1]
            else:
                # [..., x, i, x, ...]
                if abs(report[i + 2] - report[i + 1]) < abs(report[i + 2] - report[i]):
                    indices_to_remove = [i]
                else:
                    indices_to_remove = [i + 1]

        if indices_to_remove:
            assert len(indices_to_remove) <= 2      # This ensures algoritm complexity in this iteration is bounded to O(1).
            return any(_report_safe(report[:i] + report[i + 1:], dampen=False) for i in indices_to_remove)      # Maximum complexity of 2 * O(m), m = size of report.

    return False


# To be able to use: $ python3 test.py --module=main.py
def report_safe(report):
    return _report_safe(report, dampen=True)


if __name__ == '__main__':
    reports = parse_reports_file()

    BRUTE_FORCE = False

    if BRUTE_FORCE:
        # O(n * m^2), n = number of reports, m = size of report
        num_safe_reports = 0
        unsafe_reports = []
        for report in reports:
            deltas = calculate_deltas(report)
            if _report_safe(report, dampen=False):
                num_safe_reports += 1
            else:
                unsafe_reports.append(report)

        print(f'Number of safe reports: {num_safe_reports}')

        num_additional_safe_reports = 0
        for report in unsafe_reports:
            if any(_report_safe(report[:i] + report[i+1:], dampen=False) for i in range(len(report))):
                num_additional_safe_reports += 1
        print(f'Number of safe reports with dampening: {num_safe_reports + num_additional_safe_reports}')
    else:
        # O(n * m), n = number of reports, m = size of report
        num_safe_reports = 0
        for report in reports:
            if _report_safe(report, dampen=False):
                num_safe_reports += 1
        print(f'Number of safe reports: {num_safe_reports}')

        num_safe_reports = 0
        for report in reports:
            if _report_safe(report, dampen=True):
                num_safe_reports += 1

        print(f'Number of safe reports with dampening: {num_safe_reports}')
