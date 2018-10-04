import pytest
import os
import shutil

from py_cfinder import CFinder

cfinder_path = os.environ['CFINDER']
cfinder_dir = os.path.abspath(
            os.path.join(cfinder_path, os.pardir)
                    )
demo_file_path = os.path.join(
        cfinder_dir,
        'demo_files',
        'triangle.txt'
        )
demo_output_path = os.path.join(
        cfinder_dir,
        'demo_files',
        'triangle.txt_files'
        )

@pytest.fixture
def cfinder_tool():
    cf = CFinder()
    return cf

@pytest.fixture
def triangle_cliques():
    cliques =  {'clique': {0: 0, 1: 1},
                'vertices': {
                 0: ('a', 'b', 'c'),
                 1: ('a', 'd', 'e')}
             }
    return cliques

@pytest.fixture()
def triangle_graph():
    graph = {'source': {0: 'a', 1: 'a', 2: 'a', 3: 'b', 4: 'e', 5: 'e'},
             'target': {0: 'b', 1: 'c', 2: 'd', 3: 'c', 4: 'a', 5: 'd'},
              'weight': {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1}}
    return graph

@pytest.fixture
def triangle_communities():
    communities = {'community': {0: 0, 1: 1},
             'vertices': {0: ('a', 'b', 'c'), 1: ('a', 'd', 'e')}}
    return communities

@pytest.fixture
def triangle_communities_cliques():
    cc = {'community': {0: 0, 1: 1}, 'cliques': {0: ('0',), 1: ('1',)}}
    return cc

@pytest.fixture
def triangle_communities_links():
    cl = {'community': {0: 0, 1: 1},
             'edges': {0: [('a', 'b'), ('a', 'c'), ('b', 'c')],
                   1: [('a', 'd'), ('a', 'e'), ('d', 'e')]}}
    return cl

@pytest.fixture
def triangle_communities_graph():
    cg = {'source': {0: '0'}, 'target': {0: '1'}, 'weight': {0: '1'}}
    return cg

@pytest.fixture
def triangle_degree_dist():
    dd = {'degree': {0: '1'}, 'count': {0: '2'}}
    return dd

@pytest.fixture
def triangle_membership_dist():
    md = {'membership': {0: '0', 1: '1', 2: '2'},
            'count': {0: '0', 1: '4', 2: '1'}}
    return md

@pytest.fixture
def triangle_overlap_dist():
    od = {'overlap': {0: '1'}, 'count': {0: '1'}}
    return od

@pytest.fixture
def triangle_size_dist():
    sd = {'size': {0: '3'}, 'count': {0: '2'}}
    return sd

def setup_module(cfinder_tool):
    cf = CFinder()
    _ = cf.find(demo_file_path,
            o=demo_output_path,
            delete_output=False)

def test_load_community_cliques(triangle_communities_cliques):
    cf = CFinder()
    results = cf._load_community_file(
            os.path.join(demo_output_path, 'k=3', 'communities_cliques')
            )
    assert results.to_dict() == triangle_communities_cliques

def test_load_cliques(triangle_cliques):
    cf = CFinder()
    results = cf._load_community_file(
            os.path.join(demo_output_path, 'cliques')
            )
    assert results.to_dict() == triangle_cliques

def test_load_communities_links(triangle_communities_links):
    cf = CFinder()
    results = cf._load_communities_cliques_file(
            os.path.join(demo_output_path, 'k=3', 'communities_links')
            )
    assert results.to_dict() == triangle_communities_links
    
def test_load_communities_graph(triangle_communities_graph):
    cf = CFinder()
    results = cf._load_graph_file(
            os.path.join(demo_output_path, 'k=3', 'graph_of_communities')
            )
    assert results.to_dict() == triangle_communities_graph

def test_load_degree_dist(triangle_degree_dist):
    cf = CFinder()
    results = cf._load_distribution_file(
            os.path.join(demo_output_path, 'k=3', 'degree_distribution')
            )
    assert results.to_dict() == triangle_degree_dist

def test_load_membership_dist(triangle_membership_dist):
    cf = CFinder()
    results = cf._load_distribution_file(
            os.path.join(demo_output_path, 'k=3', 'membership_distribution')
            )
    assert results.to_dict() == triangle_membership_dist

def test_load_overlap_dist(triangle_overlap_dist):
    cf = CFinder()
    results = cf._load_distribution_file(
            os.path.join(demo_output_path, 'k=3', 'overlap_distribution')
            )
    assert results.to_dict() == triangle_overlap_dist

def test_load_size_dist(triangle_size_dist):
    cf = CFinder()
    results = cf._load_distribution_file(
            os.path.join(demo_output_path, 'k=3', 'size_distribution')
            )
    assert results.to_dict() == triangle_size_dist

def teardown_module():
    """ teardown any state that was previously setup with a setup_module
    method.
    """
    shutil.rmtree(demo_output_path)
