E = 5
phiofn = 12

possible_numbers = filter(lambda D: D * E % phiofn == 1, range(1, 100))

for number in possible_numbers:
    print(number)

# De volgende waardes kunnen gebruikt worden
# [5, 17, 29, 41, 53, 65, 77, 89]