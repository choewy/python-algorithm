from enum import Enum
import hashlib


# 버킷 속성
class Attribute(Enum):
    OCCUPIED = 0  # 데이터
    EMTPY = 1  # 비어있음
    DELETED = 2  # 삭제됨


# 버킷
class Bucket:
    def __init__(self, key: any = None, value: any = None, attribute=Attribute.EMTPY) -> None:
        self.key = key              # 키
        self.value = value          # 값
        self.attribute = attribute  # 속성

    def set(self, key: any, value: any, attribute) -> None:
        self.key = key
        self.value = value
        self.attribute = attribute

    def set_attribute(self, attribute) -> None:
        self.attribute = attribute


# 오픈 주소법 해시
class OpenHash:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity            # 해시 테이블의 크기
        self.table = [Bucket()] * capacity  # 해시 테이블

    # 해시값 연산
    def hash_value(self, key: any) -> int:
        if isinstance(key, int):
            return key % self.capacity
        return int(hashlib.sha256(str(key).encode()).hexdigest(), 16) % self.capacity

    # 재해시값 연산
    def rehash_value(self, key: any) -> int:
        return (self.hash_value(key) + 1) % self.capacity

    # 버킷 검색
    def search_bucket(self, key: any) -> any:
        hash_value = self.hash_value(key)
        bucket = self.table[hash_value]

        for i in range(self.capacity):
            if bucket.attribute == Attribute.EMTPY:
                break
            elif bucket.attribute == Attribute.OCCUPIED and bucket.key == key:
                return bucket
            hash_value = self.rehash_value(hash_value)  # 재해시 수행
            bucket = self.table[hash_value]

        return None

    # 원소 추가
    def add(self, key: any, value: any) -> bool:
        if self.search(key) is not None:    # 이미 등록된 키
            return False

        hash_value = self.hash_value(key)
        bucket = self.table[hash_value]

        for i in range(self.capacity):
            if bucket.attribute == Attribute.EMTPY or bucket.attribute == Attribute.DELETED:
                self.table[hash_value]= Bucket(key, value, Attribute.OCCUPIED)
                return True

            hash_value = self.rehash_value(hash_value)  # 재해시 수행
            bucket = self.table[hash_value]
        return False

    # 원소 삭제
    def remove(self, key: any) -> int:
        bucket = self.search_bucket(key)
        if bucket is None:
            return False
        bucket.set_attribute(Attribute.DELETED)
        return True

    # 원소 검색
    def search(self, key: any) -> any:
        bucket = self.search_bucket(key)
        if bucket is not None:
            return bucket.value
        else:
            return None

    # 해시 테이블 덤프
    def dump(self) -> None:
        for hv in range(self.capacity):
            print(f'hash[{hv:2}]', end='\t')
            if self.table[hv].attribute == Attribute.OCCUPIED:
                print(f'{self.table[hv].key}({self.table[hv].value})')
            elif self.table[hv].attribute == Attribute.EMTPY:
                print('-- 미등록 --')
            elif self.table[hv].attribute == Attribute.DELETED:
                print('-- 삭제됨 --')


if __name__ == "__main__":
    Menu = Enum('Menu', ['add', 'remove', 'search', 'dump', 'exit'])

    def select_menu() -> Menu:
        text = [f'({item.value}){item.name}' for item in Menu]
        while True:
            print(*text, sep=" ", end="")
            menu_index = int(input(': '))
            if 0 <= menu_index <= len(Menu):
                return Menu(menu_index)

    open_hash = OpenHash(13)
    while True:
        menu = select_menu()

        if menu == Menu.add:
            print('입력 성공' if open_hash.add(int(input('key : ')), input('value : ')) else '입력 실패')

        elif menu == Menu.remove:
            print('삭제 성공' if open_hash.remove(int(input('key : '))) else '삭제 실패')

        elif menu == Menu.search:
            print('검색 결과 :', open_hash.search(int(input('key : '))))

        elif menu == Menu.dump:
            open_hash.dump()

        elif menu == Menu.exit:
            break

        else:
            continue
