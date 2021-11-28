def app(a , x_n , n ):
    x_n1 = 0
    for i in range(n):
        x_n1 = 1/2 * (x_n + a/x_n)
        x_n = x_n1
    return x_n1

a = float(input(" Enter a number to approximate its square root : "))

n = int(input(" n : "))

x_n = float(input(" Enter a guess : "))

print(app(a , x_n , n))

