Take care of this folder that could contain private key. Be sure that this folder never is published.

SAML Python Toolkit expects that certs for the SP could be stored in this folder as:

 * sp.key     Private Key
 * sp.crt     Public cert
 * sp_new.crt Future Public cert


Also you can use other cert to sign the metadata of the SP using the:

 * metadata.key
 * metadata.crt

Key and Certificate are generated using the following command: 


```shell
openssl req -new -x509 -days 3652 -nodes -out sp.crt -keyout sp.key
```