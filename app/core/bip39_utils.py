# app/core/bip39_utils.py

from mnemonic import Mnemonic

def generate_bip39_mnemonic() -> str:
    """
    Generates a 12-word BIP39 mnemonic (English).
    """
    mnemo = Mnemonic("english")
    words = mnemo.generate(strength=128)  # 128 bits => 12 words
    return words
