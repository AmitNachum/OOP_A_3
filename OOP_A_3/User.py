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
