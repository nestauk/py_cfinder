import itertools
import os
import shutil

from collections import defaultdict
from subprocess import run
from rhodonite.utilities import save_edgelist, check_and_create_dir, flatten


class CFinder():
    def __init__(self, cfinder_path, licence_path=None):
        """CFinder
        A wrapper class for the CFinder utility.

        Args:
            cfinder_path (str): The file path for the CFinder utility.
            licence_path (str): The file path for the CFincder licence file. If
                None, then will try to use licence.txt, located in the same
                parent directory as the CFinder utility. Defaults to None.
        """
        self.cfinder_path = cfinder_path
        self.licence_path = self._locate_licence(licence_path)


    def _locate_licence(self, licence_path):
        """_locate_licence
        Returns licence file path if none provided.

        Args:
            licence_path (str): Licence path provided.

        Returns:
            licence_path (str): Licence path.
        """
        if licence_path is None:
            return os.path.join(
                    os.path.dirname(self.cfinder_path),
                    'licence.txt'
                    )
        else:
            return licence_path

    def find(self, i, o=None, W=None, w=None, d=None, t=None, D=False,
        U=True, I=False, k=None, delete_output=False):
        """find
        Run the CFinder tool on an edge list.

        input_dir (str): Input file dir. CFinder -i.
        output_dir (str) Output dir. CFinder -o.
        hi_weight_thresh (float): Upper link weight threshold. CFinder -W.
        lo_weight_thresh (float): Lower link weight threshold. CFinder -w.
        digits (int): Number of digits when creating the name of the
            default output directory of the link weight thresholded
            input. CFinder -d.
        time_max (int): Maximal time allowed for clique search per node.
            CFinder -t.
        directed (bool): Search with directed mode. CFinder -D.
        undirected (bool): Searche with un-directed mode. Declare
            explicitly the input and modules to be un-direceted.
        intensity_method (bool): Search with the intensity method and
            specify the lower link weight intensity threshold for the k 
            cliques. CFinder -I.
        k (int): The k-clique size. CFinder -k.
        delete_output (bool): Delete output files when finished. Defaults
            to False.
        """
        
        opts = [self.cfinder_path, '-l', self.licence_path, '-i', i]

        if o is None:
            out_dir = os.path.abspath(
                    os.path.join(self.cfinder_path, os.pardir)
                    )
            opts.extend(['-o',  os.path.join(out_dir, 'output')])
        else:
            opts.extend(['-o', o])

        if W is not None:
            opts.extend(['-W', W])
        if w is not None:
            opts.extend(['-w', w])
        if d is not None:
            opts.extend(['-d', d])
        if t is not None:
            opts.extend(['-t', t])
        if k is noe None:
            opts.extend(['-k', k])

        if (U == True) & (D == True):
            raise ValueError(("CFinder cannot apply directed and undirected "
                              "search algorithms at the same time.")
                              )
        else:
            if U == True:
                opts.append('-U')
            elif D == True:
                opts.append('-D')

        if I == True:
            if w is None:
                raise ValueError("No lower link weight threshold is given")
            else:
                opts.append('-I')

        run_cfinder(cfinder_path, opts)
        cliques = load_cliques_cfinder(os.path.join(output_dir, 'cliques'))
        if delete_outputs:g
            shutil.rmtree(output_dir)
        return cliques

    def run_cfinder(cfinder_path, opts):
        """run_cfinder
        Calls the CFinder tool with user defined options.

        Args:
            cfinder_path (str): The path to the CFinder app/executable on the
                system.
            opts (dict): Options to use when running CFinder.
        """
        opts_list = [cfinder_path]
        for flag, value in opts.items():
            opts_list.append(flag)
            opts_list.append(value)
        call(opts_list)

def load_cliques_cfinder(file_path):
    """load_cliques
    Loads cliques from a CFinder output file into a list of tuples.

    Args:
        file_path (str): The path to the CFinder output file. This is normally
            in a directory of outputs and named "cliques".

    Returns:
        cliques (:obj:`list` of :obj:`tuple`): A list of all of the cliques
            found by CFinder. Each clique is represented as a tuple of
            vertices.
    """
    with open(file_path, 'r') as f:
        clique_data = f.read().splitlines()
    cliques = []
    for cd in clique_data:
        if len(cd) > 0:
            if cd[0].isdigit():
                clique = cd.split(' ')[1:-1]
                clique = tuple(sorted([int(i) for i in clique]))
                cliques.append(clique)
    return cliques


    def load(self):
        pass

def load_cliques_cfinder(file_path):
    """load_cliques
    Loads cliques from a CFinder output file into a list of tuples.

    Args:
        file_path (str): The path to the CFinder output file. This is normally
            in a directory of outputs and named "cliques".

    Returns:
        cliques (:obj:`list` of :obj:`tuple`): A list of all of the cliques
            found by CFinder. Each clique is represented as a tuple of
            vertices.
    """
    with open(file_path, 'r') as f:
        clique_data = f.read().splitlines()
    cliques = []
    for cd in clique_data:
        if len(cd) > 0:
            if cd[0].isdigit():
                clique = cd.split(' ')[1:-1]
                clique = tuple(sorted([int(i) for i in clique]))
                cliques.append(clique)
    return cliques
            

def generate_clique_combinations(cliques, limit):
    for c in cliques:
        for l in range(1, limit):
            for subset in itertools.combinations(c, l):
                yield tuple(subset)

def reverse_index_cliques(clique_set):
    """reverse_index_cliques
    Takes a set of network cliques and return all possible combinations of
    cliques where all cliques in a combination contain at least one common
    value.

    Args:
        clique_set (:obj:`iter` of :obj:`iter`): A set of cliques where 
            each element in the nested iterable contain vertices in the
            network.

    Returns:
        clique_union_indices (:obj:`list` of :obj:`tuple`): A list of the
            combinations of clique indices.
        clique_union_vertices (:obj:`list` of :obj:`tuple`): A list of the
            sets of vertices that comprise the clique combinations.
    """
    mapping = defaultdict(list)
    for i, cs in enumerate(clique_set):
        for vertex in cs:
            mapping[vertex].append(i)
    mapping = {k: tuple(v) for k, v in mapping.items()}
    return mapping

# def clique_unions(clique_index_sets, clique_set, limit):
#     """clique_unions
#     Takes sets of cliques, represented by their indices, and returns the
#     possible combinations of them, as well as the vertices that they are
#     comprised from.
#     """
#     clique_combination_indices = []
#     for combination in generate_clique_combinations(
#            clique_index_sets, limit):
#         clique_combination_indices.append(combination)
#     clique_combination_indices = list(set(clique_combination_indices))
# 
#     clique_combination_vertices = []
#     for cui in clique_combination_indices:
#         combination_vertices = list(set(flatten([clique_set[i] for i in cui])))
#         clique_combination_vertices.append(combination_vertices)
# 
#     return clique_combination_indices, clique_combination_vertices

def clique_unions(clique_indices, limit):
    combos = []
    for l in range(1, limit):
        for combo in itertools.combinations(clique_indices, l):
            combos.append(tuple(combo))
    return combos

def is_subset(needle, haystack):
   """ Check if needle is ordered subset of haystack in O(n)  """

   if len(haystack) < len(needle): return False

   index = 0
   for element in needle:
      try:
         index = haystack.index(element, index) + 1
      except ValueError:
         return False
   else:
      return True

def filter_subsets(lists):
   """ Given list of lists, return new list of lists without subsets  """

   for needle in lists:
      if not any(is_subset(needle, haystack) for haystack in lists
         if needle is not haystack):
         yield needle
