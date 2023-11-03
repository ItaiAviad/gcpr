# gcpr

---

## Gcc/G++ Compile Plus Run

```bash
Usage: gcpr [options] files...

Optitons:
    -h              Show this help message
    -i              Interactive compilation
    -nr             No Running after Compilation (only compile)
    -o=<file>       Set executable file name (default: 'program')
    -s              Save executable file
    -so             Save output file (compilation running output contents, default: 'output.txt')
    
Examples:
    gcpr -h
    gcpr -s -o=run_me *.c
    gcpr -y -nr main.cpp utils.cpp
```

---
## Credits:
#### [DenLoob](https://github.com/Denloob) for `utils.py`