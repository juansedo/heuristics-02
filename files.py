def get_test_file(id):
    with open(f'data/mtVRP{id}.txt') as f:
      lines = [line.rstrip() for line in f]
      lines = [line.split() for line in lines]
      lines = [[int(x) for x in line] for line in lines]
    return [lines[0], lines[1:]]