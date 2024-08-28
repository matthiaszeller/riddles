import sympy as sm
from sympy import symbols, init_printing

from utils import *

init_printing(use_unicode=True)


# Solve equations
p, q, u, v = get_vect('p', 'q', 'u', 'v')
t, tp = symbols("t t'")

pt = p + v * t
qt = q + u * tp

res = sm.solve(pt - qt, t, tp)

fun_t = sm.lambdify([p, q, u, v], res[t])
fun_tp = sm.lambdify([p, q, u, v], res[tp])

# Data
pos, vel = parse_data(load_data(), dim=2)


def solve(pos, vel, area=(7, 27)):
    amin, amax = area

    def format_pv(p, v):
        p, v = p.astype(str), v.astype(str)
        return f'{", ".join(p)} @ {", ".join(v)}'

    # determine which paths are parallel
    vel_norm = norm(vel)
    P = vel_norm @ vel_norm.T  # parallel path have value ~ 1
    P = 1 - np.abs(P) < 1e-12

    n = len(pos)
    n_collision = 0
    for i in range(n):
        for j in range(i+1, n):
            p, v = pos[i], vel[i]
            q, u = pos[j], vel[j]

            print(f'i = {i}: {format_pv(p, v)}')
            print(f'j = {j}: {format_pv(q, u)}')

            if P[i, j]:
                print('paths are parallel', end='\n\n')
                continue

            t = fun_t(p, q, u, v)
            tp = fun_tp(p, q, u, v)
            pos_cross = p + v * t
            inside = ((pos_cross >= amin) & (pos_cross <= amax)).all()
            future = (t >= 0) and (tp >= 0)

            if inside and future:
                n_collision += 1

            print("inside" if inside else "outside", end=' ')
            print(f'(x={pos_cross[0]:.5}, y={pos_cross[1]:.5})', end=' ')
            print(f"(t={t:.5}, t'={tp:.5})", end='\n\n')

    return n_collision


n = solve(pos, vel, area=(200000000000000, 400000000000000))
