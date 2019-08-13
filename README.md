nats

```
export OPENSSL_INCLUDE_DIR=/usr/local/opt/openssl/include/
export OPENSSL_ROOT_DIR=/usr/local/opt/openssl/
```

```
git clone https://github.com/protobuf-c/protobuf-c.git
cd protobuf-c
./configure CFLAGS=-fPIC
make
make install
```
