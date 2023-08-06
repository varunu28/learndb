# Directory structure
SRC_DIR = src
TEST_DIR = tests

# Output directories
BIN_DIR = bin
OBJ_DIR = obj

# C source and object files
C_SRC = $(wildcard $(SRC_DIR)/*.c)
C_OBJ = $(patsubst $(SRC_DIR)/%.c, $(OBJ_DIR)/%.o, $(C_SRC))

# Python test file
PY_TEST = $(TEST_DIR)/test.py

# Executable name
EXEC = $(BIN_DIR)/db

all: $(EXEC)

# Build the C executable
$(EXEC): $(C_OBJ)
	@mkdir -p $(BIN_DIR)
	$(CC) $(CFLAGS) $^ -o $@

# Build C object files
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c
	@mkdir -p $(OBJ_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

.PHONY: clean test

# Clean the generated files
clean:
	rm -rf $(BIN_DIR) $(OBJ_DIR)
	rm test.db

# Run the Python test
test:
	python3 $(PY_TEST)