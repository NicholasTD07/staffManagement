#!/usr/bin/python3
# File Name : errorclass.py

class Error(Exception) :
    """ Base class for errors in the StuffClass"""
    pass

class noID(Error) :
    """没有输入员工ID"""
    pass

class notFoundInGroup(Error) :
    """员工组内没找到员工"""
    pass

class noThisStuff(Error) :
    """__stuffs 中没有此名员工Id"""
    pass

class notWaiting(Error) :
    """要求员工工作但该名员工不处于等待状态"""
    pass

class wrongType(Error) :
    """员工的工作类型指定错误
      
    不是 'Normal' 'Selected' 'Named' 任意一个"""
    pass

class norWrong(Error) :
    """员工正常工作时出现错误."""
    pass

class selWrong(Error) :
    """员工正常工作时出现错误."""
    pass

class namedWrong(Error) :
    """员工正常工作时出现错误."""
    pass

class workWrong(Error) :
    """员工正常工作时出现错误."""
    pass

class foundInGroup(Error) :
    pass
