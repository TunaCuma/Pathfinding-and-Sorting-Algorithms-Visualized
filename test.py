AAA = 3
b = 5

class Test:
    i = 3

    def change(self, a):
        Test.i = a

def deneme():
    AAA = 4
    print(AAA)
    print(b)
m = Test()
u = Test()
m.change(5)

print(m.i, u.i)
deneme()
print(AAA)