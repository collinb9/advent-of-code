import sys
import re


def parse_valves(s: str):
    return list(re.findall(r"\d+|[A-Z]{2}", s))


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [parse_valves(line) for line in fp.readlines()]
    valves = dict()
    for item in data:
        valves[item[0]] = (int(item[1]), item[2:])

    return data[0][0], valves


def released_pressure(current_time, distance, rate, end=30):
    duration = max(0, end - current_time - distance)
    return rate * duration


def main(fpath):
    start, valves = read_data(fpath)
    distances = {vv: {} for vv in valves}

    sentinel = len(valves) * 2

    # Find shortes path between all pairs of points
    for vv in valves:
        for uu in valves[vv][1]:
            distances.get(vv, {})[uu] = 1
            distances.get(vv, {})[vv] = 0

    for vv in valves:
        for uu in valves:
            for ss in valves:
                distances.get(uu, {})[ss] = min(
                    distances.get(uu, {}).get(ss, sentinel),
                    distances.get(uu, {}).get(vv, sentinel)
                    + distances.get(vv, {}).get(ss, sentinel),
                )

    ## Insights
    # * Consider valves V and U which are distances Dv and Du away and will release total pressures of Pv and Pu.
    #   If du > dv, then it is only worth going to U if Pu > Pv
    # i.e., if going to a closer valve and then a farther releases more pressure than going to a farther one and then back, then you should do the latter
    # Indeed, going to the further one via the closer one only costs 1 additional minute than skipping over the closer one

    # Find optimal path - greedy algorithm
    END = 30
    i = 1
    current = start
    total = 0
    while i <= END:
        flow_data = dict()
        # Calculate the total amount of pressure that would be released from each valve if we went there now
        print(f"== Minute {i} ==")
        flow = 0
        _next = current
        # _next_candidate = current = vv
        for vv in valves:
            # print("Checking valve", vv)
            distance = distances[current][vv]
            if distance == sentinel:
                continue
            # print("Distance: ", distances[current][vv])
            _flow = released_pressure(i, distance, valves[vv][0], end=END)
            # flow_data[vv] = {""}
            if distance == 0:
                continue
            # print("Flow for this valve will be ", _flow)
            # if current == "JJ" and vv == "HH":
            #     flow = _flow
            #     _next = vv
            #     break

            if _flow > flow:
                # if current == "JJ":
                # print("Flow rate for (vv)", vv, ":", valves[vv][0])
                # print("Distance from (current)", current, "to (_next)", _next, "is", distances[current][_next])
                # print("Distance from (current)", current, "to (vv)", vv, "is", distances[current][vv])
                # print("Distance from (_next)", _next, " to (vv)", vv, "is", distances[_next][vv])

                if distances[current][_next] < distances[current][vv]:
                    # print("Checking a further point")
                    # if current == "JJ":
                    #     print("Pressure released by further point on its own is", _flow)
                    #     print(
                    #         "Pressure released by the closer point",
                    #         _next,
                    #         "is",
                    #         released_pressure(
                    #             i,
                    #             distances[current][_next],
                    #             valves[_next][0],
                    #             end=END,
                    #         ),
                    #     )
                    #     print(
                    #         "Pressure released by the further point",
                    #         vv,
                    #         "is",
                    #         released_pressure(
                    #             i + distances[current][_next] + 1,
                    #             distances[_next][vv],
                    #             valves[vv][0],
                    #             end=END,
                    #         ),
                    #     )
                    if _flow < released_pressure(
                        i,
                        distances[current][_next],
                        valves[_next][0],
                        end=END,
                    ) + released_pressure(
                        i + distances[current][_next] + 1,
                        distances[_next][vv],
                        valves[vv][0],
                        end=END,
                    ):
                        if released_pressure(
                            i,
                            distances[current][_next],
                            valves[_next][0],
                            end=END,
                        ) + released_pressure(
                            i + distances[current][_next] + 1,
                            distances[_next][vv],
                            valves[vv][0],
                            end=END,
                        ) > released_pressure(
                            i,
                            distances[current][vv],
                            valves[vv][0],
                            end=END,
                        ) + released_pressure(
                            i + distances[current][vv] + 1,
                            distances[vv][_next],
                            valves[_next][0],
                            end=END,
                        ):
                            continue

                flow = _flow
                _next = vv
                # print("Setting next to ", current)
        if _next == current:
            print("NOWHERE TO MOVE, STOPPING")
            break
        distance = distances[current][_next]
        current = _next

        total += flow
        i += distance + 1
        print(
            "You move to and open valve",
            current,
            "at minute",
            i - 1,
            "which has a flow rate of",
            valves[current][0],
            "And will release a total pressure of",
            flow,
            "Jumping to minute",
            i,
        )

        valves[current] = (0, valves[current][1])
        # break

    return total, 0


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)
