from enum import Enum


class FixedQueue:

    class Full(Exception):              # 큐가 가득 차있을 때 예외 처리
        pass

    class Null(Exception):              # 큐가 비어있을 때 예외 처리
        pass

    def __init__(self, capacity: int) -> None:
        self.no = 0                     # 현재 데이터 개수 초기화
        self.front = 0                  # 프론트 초기화
        self.rear = 0                   # 리어 초기화
        self.capacity = capacity        # 큐의 크기 초기화
        self.queue = [None] * capacity  # 본체 초기화

    def __len__(self) -> int:
        return self.no

    def is_null(self) -> bool:
        return self.no <= 0

    def is_full(self) -> bool:
        return self.no >= self.capacity

    def enqueue(self, value: any) -> None:
        if self.is_full():
            raise FixedQueue.Full       # 예외 처리 발생
        self.queue[self.rear] = value
        self.rear += 1
        self.no += 1
        if self.rear == self.capacity:  # 리어와 큐의 크기가 같은 경우
            self.rear = 0               # 리어가 다시 맨 처음을 가리키도록 변경

    def dequeue(self) -> any:
        if self.is_null():
            raise FixedQueue.Null       # 예외 처리 발생
        value = self.queue[self.front]
        self.front += 1
        self.no -= 1
        if self.front == self.capacity: # 프론트와 큐의 크기가 같은 경우
            self.front = 0              # 프론트가 다시 맨 처음을 가리키도록 변경
        return value

    def peek(self) -> any:
        if self.is_null():
            raise FixedQueue.Null       # 예외 처리 발생
        return self.queue[self.front]

    def clear(self) -> None:
        self.no = self.front = self.rear = 0

    def find(self, value: any) -> int:
        for i in range(self.no):                    # 데이터 개수만큼 선형검색하되,
            idx = (i + self.front) % self.capacity  # front → rear 순으로 스캔하도록 연산
            if self.queue[idx] == value:
                return idx
        return -1

    def count(self, value: any) -> int:
        count = 0
        for i in range(self.no):                    # 데이터 개수만큼 선형검색하되,
            idx = (i + self.front) % self.capacity  # front → rear 순으로 스캔하도록 연산
            if self.queue[idx] == value:
                count += 1
        return count

    def __contains__(self, value: any) -> bool:
        return value in self.queue

    def dump(self) -> None:
        if self.is_null():
            print('Queue is Empty')
        else:
            for i in range(self.no):
                idx = (i + self.front) % self.capacity
                print(self.queue[idx], end="")
            print()


if __name__ == "__main__":
    Menu = Enum('Menu', ['enqueue', 'dequeue', 'peek', 'find', 'dump', 'exit'])

    def select_menu() -> Menu:
        text = [f'({item.value}){item.name}' for item in Menu]
        while True:
            print(*text, sep=" ", end="")
            num = int(input(': '))
            if 0 <= num <= len(Menu):
                return Menu(num)

    fixed_queue = FixedQueue(64)

    while True:
        print(f"현재 데이터 개수 : {len(fixed_queue)} / {fixed_queue.capacity}")
        menu = select_menu()

        if menu == Menu.enqueue:
            val = int(input('value : '))
            try:
                fixed_queue.enqueue(val)
            except fixed_queue.Full:
                print('Queue is Full')

        elif menu == Menu.dequeue:
            try:
                print(f"pop : {fixed_queue.dequeue()}")
            except fixed_queue.Null:
                print('Queue is Empty')

        elif menu == Menu.peek:
            try:
                print(f"peek : {fixed_queue.peek()}")
            except fixed_queue.Null:
                print('Queue is Empty')

        elif menu == Menu.find:
            val = int(input('value : '))
            if val in fixed_queue:
                print(f"count : {fixed_queue.count(val)}")
                print(f"index : {fixed_queue.find(val)}")
            else:
                print(f"{val} is not exist")

        elif menu == Menu.dump:
            fixed_queue.dump()

        elif menu == Menu.exit:
            break

        else:
            continue
