import hashlib

class User:

    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = self.encrypt_password(password)

    @staticmethod
    def encrypt_password(password):
        # Hash the password using SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password

    def verify_password(self, input_password):
        # Verify if the input password matches the stored hash
        return self.password == self.encrypt_password(input_password)


if __name__ == "__main__":
    # Create a user
    user = User("testuser", "mypassword123")
    print(f"Username: {user.user_name}")
    print(f"Encrypted Password: {user.password}")

    # Verify password
    print(user.verify_password("mypassword123"))  # Output: True
    print(user.verify_password("wrongpassword"))  # Output: False
