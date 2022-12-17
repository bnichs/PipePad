import hashlib
import logging
import os
from dataclasses import dataclass
from os import PathLike
from pathlib import Path
from typing import Self, Tuple
from urllib.parse import urlparse, ParseResult

from pipepad.config_old import SHORT_HASH_LENGTH, LATEST_VERSION
from pipepad.language import PadLanguage


logger = logging.getLogger(__name__)



"""
Basic format: 

$REPO_ID:$PAD_NAME:$VERSION

Valid pad ids:

* samples/sum_ints  = the sum_ints pad in the samples repo
* samples/sum_ints:5  = the fifth version of the sum_ints pad in the samples repo
* ./samples/sample_repo/sum_ints/latest.py  = the sum_ints pad specificed by file name
* file://./samples/sample_repo/sum_ints/latest.py  = the sum_ints pad specificed by file name
* git@github.com:bnichs/pad_repo/samples/sample_repo/sum_ints/latest.py
* git@github.com:bnichs/pad_repo/samples/sum_ints
* https://github.com/bnichs/pad_repo/samples/sum_ints:5
"""


class CantParseID(Exception):
    pass


class InvalidRemoteID(Exception):
    pass


def path_exists(path: PathLike):
    return os.path.exists(path) or os.path.islink(path)


def parse_version(vstr: str) -> int:
    if vstr == "latest":
        return LATEST_VERSION
    else:
        return int(vstr)



@dataclass
class RepoID:
    pass


@dataclass
class RemoteRepoID():
    scheme: str
    netloc: str
    path: str

    @classmethod
    def from_parsed(cls, parsed: ParseResult):
        logger.debug("Making remote repo id from %s", parsed)

        parts = parsed.path.split(":")
        match parts:
            case (repo_part, pad_part):
                return RemoteRepoID(scheme=parsed.scheme, netloc=parsed.netloc, path=repo_part)
            case (repo_part, pad_part, version):
                return RemoteRepoID(scheme=parsed.scheme, netloc=parsed.netloc, path=repo_part)
            case (filepath,):
                return RemoteRepoID(scheme=parsed.scheme, netloc=parsed.netloc, path=None)
            case _:
                print(parts)
                raise


# @dataclass
class PadID:
    @classmethod
    def from_str(cls, s: str) -> Self:
        logger.debug("Making PadID from %s", s)
        parsed = urlparse(s)
        print(parsed)

        if parsed.scheme == "file" or path_exists(Path(s)):
            logger.debug("Looks like a file, parsing as file")
            return LocalFilePadID.from_str(s)
        elif parsed.scheme in ["http", "https", "git"]:
            logger.debug("Looks like a remote repository")
            return RemotePadID.from_str(s)
        else:
            logger.debug("Looks like a local repo id")
            return RepoPadID.from_str(s)

        return "foo"

    def is_file(self):
        return isinstance(self, LocalFilePadID)

    def is_remote(self):
        return isinstance(self, RemotePadID)

    @classmethod
    def parse_path(cls, s: str) -> Tuple[str, str, int]:
        parts = s.split(":")
        logger.debug("Parts = %s", parts)

        match parts:
            case (repo_name, pad_name, version):
                version = parse_version(version)
                return repo_name, pad_name, version
            case (repo_name, pad_name):
                return repo_name, pad_name, LATEST_VERSION
            case (file_path, ):
                return None, file_path, None
            case _:
                raise CantParseID(s)


@dataclass
class RepoPadID(PadID):
    """A PadID with a repo and a pad name """
    repo: RepoID
    pad_name: str
    version: int = LATEST_VERSION

    @classmethod
    def from_str(cls, s: str) -> Self:
        logger.debug("Making repo+pad id from %s", s)

        repo_name, pad_name, version = cls.parse_path(s)
        return RepoPadID(repo_name, pad_name, version)


@dataclass
class RemotePadID(PadID):
    repo: RemoteRepoID
    name: str
    version: int = LATEST_VERSION

    @classmethod
    def from_str(cls, s: str) -> Self:
        logger.debug("making remote pad id from %s", s)
        parsed = urlparse(s)
        print(parsed)
        if not parsed.scheme:
            raise InvalidRemoteID(s)

        repo_name, pad_name, version = cls.parse_path(parsed.path)

        if repo_name is None and version is None:
            # Nothing parsed so it ust be a file path
            return RemotePadFileID.from_parsed(filepath=pad_name, parsed=parsed)
            pass
        else:
            # we at least got a pad name
            repo_name = ...
            print(type(parsed))
            repo = RemoteRepoID.from_parsed(parsed)
            return RemotePadID(repo=repo, name=pad_name, version=version)
            pass

        raise

    # @classmethod
    # def parse_path(cls, p: str):
    #     pass


@dataclass
class RemotePadFileID(RemotePadID):
    """A remote tht is just a file, not necessarily in a repo"""
    path: PathLike = None

    @classmethod
    def from_parsed(cls, filepath: PathLike, parsed: ParseResult):
        repo = RemoteRepoID.from_parsed(parsed)
        print(parsed)
        print(repo)
        return RemotePadFileID(repo=repo, name=None, version=None, path=filepath)


@dataclass
class LocalFilePadID(PadID):
    """A PadID that is just a file path"""
    fpath: PathLike

    @classmethod
    def from_str(cls, s: str) -> Self:
        logger.debug("Making file pad id from %s", s)
        if s.startswith("file://"):
            s = s.replace("file://", "")
        return LocalFilePadID(Path(s))

    def file_exists(self):
        return path_exists(self.fpath)



@dataclass
class PipePad:
    """Pad object containing the contents of a pad"""
    contents: str
    language: PadLanguage

    def __repr__(self):
        return f"PipePad(hash={self.get_hash()}, " \
               f"contents={self.short_contents}," \
               f"language={self.language})"

    def get_hash(self):
        return hashlib.sha256(self.contents.encode("utf-8")).hexdigest()

    @property
    def short_contents(self):
        lines = self.contents.splitlines()
        num = 10
        num = num if len(lines) > num else len(lines) - 1

        return self.contents.split("\n")[num]

    def get_short_hash(self) -> str:
        h = self.get_hash()
        print(h)
        return h[:SHORT_HASH_LENGTH]

    @property
    def extension(self):
        return self.language.extension

    @classmethod
    def create_from_file(cls, filename, language: PadLanguage) -> Self:
        logger.debug("Creating pad from file %s", filename)
        with open(filename, 'r') as f:
            contents = f.read()

            pad = PipePad(contents=contents, language=language)
            return pad


