#include <stdio.h>
#include <string.h>

#include "luaxune.h"

static int usage(void) {
    fprintf(stderr, "usage: luaxune <script.luau> [args...]\n");
    fprintf(stderr, "       luaxune -e <code> [args...]\n");
    fprintf(stderr, "       luaxune --version\n");
    return 1;
}

int main(int argc, char **argv) {
    lxstate *rt;
    int status;

    if (argc < 2) {
        return usage();
    }
    if (strcmp(argv[1], "--version") == 0 || strcmp(argv[1], "-v") == 0) {
        printf("luaxune %s (Luau)\n", lxversion());
        return 0;
    }
    if (strcmp(argv[1], "--help") == 0 || strcmp(argv[1], "-h") == 0) {
        usage();
        return 0;
    }

    rt = lxnew();
    if (!rt) {
        fprintf(stderr, "luaxune: failed to create runtime\n");
        return 1;
    }

    if (strcmp(argv[1], "-e") == 0) {
        if (argc < 3) {
            lxclose(rt);
            return usage();
        }
        lxsetargs(rt, argc - 3, (const char *const *)(argv + 3));
        status = lxdostring(rt, argv[2], "=(command line)");
    } else {
        lxsetargs(rt, argc - 2, (const char *const *)(argv + 2));
        status = lxdofile(rt, argv[1]);
    }

    if (status != 0) {
        fprintf(stderr, "%s\n", lxerror(rt));
    }
    lxclose(rt);
    return status != 0 ? 1 : 0;
}
