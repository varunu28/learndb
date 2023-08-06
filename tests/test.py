import subprocess
import unittest
import os


class TestDatabase(unittest.TestCase):
    def remove_test_file_if_exists(self):
        if os.path.exists("test.db"):
            os.remove("test.db")

    def run_script(self, commands):
        # start db server
        self.process = subprocess.Popen(
            ["./bin/db", "test.db"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        # run the commands
        for command in commands:
            self.process.stdin.write(command + "\n")
            self.process.stdin.flush()
        raw_output = self.process.stdout.read()
        # clean up
        self.process.stdin.close()
        self.process.stdout.close()
        self.process.stderr.close()
        self.process.terminate()
        self.process.wait()
        return raw_output.splitlines()

    def test_inserts_and_retrieves_a_row(self):
        self.remove_test_file_if_exists()
        result = self.run_script(
            [
                "insert 1 user1 person1@example.com",
                "select",
                ".exit",
            ]
        )
        self.assertListEqual(
            result,
            [
                "db > executed.",
                "db > (1, user1, person1@example.com)",
                "executed.",
                "db > ",
            ],
        )

    def test_prints_error_message_when_table_is_full(self):
        self.remove_test_file_if_exists()
        commands = [f"insert {i} user{i} person{i}@example.com" for i in range(1, 1402)]
        commands.append(".exit")
        result = self.run_script(commands)
        self.assertEqual(result[-2], "db > error: Table full.")

    def test_allows_inserting_strings_that_are_the_maximum_length(self):
        self.remove_test_file_if_exists()
        long_username = "a" * 32
        long_email = "a" * 255
        commands = [
            f"insert 1 {long_username} {long_email}",
            "select",
            ".exit",
        ]
        result = self.run_script(commands)
        self.assertListEqual(
            result,
            [
                "db > executed.",
                f"db > (1, {long_username}, {long_email})",
                "executed.",
                "db > ",
            ],
        )

    def test_prints_error_message_if_strings_are_too_long(self):
        self.remove_test_file_if_exists()
        long_username = "a" * 33
        long_email = "a" * 256
        commands = [
            f"insert 1 {long_username} {long_email}",
            "select",
            ".exit",
        ]
        result = self.run_script(commands)
        self.assertListEqual(
            result,
            [
                "db > string is too long.",
                "db > executed.",
                "db > ",
            ],
        )

    def test_prints_an_error_message_if_id_is_negative(self):
        self.remove_test_file_if_exists()
        commands = [
            "insert -1 cstack foo@bar.com",
            "select",
            ".exit",
        ]
        result = self.run_script(commands)
        self.assertListEqual(
            result,
            [
                "db > id must be positive.",
                "db > executed.",
                "db > ",
            ],
        )

    def test_data_is_persisted_after_closing_connection(self):
        self.remove_test_file_if_exists()
        result_one = self.run_script(
            [
                "insert 1 user1 person1@example.com",
                ".exit",
            ]
        )
        self.assertListEqual(
            result_one,
            [
                "db > executed.",
                "db > ",
            ],
        )
        result_two = self.run_script(["select", ".exit"])
        self.assertListEqual(
            result_two,
            [
                "db > (1, user1, person1@example.com)",
                "executed.",
                "db > ",
            ],
        )

    def test_prints_constants(self):
        self.remove_test_file_if_exists()
        commands = [
            ".constants",
            ".exit",
        ]
        result = self.run_script(commands)
        self.assertListEqual(
            result,
            [
                "db > Constants:",
                "ROW_SIZE: 293",
                "COMMON_NODE_HEADER_SIZE: 6",
                "LEAF_NODE_HEADER_SIZE: 10",
                "LEAF_NODE_CELL_SIZE: 297",
                "LEAF_NODE_SPACE_FOR_CELLS: 4086",
                "LEAF_NODE_MAX_CELLS: 13",
                "db > ",
            ],
        )

    def test_print_structure_one_node_btree(self):
        self.remove_test_file_if_exists()
        script = [3, 1, 2]
        commands = [f"insert {i} user{i} person{i}@example.com" for i in script]
        commands.append(".btree")
        commands.append(".exit")
        result = self.run_script(commands)
        self.assertListEqual(
            result,
            [
                "db > executed.",
                "db > executed.",
                "db > executed.",
                "db > Tree:",
                "leaf (size 3)",
                "  - 0 : 1",
                "  - 1 : 2",
                "  - 2 : 3",
                "db > ",
            ],
        )

    def test_error_for_duplicate_id(self):
        self.remove_test_file_if_exists()
        commands = [
            "insert 1 user1 person1@example.com",
            "insert 1 user1 person1@example.com",
            "select",
            ".exit",
        ]
        result = self.run_script(commands)
        self.assertListEqual(
            result,
            [
                "db > executed.",
                "db > error: Duplicate key.",
                "db > (1, user1, person1@example.com)",
                "executed.",
                "db > ",
            ],
        )


if __name__ == "__main__":
    unittest.main()
