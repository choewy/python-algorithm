class BinarySearch:
    def __init__(self, sorted_iterator: iter):
        self.sorted_iterator = sorted_iterator

    def version_1(self, key: int) -> int:
        counter = 0     # 카운터

        left = 0
        right = len(self.sorted_iterator) + 1

        while True:
            counter += 1
            center = (left + right) // 2
            if self.sorted_iterator[center] == key:
                print(f"총 반복 횟수 : {counter}")
                return center
            elif self.sorted_iterator[center] < key:
                left = center + 1
            else:
                right = center - 1

            if left > right:
                break

        print(f"총 반복 횟수 : {counter}")
        return -1


if __name__ == "__main__":
    iterator = [1, 2, 3, 4, 6, 8, 9, 10, 11, 14]
    target = 11
    binary_search = BinarySearch(iterator)
    search_index = binary_search.version_1(target)
    print(f'{target}의 인덱스 : {search_index}')
