def is_prime(n):
    for i in range(2,n):
        if n % i == 0:
            return False
    return True

def main():
    print("Is prime test")
    while(True):
        x = int(input("Enter number to check:"))
        if x < 2: continue
        if is_prime(x): print(f"{x} is a prime number")
        else: print(f"Nop, {x} is NOT a prime number")

main()