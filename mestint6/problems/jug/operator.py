from mestint6.problems.jug.state import Jug


class Operator:
    def __init__(self, from_, to):
        self.from_ = from_
        self.to = to

    # (self, ...) -> peldany fuggveny
    # nincs self: osztály fuggveny
    def precondition_fulfilled(self, jug):
        return jug.contents[self.from_] != 0 \
            and jug.contents[self.to] != jug.CAPACITIES[self.to]

    def use(self, jug):
        result = Jug()

        volume = min(jug.contents[self.from_], Jug.CAPACITIES[self.to] - jug.contents[self.to])

        index_untouched = next(filter(lambda i: i not in (self.from_, self.to),
                                Jug.INDICIES))

        # next ?
        # lambda function in python?

        result.contents[self.from_] = jug.contents[self.from_] \
            - volume 

        result.contents[self.to] = jug.contents[self.to] \
            + volume

        result.contents[index_untouched] = jug.contents[index_untouched]

        return result

    def __str__(self):
        return f"Operator [From={self.from_}, To={self.to}]"

if __name__ == "__main__":
    o1 = Operator(from_=0, to=1)
    print(o1)

    jug = Jug([2, 0, 3])
    print("---------------")
    print("Jug:", jug)
    print("Precondition:", o1.precondition_fulfilled(jug))
    print("After:", o1.use(jug))

