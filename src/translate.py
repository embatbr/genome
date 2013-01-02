#!/usr/bin/python3.3

"""
This module contains code to read and write .genome and .code files, so as
translates it's content to the internal objects.
"""


"""
Default Python library.
"""
import re


"""
Project modules 
"""
import defines


"""
Rules to scan a .genome or .code file.
"""
token_spec = [
    ('COMMENT', r'#.*'),
    ('SKIP', r'[ \t]+'),
    ('NEWLINE', r'\n'),
    ('STRING', r'".*"'),
    ('COMMAND', r'\.[a-z]+'),
    ('DONT_CARE', r'@'),
    ('ID', r'[a-zA-Z][a-zA-Z0-9_]*')
]
token_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_spec)
get_token = re.compile(token_regex).match

"""
Dictionary containing scanned Genome objects.
"""
genome_dict = {}

def scan(string):
    """
    Turns a string into a list of tokens.
    """
    match_obj = get_token(string)
    line = 1
    pos = 0
    ret = []

    while match_obj is not None:
        typ = match_obj.lastgroup
        if typ == 'NEWLINE':
            line = line + 1
        elif typ not in ('COMMENT', 'SKIP', 'NEWLINE'):
            val = match_obj.group(typ)
            if typ == 'STRING':
                val = val[1:-1]

            ret.append((typ, val))

        pos = match_obj.end()
        match_obj = get_token(string, pos)

    if pos != len(string):
        raise RuntimeError('Unexpected token \'%s\' in line %s' % (string[pos],
                           line))

    return ret

def parse_genome(tokens):
    """
    Parse a list of tokens into a Genome object.
    """
    tok = tokens.pop(0)
    if tok != ('COMMAND', '.genome'):
        raise RuntimeError('Expected command .genome')

    tok = tokens.pop(0)
    if tok[0] != 'ID':
        raise RuntimeError('Invalid genome name')
    
    ret = defines.Genome(tok[1])
    while tokens != []:
        tok = tokens.pop(0)

        if tok == ('COMMAND', '.gene'):
            tok = tokens.pop(0)
            if tok[0] != 'ID':
                raise RuntimeError('Invalid gene name')

            gene = defines.Gene(tok[1])
            ret.add_gene(gene)

        elif tok == ('COMMAND', '.allele'):
            tok = tokens.pop(0)
            if tok[0] != 'ID':
                raise RuntimeError('Invalid allele name')

            gene = ret.genes[-1]
            gene.add_allele(tok[1])

        elif tok == ('COMMAND', '.fenotipe'):
            allele1 = tokens.pop(0)
            allele2 = tokens.pop(0)
            fenotipe = tokens.pop(0)

            if ((allele1[0] not in ('ID', 'DONT_CARE')) or
            (allele2[0] not in ('ID', 'DONT_CARE'))):
                raise RuntimeError('Fenotipe allele must be an ID or DONT_CARE')
            if fenotipe[0] != 'STRING':
                raise RuntimeError('Fenotipe return must be a STRING')

            gene = ret.genes[-1]
            gene.add_fenotipe(allele1[1], allele2[1], fenotipe[1])

    genome_dict[ret.name] = ret
    return ret

def parse_code(tokens):
    """
    Parse a list of tokens into a GenomeConfig object.
    """
    tok = tokens.pop(0)
    if tok != ('COMMAND', '.code'):
        raise RuntimeError('Expected keyword .code')

    tok = tokens.pop(0)
    if tok[0] != 'ID':
        raise RuntimeError('Invalid code name')

    code_name = tok[1]

    tok = tokens.pop(0)
    if tok != ('COMMAND', '.genome'):
        raise RuntimeError('Expected keyword .genome')

    tok = tokens.pop(0)
    if tok[0] != 'ID':
        raise RuntimeError('Invalid genome name')

    genome_name = tok[1]
    if genome_name not in genome_dict:
        read_genome(genome_name)
    ret = defines.GenomeCode(code_name, genome_dict[genome_name])

    while tokens != []:
        tok = tokens.pop(0)

        if tok != ('COMMAND', '.gene'):
            raise RuntimeError('Expected keyword .gene')

        tok = tokens.pop(0)
        if tok[0] != 'ID':
            raise RuntimeError('Invalid gene name')

        gene = ret.genome.find_gene(tok[1])
        if gene == None:
            raise RuntimeError('Nonexistent gene \'%s\'' % tok[1])

        allele1 = tokens.pop(0)
        allele2 = tokens.pop(0)
        if allele1[0] != 'ID' or allele2[0] != 'ID':
            raise RuntimeError('Allele must be an ID')

        gene_code = defines.GeneCode(gene, allele1[1], allele2[1])
        ret.add_gene_code(gene_code)

    return ret

def read_genome(filename):
    """
    Reads a .genome file and returns a Genome object.
    """
    f = open('files/%s.genome' % filename)
    string = f.read()
    tokens = scan(string)
    ret = parse_genome(tokens)
    return ret

def write_genome(genome, sufix='', mode='w'):
    """
    Writes a .genome file given a Genome object.
    """
    f = open('files/%s.genome%s' % (genome.name, sufix), mode)
    print(genome, file=f)

def read_code(filename):
    """
    Reads a .code file and returns a GenomeConfig object.
    """
    f = open('files/%s.code' % filename)
    string = f.read()
    tokens = scan(string)
    ret = parse_code(tokens)
    return ret

def write_code(genome_code, sufix='', mode='w'):
    """
    Writes a .code file given a GenomeCode object.
    """
    f = open('files/%s.code%s' % (genome_code.name, sufix), mode)
    print(genome_code, file=f)