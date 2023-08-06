#ifndef STATEMENT_H
#define STATEMENT_H

#include "table.h"
#include "input_buffer.h"
#include "cursor.h"

typedef enum
{
    STATEMENT_INSERT,
    STATEMENT_SELECT
} StatementType;

typedef struct
{
    StatementType type;
    Row row_to_insert;
} Statement;

// MetaCommand are commands that dictate the terminal behavior of database such as closing the database connection
typedef enum
{
    META_COMMAND_SUCCESS,
    META_COMMAND_UNRECOGNIZED_COMMAND
} MetaCommandResult;

typedef enum
{
    EXECUTE_SUCCESS,
    EXECUTE_TABLE_FULL
} ExecuteResult;

typedef enum
{
    PREPARE_SUCCESS,
    PREPARE_SYNTAX_ERROR,
    PREPARE_STRING_TOO_LONG,
    PREPARE_NEGATIVE_ID,
    PREPARE_UNRECOGNIZED_STATEMENT
} PrepareResult;

// Prepare database operation
PrepareResult prepare_statement(InputBuffer *input_buffer, Statement *statement);

// Process MetaCommand
MetaCommandResult do_meta_command(InputBuffer *input_buffer, Table *table);

// Executes database operation
ExecuteResult execute_statement(Statement *statement, Table *table);

#endif // STATEMENT_H