import ctypes


class Uint64(int):
    def __new__(cls, value=0):
        return super().__new__(cls, ctypes.c_uint64(value).value)

    def __add_python_int(self, other: int):
        return super().__add__(other)

    def __add_uint64_t(self, other: 'Uint64'):
        return Uint64(self.value + other.value)

    def __add__(self, other):
        if isinstance(other, Uint64):
            return self.__add_uint64_t(other)
        else:
            return self.__add_python_int(other)

    def __sub__(self, other):
        if isinstance(other, Uint64):
            return Uint64(self.value - other.value)
        else:
            return self.__add__(-other)

    def __str__(self):
        return f"Uint64({self.value})"

    def __repr__(self):
        return self.__str__()

    def __mul_python_int(self, other: int):
        return super().__mul__(other)

    def __mul_uint64_t(self, other: 'Uint64'):
        return Uint64(self.value * other.value)

    def __mul__(self, other):
        if isinstance(other, Uint64):
            return self.__mul_uint64_t(other)
        else:
            return self.__mul_python_int(other)

    # left shift
    def __lshift__(self, other):


    @property
    def value(self):
        return ctypes.c_uint64(self).value

    @property
    def size(self):
        return Uint64(64)


if __name__ == '__main__':
    a = Uint64(2 ** 64 - 1)
    print(a)
    print(a + 1)
    print(a + Uint64(1))
    ...
