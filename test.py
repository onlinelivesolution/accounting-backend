from common.utils.systemadmin_security import hash_password, verify_password

password = "123456"

hashed = hash_password(password)

print("HASH:", hashed)

print("CHECK:", verify_password("123456", hashed))
