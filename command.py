class command:
    def __init__(self, name='', description='', function=None):
        self.name = name
        self.description = description
        self.f = function

    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def set_function(self, function):
        self.f = function

    def exec(self, argvs):
        self.f(argvs)

    def help(self):
        return self.description

    def __repr__(self):
        s = 'name = %s' % self.name
        s += 'description = %s' % self.description
        s += 'f = %s' % self.f
        return s


class command_book:
    def __init__(self):
        self.command = {}
        self.command['help'] = command(
            'help',
            '''
help [command] to get description of each command
try these commands below.
''',
            self.help
        )

    def append(self, c):
        if(isinstance(c, command)):
            self.command[c.name] = c
# don't check for existence of c:
# if c exist then rewrite command
        else:
            raise AttributeError('Not a command block!')

    def ret_command_list(self):
        return self.command

    def help(self, argvs):
        argv = argvs.split(' ')
        if(argv[0] == ''):
            result = ''
            for i in self.command.values():
                result = result + i.name + ', '
            result = result[:-2]
            print(self.command['help'].description)
            print(result)
        else:
            if argv[0] in self.command.keys():
                print(self.command[argv[0]].help())
            else:
                print('There is no command like that!')

    def print(self):
        print(self.command)
