import pandas
import numpy
import sklearn

def test_imports():
    """
    Simple smoke test to verify essential libraries are installed 
    and can be imported without errors.
    """
    assert pandas is not None
    assert numpy is not None
    assert sklearn is not None
    print("SUCCESS: All libraries imported and environment is valid!")

if __name__ == "__main__":
    test_imports()