Clone the original `rockstar-galaxies` repository from BitBucket
```
git clone https://bitbucket.org/pbehroozi/rockstar-galaxies.git
```

To maintain it, we connect it to own GitHub.

## Check old repository link
- Run`git remote show origin` which outputs
    ```
    * remote origin
    Fetch URL: https://bitbucket.org/pbehroozi/rockstar-galaxies.git
    Push  URL: https://bitbucket.org/pbehroozi/rockstar-galaxies.git
    HEAD branch: main
    Remote branches:
        main   tracked
        master tracked
    Local branch configured for 'git pull':
        main merges with remote main
    Local ref configured for 'git push':
        main pushes to main (up to date)
    ```
    The output says the current `Fetch` and `Push` URL which is linked to original repo. 

- Run `git config --list` which outputs
    ```
    user.name=RanitBehera
    user.email=ranitbehera1998@gmail.com
    core.repositoryformatversion=0
    core.filemode=true
    core.bare=false
    core.logallrefupdates=true
    remote.origin.url=https://bitbucket.org/pbehroozi/rockstar-galaxies.git
    remote.origin.fetch=+refs/heads/*:refs/remotes/origin/*
    branch.main.remote=origin
    branch.main.merge=refs/heads/main
    ```
Here we see the `remote.origin.url` is linked to original repository which we need to change.

## Set new repository link
We open GitHub and create a new repository named `rockstar-galxies` which gives us the new repository URL `https://github.com/RanitBehera/rockstar-galaxies.git`. We need to update the git config to this new URL. 


GitHub suggests the following for pushing an existing repository from the command line.
```
git remote add origin https://github.com/RanitBehera/rockstar-galaxies.git
git branch -M main
git push -u origin main
```
But this is for new repository which is never linked to any URL. We need to update the old URL. So we do any one of the following. Both works the same.
- Run `git remote set-url origin https://github.com/RanitBehera/rockstar-galaxies.git`
- Or open `.git/congif` and edit the `[remote "origin"]` url.

We do the first and then again run `git remote show origin` and we get
```
* remote origin
  Fetch URL: https://github.com/RanitBehera/rockstar-galaxies.git
  Push  URL: https://github.com/RanitBehera/rockstar-galaxies.git
  HEAD branch: (unknown)
  Remote branches:
    refs/remotes/origin/main   stale (use 'git remote prune' to remove)
    refs/remotes/origin/master stale (use 'git remote prune' to remove)
  Local branch configured for 'git pull':
    main merges with remote main
```
We see that the `Fetch` and `Push` url to be updated. To fix unknown HEAD branch we do the following as sugested by GitHub. Run 
`git branch -M main` and `git push -u origin main`.
Then again run `git remote show origin` which outputs
```
* remote origin
  Fetch URL: https://github.com/RanitBehera/rockstar-galaxies.git
  Push  URL: https://github.com/RanitBehera/rockstar-galaxies.git
  HEAD branch: main
  Remote branches:
    main                       tracked
    refs/remotes/origin/master stale (use 'git remote prune' to remove)
  Local branch configured for 'git pull':
    main merges with remote main
  Local ref configured for 'git push':
    main pushes to main (up to date)
```
As we have done a `git push`, go to GitHub and update. You should see the reposity files there.

## Compile original code
Run `make`. You will see various errors and warnings mostly path related to linking errors. The original `Makefile` is backed up as `Makefile.bak` and then modified to fix the erros as well as adding new files for compilation as needed. The modifications are mentioned in the files as comments.

