import sympy as sm
from scipy.linalg import solve as linsolve

from utils import *


# Let p0(t) = p0(0) + t * v0 be the rock we throw

# For rocks i = 1, ..., n, we have intersection at different times ti
#      p0(ti) = p(ti)
#  <=> p0(0) + ti * v0 = pi(0) + vi * ti
#  <=> p0(0) - pi(0) = ti * (vi - v0)
#   => (p0(0) - pi(0)) x (vi - v0) = 0
# Trick 1: ti is a scalar, hence (p0(0) - pi(0)) and (vi - v0) are collinear,
#          hence their cross product is zero vector.
# We now have a quadratic equation

# Distributing the cross product,
#      (p0(0) - pi(0)) x (vi - v0) = 0
#  <=> p0(0) x vi + pi x (v0 - vi) = p0(0) x v0 = const  for all i
# Trick 2: notice that p0 x v0 is independent of i, hence the system is now LINEAR

# We have 6 unknowns, we don't know the constant though, so we need to solve expr1 - expr2 = 0, which has 3 components
# Hence, we need to stack expr1 - expr2 = 0, expr1 - expr3 = 0 with n = 3 data points

p0, p1, p2, p3 = get_vect('p^0', 'p^1', 'p^2', 'p^3', dim=3)
v0, v1, v2, v3 = get_vect('v^0', 'v^1', 'v^2', 'v^3', dim=3)


def get_expr(p0, v0, pi, vi):
    return p0.cross(vi) + pi.cross(v0 - vi)


system = sm.Matrix([
    get_expr(p0, v0, p1, v1) - get_expr(p0, v0, p2, v2),
    get_expr(p0, v0, p1, v1) - get_expr(p0, v0, p3, v3),
])
x = [e for x in (p0, v0) for e in x]
sym_A, sym_b = sm.linear_eq_to_matrix(system, x)

fun_A = sm.lambdify((p1, p2, p3, v1, v2, v3), sym_A)
fun_b = sm.lambdify((p1, p2, p3, v1, v2, v3), sym_b)


# Solve example
pos, vel = parse_data(example, dim=3)
A = fun_A(*pos[:3], *vel[:3])
b = fun_b(*pos[:3], *vel[:3])

x = linsolve(A, b).ravel()
print('Example')
print(f'{", ".join(x[:3].round(5).astype(str))} @ {", ".join(x[3:].round(5).astype(str))}')

# Solve data
pos, vel = parse_data(load_data(), dim=3)
A = fun_A(*pos[:3], *vel[:3])
b = fun_b(*pos[:3], *vel[:3])

x = linsolve(A, b).ravel()
print('-' * 50)
print('Data')
print(f'{", ".join(x[:3].round(0).astype(str))} @ {", ".join(x[3:].round(0).astype(str))}')
