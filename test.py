from ldap3 import Server, Connection, ALL, NTLM

password = 'appsecret'

server = Server('ldap', port=3389, get_info=ALL)
conn = Connection(
    server, 'uid=termine,ou=Application,dc=example,dc=com', password)
print(conn.bind())

conn.search('dc=example,dc=com', '(objectclass=person)')

print(conn.entries)
conn.unbind()
