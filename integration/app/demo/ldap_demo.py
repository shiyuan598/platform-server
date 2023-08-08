from flask_ldap3_login import LDAP3LoginManager

ldap_manager = LDAP3LoginManager()
ldap_manager.init_config({
    "LDAP_HOST": LDAP_HOST,  # 形如'ldap://xxx.xxx.xxx.xxx:389'
    "LDAP_BASE_DN": LDAP_BASE_DN,  # 形如'dc=test,dc=com'
    "LDAP_USER_LOGIN_ATTR": LDAP_USER_LOGIN_ATTR,  # 'uid'  # 'cn' 'mail'
    "LDAP_USER_SEARCH_SCOPE": LDAP_USER_SEARCH_SCOPE,  # 'SUBTREE'
    "LDAP_BIND_USER_DN": LDAP_BIND_USER_DN,  # 形如'cn=admin,dc=test,dc=com'
    "LDAP_BIND_USER_PASSWORD": LDAP_BIND_USER_PASSWORD,  # admin的密码
    "LDAP_ALWAYS_SEARCH_BIND": LDAP_ALWAYS_SEARCH_BIND,  # 一般是True
    "LDAP_GROUP_OBJECT_FILTER": LDAP_GROUP_OBJECT_FILTER,  # "(objectclass=posixGroup)" 或者 "(objectclass=groupOfNames)" 这里踩了坑，需要配置上
})
# 然后就可以直接调用ldap_manager进行验证了
authentication_result = ldap_manager.authenticate(
    "uid", "password")  # authentication_result .status.value = 2 则表示验证成功
