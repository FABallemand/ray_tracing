# 🎇 Ray Tracing

![GitHub](https://img.shields.io/github/license/FABallemand/ray_tracing)
![GitHub last commit](https://img.shields.io/github/last-commit/FABallemand/ray_tracing/main)
![GitHub repo size](https://img.shields.io/github/repo-size/FABallemand/ray_tracing)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

## 💬 Description

In 3D computer graphics, ray tracing is a technique for modeling light transport for use in a wide variety of rendering algorithms for generating digital images. [Wikipedia](https://en.wikipedia.org/wiki/Ray_tracing_(graphics))

There is more than meets the eye in Python programming. Pure Python implementations are great if you want to avoid dependencies. On the other hand, using libraries is often recommended to gain both programming time and execution time as you use existing functions and rely on performance optimisations. One of the best optimisation consist of writing the core of the library not in Python but in C which is way faster at run time. But there is also a way to convert Python code to C...

To explore the benefits of these approaches, I implemented 3 times the same ray tracer:
- **PyTracer** is a pure Python ray tracer with absolutely no third-party dependency.
- As the name implies, **NumpyTracer** relies on the well known and well optimised Numpy library.
- Finally, **CyTracer** uses Cython to convert Python code to C...
- **BadTracer** is my first implementation of ray tracer from back when I had virtually no experience in programming! Please do not reproduce at home!

## ⚖️ Comparison

Let's see which implementation is the fastest!