
from abc import ABC, abstractmethod

class Stage(ABC):
    """
    Abstract base class for all stages
    """
    @abstractmethod
    def setPos(self, **kwargs):
        """
        Set the position of the stage device

        Parameters
        ----------
        **kwargs : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        pass

    @abstractmethod
    def getPos(self):
        """
        Query the position of the stage device

        Returns
        -------
        None.

        """
        pass

    def __enter__(self):
        """
        Enter the context manager

        Returns
        -------
        None.

        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context manager

        Parameters
        ----------
        exc_type : TYPE
            DESCRIPTION.
        exc_value : TYPE
            DESCRIPTION.
        traceback : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        pass
                
        
    
