import logging
import sys

from .base import GraphQLError

__all__ = ['GraphQLLocatedError']

DEFAULT_OUTGOING_ERROR_STRING = "Error processing request."

logger = logging.getLogger(__name__)


class GraphQLLocatedError(GraphQLError):

    def __init__(self, nodes, original_error=None):
        if original_error:

            if getattr(original_error, "is_outgoing", False):
                level = logging.INFO
                exc_info = False
                try:
                    message = str(original_error)
                except UnicodeEncodeError:
                    message = original_error.message.encode('utf-8')

            else:
                level = logging.WARNING
                exc_info = sys.exc_info()
                if exc_info[0] is None:
                    exc_info = False

                message = DEFAULT_OUTGOING_ERROR_STRING

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

        if hasattr(original_error, 'stack'):
            stack = original_error.stack
        else:
            stack = sys.exc_info()[2]

        super(GraphQLLocatedError, self).__init__(
            message=message,
            nodes=nodes,
            stack=stack
        )
        self.original_error = original_error
