import io


def is_swf_valid(swf_io: io.IOBase) -> bool:
    swf_io.seek(0)
    swf_header = swf_io.read(3)
    return swf_header in (b"FWS", b"CWS")


def is_projector_valid(projector_io: io.IOBase) -> bool:
    projector_io.seek(0)
    projector_header = projector_io.read(2)
    return projector_header == b"MZ"
