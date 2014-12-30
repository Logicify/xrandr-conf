from profileconf.domain import ContextFunction

__author__ = 'corvis'

# this one expects to have "current_display" in context
predefined_resolution = ContextFunction.builder()\
    .set_name('preferredResolution')\
    .set_handler(lambda argument, context: context.get('current_display').preferred_mode.resolution)\
    .build()