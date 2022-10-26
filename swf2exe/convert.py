import io

FLAG = 0xFA123456


def combine_player_and_swf(player_io: io.IOBase, swf_io: io.IOBase) -> io.BytesIO:
    player_io.seek(0)
    swf_io.seek(0)

    output = io.BytesIO()
    with player_io:
        output.write(player_io.read())
        with swf_io:
            swf_length = output.write(swf_io.read())

    output.write(FLAG.to_bytes(4, "little"))
    output.write(swf_length.to_bytes(4, "little"))

    output.seek(0)

    return output
