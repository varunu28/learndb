#ifndef PAGER_H
#define PAGER_H

#include <stdbool.h>
#include <stdint.h>

#define PAGE_SIZE 4096
#define TABLE_MAX_PAGES 100

typedef struct
{
    int file_descriptor;
    uint32_t file_length;
    uint32_t num_pages;
    void *pages[TABLE_MAX_PAGES]; // page caches
} Pager;

// Creates a new pager by using database filename
Pager *pager_open(const char *filename);

// Gets page associated with a page_num
void *get_page(Pager *pager, uint32_t page_num);

// Flush all contents of a page to disk
void pager_flush(Pager *pager, uint32_t page_num);

#endif // PAGER_H