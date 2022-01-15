from enum import Enum


class FixedStack:

    class Full(Exception):
        pass

    class Null(Exception):
        pass

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity        # 스택의 크기 초기화
        self.stack = [None] * capacity  # 본체 초기화
        self.pointer = 0                # 포인터 초기화

    def __len__(self) -> int:
        return self.pointer

    def is_null(self) -> bool:
        return self.pointer <= 0

    def is_full(self) -> bool:
        return self.pointer == self.capacity

    def push(self, value: any) -> None:
        if self.is_full():
            raise FixedStack.Full       # 예외 처리 발생
        self.stack[self.pointer] = value
        self.pointer += 1

    def pop(self) -> any:
        if self.is_null():
            raise FixedStack.Null       # 예외 처리 발생
        self.pointer -= 1
        return self.stack[self.pointer]

    def peek(self) -> any:
        if self.is_null():
            raise FixedStack.Null       # 예외 처리 발생
        return self.stack[self.pointer - 1]

    def clear(self) -> None:
        self.pointer = 0

    def find(self, value: any) -> int:
        for i in range(self.pointer - 1, -1, -1):   # 꼭대기부터 선형 검색
            if self.stack[i] == value:
                return i
        return -1

    def count(self, value: any) -> int:
        count = 0
        for i in range(self.pointer):   # 바닥부터 선형 검색
            if self.stack[i] == value:
                count += 1
        return count

    def __contains__(self, value: any) -> bool:
        return value in self.stack

    def dump(self) -> None:
        if self.is_null():
            print('Stack is Empty')
        else:
            print(self.stack[:self.pointer])


if __name__ == "__main__":
    Menu = Enum('Menu', ['push', 'pop', 'peek', 'find', 'dump', 'exit'])

    def select_menu() -> Menu:
        text = [f'({item.value}){item.name}' for item in Menu]
        while True:
            print(*text, sep=" ", end="")
            num = int(input(': '))
            if 0 <= num <= len(Menu):
                return Menu(num)

    fixed_stack = FixedStack(64)

    while True:
        print(f"현재 데이터 개수 : {len(fixed_stack)} / {fixed_stack.capacity}")
        menu = select_menu()

        if menu == Menu.push:
            val = int(input('value : '))
            try:
                fixed_stack.push(val)
            except FixedStack.Full:
                print('Stack is Full')

        elif menu == Menu.pop:
            try:
                print(f"pop : {fixed_stack.pop()}")
            except FixedStack.Null:
                print('Stack is Empty')

        elif menu == Menu.peek:
            try:
                print(f"peek : {fixed_stack.peek()}")
            except FixedStack.Null:
                print('Stack is Empty')

        elif menu == Menu.find:
            val = int(input('value : '))
            if val in fixed_stack:
                print(f"count : {fixed_stack.count(val)}")
                print(f"index : {fixed_stack.find(val)}")
            else:
                print(f"{val} is not exist")

        elif menu == Menu.dump:
            fixed_stack.dump()

        elif menu == Menu.exit:
            break

        else:
            continue
