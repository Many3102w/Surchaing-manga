from pywebpush import webpush
# Actually pywebpush doesn't have a direct key generation function exposed easily in top level sometimes
# Let's use cryptography directly which is a dependency
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()

private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# We need the raw bytes for the public key to base64 encode for VAPID? 
# Usually VAPID public key is the uncompressed point.
# Let's use specific encoding:
public_numbers = public_key.public_numbers()
x = public_numbers.x.to_bytes(32, byteorder='big')
y = public_numbers.y.to_bytes(32, byteorder='big')
# Uncompressed point format: 0x04 + x + y
public_bytes = b'\x04' + x + y

import base64
def to_b64(b):
    return base64.urlsafe_b64encode(b).decode('utf-8').rstrip('=')

print(f"VAPID_PRIVATE_KEY={to_b64(private_key.private_numbers().private_value.to_bytes(32, byteorder='big'))}")
print(f"VAPID_PUBLIC_KEY={to_b64(public_bytes)}")
