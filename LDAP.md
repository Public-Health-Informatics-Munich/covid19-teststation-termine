# Setup LDAP

389 Directory Server
* https://hub.docker.com/r/389ds/dirsrv
* https://directory.fedoraproject.org/docs/389ds/documentation.html

LDAP tools need to be installed

## Base setup
```
docker-compose up
```

Look for the password for the Directory Manager in the log output
```
ldap_1      | INFO: IMPORTANT: Set cn=Directory Manager password to "pp7jcVfiZYvkadsJh0G0CwTy.wxab45Neq888o1GFF4nRmJEXqWL4cq80oxWqpvFX"
```

Write the password into a file, e.g.
```
printf pp7jcVfiZYvkadsJh0G0CwTy.wxab45Neq888o1GFF4nRmJEXqWL4cq80oxWqpvFX > ldap.pw
chmod 600 ldap.pw
```
⚠  make sure that there is no new line add the end of the `ldap.pw` file!


## Create a new suffix
```
docker-compose exec ldap dsconf -D 'cn=Directory Manager' -w "$(cat ldap.pw)" localhost backend create --suffix="dc=example,dc=com" --be-name="example"
```

## Populate
``` 
ldapadd -h localhost -v -x -D 'cn=Directory Manager' -y ldap.pw < example_com.ldif 
``` 

## Test
Show all the data
``` 
ldapsearch -h localhost -v -x -D 'cn=Directory Manager' -y ldap.pw -b "dc=example,dc=com" -s sub
``` 

Test the app user:
```
ldapsearch -h localhost -v -x -D 'uid=termine,ou=Application,dc=example,dc=com' -w appsecret -b ou=People,dc=example,dc=com -s sub
```

Test user:
```
ldapsearch -h localhost -v -x -D 'uid=a,ou=People,dc=example,dc=com' -w aa -b ou=People,dc=example,dc=com 
```
