sum = 0

for i in range(13):
    for j in range(13):
        print((i,j))
        sum += j
        sum += i

print(sum - 24)