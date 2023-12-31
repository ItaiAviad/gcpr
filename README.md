# gcpr

---

## Gcc/G++ Compile Plus Run

```bash
Usage: gcpr [options] files...

Optitons:
    -h              Show this help message
    -i              Interactive Mode compilation
    -nr             No Running after Compilation (only compile)
    -o=<path>       Set the path where to save the executable file
    -q              Quiet Mode - Only print compilation errors and running output contents (no gcpr text)
        *Note*: Quiet Mode disables Interactive Mode (all files will be approved)
    -lc=<name>      Leak Check - Check memory leaks (deafult = g++ -fsanitize=address)
        *Note*: Available leak checks - gcc/g++ -fsanitize, valgrind
    
Examples:
    gcpr -h
    gcpr -o=run_me *.c
    gcpr -y -nr main.cpp utils.cpp
```

---
## Credits:
#### [DenLoob](https://github.com/Denloob) for `utils.py`
