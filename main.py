import random
from pprint import pprint
from typing import Callable, Iterable, Generator
from constraint import Problem


def rand_select(pca: list[list[int]]) -> list[int]:
    """Randomly selects a test case from the previous test cases."""
    return random.choice(pca)


def random_solution(problem: Problem, variables: int) -> list[int]:
    # for solution in problem.getSolutionIter():
    solution = random.choice(problem.getSolutions())
    return [solution[f"p{i + 1}"] for i in range(variables)]


def random_testcase(p: list[list[int]], c: list[Callable]) -> list[int]:
    """Generates a random test case that satisfies the constraints."""
    problem = Problem()
    for i, values in enumerate(p):
        problem.addVariable(f"p{i + 1}", values)
    for constraint in c:
        problem.addConstraint(constraint)

    return random_solution(problem, len(p))


def csp_solver(mr: Callable, tpre: list[int], p: list[list[int]], c: list[Callable]) -> list[int]:
    """Generates a follow-up test case that satisfies the metamorphic relation and constraints."""
    problem = Problem()
    for i, values in enumerate(p):
        problem.addVariable(f"p{i + 1}", values)
        problem.addVariable(f"p{i + 1}'", values)
    for constraint in c:
        problem.addConstraint(constraint)
    problem.addConstraint(mr, [f"p{i + 1}" for i in range(len(tpre))] + [f"p{i + 1}'" for i in range(len(tpre))])

    return random_solution(problem, len(p))


def generate_candidates(mr: Callable, p: list[list[int]], c: list[Callable], pca: list[list[int]], rep: int,
                        pr: float) -> list[list[int]]:
    """Generates a set of candidate test cases."""
    candidates = []
    r = random.random()
    if r <= pr:
        print("Using CSP Solver...")
        tpre = rand_select(pca)
        for _ in range(rep):
            t = csp_solver(mr, tpre, p, c)
            candidates.append(t)
    else:
        print("Using Random Test Case Generator...")
        for _ in range(rep):
            t = random_testcase(p, c)
            candidates.append(t)
    return candidates


def main():
    # Example of usage
    p = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    const = [
        # lambda a, b, c, *args: a + b > c,
        # lambda a, b, c, *args: a < b + c,
        lambda a, b, c, *args: a + c > b
    ]
    pca = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    def mr(a, b, c, a_, b_, c_):
        # return a + b + c == a_ + b_ + c_
        return True

    candidates = generate_candidates(mr, p, const, pca, 10, 0.5)
    pprint(candidates)


if __name__ == '__main__':
    main()
