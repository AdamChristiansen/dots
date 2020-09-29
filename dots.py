#!/usr/bin/env python3

from abc import ABC, abstractmethod
import json
import os
import re
import stat
import sys

class Default:
    """
    All default values are declared here.
    """

    # The default build directory.
    BUILD_DIR = "build"

    # The default format enabled.
    BUILD_FORMAT = True

    # The default configuration file name.
    CONFIG_FILE = "dots.json"

    # The default file executable setting.
    FILE_EXECUTABLE = False

    # The default file template setting.
    FILE_TEMPLATE = False

    # The default for whether a template include is optional.
    INCLUDE_OPTIONAL = False

    # The default template interpolation beginning token.
    TEMPLATE_BEGIN = "{{{"

    # The default template interpolation ending token.
    TEMPLATE_END = r"}}}"

    # The default template snippets directory.
    TEMPLATE_SNIPPETS = r"snippets"

class Fmt:
    """
    Provides functionality for formatting messages.
    """

    # ANSI color escapes
    NORMAL  = "\033[0m"
    BOLD    = "\033[1m"
    BLACK   = "\033[30m"
    RED     = "\033[31m"
    GREEN   = "\033[32m"
    YELLOW  = "\033[33m"
    BLUE    = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN    = "\033[36m"
    WHITE   = "\033[37m"

    # Prefixes
    PRE_GOOD = "+"
    PRE_BAD  = "-"
    PRE_DRY  = "?"

    @staticmethod
    def good(s):
        """
        Format a string with the good color.
        """
        return "{}{}{}".format(Fmt.BOLD + Fmt.GREEN, s, Fmt.NORMAL)

    @staticmethod
    def bad(s):
        """
        Format a string with the bad color.
        """
        return "{}{}{}".format(Fmt.BOLD + Fmt.RED, s, Fmt.NORMAL)

    @staticmethod
    def emph(s):
        """
        Format a string with the emphasis color.
        """
        return "{}{}{}".format(Fmt.BOLD + Fmt.YELLOW, s, Fmt.NORMAL)

    @staticmethod
    def status(title, src=None, target=None, msg=None, err=False, verbose=False, dry_run=False):
        """
        Print a status message.
        # Arguments

        * title (str): Title of the message.
        * src (str): The operation generating the message.
        * target (str): Target goal of the operation.
        * msg (str): An info or error message of the operation.
        * err (bool): Indicates the operation failed. This is ignored in dry
          run mode.
        * verbose (bool): Run in verbose mode.
        * dry_run (bool): Run in dry run mode.
        """
        if dry_run:
            c = Fmt.emph
            p = Fmt.PRE_DRY
        elif not err:
            if not verbose:
                return
            c = Fmt.good
            p = Fmt.PRE_GOOD
        else:
            c = Fmt.bad
            p = Fmt.PRE_BAD
        s = [c(f"{p} {title}")]
        if src is not None:
            s.append(src.strip())
        if target is not None:
            s.append(c("->"))
            s.append(target.strip())
        m = " ".join(s)
        if msg is not None:
            m = f"{m}{c(':')} {msg.strip()}"
        print(m, file=sys.stderr if err else sys.stdout)

class Title:
    """
    Titles for printing status information.
    """
    BUILD     = "Build"
    EXCEPTION = "Exception"
    FORMAT    = "Format"
    INSTALL   = "Install"

class DotsError(Exception):
    """
    The base class for all custom errors.
    """
    pass

class BuildError(Exception):
    """
    An errors related to the build and installation process.
    """
    pass

class JSONError(DotsError):
    """
    An error related JSON parsing or processing.
    """
    pass

def validation_error(msg, *json_path):
    """
    Create a validation exception for the JSON configuration which incorporates
    a message and the JSON path.

    # Arguments

    * msg (str): The message to display. This comes directly after the JSON
      path in the message string.
    * json_path (list<str|int>): The path to the error location in the JSON.

    # Returns

    A `JSONError` which can be raised.
    """
    def quote(x):
        for c in [".", "/", " "]:
            if c in x:
                return f"\"{x}\""
        return x
    p = ""
    for node in json_path:
        if not p:
            p = node
        elif isinstance(node, int):
            p += f"[{node}]"
        else:
            p += f".{quote(node)}"
    return JSONError(f"{p} {msg}")

def dict_remove_if(d, k, *vs):
    """
    Remove a key, `k`, from a dictionary, `d`, if the value of the key is
    contained in `vs`.
    """
    for v in vs:
        try:
            if d[k] == v:
                d.pop(k)
                return
        except ValueError:
            pass

def safe_to_json(data, minify=True):
    """
    Safely convert data into a JSON representation.

    # Arguments

    * data (AbstractConfig|dict|list|int|float|NoneType|str): The data to
      convert to JSON.
    * minify (bool): Causes the data to be minified by removing nulls and
      default values.
    """
    if isinstance(data, AbstractConfig):
        return data.to_json(minify=minify)
    elif isinstance(data, (bool, int, float, None.__class__, str)):
        return data
    elif isinstance(data, dict):
        r = { k: safe_to_json(v, minify=minify) for k, v in data.items() }
        return r if r else None
    elif isinstance(data, list):
        r = list([safe_to_json(x, minify=minify) for x in data])
        return r if r else None
    else:
        raise JSONError(f"cannot interpret data of type {type(data)}")

def expand_path(p):
    """
    Expand a path by getting the absolute path and expanding the user prefix
    and environment variables.

    # Arguments

    * p (str): The path.

    # Returns

    (str): An expanded path.

    # Raises

    (DotsError): When the name of an undefined environment variable is
        encountered.
    """
    ep = os.path.abspath(os.path.expandvars(os.path.expanduser(p)))
    matches = re.search(r"(\$([a-z_][a-z0-9_]*|{[a-z_][a-z0-9_]*}))",
        ep, re.IGNORECASE)
    if matches:
        v = matches.group(1)
        raise DotsError(f"environment variable {v} in path {p} not defined")
    return ep

class AbstractConfig(ABC):
    """
    A base class for configurations.
    """

    @abstractmethod
    def to_json(self, minify=True):
        """
        Get a JSON representation of the object.

        # Arguments

        * minify (bool): Enables minification, which removes all non-required
          and default data.

        # Returns

        (dict|list|bool|int|float|NoneType|string) The JSON representation of
        the configuration.
        """
        pass

    def _parse_bool_or_none(self, value, name, *json_path):
        """
        Parse a boolean or `None` into an attribute. When the value is `None`,
        the attribute is not modified.

        # Arguments

        * value (bool|NoneType): The value.
        * name (str): The name of the attribute to store the value in.
        * json_path (list<str|int>): The path to the error location in the JSON.

        # Raises

        (JSONError): Where the value is invalid.
        """
        default = getattr(self, name)
        if value is None:
            setattr(self, name, default)
        elif isinstance(value, bool):
            setattr(self, name, value)
        else:
            raise validation_error("must be a boolean or null", *json_path)

    def _parse_str(self, value, name, *json_path):
        """
        Parse a non-empty string into an attribute.

        # Arguments

        * value (str|NoneType): The value.
        * name (str): The name of the attribute to store the value in.
        * json_path (list<str|int>): The path to the error location in the JSON.

        # Raises

        (JSONError): Where the value is invalid.
        """
        if not isinstance(value, str) or not value:
            raise validation_error("must be a non-empty string", *json_path)
        setattr(self, name, value)

    def _parse_str_or_none(self, value, name, *json_path):
        """
        Parse a non-empty string or `None` into an attribute. When the value is
        `None`, the attribute is not modified.

        # Arguments

        * value (str|NoneType): The value.
        * name (str): The name of the attribute to store the value in.
        * json_path (list<str|int>): The path to the error location in the JSON.

        # Raises

        (JSONError): Where the value is invalid.
        """
        default = getattr(self, name)
        if value is None:
            setattr(self, name, default)
        elif isinstance(value, str) or not value:
            setattr(self, name, value)
        else:
            raise validation_error("must be a non-empty string or null", *json_path)

    def __str__(self):
        return json.dumps(self.to_json())

class Config(AbstractConfig):
    """
    Deserialized configuration.
    """

    def __init__(self, data):
        """
        Create a new configuration.

        # Arguments

        * data (dict|list|bool|int|float|NoneType|str): The JSON object
          representation of the configuration.
        """
        self.build = BuildConfig(None)
        self.packages = {}
        self.templates = TemplatesConfig(None)
        # Parse values
        if isinstance(data, dict):
            for k, v in data.items():
                if k == "build":
                    self.build = BuildConfig(v, k)
                elif k == "packages":
                    self._parse_packages(k, v, k)
                elif k == "templates":
                    self.templates = TemplatesConfig(v, k)
                else:
                    raise validation_error("is not a valid key", k)
        else:
            raise validation_error("must be a mapping", "root object")

    def _parse_packages(self, k, v, *json_path):
        if isinstance(v, dict):
            for vk, vv in v.items():
                self.packages[vk] = PackageConfig(vv, *json_path, vk)
        else:
            raise validation_error("must be a mapping or null", *json_path)

    def to_json(self, minify=True):
        data = {
            "build": safe_to_json(self.build, minify=minify),
            "packages": safe_to_json(self.packages, minify=minify),
            "templates": safe_to_json(self.templates, minify=minify)
        }
        if minify:
            dict_remove_if(data, "build", None, {})
            dict_remove_if(data, "packages", None, [])
            dict_remove_if(data, "templates", None, {})
        return data

class BuildConfig(AbstractConfig):
    """
    Deserialized build configuration.
    """

    def __init__(self, data, *json_path):
        """
        Create a new build configuration.

        # Arguments

        * data (dict|list|bool|int|float|NoneType|str): The JSON object
          representation of the configuration.
        * json_path (list<str|int>): The path of the curent location in the
          JSON.
        """
        self.dir = Default.BUILD_DIR
        self.format = Default.BUILD_FORMAT
        # Parse values
        if data is None:
            pass
        elif isinstance(data, dict):
            for k, v in data.items():
                if k == "dir":
                    self._parse_str_or_none(v, "dir", *json_path)
                elif k == "format":
                    self._parse_bool_or_none(v, "format", *json_path)
                else:
                    raise validation_error("is not a valid key", *json_path, k)
        else:
            raise validation_error("must be a mapping or null", *json_path)

    def to_json(self, minify=True):
        data = {
            "dir": safe_to_json(self.dir, minify=minify),
            "format": safe_to_json(self.format, minify=minify),
        }
        if minify:
            dict_remove_if(data, "dir", None, Default.BUILD_DIR)
            dict_remove_if(data, "format", None, Default.BUILD_FORMAT)
        return data

class FileConfig(AbstractConfig):
    """
    Deserialized file configuration.
    """

    def __init__(self, data, *json_path):
        """
        Create a new file configuration.

        # Arguments

        * data (dict|list|bool|int|float|NoneType|str): The JSON object
          representation of the configuration.
        * json_path (list<str|int>): The path of the curent location in the
          JSON.
        """
        self.dest = None
        self.executable = Default.FILE_EXECUTABLE
        self.template = Default.FILE_TEMPLATE
        # Parse values
        if isinstance(data, str) and data:
            self.dest = data
        elif isinstance(data, dict):
            for k, v in data.items():
                if k == "dest":
                    self._parse_str_or_none(v, "dest", *json_path)
                elif k == "executable":
                    self._parse_bool_or_none(v, "executable", *json_path)
                elif k == "template":
                    self._parse_bool_or_none(v, "template", *json_path)
                else:
                    raise validation_error("is not a valid key", *json_path, k)
        else:
            raise validation_error("must be a non-empty string or mapping", *json_path)

    def to_json(self, minify=True):
        data = {
            "dest": safe_to_json(self.dest, minify=minify),
            "executable": safe_to_json(self.executable, minify=minify),
            "template": safe_to_json(self.template, minify=minify),
        }
        if minify:
            dict_remove_if(data, "dest", None)
            dict_remove_if(data, "executable", None, Default.FILE_EXECUTABLE)
            dict_remove_if(data, "template", None, Default.FILE_TEMPLATE)
            # When only dest is specified do not use the whole structure
            if set(data.keys()) == set(["dest"]):
                data = data["dest"]
        return data

class IncludeConfig(AbstractConfig):
    """
    Deserialized variable inclusion configuration.
    """

    def __init__(self, data, *json_path):
        """
        Create a new variable inclusion configuration.

        # Arguments

        * data (dict|list|bool|int|float|NoneType|str): The JSON object
          representation of the configuration.
        * json_path (list<str|int>): The path of the curent location in the
          JSON.
        """
        self.path = None
        self.optional = Default.INCLUDE_OPTIONAL
        # Parse values
        if isinstance(data, str):
            self.path = data
        elif isinstance(data, dict):
            for k, v in data.items():
                if k == "path":
                    self._parse_str(v, "path", *json_path)
                elif k == "optional":
                    self._parse_bool_or_none(v, "optional", *json_path)
                else:
                    raise validation_error("is not a valid key", *json_path, k)
        else:
            raise validation_error("must be a non-empty string or mapping", *json_path)
        # Check values
        if self.path is None:
            raise validation_error("must be set", *json_path, "path")

    def to_json(self, minify=True):
        data = {
            "path": safe_to_json(self.path, minify=minify),
            "optional": safe_to_json(self.optional, minify=minify)
        }
        if minify:
            # path is required
            dict_remove_if(data, "optional", None, Default.INCLUDE_OPTIONAL)
            if set(data.keys()) == set(["path"]):
                data = data["path"]
        return data

class PackageConfig(AbstractConfig):
    """
    Deserialized package configuration.
    """

    def __init__(self, data, *json_path):
        """
        Create a new package configuration.

        # Arguments

        * data (dict|list|bool|int|float|NoneType|str): The JSON object
          representation of the configuration.
        * json_path (list<str|int>): The path of the curent location in the
          JSON.
        """
        self.files = {}
        self.requires = []
        # Parse values
        if data is None:
            pass
        elif isinstance(data, dict):
            for k, v in data.items():
                if k == "files":
                    self._parse_files(k, v, *json_path, k)
                elif k == "requires":
                    self._parse_requires(k, v, *json_path, k)
                else:
                    raise validation_error("is not a valid key", *json_path, k)
        else:
            raise validation_error("must be a mapping or null", *json_path)

    def _parse_files(self, k, v, *json_path):
        if v is None:
            pass
        elif isinstance(v, dict):
            for vk, vv in v.items():
                self.files[vk] = FileConfig(vv, *json_path, vk)
        else:
            raise validation_error("must be a mapping or null", *json_path)

    def _parse_requires(self, k, v, *json_path):
        if v is None:
            pass
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if not isinstance(item, str) or not v:
                    raise validation_error("must be a non-empty string", *json_path, i)
            self.requires = sorted(v)
        else:
            raise validation_error("must be a list", *json_path)

    def to_json(self, minify=True):
        data = {
            "files": safe_to_json(self.files, minify=minify),
            "requires": safe_to_json(self.requires, minify=minify),
        }
        if minify:
            dict_remove_if(data, "files", None, {})
            dict_remove_if(data, "requires", None, [])
        return data

class TemplatesConfig(AbstractConfig):
    """
    Deserialized template configuration.
    """

    def __init__(self, data, *json_path):
        """
        Create a new template configuration.

        # Arguments

        * data (dict|list|bool|int|float|NoneType|str): The JSON object
          representation of the configuration.
        * json_path (list<str|int>): The path of the curent location in the
          JSON.
        """
        self.begin = Default.TEMPLATE_BEGIN
        self.end = Default.TEMPLATE_END
        self.include = []
        self.snippets = Default.TEMPLATE_SNIPPETS
        self.variables = {}
        # These are the variables as they appear in the main configuration file
        self._original_variables = {}
        # Parse values
        if data is None:
            pass
        elif isinstance(data, dict):
            for k, v in data.items():
                if k == "begin":
                    self._parse_str_or_none(v, "begin", *json_path)
                elif k == "end":
                    self._parse_str_or_none(v, "end", *json_path)
                elif k == "include":
                    self._parse_include(k, v, *json_path, k)
                elif k == "snippets":
                    self._parse_str_or_none(v, "snippets", *json_path)
                elif k == "variables":
                    self._parse_variables(k, v, *json_path, k)
                else:
                    raise validation_error("is not a valid key", *json_path, k)
        else:
            raise validation_error("must be a mapping", *json_path)
        self.resolve()

    def _parse_include(self, k, v, *json_path):
        if v is None:
            pass
        elif isinstance(v, list):
            for i, item in enumerate(v):
                self.include.append(IncludeConfig(item, *json_path, i))
        else:
            raise validation_error("must be a non-empty string or list of strings", *json_path)

    def _parse_variables(self, k, v, *json_path):
        if v is None:
            pass
        elif isinstance(v, dict):
            for vk, vv in v.items():
                if not isinstance(vv, str):
                    raise validation_error("must be a string or null", *json_path, vk)
            self.variables.update(v)
            self._original_variables.update(v)
        else:
            raise validation_error("must be a mapping or null", *json_path)

    def resolve(self):
        # Coalesce includes into variables
        for include in self.include:
            try:
                data = None
                with open(include.path) as f:
                    data = json.load(f)
            except FileNotFoundError as ex:
                if not include.optional:
                    raise DotsError(f"include file {include.path} does not exist") from ex
            except IOError as ex:
                raise DotsError(f"could not open include file {include.path}") from ex
            except (OverflowError, TypeError, ValueError) as ex:
                raise DotsError(f"include file {include.path} contents are not valid") from ex
            if data is None:
                continue
            if isinstance(data, dict):
                for vk, vv in data.items():
                    if not isinstance(vv, str):
                        raise DotsError(f"include file {include.path} must be a mapping of string to string")
            else:
                raise DotsError(f"include file {include.path} must be a mapping of string to string")
            self.variables.update(data)
        if self.snippets is not None:
            for (dirpath, _, filenames) in os.walk(self.snippets):
                for filename in filenames:
                    p = os.path.join(dirpath, filename)
                    try:
                        data = None
                        with open(p) as f:
                            data = f.read()
                    except FileNotFoundError as ex:
                        if not include.optional:
                            raise DotsError(f"snippets file {p} does not exist") from ex
                    except IOError as ex:
                        raise DotsError(f"could not open snippets file {p}") from ex
                    v = os.path.basename(p).split(".")[0] # Remove all extensions
                    self.variables[v] = data
                break

    def to_json(self, minify=True):
        data = {
            "begin": safe_to_json(self.begin, minify=minify),
            "end": safe_to_json(self.end, minify=minify),
            "include": safe_to_json(self.include, minify=minify),
            "snippets": safe_to_json(self.snippets, minify=minify),
            "variables": safe_to_json(self._original_variables, minify=minify)
        }
        if minify:
            dict_remove_if(data, "begin", None, Default.TEMPLATE_BEGIN)
            dict_remove_if(data, "end", None, Default.TEMPLATE_END)
            dict_remove_if(data, "include", None, [])
            dict_remove_if(data, "snippets", None, Default.TEMPLATE_SNIPPETS)
            dict_remove_if(data, "variables", None, {})
        return data

def parse_args():
    """
    Create an argument parse for the command line and parse the inputs.

    # Returns

    (Namespace) The parsed arguments.
    """
    import argparse

    p = argparse.ArgumentParser(
        description="Manage dot files",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.set_defaults(subcommand=None)

    # Global flags
    p.add_argument("-c", "--config", metavar="FILE",
        action="store", dest="config_file",
        default=Default.CONFIG_FILE,
        help="config file path")
    p.add_argument("-v", "--verbose", action="store_true",
        help="enable verbose output")
    p.add_argument("-n", "--dry-run", action="store_true",
        help="enable a dry run which does modify any files on disk")

    # Subcommands
    sp = p.add_subparsers(title="subcommands", dest="subcommand",
        required=True)
    # Build subcommand
    sp_build = sp.add_parser("build", help="Build packages locally")
    sp_build.add_argument("packages", metavar="PACKAGE", nargs="*",
        help="package name to operate on")
    # Format subcommand
    sp_format = sp.add_parser("format", help="Format the configuration file")
    # Install subcommand
    sp_install = sp.add_parser("install",
        help="Install packages on the system")
    sp_install.add_argument("packages", metavar="PACKAGE", nargs="*",
        help="package name to operate on")

    return p.parse_args()

def format_json(data, filename):
    """
    Format a JSON object.

    # Arguments

    * data (dict|list|bool|int|float|NoneType|str): The JSON object.
    * filename (str): The name of the file to dump the formatted JSON. If the
      contents of the file are identical to the formatted JSON then it is not
      updated.

    # Returns

    (bool) True if the file war modified, false otherwise.
    """
    s = json.dumps(data, indent=2, sort_keys=True)
    with open(filename, "a+") as f:
        f.seek(0)
        original = f.read()
        f.seek(0)
        file_contents_valid = True
        try:
            original_data = json.load(f)
        except (OverflowError, TypeError, ValueError):
            file_contents_valid = False
        clean = s + "\n"
        if original != clean:
            f.truncate(0)
            f.write(clean)
            return True
    return False

def file_modifiers(file_config):
    """
    Generate a string containing file modifier information to print.

    # Arguments

    * file_config (FileConfig): A file configuration.

    # Returns

    (str): When modifiers are present, the string contains the modifiers and a
    leading space so it can be appended on to another string. When there are no
    modifiers an empty string is returned.
    """
    ms = []
    if file_config.executable:
        ms.append("executable")
    if file_config.template:
        ms.append("template")
    s = ", ".join(ms)
    if s:
        s = f" ({s})"
    return s

def fill_template(templates_config, text):
    """
    Fill in a template.

    # Arguments

    * templates_config (TemplatesConfig): A template configuration.
    * text (str): The text of the template.

    # Returns

    (str): The filled in template.

    # Raises

    (BuildError): The template was invalid.
    """
    local_vs = {}
    for k, v in templates_config.variables.items():
        local_vs["_" + k] = v
    p = re.escape(templates_config.begin) + "(.*?)" + re.escape(templates_config.end)
    try:
        text = re.sub(p,
            lambda m: str(eval(m.groups()[0], {}, local_vs)),
            text,
            flags=re.DOTALL)
    except Exception as ex:
        raise BuildError(str(ex)) from ex
    return text

def file_executable(file_path, executable):
    """
    Enable or disable executable permissions on a file.

    # Arguments

    * file_path (str): The path to the file.
    * executable (bool): Whether the file should be executable or not.
    """
    mask = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    p = os.stat(file_path)[stat.ST_MODE]
    if executable:
        pn = p | mask
    else:
        pn = p & ~mask
    # Only change the permission if it is different
    if pn != p:
        os.chmod(file_path, pn)

def process_file(config, file_config, src_path, dest_path=None):
    """
    Process a single file by filling the template, making it executable, and
    putting it where it belongs on the system.

    # Arguments

    * config (Config): A configuration.
    * file_config (FileConfig): A file configuration.
    * src_path (str): The path to the file source.
    * dest_path (str): The path to the file destination.
    """
    if dest_path is None:
        dest_path = file_config.dest
    if dest_path is not None:
        dest_path = expand_path(dest_path)
    # Load file
    with open(src_path) as f:
        text = f.read()
    if file_config.template:
        text = fill_template(config.templates, text)
    if dest_path is not None:
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with open(dest_path, "w") as f:
            f.write(text)
        file_executable(dest_path, file_config.executable)

def traverse_packages(config, package_names, build=False, install=False,
        verbose=None, dry_run=None):
    """
    Traverse the packages and run build and install operations.

    # Arguments

    * config (Config): The configuraiton.
    * packages_names (list<str>): A list of package names to install.
    * build (bool): Build the packages.
    * install (bool): Install the packages.
    * verbose (bool): Enable verbose output.
    * dry_run (bool): Enable dry run output.
    """
    for dep in dependent_packages(config, package_names):
        package = config.packages[dep]
        files = package.files if package.files else {}
        for src_path, file_config in files.items():
            if build:
                err = False
                msg = None
                try:
                    dest_path = os.path.join(config.build.dir, os.path.relpath(src_path))
                    process_file(config, file_config, src_path, dest_path=dest_path)
                except BuildError as ex:
                    err = True
                    msg = str(ex)
                Fmt.status(Title.BUILD + file_modifiers(file_config),
                    src=src_path, target=dest_path,
                    msg=msg, err=err,
                    verbose=verbose, dry_run=dry_run)
                if err:
                    sys.exit(1)
            if install:
                err = False
                msg = None
                try:
                    process_file(config, file_config, src_path)
                except BuildError as ex:
                    err = True
                    msg = str(ex)
                Fmt.status(Title.INSTALL + file_modifiers(file_config),
                    src=src_path, target=file_config.dest,
                    msg=msg, err=err,
                    verbose=verbose, dry_run=dry_run)
                if err:
                    sys.exit(1)

def dependent_packages(config, package_names):
    """
    Find all packages that must be installed.

    # Arguments

    * config (Config): The configuration.
    * package_names (list<str>): The packages to be installed.

    # Returns

    (list<str>) All of the packages in `package_names` plus any dependencies
    found.
    """
    packages = set()
    candidates = {}
    for pn in package_names:
        candidates[pn] = None
    while candidates:
        name, required_by = candidates.popitem()
        if name in config.packages:
            packages.add(name)
            for require in config.packages[name].requires:
                candidates[require] = name
            for p in packages:
                if p in candidates:
                    candidates.pop(p)
        else:
            if required_by is not None:
                raise DotsError(
                    f"package \"{name}\" required by \"{required_by}\" does not exist")
            raise DotsError(f"package \"{name}\" does not exist")
    return sorted(packages)

def main():
    args = parse_args()

    with open(args.config_file) as f:
        data = json.load(f)
        config = Config(data)

    run_format = False

    if args.subcommand == "build":
        traverse_packages(config, args.packages, build=True, install=False,
                 verbose=args.verbose, dry_run=args.dry_run)
    elif args.subcommand == "format":
        run_format = True
    elif args.subcommand == "install":
        traverse_packages(config, args.packages, build=False, install=True,
                 verbose=args.verbose, dry_run=args.dry_run)
    else:
        # This will never be hit
        Fmt.status(Title.EXCEPTION, src=args.subcommand,
            msg="Command not specified", err=True)
        sys.exit(1)

    if run_format or config.build.format:
        written = False
        if not args.dry_run:
            written = format_json(config.to_json(), filename=args.config_file)
        if args.dry_run or written:
            Fmt.status(Title.FORMAT, src=args.config_file,
                verbose=args.verbose, dry_run=args.dry_run)

if __name__ == "__main__":
    try:
        main()
    except (json.decoder.JSONDecodeError, JSONError) as ex:
        Fmt.status(Title.EXCEPTION, src="JSON Validation", msg=str(ex), err=True)
    except FileNotFoundError as ex:
        Fmt.status(Title.EXCEPTION, msg=str(ex), err=True)
    except DotsError as ex:
        Fmt.status(Title.EXCEPTION, msg=str(ex), err=True)
