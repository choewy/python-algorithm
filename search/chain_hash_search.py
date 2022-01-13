from enum import Enum
import hashlib


# 노드
class Node:
    def __init__(self, key: any, value: any, node):
        self.key = key      # 키
        self.value = value  # 값
        self.next = node    # 다음 노드


# 체인법 해시
class ChainHash:
    def __init__(self, capacity: int):
        self.capacity = capacity            # 해시 테이블의 크기
        self.table = [None] * capacity      # 해시 테이블

    # 해시값 연산
    def hash(self, key: any) -> int:
        if isinstance(key, int):
            return key % self.capacity              # key type == int
        byte_str = str(key).encode()                # key → str 변환 후 바이트 문자열 생성
        hash_value = hashlib.sha256(byte_str)       # 주어진 바이트 문자열의 해시값
        hex_int = hash_value.hexdigest()            # 해시값을 16진수 문자열로 변환
        return int(hex_int, 16) % self.capacity     # key type == int

    # 원소 추가
    def add(self, key: any, value: any) -> bool:
        hash_value = self.hash(key)
        node = self.table[hash_value]

        while node is not None:     # 이미 등록된 키
            if node.key == key:
                return False
            node = node.next

        temp = Node(key, value, self.table[hash_value])
        self.table[hash_value] = temp
        return True

    # 원소 삭제
    def remove(self, key: any) -> bool:
        hash_value = self.hash(key)
        node = self.table[hash_value]
        pre_node = None

        while node is not None:
            if node.key == key:
                if pre_node is not None:
                    self.table[hash_value] = node.next
                else:
                    pre_node.next = node.next
                return True
            pre_node = node
            node = pre_node.next
        return False

    # 원소 검색
    def search(self, key: any) -> any:
        hash_value = self.hash(key)
        node = self.table[hash_value]

        while node is not None:
            if node.key == key:
                return node.value
            node = node.next

        return None

    # 해시 테이블 덤프
    def dump(self) -> None:
        for hv in range(self.capacity):
            node = self.table[hv]
            print(f'hash[{hv:2}]', end="")
            while node is not None:
                print(f' → {node.key}({node.value})', end='')
                node = node.next
            print()


if __name__ == "__main__":
    Menu = Enum('Menu', ['add', 'remove', 'search', 'dump', 'exit'])

    def select_menu() -> Menu:
        text = [f'({item.value}){item.name}' for item in Menu]
        while True:
            print(*text, sep=" ", end="")
            menu_index = int(input(': '))
            if 0 <= menu_index <= len(Menu):
                return Menu(menu_index)

    chain_hash = ChainHash(13)

    while True:
        menu = select_menu()

        if menu == Menu.add:
            print('입력 성공' if chain_hash.add(int(input('key : ')), input('value : ')) else '입력 실패')

        elif menu == Menu.remove:
            print('삭제 성공' if chain_hash.remove(int(input('key : '))) else '삭제 실패')

        elif menu == Menu.search:
            print("검색 결과 :", chain_hash.search(int(input('key : '))))

        elif menu == Menu.dump:
            chain_hash.dump()

        elif menu == Menu.exit:
            break

        else:
            continue
