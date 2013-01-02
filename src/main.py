#!/usr/bin/python3.3

"""
Module that starts execution.
"""


"""
Imports from project
"""
import translate
import defines
import sys


arguments = sys.argv[1:]


if __name__ == '__main__' and arguments[0] == '--genome':
    filename = '%s' % arguments[1]

    genome = translate.read_genome(filename)
    translate.write_genome(genome, sufix='.out')

    for i in range(0, 15):
        random_filename = '%s%02d' % (filename, i)
        random_genome_code = defines.random_genome_code('%s' % random_filename,
                                                        genome)

        translate.write_code(random_genome_code)
        genome_code = translate.read_code(random_filename)
        translate.write_code(genome_code, sufix='.out')
        with open('files/%s.code.out' % genome_code.name, 'a') as f:
            print('\n', genome_code.fenotipe(), file=f, sep='')


if __name__ == '__main__' and arguments[0] == '--scan':
    filename = '%s' % arguments[1]
    f = open('files/%s.genome' % filename)
    string = f.read()
    tokens = translate.scan(string)

    with open('files/%s.genome.scan' % filename, 'w') as f:
        for (typ, val) in tokens:
            val_str = ('"%s"' % val) if (typ == 'STRING') else val
            print(typ, val_str, file=f)

    genome = translate.parse_genome(tokens)
    with open('files/%s.genome.out' % filename, 'w') as f:
        print(genome, file=f)


if __name__ == '__main__' and arguments[0] == '--code':
    filename = '%s' % arguments[1]

    genome_code = translate.read_code(filename)
    translate.write_code(genome_code, sufix='.out')
    with open('files/%s.code.out' % genome_code.name, 'a') as f:
        print('\n', genome_code.fenotipe(), file=f, sep='')