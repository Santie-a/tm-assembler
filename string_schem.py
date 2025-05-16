import mcschematic

def create_string_schematic(bin_string: str, schem_filename):
    schem = mcschematic.MCSchematic()

    if ' ' in bin_string or any(char not in '01X' for char in bin_string):
        raise ValueError("Invalid characters in binary string. Only '0', '1', and 'X' are allowed.")

    north_start_pos = [0, -5, 0]
    south_start_pos = [0, -5, -2]
    north_pos_list = []
    south_pos_list = []

    # Generates positions for the north and south sides
    for i in range(4):
        pos = north_start_pos.copy()
        pos[2] -= 16 * i
        for j in range(16):
            north_pos_list.append(pos.copy())
            pos[0] -= 2
            pos[1] += 1 if j % 2 == 0 else -1

        pos = north_start_pos.copy()
        pos[2] -= 16 * i
        pos[0] -= 36
        pos[1] += 1
        for j in range(16):
            north_pos_list.append(pos.copy())
            pos[0] -= 2
            pos[1] -= 1 if j % 2 == 0 else -1

    for i in range(4):
        pos = south_start_pos.copy()
        pos[2] -= 16 * i
        for j in range(16):
            south_pos_list.append(pos.copy())
            pos[0] -= 2
            pos[1] += 1 if j % 2 == 0 else -1

        pos = south_start_pos.copy()
        pos[2] -= 16 * i
        pos[0] -= 36
        pos[1] += 1
        for j in range(16):
            south_pos_list.append(pos.copy())
            pos[0] -= 2
            pos[1] -= 1 if j % 2 == 0 else -1

    # 
    facing = 'south'
    current_reg = 0

    north_reg = 0
    south_reg = 0

    # Fill the schematic with the binary string depending on the facing direction
    for i in range(len(bin_string)):
        if current_reg % 32 == 0:
            facing = 'north' if facing == 'south' else 'south'

        char = bin_string[i]
        if facing == 'north':
            top_pos = north_pos_list[north_reg].copy()
            bottom_pos = north_pos_list[north_reg].copy()
            north_reg += 1
        else:
            top_pos = south_pos_list[south_reg].copy()
            bottom_pos = south_pos_list[south_reg].copy()
            south_reg += 1
        
        bottom_pos[1] -= 2

        if char == '0':
            schem.setBlock(tuple(top_pos), f'minecraft:repeater[facing={facing},locked=true,powered=false]')
            schem.setBlock(tuple(bottom_pos), f'minecraft:repeater[facing={facing},locked=true,powered=true]')
        elif char == '1':
            schem.setBlock(tuple(top_pos), f'minecraft:repeater[facing={facing},locked=true,powered=true]')
            schem.setBlock(tuple(bottom_pos), f'minecraft:repeater[facing={facing},locked=true,powered=false]')
        elif char == 'X':
            schem.setBlock(tuple(top_pos), f'minecraft:repeater[facing={facing},locked=true,powered=true]')
            schem.setBlock(tuple(bottom_pos), f'minecraft:repeater[facing={facing},locked=true,powered=true]')

        current_reg += 1


    # Fill the rest with 00
    for i in range(current_reg, 256):
        if current_reg % 32 == 0:
            facing = 'north' if facing == 'south' else 'south'

        if facing == 'north':
            top_pos = north_pos_list[north_reg].copy()
            bottom_pos = north_pos_list[north_reg].copy()
            north_reg += 1
        else:
            top_pos = south_pos_list[south_reg].copy()
            bottom_pos = south_pos_list[south_reg].copy()
            south_reg += 1
        
        bottom_pos[1] -= 2

        schem.setBlock(tuple(top_pos), f'minecraft:repeater[facing={facing},locked=true,powered=false]')
        schem.setBlock(tuple(bottom_pos), f'minecraft:repeater[facing={facing},locked=true,powered=false]')

        current_reg += 1
        

    if schem_filename.endswith('.schem'):
        schem_filename = schem_filename[:-6]

    schem.save('.', schem_filename, version=mcschematic.Version.JE_1_18_2)


if __name__ == '__main__':
    binary_string = '1011'
    schem_filename = f'{binary_string}.schem'
    create_string_schematic(binary_string, f"strings/{schem_filename}")