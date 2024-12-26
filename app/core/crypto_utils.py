# app/core/crypto_utils.py

import ecdsa
import hashlib

def generate_key_pair():
    """
    Generate a private/public key pair using ECDSA (secp256k1).
    Return (private_key_hex, public_key_hex).
    """
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    private_key_hex = sk.to_string().hex()
    public_key_hex = vk.to_string().hex()
    return private_key_hex, public_key_hex

def derive_wallet_address(public_key_hex: str) -> str:
    """
    Derive a wallet address from the public key (simplified).
    We'll just do a double SHA-256 for demonstration.
    """
    sha_once = hashlib.sha256(bytes.fromhex(public_key_hex)).hexdigest()
    sha_twice = hashlib.sha256(bytes.fromhex(sha_once)).hexdigest()
    # In real systems, you might do Base58Check, etc.
    # We'll just take a short substring to keep it readable
    return "0x" + sha_twice[:40]  # 20 bytes (40 hex chars)
