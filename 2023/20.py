import sys
import collections
import copy


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.replace("\n", "").split("->") for line in fp.readlines()]
        # False = LOW or OFF, True = HIGH or ON
        data = {item[0].strip(): [False, {}, list(map(str.strip, item[1].split(",")))] for item in data}

    return data

# def calculate_hash(data):
#     keys = sorted()

def push_button(data, start="broadcaster", pulse=False, stop_condition=None):
    """DFS"""
    queue = collections.deque()
    # (previos_module, module, pulse)
    queue.append(("button", start, False))
    prev = start
    res = [0, 0]
    res2 = 0
    while len(queue) > 0:
        prev, current, pulse = queue.popleft()
        res[pulse] += 1
        if stop_condition is not None:
            if current == stop_condition[0]:
                print("Hit rx. Pulse:", pulse)
                if pulse == stop_condition[1]:
                    res2 += 1
        # print(f"{prev} -{'high' if pulse else 'low'}-> {current}")
        if current == start:
            state = data[current]
        else:
            state = data.get("%" + current)
            if state is not None: # %
                if not pulse: # Low
                    state[0] = not(state[0]) # Flip state
                    if state[0]: # On
                        pulse = True
                    else: # Off
                        pulse = False
                else:
                    continue

            else: # &
                state = data.get( "&" + current )
                if state is None:
                    continue
                state[1][prev] = pulse
                if all(xx for xx in state[1].values()):
                    # print(prev, current)
                    # print(state[1])
                    pulse = False
                else:
                    # print(prev, current)
                    # print(state[1])
                    pulse = True

        prev = current
        for dest in state[2]:
            queue.append((prev, dest, pulse))
    return res, res2

def main(fpath):
    data = read_data(fpath)
    for key in data:
        if key.startswith("&"):
            _key = key[1:]
            for kk, vv in data.items():
                if _key in vv[2]:
                    data[key][1][kk[1:]] = False
    # print(data)

    # print(data[start])

    data1 = copy.deepcopy(data)
    res = [0, 0]
    for _ in range(1000):
        [low, high], _ = push_button(data1)
        res[0] += low
        res[1] += high
    ans1 = res[0] * res[1]

    data2 = copy.deepcopy(data)
    ans2 = 0
    stop = 0
    while stop != 1:
        _, stop = push_button(data2, stop_condition=("rx", False))
        # print(stop)
        ans2 += 1
    # print(data)


    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)
