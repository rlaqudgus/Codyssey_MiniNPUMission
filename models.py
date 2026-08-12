# models.py - 2차원 행렬 데이터 구조 정의

class Array2D:
    def __init__(self, data):
        """
        data: 2차원 리스트 ex) [[1,2],[3,4]]
        """
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0])

    def get(self, i, j):
        """(i, j) 위치의 값 반환"""
        return self.data[i][j]

    def set(self, i, j, v):
        """(i, j) 위치에 값 v 저장"""
        self.data[i][j] = v

    def size(self):
        """(행 수, 열 수) 반환"""
        return self.rows, self.cols

    def sum(self):
        """행렬의 모든 원소 합산 반환"""
        total = 0
        for i in range(self.rows):
            for j in range(self.cols):
                total += self.data[i][j]
        return total
        



# my_Array = Array2D([[0,1,0],[1,1,1],[0,1,0]])
# print(my_Array.get(0,0))
# my_Array.set(0,0,100)
# print(my_Array.get(0,0))
# print(my_Array.size())
