#ifndef NODE_H
#define NODE_H

#include "pager.h"

typedef enum
{
    NODE_INTERNAL,
    NODE_LEAF
} NodeType;

// Leaf node pointer arithmetic functions
uint32_t *leaf_node_num_cells(void *node);
void *leaf_node_cell(void *node, uint32_t cell_num);
uint32_t *leaf_node_key(void *node, uint32_t cell_num);
void *leaf_node_value(void *node, uint32_t cell_num);
void initialize_leaf_node(void *node);
NodeType get_node_type(void *node);
void set_node_type(void *node, NodeType type);

#endif // NODE_H
