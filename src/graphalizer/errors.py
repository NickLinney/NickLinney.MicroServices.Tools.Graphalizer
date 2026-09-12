"""Stable application error classes and CLI exit codes."""


class GraphalizerError(Exception):
    exit_code = 1


class InputError(GraphalizerError):
    exit_code = 64


class RenderError(GraphalizerError):
    exit_code = 65


class ConversionError(GraphalizerError):
    exit_code = 66


class StorageError(GraphalizerError):
    exit_code = 73


class RenderTimeoutError(RenderError):
    exit_code = 75
