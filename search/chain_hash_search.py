from enum import Enum
import hashlib


# 노드
class Node:
    def __init__(self, key: any, value: any, node):
        self.key = key      # 키 초기화
        self.value = value  # 값 초기화
        self.next = node    # 참조 노드 초기화


# 체인법 해시
class ChainHash:
    def __init__(self, capacity: int):
        self.capacity = capacity            # 해시 테이블의 크기 초기화
        self.table = [None] * capacity      # 해시 테이블 초기화

    # 해시값 연산
    def hash(self, key: any) -> int:
        if isinstance(key, int):
            return key % self.capacity          # key type == int
        byte_str = str(key).encode()            # key → str 변환 후 바이트 문자열 생성
        byte_hash = hashlib.sha256(byte_str)    # 주어진 바이트 문자열의 해시값
        key = byte_hash.hexdigest()             # 해시값을 16진수 문자열로 변환
        return int(key, 16) % self.capacity     # key type == int

    # 원소 검색
    def search(self, key: any) -> any:
        hash_value = self.hash(key)     # 해시값
        ref = self.table[hash_value]    # 참조 노드

        while ref is not None:
            if ref.key == key:          # 연결 리스트 노드에서 key를 찾은 경우
                return ref.value
            ref = ref.next

        return None                     # 연결 리스트 노드에서 key를 찾지 못한 경우

    # 원소 추가
    def add(self, key: any, value: any) -> bool:
        if self.search(key) is not None:
            return False                # 이미 등록된 키
        hash_value = self.hash(key)     # 해시값
        ref = Node(key, value, self.table[hash_value])
        self.table[hash_value] = ref
        return True                     # 등록 완료

    # 원소 삭제
    def remove(self, key: any) -> bool:
        hash_value = self.hash(key)     # 해시값
        ref = self.table[hash_value]    # 참조노드
        pref = None                     # 참조노드 앞의 노드
        while ref is not None:
            if ref.key == key:
                if pref is None:        # 앞의 노드가 없는 경우
                    self.table[hash_value] = ref.next
                else:                   # 앞의 노드가 있는 경우
                    pref.next = ref.next
                return True
            pref = ref
            ref = ref.next
        return False

    # 해시 테이블 덤프
    def dump(self) -> None:
        for hash_value in range(self.capacity):
            ref = self.table[hash_value]
            print(f'hash[{hash_value:2}]', end="")
            while ref is not None:
                print(f' → {ref.key}({ref.value})', end='')
                ref = ref.next
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
