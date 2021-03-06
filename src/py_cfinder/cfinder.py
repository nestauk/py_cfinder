import itertools
import pandas
import os
import shutil

from collections import defaultdict
from subprocess import run


class CFinder():

    def __init__(self, licence_path=None):
        """CFinder
        A wrapper class for the CFinder utility.

        Args:
            cfinder_path (str): The file path for the CFinder utility.
            licence_path (str): The file path for the CFincder licence file. If
                None, then will try to use licence.txt, located in the same
                parent directory as the CFinder utility. Defaults to None.
        """

        self.cfinder_path = self._locate_cfinder()
        self.licence_path = self._locate_licence(licence_path)
        self.dirs = {
                'cliques': '{}cliques',
                'graph': '{}graph',
                'comms': '{}communities',
                'comms_cliques': '{}communities_cliques',
                'comms_graph': 'graph_of_{}communities_graph',
                'comms_links': '{}communities_links',
                'degree_dist': '{}degree_distribuion',
                'size_dist': '{}size_distribution',
                'membership_dist': '{}membership_distribution',
                'overlap_dist': '{}overlap_distribution',
                }

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

    def _locate_cfinder(self):
        """_locate_cfinder
        Checks if CFinder's location has been set as an environment variable
        and returns its path.
        """
        try:
            cfinder_path = os.environ['CFINDER']
            return cfinder_path
        except KeyError:
            raise KeyError(
                    ("There is no environment variable named CFINDER on this "
                     "system. To use this tool, set CFINDER as the directory "
                     "containing the CFinder tool. If you do not have CFinder, "
                     "you can download it from http://www.cfinder.org/")
                    )

    def find(self, i, o=None, W=None, w=None, d=None, t=None, D=False,
        I=False, k=None, delete_output=False):
        """find
        Run the CFinder tool on an edge list.
        Args
            i (str): Input file dir.
            o (str) Output dir.
            w (float): Lower link weight threshold.
            W (float): Upper link weight threshold.
            d (int): Number of digits when creating the name of the default 
                output directory of the link weight thresholded input.
            t (int): Maximal time allowed for clique search per node.
            D (bool): Search with directed mode.
            U (bool): Searche with un-directed mode. Declare explicitly the 
                input and modules to be un-direceted.
            I (bool): Search with the intensity method and
                specify the lower link weight intensity threshold for the k 
                cliques.
            k (int): The k-clique size.
            delete_output (bool): Delete output files when finished. Defaults
                to False.
        """
        

        command = [self.cfinder_path, '-l', self.licence_path, '-i', i]
        if o is None:
            self.output_dir = os.path.join(
                    os.path.abspath(
                        os.path.join(self.cfinder_path, os.pardir)
                    ),
                    'output'
                    )
            command.extend(['-o',  self.output_dir])
        else:
            self.output_dir = o
            command.extend(['-o', o])

#         if os.path.isdir(self.output_dir):
#             shutil.rmtree(self.output_dir)

        if W is not None:
            command.extend(['-W',str(W)])
        if w is not None:
            command.extend(['-w', str(w)])
        if d is not None:
            command.extend(['-d', d])
        if t is not None:
            command.extend(['-t', str(t)])
        if k is not None:
            command.extend(['-k', str(k)])

        if D == False:
            command.append('-U')
            clique_dir = self.dirs['cliques'].format('')
        elif D == True:
            command.append('-D')
            clique_dir = self.dirs['cliques'].format('directed_')

        if I == True:
            if w is None:
                raise ValueError("No lower link weight threshold is given")
            else:
                command.append('-I')

        run(command)

        cliques = self._load_community_file(
                os.path.join(self.output_dir, clique_dir)
                )
        
        if delete_output:
            shutil.rmtree(self.output_dir)

        return cliques

    def load(self, output_dir=None, directed=False):
        """load
        Loads results from a CFinder output directory.

        Args:
            output_dir (str): Output directory for the results. If None, will
                try to use class output_dir attribute. Defaults to None.

        Returns:
            results (dict): Dictionary containing dataframes for all outputs.
                The structure of the reults is:
                {'cliques': cliques_df,
                 'graph': graph_df,
                 'k=...': {
                    'communities': communities_df,
                    'communities_cliques': communities_cliques_df,
                    'communities_links': communities_links_df,
                    'communities_graph': graph_of_communities_df,
                    'degree_distribution': degree_distribution_df,
                    'membership_distribution': membership_distribution_df,
                    'overlap_distribution': overlap_distribution_df,
                    'size_distribution': size_distribution_df,
                    },
                }
        """
        if output_dir is None:
            output_dir = self.output_dir

        if directed:
            dirs = {k: v.format('directed_') for k, v in self.dirs.items()}
        else:
            dirs = {k: v.format('') for k, v in self.dirs.items()}

        results = {}

        results['cliques'] = self._load_community_file(
                os.path.join(output_dir, dirs['cliques'])
                )
        results['graph'] =self._load_graph_file(
                os.path.join(output_dir, dirs['graph'])
                )

        k_dirs = self._get_k_directories(output_dir)

        for k_dir in k_dirs:
            k = int(k_dir.split('=')[-1])
            results[k] = {}
            k_output_dir = os.path.join(output_dir, k_dir)
            results[k]['communities'] = self._load_community_file(
                    os.path.join(k_output_dir, dirs['comms'])
                    )
            results[k]['communities_cliques'] = self._load_community_file(
                    os.path.join(k_output_dir, dirs['comms_cliques'])
                    )
            results[k]['communities_links'] = self._load_communities_cliques_file(
                    os.path.join(k_output_dir, dirs['comms_links'])
                    )
            results[k]['communities_graph'] = self._load_graph_file(
                    os.path.join(k_output_dir, dirs['comms_graph'])
                    )
            results[k]['degree_distribution'] = self._load_distribution_file(
                    os.path.join(k_output_dir, dirs['degree_dist'])
                    )
            results[k]['membership_distribution'] = self._load_distribution_file(
                    os.path.join(k_output_dir, dirs['membership_dist'])
                    )
            results[k]['overlap_distribution'] = self._load_distribution_file(
                    os.path.join(k_output_dir, dirs['overlap_dist'])
                    )
            results[k]['size_distribution'] = self._load_distribution_file(
                    os.path.join(k_output_dir, dirs['size_dist'])
                    )

        return results

    
    def _load_community_file(self, file_path):
        """_load_community_file
        Loads a CFinder communities or cliques output file.

        Community file format example:

        0: 1 3 4
        1: 1 2 4 5
        2: 2 3 4 6
        3: 2 3 5
        4: 4 6 7 8 9 10

        Args:
            file_path (str): Path to a CFinder output file.

        Returns:
            data_dict (dict): A dict with keys for the community
                of clique ID and for the elements that it contains.

        """
        file_name = file_path.split(os.sep)[-1]
        columns = file_name.split('_')
        columns = [c for c in columns if c != 'directed']

        if len(columns) == 1:
            if columns[0] == 'communities':
                comm_id, comm_nodes = ['community', 'vertices']
            elif columns[0] == 'cliques':
                comm_id, comm_nodes = ['clique', 'vertices']
        elif file_name == 'communities_cliques':
            comm_id, comm_nodes = ['community', 'cliques']
        
        data_dict = {comm_id: [], comm_nodes: []}
        data = self._read_data(file_path)
        for row in data:
            i, d = row.split(': ')
            d = tuple(d.split(' ')[:-1])
            data_dict[comm_id].append(int(i))
            data_dict[comm_nodes].append(d)
 
        data_dict[comm_nodes] = [tuple(self._digits_to_nums(i)) for i in data_dict[comm_nodes]]

        return data_dict
            
    def _load_graph_file(self, file_path):
        """_load_graph_file
        Loads a CFinder file that represents edges of a graph.

        Graph file format example (with weight):
        
        1 2 1
        1 3 2
        1 4 1
        2 3 3
        3 4 1

        Args:
            file_path (str): Path to a CFinder output file.

        Returns:
            df (pandas.DataFrame): Dataframe with columns for edge source, 
                target, and weight. Weights default to 1 if no weights are
                present in file.

        """
        data_dict = {'source': [], 'target': [], 'weight': []}
        data = self._read_data(file_path)
        if len(data) > 0:
            if len(data[0].split(' ')) > 2:
                weight = True
            else:
                weight = False

            for row in data:
                if weight:
                    s, t, w = row.split(' ')
                    data_dict['weight'].append(w)
                else:
                    s, t = row.split(' ')
                    data_dict['weight'].append('1')
                data_dict['source'].append(s)
                data_dict['target'].append(t)

            data_dict['source'] = self._digits_to_nums(data_dict['source'])
            data_dict['target'] = self._digits_to_nums(data_dict['target'])
            data_dict['weight'] = self._digits_to_nums(data_dict['weight'])
            return data_dict

    def _load_distribution_file(self, file_path):
        """_load_distribution_file
        Loads a CFinder distribution file in to a dataframe.

        Distribution file format example:

        0 12415
        1 3422
        3 1231
        4 357
        5 54

        Args:
            file_path (str): Path to a CFinder distribution output file.
                File name could be one of 'degree_distribution', 
                'size_distribution', 'membership_distribution',
                or 'overlap_distribution'.

        Returns:
            df (pandas.DataFrame): Dataframe with columns for the metric name
                and its count.
        """
        file_name = file_path.split(os.sep)[-1]
        file_name = file_name.split('_')
        if file_name[0] == 'directed':
            metric = file_name[1]
        else:
            metric = file_name[0]
        data_dict = {metric: [], 'count': []}

        data = self._read_data(file_path)
        # distribution files have two blank lines at end
        for row in data[:-1]:
            m, c = row.split(' ')
            data_dict[metric].append(int(m))
            data_dict['count'].append(int(c))
        return data_dict

    def _load_communities_cliques_file(self, file_path):
        """_load_communities_cliques_file

        Args:
            file_path (str): Path to a CFinder output file.

        Returns:
        """
        data = self._read_data(file_path)
        data_dict = {'community': [], 'edges': []}
        
        community_edges = defaultdict(list)
        for row in data:
            if ':' in row:
                community = int(row.split(':')[0])
            else:
                e = tuple(self._digits_to_nums(row.split(' '))) 
                community_edges[community].append(e)

        for k, v in community_edges.items():
            data_dict['community'].append(k)
            data_dict['edges'].append(v)
        return data_dict
    
    def _digits_to_nums(self, l):
        """digits_to_ints
        Replaces string numbers with int or float representations
        """
        n = []
        for i in l:
            if i.isdigit():
                n.append(int(i))
            elif i.isdecimal():
                n.append(float(i))
            else:
                n.append(i)
        return n

    def _read_data(self, file_path):
        """_read_data
        Reads in an output file from CFinder and removes header lines.

        Args:
            file_path (str): Path to a CFinder output file.

        Returns:
            data (list): List of data lines from the file.

        """
        with open(file_path, 'r') as f:
            data = f.read().splitlines()[6:]

        if len(data[0]) == 0:
            data = data[1:]

        return data
    
    def _get_k_directories(self, output_dir):
        """_get_k_directories
        Get 'k' subdirectory names of CFinder output directory.

        Args:
            output_dir (str): CFinder output directory.

        Returns:
            (list): Subdirectory names that contain 'k='.
        """
        return [name for name in os.listdir(output_dir)
            if (os.path.isdir(os.path.join(output_dir, name))) & ('k=' in name)]

