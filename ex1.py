import hashlib

while True:
    password = input("Enter your password: ")
    sha256 = hashlib.sha256(password.encode('utf-8')).hexdigest()
    print(sha256)



# bart tungsten
# bob 123456789
# carlton 123456789
# homer tungsten
# john 123456789
# lisa tungsten
# march tungsten
# william 123456789