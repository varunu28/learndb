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
            ["./src/db", "test.db"],
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
        script = [f"insert {i} user{i} person{i}@example.com" for i in range(1, 1402)]
        script.append(".exit")
        result = self.run_script(script)
        self.assertEqual(result[-2], "db > error: Table full.")

    def test_allows_inserting_strings_that_are_the_maximum_length(self):
        self.remove_test_file_if_exists()
        long_username = "a" * 32
        long_email = "a" * 255
        script = [
            f"insert 1 {long_username} {long_email}",
            "select",
            ".exit",
        ]
        result = self.run_script(script)
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
        script = [
            f"insert 1 {long_username} {long_email}",
            "select",
            ".exit",
        ]
        result = self.run_script(script)
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
        script = [
            "insert -1 cstack foo@bar.com",
            "select",
            ".exit",
        ]
        result = self.run_script(script)
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


if __name__ == "__main__":
    unittest.main()
