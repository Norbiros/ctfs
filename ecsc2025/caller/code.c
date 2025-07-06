#include <stdio.h>
#include <string.h>

char* f(){{
    char* flag = "{FLAG}";
    printf("%s",flag);
    return flag;
}}

// I love AI
void g(char* a[f()[0]]){{}}

int main(){{
    g(NULL);
    return 0;
}}