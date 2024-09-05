from pathlib import Path

def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()
    
    
def parse_data(data: str):
    pass


def to_base10(n: str, base: int = 5):
    res = 0
    for i, digit in enumerate(n[::-1]):
        val = base ** i
        res += val * int(digit)

    return res


def from_base10(n: int, base: int = 5):
    if n == 0:
        return [0]

    digits = []
    while n > 0:
        a, b = divmod(n, base)
        digits.append(b)
        n = a

    return digits[::-1]


_SNAFU_TO_BASE_10 = {'1': 1, '2': 2, '-': -1, '=': -2, '0': 0}
_BASE10_TO_SNAFU = {v: k for k, v in _SNAFU_TO_BASE_10.items()}

def snafu_to_base10(n: str):
    res = 0
    for i, digit in enumerate(n[::-1]):
        val = 5 ** i
        res += val * _SNAFU_TO_BASE_10[digit]

    return res


def base10_to_snafu(n: int):
    """
    18 is a good example: 18 = 5^0 * 3 + 5^1 * 3, but 3 is not a SNAFU digit.

    n = 18, (a, b) = divmod(n, 5) = (3, 3)
            since 3 ∉ symbols, use symbol s = b - 5 = -2 ∈ symbols, use a CARRY OVER * (a += 1)
                -> n = 5^0 * (-2) + 5^1 * (3 + 1*)
            now assign (3+1*) to n

    n = 4,  (a, b) = divmod(n, 5) = (0, 4)
            since 4 ∉ symbols, we use symbol s = b - 5 = -1 ∈ symbols, use a CARRY OVER * (a += 1)
                -> n = 5^0 * (-1) + 5^1 * (1)

    n = 1,  (a, b) = divmod(n, 5) = (0, 1)
            use symbol 1
    """
    if n == 0:
        return '0'

    digits = []
    while n > 0:
        a, b = divmod(n, 5)
        if b in _BASE10_TO_SNAFU:
            digits.append(_BASE10_TO_SNAFU[b])
            n = a
        else:
            digits.append(_BASE10_TO_SNAFU[b-5])
            n = a + 1

    return ''.join(digits[::-1])


example = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""


data = """1=120=22222-=10-=
1--22-=-
21
1=0222=-1=-0--220=02
122102
22--=20==2===201
100-1-01=0-1
20200-2==220120-
2220-2200=000=
1==002=221-2
2--221-22=
1022=121=1-22=-01
2=1=1-1=02-=02=2=
1-21112=02
2=1-22021
1---=-221=-22122
10020
1=--101
1=12=02-1--12
1=0-=1002020-2=
120=1==201102==2==
2==-=0120112=2-=-
1---1
12=2--02-00==-22
12==1-=0-2=0--11--
1=10=0-1221
1=201-0-
22
10-0=21-2-1-2-=211
1=1--12==0=--1
2=-1022=1=-10-
12-02-2-
1=-1=00---
1=100120=101
112=01
20-22=00-=1=1=10
200--=0-221101=
10-2=01=-20
10=11=1
20-1-
2=012-002-02-1221
1==1=1-012100
10=221202-0-0-
1-0121-
2==1100-=
102=022=202
2=2-
21-2=12-22-1
1-2100
1-200101==0
2==0200-12012-=1=02
1=1010-2=22=2
1-2=-12-2-2=112=120
1=-=-
2-=
100=0-1-1=000
11=1-=2--00=0=2-=1
1221120122=11110-
111=10-002=
20=-=200
2==21
1=--2=-=2-102211
20=1=-0=1=
12
202=-0-=1220-0
1=0112=1-=-1
21-=-===0=-122000
1=
112010-11221=-00
112-2==102=2-1=1
1==-0=
1=01-11-211
21=-1-20--2=202122
1=01
20221
100
10=22-1=-1121-2
2-0=-
101012-200=010=
1011=0011
1-0202=0-11
101==10
10=
10111-1=-0
1112=0101=-
11=0=-1111-000
12=11
1102222=20
2=0=--==022-
11222
2100=
1=-0
12-11-2=-222-
1-10-012=21-0
1-2=
112
111=20
1221=-2
1===1==0010=0-
1-=1-==-=20"""


if __name__ == '__main__':
    for n in (12310, 2, 0, 4, 401, 420):
        res = to_base10(str(n), base=5)
        assert res == int(str(n), 5)

    for n in (0, 1, 5, 213, 91487, 129764):
        m = from_base10(n, base=5)
        m = ''.join(map(str, m))
        assert to_base10(m) == n

