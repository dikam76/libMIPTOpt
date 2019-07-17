def ternary_search_vec(xk, zk, func):
    a = 0.
    b = 1.
    while b - a > 1e-3:
        c = a + (b - a) / 3
        d = a + (b - a) / 3 * 2
        if func(xk * c + zk * (1 - c)) >= func(xk * d + zk * (1 - d)):
            a = c
        else:
            b = d
    return (b + a) / 2


def triangles_1_5(x0, func, grad, steps, L):
    xk = x0.copy()
    zk = x0
    ak = 1 / L
    res = [func(xk)]
    for i in range(1, steps):
        a_bigk = 1000 / i ** 0.5
        ak = 1 / L * 0.5 + (1 / L**2 * 0.25 + ak**2)**0.5
        alpha = ternary_search_vec(xk, zk, func)
        yk = xk * alpha + zk * (1 - alpha)
        xk -= ak * grad(yk)
        zk = xk * alpha + zk * (1 - alpha)
        a_bigk += ak
        res.append(func(xk))
    return xk, res


def ternary_search(a, b, xk, func, grad):
    while b - a > 1e-3:
        c = a + (b - a) / 3
        d = a + (b - a) / 3 * 2
        if func(xk - c * grad(xk)) >= func(xk - d * grad(xk)):
            a = c
        else:
            b = d
    return (b + a) / 2


def bin_pow_ray(a, b, xk, func, grad):
    c = (a + b) / 2
    if func(xk - c * grad(xk)) <= func(xk - b * grad(xk)):
        return ternary_search(a, b, xk, func, grad)
    else:
        return bin_pow_ray(b, 2 * b, xk, func, grad)


def triangles_2_0(x0, func, grad, steps):
    xk = x0.copy()
    zk = x0
    res = [func(xk)]
    for i in range(1, steps):
        a_bigk = 1000 / i ** 0.5
        ak = bin_pow_ray(0., 1., xk, func, grad)
        alpha = ternary_search_vec(xk, zk, func)
        yk = xk * alpha + zk * (1 - alpha)
        xk -= ak * grad(yk)
        zk = xk * alpha + zk * (1 - alpha)
        a_bigk += ak
        res.append(func(xk))
    return xk, res
