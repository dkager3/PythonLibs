#!/usr/bin/python3

from dataclasses import dataclass
from typing import List

class Tukey:
  """
  Class to run the Tukey test on a set of data.
  
  Attributes
  ----------
  None
  
  Methods
  -------
  __median(p_list)
    Finds median value of pre-sorted list
  __medianIdx(p_list)
    Finds index of median value of pre-sorted list
  run(p_list)
    Runs Tukey test on given dataset (List)
  """

  @dataclass
  class TukeyResult:
    """
    Class to store result of Tukey test.
    
    Attributes
    ----------
    outliers: List
      List of outliers in dataset
    non_outliers: List
      List of non-outliers in dataset
    lower_fence: float
      Lower boundary/cutoff for outlier data
    upper_fence: float
      Upper boundary/cutoff for outlier data
    
    Methods
    -------
    None
    """
    outliers: List
    non_outliers: List
    lower_fence: float
    upper_fence: float

  @staticmethod
  def run(p_list: List) -> TukeyResult:
    """
    Runs Tukey test on given dataset (List).
    
    Paramters
    ---------
      p_list : List
        Data set to run Tukey test on
    
    Returns
    -------
      Result of Tukey test : Tukey.TukeyResult
    """
    result = None

    # Check that list is populated
    if p_list is not None and len(p_list) > 0:
      outliers = []
      non_outliers = []
      lower_fence = None
      upper_fence = None

      if len(p_list) == 1:
        # If there is only one value in the list, there are no elements
        # to compare it to.
        non_outliers = p_list
      else:
        # More than one value allows full Tukey test to run
        p_list.sort() # Sort list before starting
        split_idx = Tukey.__medianIdx(p_list)
        lower_list = p_list[0:split_idx]
        upper_list = []

        if len(p_list) % 2 == 0:
          # Even number of elements, split normally for
          # upper_list
          upper_list = p_list[split_idx:]
        else:
          # Odd number of elements in list, remove median number
          # for upper_list
          upper_list = p_list[split_idx+1:]

        Q1 = Tukey.__median(lower_list) # Median of lower list
        Q3 = Tukey.__median(upper_list) # Median of upper list
        IQR = Q3-Q1                     # Inter-Quartile Range
        lower_fence = Q1 - (IQR * 1.5)  # Anything below this boundary is an outlier
        upper_fence = Q3 + (IQR * 1.5)  # Anything above this boundary is an outlier

        # Filter outliers and non-outliers
        for elem in p_list:
          if elem < lower_fence or elem > upper_fence:
            outliers.append(elem)
          else:
            non_outliers.append(elem)

      result = Tukey.TukeyResult(outliers, non_outliers, lower_fence, upper_fence)

    return result
  
  @staticmethod
  def __median(p_list: List) -> float:
    """
    Finds median value of pre-sorted list.
    
    Paramters
    ---------
      p_list : List
        Data set to find median of
    
    Returns
    -------
      Median value : float
    """
    return p_list[Tukey.__medianIdx(p_list)]

  @staticmethod
  def __medianIdx(p_list: List) -> int:
    """
    Finds index of median value of pre-sorted list.
    
    Paramters
    ---------
      p_list : List
        Data set to find median index of
    
    Returns
    -------
      Median index : int
    """
    # Index of median value in sorted list. Works for both even/odd number 
    # of elements because int-cast drops decimal precision. Essentially
    # gives the "floor" of the decimal value.
    return int((len(p_list))/2)
