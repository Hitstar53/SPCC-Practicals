#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_RULES 10
#define MAX_SYMBOLS 10
#define MAX_STATES 10
#define MAX_STRING_LENGTH 100

// Structure to represent a production rule
typedef struct
{
    char lhs;
    char rhs[MAX_SYMBOLS];
} Rule;

// Structure to represent an item in the augmented grammar
typedef struct
{
    Rule rule;
    int dotPosition;
} Item;

// Structure to represent a state in the LR(0) automaton
typedef struct
{
    int id;
    int numItems;
    Item items[MAX_RULES];
} State;

// Structure to represent the LR(0) parse table
typedef struct
{
    char action;
    int nextState;
} ParseTableEntry;

// Function prototypes
void buildCanonicalCollection(Rule grammar[], int numRules, State canonicalCollection[], int *numStates);
void generateParseTable(State canonicalCollection[], int numStates, Rule grammar[], int numRules, ParseTableEntry parseTable[][MAX_SYMBOLS]);
void printParseTable(ParseTableEntry parseTable[][MAX_SYMBOLS]);
int parseString(char inputString[], ParseTableEntry parseTable[][MAX_SYMBOLS], int numStates, Rule grammar[], int numRules);

int main()
{
    Rule grammar[MAX_RULES];
    int numRules;

    printf("Enter the number of rules: ");
    scanf("%d", &numRules);

    printf("Enter the grammar rules:\n");
    for (int i = 0; i < numRules; i++)
    {
        printf("Rule %d: ", i + 1);
        scanf(" %c -> %s", &grammar[i].lhs, grammar[i].rhs);
    }

    State canonicalCollection[MAX_STATES];
    int numStates;
    buildCanonicalCollection(grammar, numRules, canonicalCollection, &numStates);

    ParseTableEntry parseTable[MAX_STATES][MAX_SYMBOLS];
    generateParseTable(canonicalCollection, numStates, grammar, numRules, parseTable);

    printf("\nParse Table:\n");
    printParseTable(parseTable);

    char inputString[MAX_STRING_LENGTH];
    printf("\nEnter the string to parse: ");
    scanf("%s", inputString);

    int result = parseString(inputString, parseTable, numStates, grammar, numRules);

    if (result)
        printf("\nAccepted\n");
    else
        printf("\nRejected\n");

    return 0;
}

void closure(Item items[], int *numItems, Rule grammar[], int numRules);
void gotoState(State *currentState, char symbol, Rule grammar[], int numRules);
int findState(State canonicalCollection[], int numStates, State *state);

void closure(Item items[], int *numItems, Rule grammar[], int numRules)
{
    int numItemsAdded = 0;

    do
    {
        numItemsAdded = 0;

        for (int i = 0; i < *numItems; i++)
        {
            Item currentItem = items[i];

            if (currentItem.dotPosition < strlen(currentItem.rule.rhs))
            {
                char nextSymbol = currentItem.rule.rhs[currentItem.dotPosition];

                if (nextSymbol >= 'A' && nextSymbol <= 'Z')
                {
                    for (int j = 0; j < numRules; j++)
                    {
                        if (grammar[j].lhs == nextSymbol)
                        {
                            Item newItem = {grammar[j], 0};

                            // Check if the item is already in the closure
                            int found = 0;
                            for (int k = 0; k < *numItems; k++)
                            {
                                if (memcmp(&items[k], &newItem, sizeof(Item)) == 0)
                                {
                                    found = 1;
                                    break;
                                }
                            }

                            if (!found)
                            {
                                items[*numItems] = newItem;
                                (*numItems)++;
                                numItemsAdded++;
                            }
                        }
                    }
                }
            }
        }
    } while (numItemsAdded > 0);
}

void gotoState(State *currentState, char symbol, Rule grammar[], int numRules)
{
    int numItemsAdded = 0;

    for (int i = 0; i < currentState->numItems; i++)
    {
        Item currentItem = currentState->items[i];

        if (currentItem.dotPosition < strlen(currentItem.rule.rhs))
        {
            char nextSymbol = currentItem.rule.rhs[currentItem.dotPosition];

            if (nextSymbol == symbol)
            {
                Item newItem = {currentItem.rule, currentItem.dotPosition + 1};

                // Check if the item is already in the state
                int found = 0;
                for (int j = 0; j < currentState->numItems; j++)
                {
                    if (memcmp(&currentState->items[j], &newItem, sizeof(Item)) == 0)
                    {
                        found = 1;
                        break;
                    }
                }

                if (!found)
                {
                    currentState->items[currentState->numItems] = newItem;
                    currentState->numItems++;
                    numItemsAdded++;
                }
            }
        }
    }
}

int findState(State canonicalCollection[], int numStates, State *state)
{
    for (int i = 0; i < numStates; i++)
    {
        if (canonicalCollection[i].numItems == state->numItems)
        {
            int found = 1;
            for (int j = 0; j < state->numItems; j++)
            {
                if (memcmp(&canonicalCollection[i].items[j], &state->items[j], sizeof(Item)) != 0)
                {
                    found = 0;
                    break;
                }
            }

            if (found)
                return i;
        }
    }

    return -1;
}

void buildCanonicalCollection(Rule grammar[], int numRules, State canonicalCollection[], int *numStates)
{
    State initial;
    initial.id = 0;
    initial.numItems = 0;

    // Add augmented grammar rule as the initial item
    initial.items[0].rule = grammar[0];
    initial.items[0].dotPosition = 0;
    initial.numItems++;

    // Compute closure of initial state
    closure(initial.items, &initial.numItems, grammar, numRules);

    // Initialize canonical collection
    canonicalCollection[0] = initial;
    *numStates = 1;

    // Process each state in the canonical collection
    for (int i = 0; i < *numStates; i++)
    {
        State currentState = canonicalCollection[i];

        // Collect all symbols that can follow the dot in items of the current state
        char symbolsFollowingDot[MAX_SYMBOLS];
        int numSymbols = 0;

        for (int j = 0; j < currentState.numItems; j++)
        {
            if (currentState.items[j].dotPosition < strlen(currentState.items[j].rule.rhs))
            {
                char nextSymbol = currentState.items[j].rule.rhs[currentState.items[j].dotPosition];
                if (!strchr(symbolsFollowingDot, nextSymbol))
                {
                    symbolsFollowingDot[numSymbols++] = nextSymbol;
                }
            }
        }

        // Generate new states using GOTO operation
        for (int j = 0; j < numSymbols; j++)
        {
            State nextState;
            nextState.numItems = 0;

            gotoState(&currentState, symbolsFollowingDot[j], grammar, numRules);

            // Compute closure of the new state
            closure(currentState.items, &currentState.numItems, grammar, numRules);

            // Check if the new state is already in the canonical collection
            int existingStateIndex = findState(canonicalCollection, *numStates, &currentState);

            if (existingStateIndex == -1)
            {
                // Add the new state to the canonical collection
                nextState = currentState;
                nextState.id = *numStates;
                canonicalCollection[*numStates] = nextState;
                (*numStates)++;
            }
            else
            {
                // The state already exists, update nextState with the existing state
                nextState = canonicalCollection[existingStateIndex];
            }

            // Update parse table with nextState information
            // This is where you would typically update your parse table entries
            // based on the current state, the symbol, and the nextState id.
            // For simplicity, I'll just print the information here.
            printf("GOTO(I%d, %c) = I%d\n", currentState.id, symbolsFollowingDot[j], nextState.id);
        }
    }
}

void generateParseTable(State canonicalCollection[], int numStates, Rule grammar[], int numRules, ParseTableEntry parseTable[][MAX_SYMBOLS])
{
    for (int i = 0; i < numStates; i++)
    {
        State currentState = canonicalCollection[i];

        // Fill in the parse table entries for shift and goto actions
        for (int j = 0; j < currentState.numItems; j++)
        {
            Item currentItem = currentState.items[j];

            // Shift actions
            if (currentItem.dotPosition < strlen(currentItem.rule.rhs))
            {
                char nextSymbol = currentItem.rule.rhs[currentItem.dotPosition];
                if (nextSymbol >= 'A' && nextSymbol <= 'Z')
                {
                    State nextState;
                    nextState.numItems = 0;
                    gotoState(&currentState, nextSymbol, grammar, numRules);
                    closure(currentState.items, &currentState.numItems, grammar, numRules);

                    int nextStateIndex = findState(canonicalCollection, numStates, &currentState);
                    parseTable[i][nextSymbol] = (ParseTableEntry){'S', nextStateIndex};
                }
            }

            // Goto actions
            if (currentItem.dotPosition == strlen(currentItem.rule.rhs))
            {
                if (currentItem.rule.lhs >= 'A' && currentItem.rule.lhs <= 'Z')
                {
                    char lhsSymbol = currentItem.rule.lhs;
                    int gotoStateIndex = findState(canonicalCollection, numStates, &currentState);
                    parseTable[i][lhsSymbol] = (ParseTableEntry){'G', gotoStateIndex};
                }
            }
        }

        // Fill in the parse table entries for reduce actions
        for (int j = 0; j < currentState.numItems; j++)
        {
            Item currentItem = currentState.items[j];

            if (currentItem.dotPosition == strlen(currentItem.rule.rhs))
            {
                if (currentItem.rule.lhs == 'S' && currentItem.rule.rhs[0] == 'E')
                {
                    // Accept action
                    parseTable[i]['$'] = (ParseTableEntry){'A', 0};
                }
                else
                {
                    // Reduce actions
                    int ruleIndex = -1;
                    for (int k = 0; k < numRules; k++)
                    {
                        if (memcmp(&grammar[k], &currentItem.rule, sizeof(Rule)) == 0)
                        {
                            ruleIndex = k;
                            break;
                        }
                    }

                    // Fill in the parse table entries for reduce actions
                    for (int k = 0; k < strlen(currentItem.rule.rhs); k++)
                    {
                        parseTable[i][currentItem.rule.rhs[k]] = (ParseTableEntry){'R', ruleIndex};
                    }
                }
            }
        }
    }
}

void printParseTable(ParseTableEntry parseTable[][MAX_SYMBOLS])
{
    printf("State\t");
    for (char symbol = 'A'; symbol <= 'Z'; symbol++)
    {
        printf("%c\t", symbol);
    }
    printf("$\n");

    for (int i = 0; i < MAX_STATES; i++)
    {
        if (parseTable[i][0].action == 0)
            break;

        printf("I%d\t", i);
        for (char symbol = 'A'; symbol <= 'Z'; symbol++)
        {
            if (parseTable[i][symbol].action == 0)
                printf("\t");
            else
                printf("%c%d\t", parseTable[i][symbol].action, parseTable[i][symbol].nextState);
        }
        printf("%c%d\n", parseTable[i]['$'].action, parseTable[i]['$'].nextState);
    }
}

int parseString(char inputString[], ParseTableEntry parseTable[][MAX_SYMBOLS], int numStates, Rule grammar[], int numRules)
{
    char stack[MAX_STRING_LENGTH];
    int top = -1;

    stack[++top] = '0'; // Start with initial state

    int inputIndex = 0;

    while (true)
    {
        int currentState = stack[top] - '0';
        char currentSymbol = inputString[inputIndex];

        ParseTableEntry tableEntry = parseTable[currentState][currentSymbol];

        if (tableEntry.action == 'S')
        {
            // Shift action
            stack[++top] = currentSymbol;
            stack[++top] = tableEntry.nextState + '0';
            inputIndex++;
        }
        else if (tableEntry.action == 'R')
        {
            // Reduce action
            int ruleIndex = tableEntry.nextState;
            Rule reduceRule = grammar[ruleIndex];

            // Pop 2 * len(rhs) symbols from the stack
            int popCount = 2 * strlen(reduceRule.rhs);
            while (popCount--)
            {
                top--;
            }

            // Get the current state and non-terminal symbol
            int currentState = stack[top] - '0';
            char nonTerminal = reduceRule.lhs;

            // Goto to the next state using the non-terminal symbol
            int nextState = parseTable[currentState][nonTerminal].nextState;
            stack[++top] = nonTerminal;
            stack[++top] = nextState + '0';
        }
        else if (tableEntry.action == 'A')
        {
            // Accept action
            printf("String Accepted\n");
            return 1;
        }
        else
        {
            // Error or Reject action
            printf("String Rejected\n");
            return 0;
        }
    }
}
