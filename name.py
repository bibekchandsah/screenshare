import os
name = "𝓓𝓮𝓿𝓮𝓵𝓸𝓹𝓮𝓭 𝓫𝔂 𝓑𝓲𝓫𝓮𝓴..."
width = os.get_terminal_size().columns  # get terminal width
print(name.rjust(width))  # right-align text


