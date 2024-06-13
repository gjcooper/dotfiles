#!/usr/bin/env python3
#
import sys
import os
import subprocess
import itertools
import argparse

userdir = os.path.expanduser('~')
scriptdir = os.path.join(userdir, '.local', 'bin')
ohmyzsh_clone_call = ['git', 'clone', 'https://github.com/robbyrussell/oh-my-zsh.git', os.path.join(userdir, '.oh-my-zsh')]
apt_software_list = ['vim-gtk', 'zsh', 'tmux', 'dos2unix', 'i3',
                     'bemenu', 'sway', 'swaylock', 'swayidle', 'swaybg']
other_software = ['curl https://pyenv.run | bash']


def directory_path(string):
    """takes a string and returns it if it refers to a directory,
    otherwise raise and argparse.ArgumentError"""
    if os.path.isdir(string):
        return string
    raise argparse.ArgumentTypeError('{} does not point to a directory'.format(string))


class LinkManager():
    """manages all links for the setup script"""
    def __init__(self, basedir):
        super().__init__()
        self.rawlinks = os.listdir(basedir)
        self.basedir = basedir
        self.links = {}
        self.base = {}
        self.manual = {}
        self.__process__()

    def __linkname__(self, srclinkname):
        """get destination link name from source file"""
        linksplit = srclinkname.split('.')
        try:
            return os.path.join(userdir, '.' + '.'.join(linksplit[0:-1]))
        except IndexError:
            message('fail', 'Unable to find 2nd last component of {}'.format(srclinkname + ":" + linksplit))

    def __configname__(self, srclinkname):
        """get destination link name from source file, new type of config file that
        is placed in a .config folder within the users home dir"""
        linksplit = srclinkname.split('.')
        try:
            return os.path.join(userdir, '.config', '.'.join(linksplit[0:-1]))
        except IndexError:
            message('fail', 'Unable to find 2nd last component of {}'.format(srclinkname + ":" + linksplit))

    def __process__(self):
        for rl in self.rawlinks:
            if rl.endswith('.symlink'):
                self.links[rl] = self.__linkname__(rl)
            elif rl.endswith('.base'):
                with open(self.fullpath(rl)) as linkbase:
                    self.base[rl] = linkbase.read()
            elif rl.endswith('.manual'):
                self.manual[rl] = self.lookUp(rl)
            elif rl.endswith('.config'):
                self.links[rl] = self.__configname__(rl)
            else:
                raise RuntimeError('Unknown link type for setup script')

    def fullpath(self, filename):
        """Return the full path for a given link file"""
        return os.path.join(self.basedir, filename)

    def lookUp(self, linkname):
        """look up the final location for a manual link file"""
        maplinks = {
            'i3config.manual': os.path.join(userdir, '.config', 'i3', 'config'),
            'i3statconfig.manual': os.path.join(userdir, '.config', 'i3status', 'config'),
            'flake8.manual': os.path.join(userdir, '.config', 'flake8'),
            'praw.manual': os.path.join(userdir, '.config', 'praw.ini'),
            'conkyrc1.manual': os.path.join(userdir, 'conkyrc1'),
            'terminator.manual': os.path.join(userdir, '.config', 'terminator', 'config')}
        return maplinks[linkname]


class SetupManager():
    '''Manages home directory setup for the script'''
    def __init__(self, repodir):
        self.repodir = os.path.abspath(repodir)
        self.linkman = LinkManager(os.path.join(self.repodir, 'links'))

    def getinput(self, text):
        message('user', text)
        return input()

    def base2link(self, replacefunc, basefile):
        """Get basefile text, replace using dict in replacefunc and write to new link"""
        if basefile not in self.linkman.base:
            raise RuntimeError('Expected {}, but not found in links directory'.format(basefile))
        modlinkname = basefile.rsplit('.', 1)[0]
        try:
            with open(self.linkman.fullpath(modlinkname), 'x') as modfile:
                basetext = self.linkman.base[basefile]
                for k, v in replacefunc().items():
                    basetext = basetext.replace(k, v)
                modfile.write(basetext)
        except FileExistsError:
            message('info', 'Generated symlink from base already exists, ignoring')
        self.linkman.links[modlinkname] = self.linkman.__linkname__(modlinkname)

    def __gitreplace__(self):
        print('Setting up gitconfig')
        author = self.getinput(' - What is your git author name?')
        email = self.getinput(' - What is your git author email?')
        gitcred = 'cache'
        return {'AUTHORNAME': author, 'AUTHOREMAIL': email, 'GIT_CREDENTIAL_HELPER': gitcred}

    def __pypireplace__(self):
        print('Setting up pypirc')
        pypiuser = self.getinput(' - What is your pypi user name?')
        pypipass = self.getinput(' - What is your pypi password?')
        testuser = self.getinput(' - What is your testpypi user name?')
        testpass = self.getinput(' - What is your testpypi password?')
        return {'PYPI_USERNAME': pypiuser, 'PYPI_PASSWD': pypipass,
                'TEST_USERNAME': testuser, 'TEST_PASSWD': testpass}

    def config(self, section):
        """Configure a section that requires user input"""
        if section == 'git':
            self.base2link(self.__gitreplace__, 'gitconfig.symlink.base')
        elif section == 'pypi':
            self.base2link(self.__pypireplace__, 'pypirc.symlink.base')
        else:
            message('fail', 'Unknown base symlink configuration section')
        message('success', section)

    def regen_or_ignore(self, src, dest):
        '''After a failed symlink call, either regenerate or continue'''
        if self.getinput('{} already exists, Regenerate (y/N)'.format(dest)).upper() == 'Y':
            os.remove(dest)
            os.symlink(src, dest)

    def install_software(self):
        """Install software provided in our list"""
        subprocess.run(['sudo', 'apt', 'install', '-y', *apt_software_list])
        for sw in other_software:
            subprocess.run(sw, shell=True)
        message('info', 'All software installed')

    def install_scripts(self):
        """Install scripts used for managing PC"""
        if not os.path.exists(scriptdir):
            os.makedirs(scriptdir)
        for script in os.listdir(os.path.join(userdir, 'dotfiles', 'scripts')):
            ans = self.getinput('Install {}? (Y/n)'.format(script))
            if ans.lower() in {'', 'y', 'yes'}:
                os.symlink(os.path.join(userdir, 'dotfiles', 'scripts', script),
                           os.path.join(userdir, '.local', 'bin', os.path.splitext(script)[0]))

    def install_links(self):
        """For each link in LinkManager install it to the home directory"""
        for src, dest in itertools.chain(self.linkman.links.items(), self.linkman.manual.items()):
            src = self.linkman.fullpath(src)
            try:
                os.symlink(src, dest)
            except FileExistsError:
                self.regen_or_ignore(src, dest)
            except FileNotFoundError:
                os.makedirs(os.path.dirname(dest))
                os.symlink(src, dest)
        message('success', 'symlinks')

    def setup(self, software):
        """Run the setup tasks for a certain software package"""
        if software == 'vim':
            message('info', 'Installing vim bundles')
            if subprocess.call(vundle_clone_call):
                message('info', 'Vundle clone failed, trying to use anyway')
            subprocess.call(vundle_plugin_call)
        elif software == 'ohmyzsh':
            message('info', 'Installing ohmyzsh')
            if subprocess.call(ohmyzsh_clone_call):
                message('info', 'Clone issue - perhaps oh-my-zsh directory already found in home dir')


def message(messagetype, messagetext):
    """Print a message to screen for the user"""
    if messagetype == 'info':
        print('\r  [ \033[00;34m..\033[0m ] {}\n'.format(messagetext))
    elif messagetype == 'user':
        print('\r  [ \033[0;33m??\033[0m ] {}\n'.format(messagetext))
    elif messagetype == 'success':
        print('\r\033[2K  [ \033[00;32mOK\033[0m ] {}\n'.format(messagetext))
    elif messagetype == 'fail':
        print('\r\033[2K  [\033[0;31mFAIL\033[0m] {}\n'.format(messagetext))
        sys.exit()
    else:
        message('fail', 'Unknown message type sent internally')


def runall(management_directory=None, config=['git', 'pypi'],
           software=True, scripts=True, links=True, setup=['vim', 'ohmyzsh']):
    """run all setup scripts for a new home directory"""
    sm = SetupManager(management_directory)
    for app in config:
        sm.config(app)
    run_args = [software, scripts, links]
    run_cmds = [sm.install_software, sm.install_scripts, sm.install_links]
    for runit, func in zip(run_args, run_cmds):
        if runit:
            func()
    for app in setup:
        sm.setup(app)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Set up a system')
    parser.add_argument('management_directory', type=directory_path, help='A path to the dotfiles base directory')
    parser.add_argument('--config', choices=['git', 'pypi'], default=[], nargs='+', help='Run the config process for the chosen program(s), getting manual input to add to the linked file')
    parser.add_argument('--software', action='store_true', help='Install all software in the list')
    parser.add_argument('--scripts', action='store_true', help='Install all user scripts in the ~/.local/bin directory (by linking)')
    parser.add_argument('--links', action='store_true', help='Install all user configuration files in the appropriate directory (by linking)')
    parser.add_argument('--setup', choices=['vim', 'ohmyzsh'], default=[], nargs='+', help='Installing and setting up vim bundles and/or ohmyzsh')

    args = parser.parse_args()
    if any(val for key, val in vars(args).items() if key != 'management_directory'):
        runall(**vars(args))
    else:
        runall(args.management_directory)
