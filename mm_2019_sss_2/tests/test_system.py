"""
Unit and regression test for the mm_2019_sss_2 package.
"""

# Import package, test suite, and other packages as needed
import sys

def test_mm_2019_sss_2_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "mm_2019_sss_2" in sys.modules

## Tests for system class
def test_initialize_random_simulation_np():
    num_particles = ['2', 2, 2.0]

    for ivalue in num_particles:
        try:
            ivalue += 1
        except TypeError:
            print('Box length is not a numeric type (float or int).')

def test_initialize_random_simulation_bl():
        box_length = ['2', 2, 2.0]

        for ivalue in box_length:
            try:
                ivalue += 1
            except TypeError:
                print('Box length is not a numeric type (float or int).')