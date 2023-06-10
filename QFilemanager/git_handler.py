import os
from datetime import datetime

class CommitObject:
    def __init__(self, before, commit_message, branch, author, diff, now):
        self.before = before
        self.commit_message = commit_message
        self.branch = branch
        self.author = author
        self.diff = diff
        self.now = now

def git_status(dir_path):
    os.chdir(dir_path)
    result = os.popen('git status').read()
    print('result: ' + result)
    if result == '':
        return False
    return True

def git_init(dir_path):
    os.chdir(dir_path)
    result = os.popen('git init').read()
    if "fatal: " in result:
        return False
    return True

def git_add(dir_path, file_name):
    os.chdir(dir_path)
    result = os.popen('git add "' + file_name + '"').read()
    return True

def git_restore(dir_path, file_name):
    os.chdir(dir_path)
    result = os.popen('git restore "' + file_name + '"').read()
    if "fatal: " in result:
        return False
    return True

def git_restore_staged(dir_path, file_name):
    os.chdir(dir_path)
    result = os.popen('git restore --staged "' + file_name + '"').read()
    if "fatal: " in result:
        return False
    return True

def git_untrack(dir_path, file_name):
    os.chdir(dir_path)
    result = os.popen('git rm --cached "' + file_name + '"').read()
    if "fatal: " in result:
        return False
    return True

def git_rm(dir_path, file_name):
    os.chdir(dir_path)
    result = os.popen('git rm "' + file_name + '"').read()
    if "fatal: " in result:
        return False
    return True

def git_mv(dir_path, file_name, new_name):
    os.chdir(dir_path)
    result = os.popen('git mv "' + file_name + '" "' + new_name + '"').read()
    if "fatal: " in result:
        return False
    return True

def git_commit(dir_path, commit_msg, branch):
    global commit_history

    os.chdir(dir_path)
    result = os.popen('git commit -m "' + commit_msg + '"').read()
    if "fatal: " in result:
        return False
    
    author = 'USER' # TODO: 현재 작성자 추가하기
    diff = os.popen('git diff --staged').read().split('\n')
    now = datetime.today().strftime('%Y-%m-%d %H:%M')
    before = None if len(commit_history[branch]) == 0 else commit_history[branch][-1]
    commit_history[branch].append(CommitObject(before, commit_msg, branch, author, diff, now))
    return True

def get_status_list(dir_path):
    os.chdir(dir_path)

    status_list = {}

    result = os.popen('git status').read().split('\n')


    # for changes staged
    staged_index = -1
    if 'Changes to be committed:' in result:
        staged_index = result.index('Changes to be committed:')
    
    staged = {}
    staged['renamed'] = []
    staged['new'] = []
    staged['modified'] = []
    staged['deleted'] = []

    if not staged_index == -1:
        i = 2
        while '\t' in result[staged_index + i]:
            if 'renamed' in result[staged_index + i].split()[0]:
                staged['renamed'].append(" ".join(result[staged_index + i].split()[3:]))
            if 'new' in result[staged_index + i].split()[0]:
                staged['new'].append(" ".join(result[staged_index + i].split()[2:]))
            if 'modified' in result[staged_index + i].split()[0]:
                staged['modified'].append(" ".join(result[staged_index + i].split()[1:]))
            if 'deleted' in result[staged_index + i].split()[0]:
                staged['deleted'].append(" ".join(result[staged_index + i].split()[1:]))            
            i = i + 1


    # for changes not staged
    not_staged_index = -1
    if 'Changes not staged for commit:' in result:
        not_staged_index = result.index('Changes not staged for commit:')

    not_staged = {}
    not_staged['renamed'] = []
    not_staged['new'] = []
    not_staged['modified'] = []
    not_staged['deleted'] = []

    if not not_staged_index == -1:
        i = 3
        while '\t' in result[not_staged_index + i]:
            if 'renamed' in result[not_staged_index + i].split()[0]:
                not_staged['renamed'].append(" ".join(result[not_staged_index + i].split()[3:]))
            if 'new' in result[not_staged_index + i].split()[0]:
                not_staged['new'].append(" ".join(result[not_staged_index + i].split()[2:]))
            if 'modified' in result[not_staged_index + i].split()[0]:
                not_staged['modified'].append(" ".join(result[not_staged_index + i].split()[1:]))
            if 'deleted' in result[not_staged_index + i].split()[0]:
                not_staged['deleted'].append(" ".join(result[not_staged_index + i].split()[1:]))
            i = i + 1


    # for untracked files
    untracked_index = -1
    if 'Untracked files:' in result:
        untracked_index = result.index('Untracked files:')
    
    untracked = []
    
    if not untracked_index == -1:
        i = 2
        while '\t' in result[untracked_index + i]:
            untracked.append(" ".join(result[untracked_index + i].split()[0:]))
            i = i + 1
    

    status_list['staged'] = staged
    status_list['not_staged'] = not_staged
    status_list['untracked'] = untracked

    return status_list

commit_history = {'main': []}