#ifndef INPUT_BUFFER_H
#define INPUT_BUFFER_H

#include <stdlib.h>
#include <unistd.h>

typedef struct
{
    char *buffer;
    size_t buffer_length;
    ssize_t input_length;
} InputBuffer;

// Create new InputBuffer
InputBuffer *new_input_buffer();

// Reads user input & stores it in InputBuffer instance
void read_input(InputBuffer *input_buffer);

#endif // INPUT_BUFFER_H