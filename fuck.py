diff - -git
a / README.md
b / README.md
index
46
a1d24b..f702ac5e
100644
--- a / README.md
+++ b / README.md


@ @-456

, 6 + 456, 7 @ @ Or
via
environment
variables:
*`THEFUCK_RULES` & ndash;
list
of
enabled
rules, like
`DEFAULT_RULES: rm_root
` or `sudo: no_command
`;
*`THEFUCK_EXCLUDE_RULES` & ndash;
list
of
disabled
rules, like
`git_pull: git_push
`;
*`THEFUCK_REQUIRE_CONFIRMATION` & ndash;
require
confirmation
before
running
new
command, `true / false`;
+ * `THEFUCK_REQUIRE_DOUBLE_CONFIRMATION` & ndash;
require
double
confirmation
before
running
potentially
volitile
commands(eg.
`reboot`), value
of
`true / false`;
*`THEFUCK_WAIT_COMMAND` & ndash;
max
amount
of
time in seconds
for getting previous command output;
*`THEFUCK_NO_COLORS` & ndash;
disable
colored
output, `true / false`;
*`THEFUCK_PRIORITY` & ndash;
priority
of
the
rules, like
`no_command = 9999:apt_get = 100
`,
diff - -git
a / thefuck / const.py
b / thefuck / const.py
index
d272f1b2..fb8eab93
100644
--- a / thefuck / const.py
+++ b / thefuck / const.py


@ @-28

, 10 + 28, 13 @ @


def __repr__(self):
    DEFAULT_RULES = [ALL_ENABLED]
    DEFAULT_PRIORITY = 1000


+DOUBLE_CONFIRMATION_SCRIPTS = {"reboot": "Are you sure you would like to reboot the system?"}
+
DEFAULT_SETTINGS = {'rules': DEFAULT_RULES,
                    'exclude_rules': [],
                    'wait_command': 3,
                    'require_confirmation': True,
                    +                    'require_double_confirmation': False,
                    'no_colors': False,
                    'debug': False,
                    'priority': {},
                   @ @ -49, 6 + 52, 7 @ @


def __repr__(self):
    'THEFUCK_EXCLUDE_RULES': 'exclude_rules',
    'THEFUCK_WAIT_COMMAND': 'wait_command',
    'THEFUCK_REQUIRE_CONFIRMATION': 'require_confirmation',
    +               'THEFUCK_REQUIRE_DOUBLE_CONFIRMATION': 'require_double_confirmation',
    'THEFUCK_NO_COLORS': 'no_colors',
    'THEFUCK_DEBUG': 'debug',
    'THEFUCK_PRIORITY': 'priority',
    diff - -git
    a / thefuck / entrypoints / fix_command.py
    b / thefuck / entrypoints / fix_command.py
    index
    47e9856
    d.
    .6946653
    e
    100644
    --- a / thefuck / entrypoints / fix_command.py
    +++ b / thefuck / entrypoints / fix_command.py

    @ @-6

    , 7 + 6, 7 @ @
    from ..conf import settings
    from ..corrector import get_corrected_commands
    from ..exceptions import EmptyCommand


-
from ..ui import select_command, confirm_command

+
from ..ui import select_command
from ..utils import get_alias, get_all_executables


@ @-29

, 7 + 29, 6 @ @


def _get_raw_command(known_args):
    def fix_command(known_args):
        """Fixes previous command. Used when `thefuck` called without arguments."""
        settings.init(known_args)


-    double_check_commands = {"reboot": "reboot system?"}
with logs.debug_time('Total'):
    logs.debug(u'Run with settings: {}'.format(pformat(settings)))
    raw_command = _get_raw_command(known_args)


@ @-43

, 11 + 42, 7 @ @


def fix_command(known_args):
    corrected_commands = get_corrected_commands(command)
    selected_command = select_command(corrected_commands)


-        confirmation = True
-
if selected_command.script in double_check_commands:
    -            confirmation = confirm_command(double_check_commands[selected_command.script])
-
-
if selected_command and confirmation:
    +
    if selected_command:
        selected_command.run(command)
else:
    sys.exit(1)
diff - -git
a / thefuck / logs.py
b / thefuck / logs.py
index
a69d7d00.
.54
a856a6
100644
--- a / thefuck / logs.py
+++ b / thefuck / logs.py


@ @-57

, 33 + 57, 34 @ @


def show_corrected_command(corrected_command):
    def confirm_text(corrected_command):


-
if corrected_command.script != 'reboot system?':
    -        sys.stderr.write(
        -            (u'{prefix}{clear}{bold}{script}{reset}{side_effect} '
                      - u'[{green}enter{reset}/{blue}↑{reset}/{blue}↓{reset}'
                      - u'/{red}ctrl+c{reset}]').format(
            -                prefix = const.USER_COMMAND_MARK,
                                      -                script = corrected_command.script,
                                                                -                side_effect = ' (+side effect)' if corrected_command.side_effect else '',
                                                                                               -                clear = '\033[1K\r',
                                                                                                                        -                bold = color(
        colorama.Style.BRIGHT),
                                                                                                                                                -                green = color(
        colorama.Fore.GREEN),
                                                                                                                                                                         -                red = color(
        colorama.Fore.RED),
                                                                                                                                                                                                -                reset = color(
        colorama.Style.RESET_ALL),
                                                                                                                                                                                                                         -                blue = color(
        colorama.Fore.BLUE)))
    - else:
    -        sys.stderr.write(
        -            (u'{prefix}{clear}{bold}{script}{reset}{side_effect} '
                      - u'[{green}enter{reset}'
                      - u'/{red}ctrl+c{reset}]').format(
            -                prefix = const.USER_COMMAND_MARK,
                                      -                script = corrected_command.script,
                                                                -                side_effect = ' (+side effect)' if corrected_command.side_effect else '',
                                                                                               -                clear = '\033[1K\r',
                                                                                                                        -                bold = color(
        colorama.Style.BRIGHT),
                                                                                                                                                -                green = color(
        colorama.Fore.GREEN),
                                                                                                                                                                         -                red = color(
        colorama.Fore.RED),
                                                                                                                                                                                                -                reset = color(
        colorama.Style.RESET_ALL)))
    +    sys.stderr.write(
        +        (u'{prefix}{clear}{bold}{script}{reset}{side_effect} '
                  + u'[{green}enter{reset}/{blue}↑{reset}/{blue}↓{reset}'
                  + u'/{red}ctrl+c{reset}]').format(
            +            prefix = const.USER_COMMAND_MARK,
                                  +            script = corrected_command.script,
                                                        +            side_effect = ' (+side effect)' if corrected_command.side_effect else '',
                                                                                   +            clear = '\033[1K\r',
                                                                                                        +            bold = color(
        colorama.Style.BRIGHT),
                                                                                                                            +            green = color(
        colorama.Fore.GREEN),
                                                                                                                                                 +            red = color(
        colorama.Fore.RED),
                                                                                                                                                                    +            reset = color(
        colorama.Style.RESET_ALL),
                                                                                                                                                                                         +            blue = color(
        colorama.Fore.BLUE)))
    +
    +
    +


    def double_confirm_text(confirmation_text):
        +    sys.stderr.write(
            +        (u'{prefix}{clear}{bold}{text}{reset} '
                      + u'[{green}enter{reset}'
                      + u'/{red}ctrl+c{reset}]').format(
                +            prefix = const.USER_COMMAND_MARK,
                                      +            text = confirmation_text,
                                                          +            clear = '\033[1K\r',
                                                                               +            bold = color(
            colorama.Style.BRIGHT),
                                                                                                   +            green = color(
            colorama.Fore.GREEN),
                                                                                                                        +            red = color(
            colorama.Fore.RED),
                                                                                                                                           +            reset = color(
            colorama.Style.RESET_ALL),
                                                                                                                                                                +        ))

        def debug(msg):

            @ @-153

        , 16 + 154, 3 @ @

        def version(thefuck_version, python_version, shell_info):
            u'The Fuck {} using Python {} and {}\n'.format(thefuck_version,
                                                           python_version,
                                                           shell_info))
            -
            -
            -

            def confirmation(confirm, msg):

                -
            if confirm is True:
                -        sys.stderr.write(u"\n{bold}System will now {message}\n{reset}".format(
                    -            bold = color(colorama.Style.BRIGHT),
                                        -            message = msg[:-1],
                                                               -            reset = color(colorama.Style.RESET_ALL)))
            - else:
            -        sys.stderr.write(u"\n{bold}{message} cancelled{reset}\n".format(
                -            bold = color(colorama.Style.BRIGHT),
                                    -            message = msg[:-1],
                                                           -            reset = color(colorama.Style.RESET_ALL)))
            diff - -git
            a / thefuck / ui.py
            b / thefuck / ui.py
            index
            b3813437..ebe05a9e
            100644
            --- a / thefuck / ui.py
            +++ b / thefuck / ui.py

            @ @-6

            , 7 + 6, 6 @ @
            from .system import get_key
            from .utils import get_alias
            from . import logs, const
            -
            from .types import CorrectedCommand

            def read_actions():

                @ @-81

            , 10 + 80, 13 @ @

            def select_command(corrected_commands):

                logs.confirm_text(selector.value)

            -
            for action in read_actions():
                +    selected = False
            +
            while not selected:
                +        action = next(read_actions())
            +
            if action == const.ACTION_SELECT:
                sys.stderr.write('\n')
            -
            return selector.value
            +            selected = True
            elif action == const.ACTION_ABORT:
            logs.failed('\nAborted')
            return

            @ @-95

            , 26 + 97, 20 @ @

            def select_command(corrected_commands):
                selector.next()
                logs.confirm_text(selector.value)

            +
            if settings.require_double_confirmation and selector.value.script in const.DOUBLE_CONFIRMATION_SCRIPTS:
                +        selector.value = double_confirm(selector)

            -

            def confirm_command(confirmation_text):
                -    """Returns:
-
-     - the first command when confirmation disabled;
-     - None when ctrl+c pressed;
-     - selected command.
-
-    :type corrected_commands: Iterable[thefuck.types.CorrectedCommand]
-    :rtype: thefuck.types.CorrectedCommand | None
+    return selector.value

-    """

            -    logs.confirm_text(CorrectedCommand(confirmation_text, None, 0))
            +

            def double_confirm(selector):
                +    confirmation_text = const.DOUBLE_CONFIRMATION_SCRIPTS[selector.value.script]

            +    logs.double_confirm_text(confirmation_text)

            -    action = read_actions()
            for action in read_actions():
                if action == const.ACTION_SELECT:
            -            logs.confirmation(True, confirmation_text)
            -
            return True
            +            sys.stderr.write('\n')
            +
            return selector.value
            elif action == const.ACTION_ABORT:
            -            logs.confirmation(False, confirmation_text)
            -
            return False
            +            logs.failed('\nAborted')
            +
            return