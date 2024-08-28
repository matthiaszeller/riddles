import numpy as np
import sympy as sm
import torch
from scipy.optimize import minimize

sm.init_printing(use_unicode=True)

from utils import *


#     pi(ti) = q(ti)
# <=> pi(0) + vi * ti = q(0) + u * ti, non linear because u, q(0), ti are unknown

def fun_pos(pos, vel, t):
    return pos + vel * t


def residuals(q0, u, t, p, v):
    t = t.reshape(-1, 1)
    diff = fun_pos(q0, u, t) - fun_pos(p, v, t)
    res = (diff ** 2).mean()
    return res


def extract_unknowns(X):
    q0 = X[:3]
    u = X[3:6]
    t = X[6:]
    return q0, u, t


def fun_wrapper(X, p, v):
    q0, u, t = extract_unknowns(X)
    return residuals(q0, u, t, p, v)


def jacobian_torch(X, p, v):
    X = torch.tensor(X, dtype=torch.float64, requires_grad=True)
    p = torch.tensor(p, dtype=torch.float64)
    v = torch.tensor(v, dtype=torch.float64)

    loss = fun_wrapper(X, p, v)
    loss.backward()
    return X.grad.numpy()


def solve(pos, vel):
    X0 = np.concatenate([
        pos.mean(axis=0),
        vel.mean(axis=0),
        np.ones(pos.shape[0]) * np.ptp(pos) / 2
    ])
    res = minimize(
        fun_wrapper,
        X0,
        args=(pos, vel),
        # jac=jacobian_torch
    )
    return res


def print_sol(res, round=5):
    print(f'residuals: {res.fun:.5} after {res.nit} iterations')
    q0, u, t = extract_unknowns(res.x.round(round))
    print(f'rock: {", ".join(q0.astype(str))} @ {", ".join(u.astype(str))}')


def standardize(data):
    mu = data.mean(axis=0)
    s = data.std(axis=0)
    return (data - mu) / s, mu, s


def unstandardize(data, mean , s):
    return s * data + mean


def solve_standardized(pos, vel):
    pos, mu_p, s_p = standardize(pos)
    vel, mu_v, s_v = standardize(vel)
    res = solve(pos, vel)
    q0, u, t = extract_unknowns(res.x)
    q0 = unstandardize(q0, mu_p, s_p)
    u = unstandardize(u, mu_v, s_v)
    res.x = np.concatenate((q0, u, t))
    return res


pos, vel = parse_data(example, dim=3)
res = solve(pos, vel)
print_sol(res)

res = solve_standardized(pos, vel)
print_sol(res)

print('-' * 50)

# pos, vel = parse_data(load_data(), dim=3)
# res = solve(pos, vel)
# print_sol(res)


# pos, mu_p, s_p = standardize(pos)
# vel, mu_v, s_v = standardize(vel)
# q0 = unstandardize(q0, mu_p, s_p)
# u = unstandardize(u, mu_v, s_v)
