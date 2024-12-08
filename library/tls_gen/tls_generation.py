from datetime import datetime, timedelta
import ipaddress

def generate_tls_certificate(hostname, ip_addresses=None, key=None):
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization

    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    with open("private_key.pem", "wb") as f:
        f.write(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    csr = (
        x509.CertificateSigningRequestBuilder()
        .subject_name(
            x509.Name(
                [
                    x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
                    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
                    x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
                    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Company"),
                    x509.NameAttribute(NameOID.COMMON_NAME, u"mywebsite.com"),
                ]
            )
        )
        .sign(key, hashes.SHA256())
    )

    with open("csr.pem", "wb") as f:
        f.write(csr.public_bytes(serialization.Encoding.PEM))




