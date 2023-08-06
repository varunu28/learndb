#include "input_buffer.h"
#include "statement.h"
#include "table.h"

void print_prompt()
{
    printf("db > ");
}

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        printf("must supply a database filename.\n");
        exit(EXIT_FAILURE);
    }
    char *filename = argv[1];
    Table *table = db_open(filename);
    InputBuffer *input_buffer = new_input_buffer();
    while (true)
    {
        print_prompt();
        read_input(input_buffer);

        if (input_buffer->buffer[0] == '.')
        {
            switch (do_meta_command(input_buffer, table))
            {
            case META_COMMAND_SUCCESS:
                continue;
            case META_COMMAND_UNRECOGNIZED_COMMAND:
                printf("unrecognized command\n");
                continue;
            default:
                break;
            }
        }

        Statement statement;
        switch (prepare_statement(input_buffer, &statement))
        {
        case PREPARE_SUCCESS:
            break;
        case PREPARE_SYNTAX_ERROR:
            printf("syntax error. Could not parse statement. \n");
            continue;
        case PREPARE_UNRECOGNIZED_STATEMENT:
            printf("uncrecognized keyword at start of %s. \n", input_buffer->buffer);
            continue;
        case PREPARE_STRING_TOO_LONG:
            printf("string is too long.\n");
            continue;
        case PREPARE_NEGATIVE_ID:
            printf("id must be positive.\n");
            continue;
        default:
            break;
        }

        switch (execute_statement(&statement, table))
        {
        case EXECUTE_SUCCESS:
            printf("executed.\n");
            break;
        case EXECUTE_TABLE_FULL:
            printf("error: Table full.\n");
            break;
        }
    }
}
