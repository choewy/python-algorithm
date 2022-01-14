# 선형검색(=순차검색, Sequence Search)
class LinearSearch:
    def __init__(self, iterator: iter):
        self.iterator = iterator

    # while 문 사용
    def version_1(self, key) -> int:
        counter = 0     # 카운터

        i = 0
        while True:
            counter += 1
            if i == len(self.iterator):
                print(f"총 반복 횟수 : {counter}")
                return -1
            if self.iterator[i] == key:
                print(f"총 반복 횟수 : {counter}")
                return i
            i += 1

    # for 문 사용
    def version_2(self, key) -> int:
        counter = 0     # 카운터

        if len(self.iterator) == 0:
            return -1
        else:
            for i, value in enumerate(self.iterator):
                counter += 1
                if key == value:
                    print(f"총 반복 횟수 : {counter}")
                    return i

            print(f"총 반복 횟수 : {counter}")
            return -1

    # 보초법(sentinel method) 사용
    def version_3(self, key) -> int:
        counter = 0     # 카운터

        iterator = [x for x in self.iterator] + [key]

        i = 0
        while True:
            counter += 1
            if iterator[i] == key:
                break
            i += 1

        print(f"총 반복 횟수 : {counter}")
        return -1 if i == len(self.iterator) else i


if __name__ == '__main__':
    lst = [1, 3, 4, 5, 6, 7, 8, 11]
    target = 7
    linear_search = LinearSearch(lst)
    search_index = linear_search.version_3(target)

    if search_index == -1:
        print('검색실패')
    else:
        print(f'{target}의 인덱스 : {search_index}')
