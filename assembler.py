import sys

def assemble(input_file: str, output_file: str):
    """
    Assembles a TM assembly file into machine code.

    - Tape alphabet: B, 0, 1, X
    - Input alphabet: 0, 1, X
    - Movement: L, R, S

    :param assembly_filename: The name of the assembly file to assemble.
    :param mc_filename: The name of the output machine code file.

    :return: None
    :raises ValueError: If the assembly file is malformed or contains errors.
    """ 

    assembly_file = open(input_file, 'r')
    lines = (line.strip() for line in assembly_file)

    # Remove comments and blanklines
    for comment_symbol in ['/', ';', '#']:
        lines = [line.split(comment_symbol)[0] for line in lines]
    lines = [line for line in lines if line.strip()]

    lines = [line.split() for line in lines]

    # Symbol encoding: '_' = blank, 0 = zero, 1 = one
    symbols = {'_': '00', '0': '01', '1': '10', 'X': '11'}

    # Movement encoding: '<' = left, '>' = right, '=' = stay
    movements = {'<': '00', '>': '01', '=': '10'}

    transitions = {}
    states = {}

    # Assign or retrieve a 8-bit binary code for a state name
    def encode_state(name):
        if name == 'HALT':
            return '00000000'
        if name == 'REJECT':
            return '00000000'
        if name not in states:
            states[name] = format(len(states), '08b')  # assign new 8-bit code
        return states[name]

    with open(input_file, 'r') as infile:
        for line in infile:
            line = line.strip()
            if not line or line.startswith('//'):
                continue  # ignore empty lines and comments
            if not line.startswith('('):
                continue  # ignore malformed lines

            # Format expected: (q0, 0) - (1, R, q1)
            try:
                left, right = line.split('-')
                left = left.strip()[1:-1]   # remove outer parentheses
                right = right.strip()[1:-1]

                current_state, read_symbol = map(str.strip, left.split(','))
                line_num = int(f"{encode_state(current_state)}{symbols[read_symbol]}", 2)
                next_state, write_symbol, move = map(str.strip, right.split(','))

                # Determine halt bits (2 bits) '11' for HALT, '10' for continue. '00' for blocked computation.
                if next_state == 'REJECT':
                    halt = '00'
                elif next_state == 'HALT':
                    halt = '11'
                else:
                    # If the next state is not HALT or REJECT, we assume it's a valid state
                    # and we set the halt bits to '10' (continue)
                    halt = '10'

                # Encode each field
                move_bits = movements[move]
                write_bits = symbols[write_symbol]
                next_state_bits = encode_state(next_state)

                # Final 16-bit binary: next_state(8) + halt(2) + move(2) + write(2) + padding(2)
                binary_code = (
                    next_state_bits +
                    halt +
                    move_bits +
                    write_bits +
                    '00'  # reserved / padding
                )
                transitions[line_num] = binary_code
            except Exception as e:
                raise ValueError(f'Error processing line: {line}') from e

    # Write binary transitions to output file
    with open(output_file, 'w') as outfile:
        current_line = 0
        while len(transitions.keys()) > 0:
            if current_line in transitions:
                code = transitions[current_line]
                del transitions[current_line]
            else:
                code = '0000000000000000'
            
            outfile.write(code + '\n')
            current_line += 1

if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit("Not enough arguments.")

    assemble(sys.argv[1], sys.argv[2] if len(sys.argv) >= 3 else 'output.mc')