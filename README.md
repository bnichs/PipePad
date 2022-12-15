# PipePad
PipePad is a utility for writing code just a little bit too complicated for  pipes and the command line. It's and easy-to-use platform for handling stream processing in a way that doesn't require so much repetition--Gone are the days of ::edit-up-enter:: over and over, and gone are the days of overly complicated single-line shell scripts or worse, awk scripts, PipePad gives you the benefits of strong scripting languages with the versatility of pipe commands.


## Demo
Some damn videos

## Usage


#### REPO_ID
Repos are identified using the following syntax:
- `git://foo.bar.com/`
- `file://foo/bar/repo`
- `local`

#### PAD_ID
Pads are identified using the following syntax:
- `local/sum_timestamps:latest`
- `sum_timestamps:latest`
- `sum_timestamps`
- `sum_timestamps:4`
- `git://foo.bar.com/sum_timestamps:latest`

### Piping pads
```shell
# Create a pad with the default language
cat sample_data/timestamps.txt | pad 

# Specify langauge
cat sample_data/timestamps.txt | pad --language=python

# Execute a specific pad against file 
cat sample_data/timestamps.txt | pad run PAD_ID
```


### Managing pads

#### List
```shell
# Defaults to all pads in all repos
pad list 

# Allow drilldown into pads
pad list pads

# List just the repos 
pad list repos

# TODO Different than just `pad show PAD_ID`????
pad list versions PAD_ID
```

#### Edit
```shell
pad edit PAD_ID

```

#### Add
```shell
pad add repo REPO_ID

pad add file://fooo
```


#### Remove
```shell
pad remove repo REPO_ID

pad remove PAD_ID
```


#### Show
```shell
pad show pad PAD_ID

#? needed
pad show version PAD_ID

pad show repo REPO_ID
```

### Config
```shell
# Show the config file or contents
pad config show file

# Edit the config file
pad config edit

pad config set $CONFIG_ID val

pad config get $CONFIG_ID
```


## What it does 

## How it Works


## Development
