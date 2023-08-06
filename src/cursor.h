#ifndef CURSOR_H
#define CURSOR_H

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "table.h"
#include "node.h"

typedef struct
{
    Table *table;
    uint32_t page_num;
    uint32_t cell_num;
    int end_of_table; // one past the last element
} Cursor;

// Creates a Cursor implementation that points to the start of page
Cursor *table_start(Table *table);

/**
 * Return the position of given key. If key is not present then return the correct insertion position for the key
 */
Cursor *table_find(Table *table, uint32_t key);

void *cursor_value(Cursor *cursor);

// Update the cursor to point to next row.
void cursor_advance(Cursor *cursor);

void leaf_node_insert(Cursor *cursor, uint32_t key, Row *value);

#endif // CURSOR_H
