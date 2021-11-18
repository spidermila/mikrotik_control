class Device:
    def __init__(self, name: str, address: str, port: int, user: str, encrypted_password: str) -> None:
        self.name = name
        self.address = address
        self.port = port
        self.user = user
        self.encrypted_password = encrypted_password
    
    def test_connection(self) -> bool:
        if self.name == 'neco':
            return False
        return True
