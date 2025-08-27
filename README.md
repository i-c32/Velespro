~~~
----------------------------------------------------------------------------------------------------------------
VVVVV           VVVVVVV            llllll EEEEEEEEEEEEEE  SSSSSSSSSSSS PPPPPPPPPPPPPP                           
V:::V           V:::::V            l::::l E::::::::::::E S::::::::::::SP:::::::::::::P
V:::V           V:::::V            l::::l E::::::::::::ES::::SSSSS::::SP:::::PPPPP::::P
V:::V           V:::::V            l::::l EE::::EEEEE::ES::::S    SSSSSPP::::P    P::::P
V:::V           V::::V eeeeeeeeee   l:::l   E:::E   EEEES::::S           P:::P    P::::Prrr   rrrrr     oooooo
V::::V         V::::Vee::::::::::e  l:::l   E:::E       S::::S           P:::P    P::::Pr::rrr:::::r   o::::::o
 V::::V       V::::Ve::::eeeee::::eel:::l   E::::EEEEEE  ::::SSS         P:::PPPPP::::P r:::::::::::r o::::::::o
  V::::V     V::::Ve::::e     e::::el:::l   E:::::::::E  SS:::::SSSS     P:::::::::::P  rr::::rrr::::ro:::oo:::o
   V::::V   V::::V e:::::eeeee:::::el:::l   E:::::::::E    SSS::::::S    P:::PPPPPPPP    r:::r   r:::ro::o  o::o
    V::::V V::::V  e::::::::::::::e l:::l   E::::EEEEEE       SSSSS::S   P:::P           r:::r   rrrrro::o  o::o
     V::::V::::V   e::::eeeeeeeeee  l:::l   E:::E                 S:::S  P:::P           r:::r        o::o  o::o
      V:::::::V    e:::::e          l:::l   E:::E   EEEE          S:::S  P:::P           r:::r        o::o  o::o
       V:::::V     e::::::e        l:::::lEE::::EEEE:::ESSSSSS    S:::SPP:::::PP         r:::r        o:::oo:::o
        V:::V       e::::::eeeeeee l:::::lE::::::::::::ES:::::SSSSS:::SP:::::::P         r:::r        o::::::::o
         V:V         ee::::::::::e l:::::lE::::::::::::ES::::::::::::S P:::::::P         r:::r         o::::::o
          V            eeeeeeeeeee lllllllEEEEEEEEEEEEEE SSSSSSSSSSSS  PPPPPPPPP         rrrrr          oooooo
----------------------------------------------------------------------------------------------------------------
~~~
Quantum chemistry program in python

# HOW TO USE IT LOCALLY

The proposed Python workflow consists of the following stages:

1. Dependencies installation.
2. Execute.

### Environment set up

For developer using this package, it is recommended to work within a Virtual Environment.
The creation and activation of a given environment shall be done after any of the stages listed above.

The following command can be used for creating a new venv.

```bash
python3 -m venv <venv_name>
```

This is for activating the venv.

```bash
#Linux
source <venv_name>/bin/activate

or

#Windows
.\<venv_name>\Script\activate
```

And this one is for deactivating the venv.

```bash
deactivate
```

### Install the dependencies

You can install the dependencies with the next command.

```bash
python -m pip install -r requirements.txt
```

or you can install the proyect.

```
# 1. Build the project
python -m pip install build
python -m build

# 2. Install the source distribution
pip install dist/your_project-0.1.0.tar.gz
```

### Run process locally

First you need to complete the user and password for artifactory in the config file:
```
Velespro {

}
```

```bash
python -m src.velespro <input.conf>
```

#### Obtain the visualization of the input
There are a jupyter notebook in utils that you can use to visualize the molecules in the input.

```bash
jupyter lab utils/molecule_drawer.ipynb
```

## HOW TO USE OBTAIN THE COVERAGE

1. Run all the test:
```bash
coverage run -m pytest
