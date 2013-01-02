#!/usr/bin/python3.3

"""
The defines module has functionalities to define and work with genes, genomes and
specific genetic codes.
"""


"""
Default library imports.
"""
import random


class Fenotipe:
    """
    A fenotipe for a gene (allele1, allele2, fenotipe_output).
    """
    def __init__(self, allele1, allele2, fenotipe):
        self.alleles = (allele1, allele2)
        self.fenotipe = fenotipe

    def __str__(self):
        ret = '.fenotipe %s %s "%s"' % (self.alleles[0], self.alleles[1],
                                        self.fenotipe)
        return ret

    def show(self, allele1, allele2):
        """
        Show the fenotipe output given 2 alleles. It returns None if one of the
        alleles aren't in the allele list.
        """
        if self.alleles == ('@', '@'):
            return self.fenotipe
        elif (self.alleles[0] == '@') or (self.alleles[1] == '@'):
            if (allele1 in self.alleles) or (allele2 in self.alleles):
                return self.fenotipe
        elif (allele1, allele2) == self.alleles or (allele2, allele1) == self.alleles:
            return self.fenotipe

        return None


class FenotipeGroup:
    """
    The group of Fenotipe objects. It is all the possible fenotipes for a gene.
    """
    def __init__(self):
        self.fenotipes = []

    def __str__(self):
        ret = ''
        for f in self.fenotipes:
            ret = '%s%s\n' % (ret, f)

        return ret

    def add_fenotipe(self, fenotipe):
        """
        Adds a Fenotipe object to the group.
        """
        self.fenotipes.append(fenotipe)

    def show(self, allele1, allele2):
        """
        Show the fenotipe output given 2 alleles. It returns None if one of the
        alleles aren't in the allele list of any fenotipe.
        """

        for f in self.fenotipes:
            ret = f.show(allele1, allele2)
            if ret is not None:
                return ret

        return None


class Gene(object):
    """
    The representation of a gene. A gene contains it's name, values (alleles)
    and the possible fenotipes.
    """
    def __init__(self, name):
        self.name = name
        self.alleles = []
        self.fenotipe_group = FenotipeGroup()

    def __str__(self):
        ret = '.gene %s' % self.name
        for allele in self.alleles:
            ret = '%s\n.allele %s' % (ret, allele)

        ret = '%s\n%s' % (ret, self.fenotipe_group)
        return ret[:-1]

    def add_allele(self, allele):
        """
        Adds a allele to the Gene object.
        """
        if allele in self.alleles:
            raise RuntimeError('The gene \'%s\' alredy has allele \'%s\'' %
                               (self.name, allele))

        self.alleles.append(allele)

    def add_fenotipe(self, allele1, allele2, fenotipe):
        """
        Adds a Fenotipe object to the Gene object. It is given the __init__
        parameters for the Fenotipe object.
        """
        if (allele1 != '@') and (allele1 not in self.alleles):
            raise RuntimeError('\'%s\' not in allele list' % allele1)
        if (allele2 != '@') and (allele2 not in self.alleles):
            raise RuntimeError('\'%s\' not in allele list' % allele2)

        self.fenotipe_group.add_fenotipe(Fenotipe(allele1, allele2, fenotipe))

    def fenotipe(self, allele1, allele2):
        """
        Shows the fenotipe for the given configuration.
        """
        return self.fenotipe_group.show(allele1, allele2)


class Genome(object):
    """
    A Genome is a set of genes that form the being genetic code.
    """
    def __init__(self, name):
        self.name = name
        self.genes = []

    def __str__(self):
        ret = '.genome %s\n' % self.name
        for gene in self.genes:
            ret = '%s\n%s\n' % (ret, gene)

        return ret

    def add_gene(self, gene):
        """
        Adds a Gene object to the Genome object.
        """
        for g in self.genes:
            if gene.name == g.name:
                raise RuntimeError('The \'%s\' genome alredy has the gene \'%s\'' %
                                  (self.name, gene.name))

        self.genes.append(gene)

    def find_gene(self, name):
        """
        Find the Gene object. If such object doesn't exists, returns None.
        """
        for gene in self.genes:
            if name == gene.name:
                return gene

        return None
        

class GeneCode:
    """
    A "instance" of a Gene. A GeneCode contains a reference to the Gene object
    it takes it's information and two alleles (it's configuration).
    """
    def __init__(self, gene, allele1, allele2):
        self.gene = gene
        self.allele1 = allele1
        self.allele2 = allele2

    def __str__(self):
        ret = '.gene %s %s %s' % (self.gene.name, self.allele1, self.allele2)
        return ret

    def fenotipe(self):
        """
        Show the fenotipe for this gene configuration.
        """
        return self.gene.fenotipe(self.allele1, self.allele2)


class GenomeCode:
    """
    A GenomeCode is a "instance" of a Genome. It contains a set of GeneCode
    objects.
    """
    def __init__(self, name, genome):
        self.name = name
        self.genome = genome
        self.gene_codes = []

    def __str__(self):
        ret = '.code %s\n.genome %s\n' % (self.name, self.genome.name)
        for g in self.gene_codes:
            ret = '%s\n%s' % (ret, g)

        return ret

    def add_gene_code(self, gene_code):
        """
        Adds a GeneCode object to the GenomeCode object.
        """
        for g in self.gene_codes:
            if gene_code.gene.name == g.gene.name:
                raise RuntimeError('The \'%s\' genome code alredy has the gene code \'%s\'' %
                                  (self.name, gene.name))

        self.gene_codes.append(gene_code)

    def fenotipe(self):
        """
        Show the fenotipe for this genetic code.
        """
        ret = ''
        for g in self.gene_codes:
            ret = '%s%s\n' % (ret, g.fenotipe())

        return ret


def random_gene_code(gene):
    allele1 = random.choice(10*gene.alleles)
    allele2 = random.choice(10*gene.alleles)

    ret = GeneCode(gene, allele1, allele2)
    return ret

def random_genome_code(name, genome):
    ret = GenomeCode(name, genome)
    for gene in genome.genes:
        gene_code = random_gene_code(gene)
        ret.add_gene_code(gene_code)

    return ret