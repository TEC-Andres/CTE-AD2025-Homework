def print_counter(start, stop, step):
    print("Sequence: ", end='')
    for i in range(start, stop, step):
        print(f"{i}", end=' ')

def count_hits_in_range(start, stop, step, threshold):
    print_counter(start, stop, step)

    count = 0
    for i in range(start, stop, step):
        if i <= threshold:
            count += 1
    print(f"\nValues: <= {threshold} : {count}")

    if count == 0:
        print(f"\nNo values within the threshold {threshold}")
    return

if __name__ == "__main__":
    start, stop, step, threshold = int(input("Place start: ")), int(input("Place stop: ")), int(input("Place step: ")), int(input("Place threshold: "))
    count_hits_in_range(start, stop, step, threshold)