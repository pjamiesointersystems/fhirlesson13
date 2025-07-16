def count_up_to(max_value):
    """Generator that yields numbers from 1 to max_value."""
    current = 1
    while current <= max_value:
        yield current  # Yield the current number and pause the function here.
        current += 1  # Resume here on the next iteration.


if __name__ == "__main__":
# Using the generator:
  for number in count_up_to(10):
     print(number)