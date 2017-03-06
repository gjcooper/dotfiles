#!/usr/bin/env python3
#
import sys
import os


class LinkManager():
    """manages all links for the setup script"""
    def __init__(self, basedir):
        super().__init__()
        self.rawlinks = os.listdir(basedir)
        self.basedir = basedir
        self.links = {}
        self.base = {}
        self.userdir = os.path.expanduser('~')
        self.__process__()

    def __linkname__(self, srclinkname):
        """get destination link name from source file"""
        linksplit = srclinkname.split('.')
        return os.path.join(self.userdir, '.' + linksplit[-2])

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
                'i3config.manual': os.path.join(self.userdir, '.config', 'i3', 'config'),
                'conkyrc1.manual': os.path.join(self.userdir, 'conkyrc1'),
                'terminator.manual': os.path.join(self.userdir, '.config', 'terminator', 'config')
                }
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
        modlinkname = basefile.rsplit('.')[0]
        basetext = self.linkman.base[basefile]
        for k, v in replacefunc().items():
            basetext = basetext.replace(k, v)
        with open(self.linkman.fullpath(modlinkname), 'x') as modfile:
            modfile.write(basetext)
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

    def colorise(self):
        """Set up the solarised color scheme"""

        

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
    sm.install_links()
    sm.setup('vim')
    sm.setup('ohmyzsh')


if __name__ == '__main__':
    runall(sys.argv[1])
