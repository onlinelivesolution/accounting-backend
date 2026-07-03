from common.utils.systemadmin_security import hash_password, verify_password

password = "admin123"

hashed = hash_password(password)

print("HASH:", hashed)

print("CHECK:", verify_password("admin123", hashed))
