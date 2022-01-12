import hashlib


# 해시를 구성하는 노드
class Node:
    def __init__(self, key: any, value: any, next):
        self.key = key
        self.value = value
        self.next = next


# 체인법 해시
class ChainHash:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.table = [None] * self.capacity

    def hash_value(self, key: any) -> int:
        if isinstance(key, int):
            return key % self.capacity
        return int(hashlib.sha256(str(key).encode()).hexdigest(), 16) % self.capacity

    def hash_search(self, key: any) -> any:
        hash_value = self.hash_value(key)
        node = self.table[hash_value]

        while node is not None:
            if node.key == key:
                return node.value
            node = node.next

        return None

    def hash_add(self, key: any, value: any) -> bool:
        hash_value = self.hash_value(key)
        node = self.table[hash_value]

        while node is not None:
            if node.key == key:
                return False
            node = node.next

        temp = Node(key, value, self.table[hash_value])
        self.table[hash_value] = temp
        return True

    def hash_remove(self, key: any) -> bool:
        hash_value = self.hash_value(key)
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

    def hash_dump(self) -> None:
        for hash_value in range(self.capacity):
            node = self.table[hash_value]
            print(f'hash[{hash_value}]', end="")
            while node is not None:
                print(f' → {node.key}({node.value})', end='')
                node = node.next
            print()


if __name__ == "__main__":

    # 메뉴
    class Menu:
        def __init__(self):
            self.items = ["추가", "삭제", "검색", "덤프", "종료"]

        def select(self) -> str:
            while True:
                print('메뉴를 입력하세요.', end="")
                print(f'({" ".join([f"{menu_item}:{i}" for i, menu_item in enumerate(self.items)])})')
                try:
                    item_index = int(input())
                    if 0 <= item_index < len(self.items):
                        return self.items[item_index]
                except:
                    pass

    chain_hash = ChainHash(13)

    menu = Menu()
    while True:
        item = menu.select()

        if item == '추가':
            print("key : ", end="")
            item_key = int(input())
            print("value : ", end="")
            item_value = input()
            result = chain_hash.hash_add(item_key, item_value)
            print("결과 :", "완료" if result else "실패")

        elif item == '삭제':
            print("key : ", end="")
            item_key = int(input())
            result = chain_hash.hash_remove(item_key)
            print("결과 :", "완료" if result else "실패")

        elif item == '검색':
            print("key : ", end="")
            item_key = int(input())
            print("결과 :", chain_hash.hash_search(item_key))

        elif item == "덤프":
            print(chain_hash.hash_dump())

        elif item == '종료':
            break
