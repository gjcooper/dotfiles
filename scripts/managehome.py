#!/usr/bin/env python3
#
import sys
import os
import subprocess
import itertools

userdir = os.path.expanduser('~')
scriptdir = os.path.join(userdir, '.local', 'bin')
vundle_clone_call = ['git', 'clone', 'https://github.com/VundleVim/Vundle.vim.git', os.path.join(userdir, '.vim', 'bundle', 'Vundle.vim')]
vundle_plugin_call = ['vim', '+PluginInstall', '+qall']
ohmyzsh_clone_call = ['git', 'clone', 'https://github.com/robbyrussell/oh-my-zsh.git', os.path.join(userdir, '.oh-my-zsh')]
software_list = ['curl', 'vim-nox', 'gitk', 'zsh', 'tmux', 'python3', 'ipython',
                 'ipython3', 'dos2unix', 'python-pip', 'python3-pip', 'i3',
                 'terminator', 'suckless-tools', 'lightdm', 'dbus-x11', 'xsel',
                 'dkms', 'feh', 'conky', 'compton', 'python3-venv', 'python3-tk']


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

    def __process__(self):
        for rl in self.rawlinks:
            if rl.endswith('.symlink'):
                self.links[rl] = self.__linkname__(rl)
            elif rl.endswith('.base'):
                with open(self.fullpath(rl)) as linkbase:
                    self.base[rl] = linkbase.read()
            elif rl.endswith('.manual'):
                self.manual[rl] = self.lookUp(rl)
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
            'conkyrc1.manual': os.path.join(userdir, 'conkyrc1'),
            'terminator.manual': os.path.join(userdir, '.config', 'terminator', 'config')}
        return maplinks[linkname]


class SetupManager():
    '''Manages home directory setup for the script'''
    def __init__(self, repodir):
        self.repodir = repodir
        self.linkman = LinkManager(os.path.join(repodir, 'links'))

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

    def colorise(self):
        """Set up the solarised color scheme"""
        solar_git = ['git', 'clone', 'https://github.com/seebi/dircolors-solarized.git',
                     os.path.join(self.repodir, 'local', 'dircolors')]
        if subprocess.call(solar_git):
            message('info', 'Unable to clone dircolors repository')
        scheme = self.getinput(' - What is your preferred colour scheme? (dark/light)')
        if scheme not in {'dark', 'light'}:
            message('info', 'Unknown colour scheme selected')
            self.colorise()
        src = os.path.join(self.repodir, 'local', 'dircolors', 'dircolors.ansi-{}'.format(scheme))
        try:
            os.symlink(src, os.path.join(userdir, '.dircolors'))
        except FileExistsError:
            if self.getinput('Symlink for solarised already found: Regenerate (y/N)').upper() == 'Y':
                os.remove(os.path.join(userdir, '.dircolors'))
                os.symlink(src, os.path.join(userdir, '.dircolors'))
            else:
                return
        message('success', 'dircolors')

    def regen_or_ignore(self, src, dest):
        '''After a failed symlink call, either regenerate or continue'''
        if self.getinput('{} already exists, Regenerate (y/N)'.format(dest)).upper() == 'Y':
            os.remove(dest)
            os.symlink(src, dest)

    def install_software(self):
        """Install software provided in our list"""
        for sw in software_list:
            subprocess.call(['sudo', 'apt', '-y', 'install', sw])
        message('info', 'All software installed')

    def install_scripts(self):
        """Install scripts used for managing PC"""
        if not os.exists(os.path.join(userdir, '.local', 'bin')):
            os.makedirs(os.path.join(userdir, '.local', 'bin'))
        for script in os.listdir(os.path.join(userdir, 'dotfiles', 'scripts')):
            ans = self.getinput('Install {}? (Y/n)'.format(script))
            if ans.lower() in {'', 'y', 'yes'}:
                os.symlink(os.path.join(userdir, 'dotfiles', 'scripts'),
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


def runall(repodir):
    """run all setup scripts for a new home directory"""
    sm = SetupManager(repodir)
    sm.config('git')
    sm.config('pypi')
    sm.colorise()
    sm.install_software()
    sm.install_scripts()
    sm.install_links()
    sm.setup('vim')
    sm.setup('ohmyzsh')


if __name__ == '__main__':
    runall(sys.argv[1])
