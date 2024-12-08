from datetime import datetime, timedelta
import ipaddress

def generate_tls_certificate(hostname: str, cert_path: str, email: str, private_key_path, company_name="My Company",
                             country_code="US", province="California", ip_addresses=None, key=None):
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization
    from acme import client, messages, challenges
    from acme.jose import JWKRSA

    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    with open(private_key_path, "wb") as f:
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
                    x509.NameAttribute(NameOID.COUNTRY_NAME, country_code),
                    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, province),
                    x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
                    x509.NameAttribute(NameOID.ORGANIZATION_NAME, company_name),
                    x509.NameAttribute(NameOID.COMMON_NAME, hostname),
                ]
            )
        )
        .add_extension(
            x509.SubjectAlternativeName(
                [x509.DNSName(hostname)] + [x509.IPAddress(ipaddress.ip_address(ip)) for ip in
                                                      ip_addresses or []]
            ),
            critical=False,
        )
        .sign(key, hashes.SHA256())
    )

    with open("csr.pem", "wb") as f:
        f.write(csr.public_bytes(serialization.Encoding.PEM))

    jwk = JWKRSA(key=key)

    directory_url = "https://acme-v02.api.letsencrypt.org/directory"

    net = client.ClientNetwork(jwk)
    acme_client = client.ClientV2(directory=directory_url, net=net)

    registration = acme_client.new_account(messages.NewRegistration.from_data(email=email, terms_of_service_agreed=True))

    # Create order
    order = acme_client.new_order(csr.public_bytes(serialization.Encoding.DER))

    # Get authorization challenges
    authz = order.authorizations[0]
    challenge = next(c for c in authz.challenges if isinstance(c.chall, challenges.HTTP01))

    # Solve the challenge
    challenge_response = challenge.response(jwk)

    # Write challenge file to /.well-known/acme-challenge/
    challenge_path = f".well-known/acme-challenge/{challenge.token}"
    with open(challenge_path, "w") as f:
        f.write(challenge_response.key_authorization)

    # Notify ACME server to validate the challenge
    acme_client.answer_challenge(challenge, challenge_response)

    # Wait for validation
    authz = acme_client.poll(authz)
    if authz.status != messages.STATUS_VALID:
        raise Exception("Authorization failed")

    # Finalize order and retrieve certificate
    order = acme_client.finalize_order(order)
    certificate = acme_client.fetch_certificate(order)

    # Save certificate to file
    with open(cert_path, "wb") as f:
        f.write(certificate)
