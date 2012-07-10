#!/usr/bin/python3
# File Name : errorclass.py

#    Copyright 2012 Nicholas Tian

#    This file is part of Staff Management Project.
#
#    Staff Management Project is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Foobar is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

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

class noGrpNum(Error) :
    pass
