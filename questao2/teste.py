output_file = 'output.md'

with open(output_file, 'w') as f_out:
    # Write numbers from 1 to 3000 to the output file
    for number in range(1, 3001):
        f_out.write(str(number) + '\n')
