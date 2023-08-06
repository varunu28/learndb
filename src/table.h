#ifndef TABLE_H
#define TABLE_H

#include <string.h>
#include "pager.h"
#include "node.h"

typedef struct
{
    uint32_t id;
    char username[COLUMN_USERNAME_SIZE + 1];
    char email[COLUMN_EMAIL_SIZE + 1];
} Row;

typedef struct
{
    uint32_t root_page_num;
    Pager *pager;
} Table;

// Create a table instance from database file
Table *db_open(const char *filename);

/*
 * Close the database connection by doing below steps:
 * - Flush all pages in table on disk.
 * - perform cleanup for memory allocated for database resources.
 */
void db_close(Table *table);

// Prints a database row
void print_row(Row *row);

void serialize_row(Row *source, void *destination);

void deserialize_row(void *source, Row *destination);

#endif // TABLE_H