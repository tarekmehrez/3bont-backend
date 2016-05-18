"""
Contains the IOLayer class as part of the util subpackage.
"""
import os
import csv
import json
import log

logger = log.get_logger()


class IO(object):

    """
    Handles io operations for the entire package.
    """

    def _set_extension(self, file_path):
        """
        Get absolute path, extract file extension.

        Args:
            file_path (str)
        """
        self._file_path = os.path.abspath(file_path)
        base_name = os.path.basename(file_path)
        self._file_ext = base_name.split('.')[-1]

    def read(self, file_path):
        """
        Given a file, read it, return its content.

        Returns:
            obj: file content as list or str, depends
            on the extension
        """
        # get the absolute path
        self._set_extension(file_path)

        logger.debug("reading %s", self._file_path)

        if self._file_ext == 'csv':
            self._read_csv()

        if self._file_ext == 'json':
            self._read_json()

        if self._file_ext == 'txt':
            self._read_txt()

        return self._content

    def write(self, file_path, content):
        """
        Write content to self._file_path.

        Args:
            content obj: content to write
        """
        self._set_extension(file_path)

        logger.debug("writing to %s", self._file_path)

        self._content = content

        if self._file_ext == 'json':
            self._write_json()

    def _read_csv(self):
        """
        Read in csv files.
        """
        with open(self._file_path, 'rb') as f:
            reader = csv.DictReader(f, delimiter=',')
            self._content = [row for row in reader]

    def _read_txt(self):
        with open(self._file_path, 'rb') as f:
            self._content = f.read().split('\n')

        self._content = filter(None, self._content)

    def _read_json(self):
        """
        Read json files.
        """
        with open(self._file_path, 'r') as f:
            self._content = json.load(f)

    def _write_json(self):
        """
        Write to json file.
        """
        with open(self._file_path, 'w') as f:
            json.dump(self._content, f, indent=4, separators=None,
                      encoding='utf-8', sort_keys=False)
