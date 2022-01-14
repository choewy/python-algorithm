from enum import Enum
import hashlib


# 버킷 속성
class Attribute(Enum):
    SAVED = 0       # 데이터 저장 상태
    NULL = 1        # 비어있는 상태
    DELETED = 2     # 삭제된 상태


# 버킷
class Bucket:
    def __init__(self, key: any = None, value: any = None,
                 attribute: Attribute = Attribute.NULL) -> None:
        self.key = key              # 키 초기화
        self.value = value          # 값 초기화
        self.attribute = attribute  # 속성 초기화

    def set(self, key: any, value: any, attribute: Attribute) -> None:
        self.key = key              # 키 변경
        self.value = value          # 값 변경
        self.attribute = attribute  # 속성 변경

    def set_attribute(self, attribute: Attribute) -> None:
        self.attribute = attribute  # 속성 변경


# 오픈 주소법 해시
class OpenHash:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity            # 해시 테이블의 크기 초기화
        self.table = [Bucket()] * capacity  # 해시 테이블 초기화

    # 해시값 연산
    def hash(self, key: any) -> int:
        if isinstance(key, int):
            return key % self.capacity          # key type == int
        byte_str = str(key).encode()            # key → str 변환 후 바이트 문자열 생성
        byte_hash = hashlib.sha256(byte_str)    # 주어진 바이트 문자열의 해시값
        key = byte_hash.hexdigest()             # 해시값을 16진수 문자열로 변환
        return int(key, 16) % self.capacity     # key type == int

    # 재해시값 연산
    def rehash(self, key: any) -> int:
        hash_value = self.hash(key) + 1
        return hash_value % self.capacity

    # 버킷 검색
    def bucket(self, key: any) -> any:
        hash_value = self.hash(key)
        bucket = self.table[hash_value]
        for i in range(self.capacity):
            if bucket.attribute == Attribute.NULL:
                break
            elif bucket.attribute == Attribute.SAVED and bucket.key == key:
                return bucket
            hash_value = self.rehash(hash_value)    # 재해시 수행
            bucket = self.table[hash_value]
        return None

    # 원소 검색
    def search(self, key: any) -> any:
        bucket = self.bucket(key)
        if bucket is not None:
            return bucket.value
        else:
            return None

    # 원소 추가
    def add(self, key: any, value: any) -> bool:
        if self.search(key) is not None:    # 이미 등록된 키
            return False

        hash_value = self.hash(key)
        bucket = self.table[hash_value]

        for i in range(self.capacity):
            if bucket.attribute == Attribute.NULL or bucket.attribute == Attribute.DELETED:
                self.table[hash_value] = Bucket(key, value, Attribute.SAVED)
                return True

            hash_value = self.rehash(hash_value)  # 재해시 수행
            bucket = self.table[hash_value]
        return False

    # 원소 삭제
    def remove(self, key: any) -> int:
        bucket = self.bucket(key)
        if bucket is None:
            return False
        bucket.set_attribute(Attribute.DELETED)
        return True

    # 해시 테이블 덤프
    def dump(self) -> None:
        for hv in range(self.capacity):
            print(f'hash[{hv:2}]', end='\t')
            if self.table[hv].attribute == Attribute.SAVED:
                print(f'{self.table[hv].key}({self.table[hv].value})')
            elif self.table[hv].attribute == Attribute.NULL:
                print('-- 미등록 --')
            elif self.table[hv].attribute == Attribute.DELETED:
                print('-- 삭제됨 --')


if __name__ == "__main__":
    Menu = Enum('Menu', ['add', 'remove', '검색 알고리즘', 'dump', 'exit'])

    def select_menu() -> Menu:
        text = [f'({item.value}){item.name}' for item in Menu]
        while True:
            print(*text, sep=" ", end="")
            num = int(input(': '))
            if 0 <= num <= len(Menu):
                return Menu(num)

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
