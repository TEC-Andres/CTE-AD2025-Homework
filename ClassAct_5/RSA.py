def rsa_crypt(key, value: int) -> int:
    n, exp = key
    if value >= n:
        raise ValueError("Message too large for modulus")
    return pow(value, exp, n)

if __name__ == "__main__":
    # Primes
    p = 12112572818808449571731807900411592884580333783004921220036314205922081529365512636323573404792363495042987361979515747470822505559167163939254402502476302604462332232098357347816254913444054071773754360834540498272192974899588178228937337976457776002975701508061478120414696120848850869270689503237265357014664150303285163162363100503796599696257868364570099238521754121591549467756150197608766818532287541184670177846734220167344613651218977558122945458294269016799447107522487935760001671159477553
    q = 14423872683440479050886524646105853804158654552017475284103259631845308899548514037388504364190204962218463011946278757823138594761009688229478206772822110657960643973429464487398166689106154955704159002068787506343909550603950103503398360090558372805455633693863420834158654215094998701149629230482785979309621230883456631251329578316564995669244293150395492859037399229150600462621669051001397990721821860831763866861844109888796631605221464409812333213750408126662568144972243795386122477898479601
    
    n = p * q                   # Modulus (coprime)
    phi = (p - 1) * (q - 1)     # Phi(p,q)
    e = 65537                   # Small public exponent
    d = pow(e, -1, phi)         # Private exponent
    pub = (n, e)                # Public key
    priv = (n, d)               # Private key

    text = input("Enter message to encrypt: ")
    message_int = int.from_bytes(text.encode(), "big")

    c = rsa_crypt(pub, message_int)
    m2_int = rsa_crypt(priv, c)

    # Displaying results
    print("Original:", text)
    print("Encrypted:", c)
    print("Private key:", priv)

    # Decrypting with provided encrypted integer and private key
    encrypted_input = int(input("Enter encrypted integer to decrypt: "))
    priv_n = int(input("Enter private key modulus n: "))
    priv_d = int(input("Enter private key exponent d: "))
    decrypted_int = rsa_crypt((priv_n, priv_d), encrypted_input)
    decrypted_text = decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, "big").decode()
    print("Decrypted from encrypted input and private key:", decrypted_text)
