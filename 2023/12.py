import sys
import itertools
import copy
import operator
import functools

def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.replace("\n", "").split() for line in fp.readlines()]

    return data


def possible(record, contiguous_groups):
    """Check if it is possible for this record to be split up into contiguous groups of given sizes"""
    # record = [item for item in record.split(".") if item]
    return False


def match(record, contiguous_groups):
    """Check if it is possible for this record to be split up into contiguous groups of given sizes"""
    record = [item for item in record.split(".") if item]
    for group, count in itertools.zip_longest(record, contiguous_groups):
        if group is None or count is None:
            return False
        if len(group) != count:
            return False
    return True

def find_all_partitions(data):
    full_partitions = []
    for record, contiguous_group_sizes in data:
        result = []
        stack = []
        stack.append((0, [[0, 0]]))
        while stack:
            # record_index = the index of the character in the record
            # partition_index = the index partition in contiguous_group_sizes
            # partitions = current partitioning applied. This is an array of ranges of partition indices
            #   e.g. [[0, 0], [1, 3]] means that the first group in the record is used for the first partition,
            #   and the second group is used for partitions 2,3,4
            record_index, partitions = stack.pop()
            partition_range = partitions[record_index]
            # print(record_index, partitions)
            _range = contiguous_group_sizes[partition_range[0] : partition_range[1] + 1]
            if (
                len(record[record_index])
                >= sum( _range) + len(_range) - 1
            ):  # Can partition it this way
                # print("Valid configuration so far")
                # Increment partition index if possible, otherwise we have hit the end
                if partition_range[1] == len(contiguous_group_sizes) - 1:
                    result.append(partitions)
                    continue
                if record_index < len(record) - 1: # Move to next chunk
                    # print("Move to next chunk")
                    _tuple = (
                            record_index + 1,
                            partitions
                            + [[partition_range[-1] + 1, partition_range[-1] + 1]],
                        )
                    # print("Appending:", _tuple)
                    stack.append(copy.deepcopy(_tuple))
                if partition_range[1] < len(contiguous_group_sizes) - 1:  # Continue partitioning this chunk
                    # print('Continue to partition this chunk')
                    partition_range[1] += 1
                    _tuple = (record_index, partitions)
                    # print("Appending:", _tuple)
                    stack.append(copy.deepcopy(_tuple))

        full_partitions.append(result)
    return full_partitions

def count_valid_arrangements(record, contiguous_group_sizes, partitions):
    ans1 = 0
    stack = [(0, 0)]
    # print(record, contiguous_group_sizes, partitions)
    while stack:
        record_index, shift = stack.pop()
        start, end = partitions[record_index]
        _group_range = contiguous_group_sizes[start : end + 1]
        # print("shift:", shift)
        # print("Checking", record, _index, contiguous_group_sizes, partitions, _partition, _range, "shifted by", shift)
        if start == end:
            if (_group_range[0] + shift == len(record[record_index])): # After the partition is the end of the chunk
                if (shift > 0 and record[record_index][shift-1] == "?") or shift == 0: # Check that the character before the chunk is a '?'
                    stack.append((record_index+1, 0))
            elif (record[_index][_group_range[0] + shift] == "?"): # Check that the character after the partition is a '?'
                if (shift > 0 and record[_index][shift-1] == "?") or shift == 0: # Check that the character before the chunk is a '?'
                    stack.append((record_index, shift + 1))
                    stack.append((record_index+1, 0))
        # for kk, ii in enumerate(_group_range):
        #     # print("ii:", ii)
        #     # print("kk:", kk)
        #     if record[record_index][sum(_group_range[: ii + 1]) + kk + shift] == "?": # Check that the character after the chunk is a '?'
        #         # print("Item is not '?', breaking")
        #         if (shift > 0 and record[record_index][shift-1] == "?") or shift == 0: # Check that the character before the chunk is a '?'
        #             stack.append((record_index+1, 0))
        #             stack.append((record_index, shift + 1))
        #     ans1 += 0
            # print("Ways of arranging each partition:", _partition_ans)
            # ans1 += functools.reduce(operator.mul, _partition_ans)
    # inner(record, contiguous_group_sizes, partitions, shift=0)
    return ans1

def main(fpath):
    data = read_data(fpath)
    for line in data:
        line[0] = [item for item in line[0].split(".") if item]
        line[1] = list(map(int, line[1].split(",")))
    # print(data)

    # Part 1
    # First idea is to split the problem into 2 parts:
    #   - Find all possible partitions that match the given sizes
    #   - For each valid partition, calculate the number of permutations that are valid

    ans1 = 0

    # Find all possible partitions

    full_partitions = find_all_partitions(data)
    for (record, contiguous_group_sizes), partitions in zip(data, full_partitions):
        ans1 += count_valid_arrangements(record, contiguous_group_sizes, partitions)


    # for (record, contiguous_group_sizes), partitions in zip(data, final_partitions):
    #     print(record, contiguous_group_sizes, partitions)
        # possible_partitions = []
        # _partition = []
        # current_parition = []
        # for group in record[::-1]:
        #     contiguous_group_size = contiguous_group_sizes.pop()
        #     _partition.insert(0, contiguous_group_size)
        #     if len(group) >= sum(partition) + len(partition)-1: # Can partition it this way
        #         current_partition.append(_partition)
        #         _partition = []

    # for record, contiguous_groups in data:
    #     stack = [record]
    #     while stack:
    #         _record = stack.pop()
    #         if possible(_record, contiguous_groups):  # Early stopping condition
    #             try:
    #                 i = _record.index("?")
    #             except ValueError:
    #                 if matches(
    #                     _record, contiguous_groups
    #                 ):  # This is a valid configuration
    #                     ans += 1
    #                 continue
    #             stack.append(_record[:i] + "." + _record[i:])
    #             stack.append(_record[:i] + "#" + _record[i:])
    # for chars, groups in data:
    #     if len(chars) == len(groups):
    #         for xx, yy in zip(chars, group):
    #             count = 0
    #             for _char in xx:
    #                 if xx == "?":
    #                     count += 1
    #             ans += itertools.combinations()
    return ans1, 0


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)
