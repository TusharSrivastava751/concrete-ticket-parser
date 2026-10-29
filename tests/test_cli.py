from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
COMMAND = ['ticket_parser.py', 'examples/ticket-001.txt', 'examples/ticket-002.txt', 'examples/ticket-review.txt']
class CliTests(unittest.TestCase):
    def test_example_and_refuse_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'report'
            command=[sys.executable]+COMMAND+['--out',str(out)]
            run=subprocess.run(command,capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stderr)
            self.assertTrue(list(out.iterdir()))
            again=subprocess.run(command,capture_output=True,text=True)
            self.assertEqual(again.returncode,2)
    def test_missing_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            command=[sys.executable]+COMMAND.copy()+['--out',str(Path(tmp)/'out')]
            command[2]='does-not-exist.csv'
            run=subprocess.run(command,capture_output=True,text=True)
            self.assertEqual(run.returncode,2)
            self.assertFalse((Path(tmp)/'out').exists())
if __name__=='__main__': unittest.main()
