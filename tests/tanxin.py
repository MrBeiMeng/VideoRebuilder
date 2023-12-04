def cover_interval(segments, interval):
    """
    Find the minimum number of segments to cover a given interval.

    :param segments: List of tuples representing the segments (start, end)
    :param interval: Tuple representing the target interval (start, end)
    :return: List of segments that cover the interval
    """
    # Sort the segments based on their starting point
    segments.sort(key=lambda x: x[0])

    # Initialize variables
    result = []
    current_end = interval[0]
    idx = 0
    n = len(segments)

    while current_end < interval[1] and idx < n:
        # Find the segment that covers the current end and reaches the farthest
        farthest_reach = current_end
        chosen_segment = None
        while idx < n and segments[idx][0] <= current_end:
            if segments[idx][1] > farthest_reach:
                farthest_reach = segments[idx][1]
                chosen_segment = segments[idx]
            idx += 1

        # If no segment can extend the coverage, break the loop
        if chosen_segment is None:
            break

        # Update the current end and add the chosen segment to the result
        current_end = farthest_reach
        result.append(chosen_segment)

    # Check if the entire interval is covered
    # if current_end < interval[1]:
    #     return None  # The interval can't be fully covered

    return result


# Example usage
segments = [(1, 4), (3, 5), (6, 8), (7, 10)]
interval = (2, 9)
print(cover_interval(segments, interval))
