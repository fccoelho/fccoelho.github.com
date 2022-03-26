from fabric import task, local 

@task
def make():
    local('make html')
    
@task   
def deploy():
    local('git add *')
#    local('mv -f html/* .')
    local('git commit -a -m "updated"')
    local('git push')
    
