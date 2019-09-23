import logging
import sys

from .base import GraphQLError

__all__ = ['GraphQLLocatedError']

DEFAULT_OUTGOING_ERROR_STRING = "Error processing request."

logger = logging.getLogger(__name__)


class GraphQLLocatedError(GraphQLError):

    def __init__(self, nodes, original_error=None):
        if original_error:

            if not getattr(original_error, "is_outgoing", False):
                level = logging.ERROR
                exc_info = original_error

                message = DEFAULT_OUTGOING_ERROR_STRING

            else:
                level = logging.INFO
                exc_info = False
                try:
                    message = str(original_error)
                except UnicodeEncodeError:
                    message = original_error.message.encode('utf-8')

            logger.log(
                level,
                "%s caught: %s",
                type(original_error).__name__,
                str(original_error),

                extra={
                    "nodes": repr(nodes),
                },
                exc_info=exc_info,
            )

        else:
            message = 'An unknown error occurred.'

        stack = (
            original_error
            and (
                getattr(original_error, "stack", None)
                # unfortunately, this is only available in Python 3:
                or getattr(original_error, "__traceback__", None)
            )
            or sys.exc_info()[2]
        )

        super(GraphQLLocatedError, self).__init__(
            message=message,
            nodes=nodes,
            stack=stack
        )
        self.original_error = original_error
