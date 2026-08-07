import re
import runpy
from unittest import mock

import bot


class TestRunGitCommand:
    def test_returns_subprocess_returncode(self):
        completed = mock.Mock(returncode=0)
        with mock.patch("bot.subprocess.run", return_value=completed) as run:
            assert bot.run_git_command("git status") == 0
        run.assert_called_once_with(
            "git status", shell=True, capture_output=True, text=True
        )

    def test_propagates_nonzero_returncode(self):
        completed = mock.Mock(returncode=128)
        with mock.patch("bot.subprocess.run", return_value=completed):
            assert bot.run_git_command("git bogus") == 128


class TestAppendToFile:
    def test_appends_timestamped_message(self, tmp_path):
        target = tmp_path / "data.txt"
        with mock.patch.object(bot, "FILE_NAME", str(target)):
            bot.append_to_file("hello world")

        content = target.read_text(encoding="utf-8")
        assert content.endswith("hello world\n")
        assert re.match(
            r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] - hello world\n$", content
        )

    def test_appends_without_overwriting_existing_content(self, tmp_path):
        target = tmp_path / "data.txt"
        target.write_text("existing line\n", encoding="utf-8")
        with mock.patch.object(bot, "FILE_NAME", str(target)):
            bot.append_to_file("new line")

        lines = target.read_text(encoding="utf-8").splitlines()
        assert len(lines) == 2
        assert lines[0] == "existing line"
        assert lines[1].endswith("- new line")


class TestGitPush:
    def test_returns_true_when_all_git_commands_succeed(self):
        with mock.patch.object(bot, "append_to_file") as append, mock.patch.object(
            bot, "run_git_command", return_value=0
        ) as run, mock.patch.object(bot.random, "choice", return_value="feat: x"):
            assert bot.git_push() is True

        append.assert_called_once_with("feat: x")
        assert [c.args[0] for c in run.call_args_list] == [
            "git add .",
            'git commit -m "feat: x"',
            "git push origin main",
        ]

    def test_returns_false_when_git_add_fails(self):
        with mock.patch.object(bot, "append_to_file"), mock.patch.object(
            bot, "run_git_command", return_value=1
        ) as run, mock.patch.object(bot.random, "choice", return_value="feat: x"):
            assert bot.git_push() is False

        run.assert_called_once_with("git add .")

    def test_returns_false_when_commit_fails(self):
        with mock.patch.object(bot, "append_to_file"), mock.patch.object(
            bot, "run_git_command", side_effect=[0, 1]
        ) as run, mock.patch.object(bot.random, "choice", return_value="feat: x"):
            assert bot.git_push() is False

        assert [c.args[0] for c in run.call_args_list] == [
            "git add .",
            'git commit -m "feat: x"',
        ]

    def test_returns_false_when_push_fails(self):
        with mock.patch.object(bot, "append_to_file"), mock.patch.object(
            bot, "run_git_command", side_effect=[0, 0, 1]
        ) as run, mock.patch.object(bot.random, "choice", return_value="feat: x"):
            assert bot.git_push() is False

        assert run.call_args_list[-1].args[0] == "git push origin main"

    def test_uses_message_from_random_texts(self):
        with mock.patch.object(bot, "append_to_file") as append, mock.patch.object(
            bot, "run_git_command", return_value=0
        ), mock.patch.object(bot.random, "choice", wraps=bot.random.choice):
            bot.git_push()

        assert append.call_args.args[0] in bot.RANDOM_TEXTS


class TestMainEntryPoint:
    def test_commits_when_random_below_threshold(self):
        with mock.patch("bot.git_push") as git_push, mock.patch(
            "bot.random.random", return_value=0.5
        ):
            runpy.run_module("bot", run_name="__main__")
        git_push.assert_called_once_with()

    def test_skips_when_random_at_or_above_threshold(self):
        with mock.patch("bot.git_push") as git_push, mock.patch(
            "bot.random.random", return_value=0.95
        ):
            runpy.run_module("bot", run_name="__main__")
        git_push.assert_not_called()
