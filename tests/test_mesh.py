import numpy

from stl.mesh import Mesh
from stl.base import RemoveDuplicates


def test_units_1d():
    data = numpy.zeros(1, dtype=Mesh.dtype)
    data['vectors'][0] = numpy.array([[0, 0, 0],
                                      [1, 0, 0],
                                      [2, 0, 0]])

    mesh = Mesh(data, remove_empty_areas=False)
    mesh.update_units()

    assert mesh.areas == 0
    assert (mesh.normals == [0, 0, 0]).all()
    assert (mesh.units == [0, 0, 0]).all()


def test_units_2d():
    data = numpy.zeros(2, dtype=Mesh.dtype)
    data['vectors'][0] = numpy.array([[0, 0, 0],
                                      [1, 0, 0],
                                      [0, 1, 0]])
    data['vectors'][1] = numpy.array([[1, 0, 0],
                                      [0, 1, 0],
                                      [1, 1, 0]])

    mesh = Mesh(data, remove_empty_areas=False)
    mesh.update_units()

    assert (mesh.areas == [.5, .5]).all()
    assert (mesh.normals == [[0, 0, 1.],
                             [0, 0, -1.]]).all()

    assert (mesh.units == [[0, 0, 1],
                           [0, 0, -1]]).all()


def test_units_3d():
    data = numpy.zeros(1, dtype=Mesh.dtype)
    data['vectors'][0] = numpy.array([[0, 0, 0],
                                      [1, 0, 0],
                                      [0, 1, 1.]])

    mesh = Mesh(data, remove_empty_areas=False)
    mesh.update_units()

    assert (mesh.areas - 2 ** .5) < 0.0001
    assert (mesh.normals == [0, -1, 1]).all()

    units = mesh.units[0]
    assert units[0] == 0
    # Due to floating point errors
    assert (units[1] + .5 * 2 ** .5) < 0.0001
    assert (units[2] - .5 * 2 ** .5) < 0.0001


def test_duplicate_polygons():
    data = numpy.zeros(6, dtype=Mesh.dtype)
    data['vectors'][0] = numpy.array([[1, 0, 0],
                                      [0, 0, 0],
                                      [0, 0, 0]])
    data['vectors'][1] = numpy.array([[2, 0, 0],
                                      [0, 0, 0],
                                      [0, 0, 0]])
    data['vectors'][2] = numpy.array([[0, 0, 0],
                                      [0, 0, 0],
                                      [0, 0, 0]])
    data['vectors'][3] = numpy.array([[2, 0, 0],
                                      [0, 0, 0],
                                      [0, 0, 0]])
    data['vectors'][4] = numpy.array([[1, 0, 0],
                                      [0, 0, 0],
                                      [0, 0, 0]])
    data['vectors'][5] = numpy.array([[0, 0, 0],
                                      [0, 0, 0],
                                      [0, 0, 0]])

    mesh = Mesh(data)
    assert mesh.data.size == 6

    mesh = Mesh(data, remove_duplicate_polygons=0)
    assert mesh.data.size == 6

    mesh = Mesh(data, remove_duplicate_polygons=False)
    assert mesh.data.size == 6

    mesh = Mesh(data, remove_duplicate_polygons=None)
    assert mesh.data.size == 6

    mesh = Mesh(data, remove_duplicate_polygons=RemoveDuplicates.NONE)
    assert mesh.data.size == 6

    mesh = Mesh(data, remove_duplicate_polygons=RemoveDuplicates.SINGLE)
    assert mesh.data.size == 3

    mesh = Mesh(data, remove_duplicate_polygons=True)
    assert mesh.data.size == 3

    assert (mesh.vectors[0] == numpy.array([[1, 0, 0],
                                            [0, 0, 0],
                                            [0, 0, 0]])).all()
    assert (mesh.vectors[1] == numpy.array([[2, 0, 0],
                                            [0, 0, 0],
                                            [0, 0, 0]])).all()
    assert (mesh.vectors[2] == numpy.array([[0, 0, 0],
                                            [0, 0, 0],
                                            [0, 0, 0]])).all()

    mesh = Mesh(data, remove_duplicate_polygons=RemoveDuplicates.ALL)
    assert mesh.data.size == 3

    assert (mesh.vectors[0] == numpy.array([[1, 0, 0],
                                            [0, 0, 0],
                                            [0, 0, 0]])).all()
    assert (mesh.vectors[1] == numpy.array([[2, 0, 0],
                                            [0, 0, 0],
                                            [0, 0, 0]])).all()
    assert (mesh.vectors[2] == numpy.array([[0, 0, 0],
                                            [0, 0, 0],
                                            [0, 0, 0]])).all()


def test_remove_all_duplicate_polygons():
    data = numpy.zeros(5, dtype=Mesh.dtype)
    data['vectors'][0] = numpy.array([[0, 0, 0],
                                      [0, 0, 0],
                                      [0, 0, 0]])
    data['vectors'][1] = numpy.array([[1, 0, 0],
                                      [0, 0, 0],
                                      [0, 0, 0]])
    data['vectors'][2] = numpy.array([[2, 0, 0],
                                      [0, 0, 0],
                                      [0, 0, 0]])
    data['vectors'][3] = numpy.array([[3, 0, 0],
                                      [0, 0, 0],
                                      [0, 0, 0]])
    data['vectors'][4] = numpy.array([[3, 0, 0],
                                      [0, 0, 0],
                                      [0, 0, 0]])

    mesh = Mesh(data, remove_duplicate_polygons=False)
    assert mesh.data.size == 5
    Mesh.remove_duplicate_polygons(mesh.data, RemoveDuplicates.NONE)

    mesh = Mesh(data, remove_duplicate_polygons=RemoveDuplicates.ALL)
    assert mesh.data.size == 3

    assert (mesh.vectors[0] == numpy.array([[0, 0, 0],
                                            [0, 0, 0],
                                            [0, 0, 0]])).all()
    assert (mesh.vectors[1] == numpy.array([[1, 0, 0],
                                            [0, 0, 0],
                                            [0, 0, 0]])).all()
    assert (mesh.vectors[2] == numpy.array([[2, 0, 0],
                                            [0, 0, 0],
                                            [0, 0, 0]])).all()


def test_empty_areas():
    data = numpy.zeros(3, dtype=Mesh.dtype)
    data['vectors'][0] = numpy.array([[0, 0, 0],
                                      [1, 0, 0],
                                      [0, 1, 0]])
    data['vectors'][1] = numpy.array([[1, 0, 0],
                                      [0, 1, 0],
                                      [1, 0, 0]])
    data['vectors'][2] = numpy.array([[1, 0, 0],
                                      [0, 1, 0],
                                      [1, 0, 0]])

    mesh = Mesh(data, remove_empty_areas=False)
    assert mesh.data.size == 3

    mesh = Mesh(data, remove_empty_areas=True)
    assert mesh.data.size == 1

