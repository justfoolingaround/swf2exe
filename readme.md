<h1 align="center">swf2exe.py</h1>

Convert any Shockwave Flash (SWF) file to a portable Windows executable.

### Usage

```
Usage: __main__.py [OPTIONS] SWF_FILE

Options:
  -o, --output PATH     User specified output file
  -p, --projector PATH  User specified projector file
  --clean               Supress all file IO except for the output file
  --help                Show this message and exit
```

> **Note**: If you're converting from a massive list of SWF files intended for exporting within an archive, you'll save an extreme amount of space just by adding the projector and the SWF separately. Users can run the SWF by dragging it to the projector.

### Warning

User provided `swf` and `exe` files are not checked for malicious content. The project simply serves as a bridge between the two file types.
