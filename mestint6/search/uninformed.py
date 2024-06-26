# nem informált: nem használ valami féle heurisztikát
import time


# ZH: visszafele leolvasás listából (célból állapotból, induló állapotba) !!

def get_solution(goal_node):
    history = []

    n = goal_node

    while n is not None:
        history.append(n.operator)
        n = n.parent

    # return history reversed
    return history[::-1][1:]


class BackTrackNode:
    def __init__(self, state, parent, operator, applicable):
        self.state = state
        self.parent = parent
        self.operator = operator
        self.applicable = applicable

    # nem zh type str
    def __str__(self):
        return f"BackTrackNode [state={str(self.state)}, operator={str(self.operator)}"


class BackTrack:
    def __init__(self, delay_seconds):
        self.delay_seconds = delay_seconds

    def search(self, start_state, operators):
        # aktuális csomopont
        actual_node = BackTrackNode(
            state=start_state,
            parent=None,
            operator=None,
            applicable=list(filter(lambda o: o.precondition_fulfilled(start_state), operators))
        )
        while True:
            if actual_node is None:
                break
            if actual_node.is_goal_state():
                break
            if len(actual_node.applicable) > 0:
                operator = actual_node.applicable[0]
                actual_node.applicable = [o for o in actual_node.applicable if o != operator]

                new_node = BackTrackNode(
                    state=operator.use(actual_node.state),
                    parent=actual_node,
                    operator=operator,
                    applicable=None
                )
                new_node.applicable = list(filter(lambda o: o.precondition_fulfilled(new_node.state), operator))

                actual_node = new_node

            else:
                actual_node = actual_node.parent

            time.sleep(self.delay_seconds)
            print("Actual node:", actual_node)

        if actual_node is not None:
            print("Solution found:")
            print(get_solution(actual_node))
        else:
            print("No solution found during search")

        return actual_node


# same as BackTrack above but with update (shown in comments where the updates happened)
class BackTrackWithCircleMonitoring:
    def __init__(self, delay_seconds):
        self.delay_seconds = delay_seconds
        # update ("volt már" pszeudokodba)
        self.history = []

    # update
    def seen_already(self, state):
        return state in self.history

    def search(self, start_state, operators):
        # aktuális csomopont
        actual_node = BackTrackNode(
            state=start_state,
            parent=None,
            operator=None,
            applicable=list(filter(lambda o: o.precondition_fulfilled(start_state), operators))
        )
        while True:
            if actual_node.is_goal_state():
                break
            # update here
            if self.seen_already(actual_node.state):
                actual_node = actual_node.parent
            if actual_node is None:
                break
            self.history.append(actual_node.state)
            if len(actual_node.applicable) > 0:
                operator = actual_node.applicable[0]
                actual_node.applicable = [o for o in actual_node.applicable if o != operator]

                new_node = BackTrackNode(
                    state=operator.use(actual_node.state),
                    parent=actual_node,
                    operator=operator,
                    applicable=None
                )
                new_node.applicable = list(filter(lambda o: o.precondition_fulfilled(new_node.state), operator))

                actual_node = new_node

            else:
                actual_node = actual_node.parent

            time.sleep(self.delay_seconds)
            print("Actual node:", actual_node)

        if actual_node is not None:
            print("Solution found:")
            print(get_solution(actual_node))
        else:
            print("No solution found during search")

        return actual_node


# 5.het: szélességi kereső
# depth added
class TreeNode:
    def __init__(self, state, parent, operator, depth):
        self.state = state
        self.parent = parent
        self.operator = operator
        self.depth = depth

    # nem zh type str
    def __str__(self):
        return f"TreeNode [state={str(self.state)}, operator={str(self.operator)}"


class BreadthSearchAlgorithm:
    def __init__(self, delay_seconds=1):
        self.delay_seconds = delay_seconds

    def extend(self, node, open_nodes, closed_nodes, operators):
        for o in operators:
            if o.precondition_fulfilled(node.state):
                state = o.use(node.state)

                # ?? : next function
                state_in_open_nodes = next(filter(lambda n: n.state == state, open_nodes), None)

                state_in_closed_nodes = next(filter(lambda n: n.state == state, closed_nodes), None)

                if state_in_open_nodes is None and state_in_closed_nodes is None:
                    new_node = TreeNode(
                        state=state,
                        parent=node,
                        operator=o,
                        depth=node.depth + 1
                    )

                    open_nodes.append(new_node)

        open_nodes.remove(node)
        closed_nodes.append(node)

    def search(self, start_state, operators):
        # TODO: fix this
        new_node = TreeNode(
            state=start_state,
            parent=None,
            operator=None,
            depth=0
        )

        open_nodes = [new_node]
        closed_nodes = []

        while True:
            if len(open_nodes) == 0:
                break

            min_depth = min([n.depth for n in open_nodes])
            node = next(filter(lambda n: n.depth == min_depth, open_nodes))

            if node.state.is_goal_state():
                break

            self.extend(node, open_nodes, closed_nodes, operators)

            time.sleep(self.delay_seconds)

            print("node:", node)

        if len(open_nodes) != 0:
            print("Solution found:")
            print("\n".join([str(n) for n in get_solution(node)]))
        else:
            print("no solution found during search")

        return node


class DepthFirstSearch:
    def __init__(self, delay_seconds=1):
        self.delay_seconds = delay_seconds

    def extend(self, node, open_nodes, closed_nodes, operators):
        for o in operators:
            if o.precondition_fulfilled(node.state):
                state = o.use(node.state)

                # ?? : next function
                state_in_open_nodes = next(filter(lambda n: n.state == state, open_nodes), None)

                state_in_closed_nodes = next(filter(lambda n: n.state == state, closed_nodes), None)

                if state_in_open_nodes is None and state_in_closed_nodes is None:
                    new_node = TreeNode(
                        state=state,
                        parent=node,
                        operator=o,
                        depth=node.depth + 1
                    )

                    open_nodes.append(new_node)

            open_nodes.remove(node)
            closed_nodes.append(node)

    def search(self, start_state, operators):
        new_node = TreeNode(
            state=start_state,
            parent=None,
            operator=None,
            depth=0
        )

        open_nodes = [new_node]
        closed_nodes = []

        while True:
            if len(open_nodes) == 0:
                break

            max_depth = max([n.depth for n in open_nodes])
            node = next(filter(lambda n: n.depth == max_depth, open_nodes))

            if node.state.is_goal_state():
                break

            self.extend(node, open_nodes, closed_nodes, operators)

            time.sleep(self.delay_seconds)

            print("node:", node)

        if len(open_nodes) != 0:
            print("Solution found:")
            get_solution(node)
        else:
            print("no solution found during search")

        return node

