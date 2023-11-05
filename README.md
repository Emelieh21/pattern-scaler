# Pattern Scaler

### How to use

Install poetry:

```
pip3 install poetry
```

Install the dependencies for the repository:

```
poetry install
```

Run the main python script, open the terminal in the `src` folder and run:

```
poetry run python main.py
```

### Repo creation (to remove later)

Initialized poetry repo with:

```
poetry init
```

The dependencies can be added with:

```
poetry add opencv-python
poetry add Pillow
```

### Dependency issues I struggled with
I struggled quite long with a cv2 import error that suddenly started happening. Also switching to poetry and using poetry's environment did not solve the issue. 

First of all, adding opencv got stuck everytime I tried doing it with the `poetry add` command above. I managed to install it with the following:

```
poetry shell
pip install --upgrade pip setuptools wheel
pip install --no-use-pep517 opencv-python
pip add opencv-python
```

However, I would still get the same ImportError, indicating an issue with `libffi` (which I already tried to uninstall and reinstall a few times):

```
Library not loaded: /usr/local/opt/libffi/lib/libffi.7.dylib
```

In the end what fixed it for me was a suggestion from this [post](https://github.com/pyenv/pyenv/issues/1721):

```
cd /usr/local/opt/libffi/lib
ln -s libffi.8.dylib libffi.7.dylib
```