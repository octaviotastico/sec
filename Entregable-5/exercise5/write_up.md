# Ejercicio 5

Cosas que fui encontrando:

## KBeast
- Loads as an LKM (Loadable Kernel Module)
- Hides processes, files, directories, and network connections and provides keylogging capabilities
- Gains control by hooking the system call table and /proc/net/tcp
- Hides itself from modules list
- It does not hide itself from `sysfs`, tipically no root-kit does it anyway
- KBeast hooks a number of system calls in order to hide attacker activity

```
└──╼ $python vol.py -f ../ubuntu-10.04.3-i386-LiveCD-kbeast.mem --profile=LinuxUbuntu10043x86 linux_bash
Volatility Foundation Volatility Framework 2.6.1
Pid      Name                 Command Time                   Command
-------- -------------------- ------------------------------ -------
    4204 bash                 2012-05-01 14:41:26 UTC+0000   ifconfig
    4204 bash                 2012-05-01 14:41:26 UTC+0000   ps auwx | grep 3719
    4204 bash                 2012-05-01 14:41:26 UTC+0000   ifconfig
    4204 bash                 2012-05-01 14:41:26 UTC+0000   ps auwx | grep aptd
    4204 bash                 2012-05-01 14:41:26 UTC+0000   sudo kill -TERM 1350
    4204 bash                 2012-05-01 14:41:26 UTC+0000   sudo /etc/init.d/networking restart
    4204 bash                 2012-05-01 14:41:26 UTC+0000   more /etc/resolv.conf 
    4204 bash                 2012-05-01 14:41:26 UTC+0000   sudo kill -TERM 986
    4204 bash                 2012-05-01 14:41:31 UTC+0000   more /etc/lsb-release 
    4204 bash                 2012-05-01 14:43:00 UTC+0000   df
    4204 bash                 2012-05-01 14:43:12 UTC+0000   cp /media/Data/ipsecs-kbeast-v1.tar.gz . # -> apa la papa
    4204 bash                 2012-05-01 14:43:28 UTC+0000   tar xf ipsecs-kbeast-v1.tar.gz 
    4204 bash                 2012-05-01 14:43:31 UTC+0000   ls
    4204 bash                 2012-05-01 14:43:35 UTC+0000   cd kbeast-v1/
    4204 bash                 2012-05-01 14:43:36 UTC+0000   ls
    4204 bash                 2012-05-01 14:43:38 UTC+0000   nano config.h 
    4204 bash                 2012-05-01 14:43:55 UTC+0000   more setup 
    4204 bash                 2012-05-01 14:44:03 UTC+0000   ls
    4204 bash                 2012-05-01 14:44:05 UTC+0000   more README.TXT 
    4204 bash                 2012-05-01 14:44:18 UTC+0000   ./setup build
    4204 bash                 2012-05-01 14:44:44 UTC+0000   ls
    4204 bash                 2012-05-01 14:44:45 UTC+0000   ls
    4204 bash                 2012-05-01 14:44:45 UTC+0000   cd
    4204 bash                 2012-05-01 14:44:47 UTC+0000   cd _h4x_/
    4204 bash                 2012-05-01 14:44:48 UTC+0000   ls
    4204 bash                 2012-05-01 14:44:52 UTC+0000   ls -lrt
    4204 bash                 2012-05-01 14:45:13 UTC+0000   sudo insmod ipsecs-kbeast-v1.ko  # hmmm...
    4204 bash                 2012-05-01 14:45:20 UTC+0000   cd
    4204 bash                 2012-05-01 14:48:02 UTC+0000   ls
    4204 bash                 2012-05-01 14:48:07 UTC+0000   top
    4204 bash                 2012-05-01 14:48:15 UTC+0000   ps auwx
    4204 bash                 2012-05-01 14:48:25 UTC+0000   netstat -tn
    4204 bash                 2012-05-01 14:48:27 UTC+0000   netstat -tnl
    4204 bash                 2012-05-01 14:48:34 UTC+0000   sudo netstat -tnlp
```

`linux_check_modules` usa `sysfs` para encontrar modulos escondidos
```
└──╼ $python vol.py -f ../ubuntu-10.04.3-i386-LiveCD-kbeast.mem --profile=LinuxUbuntu10043x86 linux_check_modules
Volatility Foundation Volatility Framework 2.6.1
Module Address Core Address Init Address Module Name             
-------------- ------------ ------------ ------------------------
    0xf817eae0   0xf817d000          0x0 ipsecs_kbeast_v1
```

Check system calls for KBeast activity
```
└──╼ $python vol.py -f ../ubuntu-10.04.3-i386-LiveCD-kbeast.mem --profile=LinuxUbuntu10043x86 linux_check_syscall > ..dumps/ksyscall

└──╼ $grep -c HOOKED ../dumps/ksyscall # Esto nos dice que la syscall fue modificada
11
```

```
└──╼ $python vol.py -f ../ubuntu-10.04.3-i386-LiveCD-kbeast.mem --profile=LinuxUbuntu10043x86 linux_check_afinfo
Volatility Foundation Volatility Framework 2.6.1
Symbol Name                                Member                         Address   
------------------------------------------ ------------------------------ ----------
tcp4_seq_afinfo                            show                           0xf817d650  # Esta funcion ha sido manipulada
```

