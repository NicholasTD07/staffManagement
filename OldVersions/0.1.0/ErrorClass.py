#!/usr/bin/python3
# File Name : errorclass.py

class Error(Exception) :
    """ Base class for errors in the StuffClass"""
    pass

class noID(Error) :
    """没有输入员工ID"""
    pass

class hadID(Error) :
    """已有该员工ID"""
    pass

class notWaiting(Error) :
    """要求员工工作但该名员工不处于等待状态"""
    pass

class wrongType(Error) :
    """员工的工作类型指定错误
      
    不是 'Normal' 'Selected' 'Named' 任意一个"""
    pass
