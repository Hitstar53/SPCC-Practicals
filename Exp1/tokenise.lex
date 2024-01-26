%{
#include <stdio.h>
#include <string.h>

int keywordCount = 0;
int stringCount = 0;
int constantCount = 0;
int identifierCount = 0;
int specialSymbolCount = 0;
int operatorCount = 0;
int unrecognizedCount = 0;
%}

%%
"auto"|"break"|"default"|"const"|"void"|"union"|"extern"|"if"|"else"|"while"|"do"|"break"|"continue"|"int"|"double"|"float"|"return"|"char"|"case"|"sizeof"|"long"|"short"|"typedef"|"switch"|"unsigned"|"void"|"static"|"struct"|"goto" { printf("KEYWORD: %s\n", yytext); keywordCount++; }
\"[^\n\"]*\"    { printf("STRING: %s\n", yytext); stringCount++; }
[0-9]+          { printf("CONSTANT: %s\n", yytext); constantCount++; }
[a-zA-Z_][a-zA-Z0-9_]* { printf("IDENTIFIER: %s\n", yytext); identifierCount++; }
[ \t\n]         /* Ignore whitespace */
[{}()[\],;.]    { printf("SPECIAL SYMBOL: %s\n", yytext); specialSymbolCount++; }
[+\-*/%&|!<>^=]=? { printf("OPERATOR: %s\n", yytext); operatorCount++; }
[@.]               { printf("UNRECOGNIZED: %s\n", yytext); unrecognizedCount++; }
%%

int yywrap(void) {}

int main() {
    yylex();
    printf("Keyword count: %d\n", keywordCount);
    printf("String constant count: %d\n", stringCount);
    printf("Constant count: %d\n", constantCount);
    printf("Identifier count: %d\n", identifierCount);
    printf("Special symbol count: %d\n", specialSymbolCount);
    printf("Operator count: %d\n", operatorCount);
    printf("Unrecognized count: %d\n", unrecognizedCount);
    return 0;
}