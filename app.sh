module purge
module load python/2.6.5

export LD_LIBRARY_PATH=/scratch/00019/gregj/VTK-python-tkinter/local/lib/vtk-5.10:${LD_LIBRARY_PATH}
export PYTHONPATH=/scratch/00019/gregj/VTK-python-tkinter/local/lib/python2.6/site-packages:${PYTHONPATH}

vglrun python App.py
